"""Learning Center router for self-documenting features.

Provides endpoints for:
- File system browsing
- File content reading
- Contextual help for each step
- Error troubleshooting information
- Real-time log streaming
"""

import logging
import asyncio
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field
from app.main import settings

logger = logging.getLogger(__name__)

router = APIRouter()


# ============================================================================
# LOG STREAMING INFRASTRUCTURE
# ============================================================================

class LogBroadcaster:
    """Manages WebSocket connections and broadcasts log messages."""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.log_buffer: List[Dict[str, Any]] = []
        self.max_buffer_size = 1000

    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection and send buffered logs."""
        await websocket.accept()
        self.active_connections.add(websocket)

        # Send buffered logs to new connection
        for log_entry in self.log_buffer:
            try:
                await websocket.send_json(log_entry)
            except Exception:
                pass

    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection."""
        self.active_connections.discard(websocket)

    async def broadcast(self, log_entry: Dict[str, Any]):
        """Broadcast log entry to all connected clients."""
        # Add to buffer
        self.log_buffer.append(log_entry)
        if len(self.log_buffer) > self.max_buffer_size:
            self.log_buffer.pop(0)

        # Broadcast to all connections
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(log_entry)
            except Exception:
                disconnected.add(connection)

        # Clean up disconnected clients
        for connection in disconnected:
            self.active_connections.discard(connection)

    def clear_buffer(self):
        """Clear the log buffer."""
        self.log_buffer.clear()


# Global log broadcaster instance
log_broadcaster = LogBroadcaster()


class WebSocketLogHandler(logging.Handler):
    """Custom log handler that broadcasts to WebSocket clients."""

    def __init__(self, broadcaster: LogBroadcaster):
        super().__init__()
        self.broadcaster = broadcaster

    def emit(self, record: logging.LogRecord):
        """Emit log record to WebSocket clients."""
        try:
            log_entry = {
                "timestamp": datetime.fromtimestamp(record.created).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": self.format(record),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno
            }

            # Try to extract step number from logger name or message
            step_number = None
            if "step" in record.name.lower():
                # Try to extract step number from logger name
                parts = record.name.lower().split("step")
                if len(parts) > 1 and parts[1][:1].isdigit():
                    step_number = int(parts[1][:1])
            elif "step" in record.getMessage().lower():
                # Try to extract from message
                msg = record.getMessage().lower()
                if "step 1" in msg:
                    step_number = 1
                elif "step 2" in msg:
                    step_number = 2
                elif "step 3" in msg:
                    step_number = 3
                elif "step 4" in msg:
                    step_number = 4
                elif "step 5" in msg:
                    step_number = 5
                elif "step 6" in msg:
                    step_number = 6

            if step_number:
                log_entry["step"] = step_number

            # Schedule broadcast (must be done in async context)
            asyncio.create_task(self.broadcaster.broadcast(log_entry))

        except Exception:
            self.handleError(record)


# Install WebSocket log handler
ws_log_handler = WebSocketLogHandler(log_broadcaster)
ws_log_handler.setLevel(logging.INFO)
ws_log_handler.setFormatter(logging.Formatter('%(message)s'))

# Add handler to root logger so we capture all logs
root_logger = logging.getLogger()
root_logger.addHandler(ws_log_handler)


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class FileNode(BaseModel):
    """File or directory node in the file tree."""
    name: str = Field(..., description="File or directory name")
    path: str = Field(..., description="Relative path from pydantic_library root")
    type: str = Field(..., description="'file' or 'directory'")
    size: Optional[int] = Field(None, description="File size in bytes (None for directories)")
    extension: Optional[str] = Field(None, description="File extension (e.g., '.py', '.yaml')")
    children: Optional[List['FileNode']] = Field(None, description="Child nodes (for directories)")


class FileContentResponse(BaseModel):
    """File content with metadata."""
    path: str = Field(..., description="File path")
    content: str = Field(..., description="File content")
    size: int = Field(..., description="File size in bytes")
    extension: str = Field(..., description="File extension")
    language: str = Field(..., description="Programming language for syntax highlighting")


class StepHelpResponse(BaseModel):
    """Contextual help for a workflow step."""
    step_number: int = Field(..., description="Step number (1-6)")
    step_name: str = Field(..., description="Step name")
    description: str = Field(..., description="What happens in this step")
    files_used: List[str] = Field(..., description="Files involved in this step")
    libraries: List[str] = Field(..., description="Libraries used in this step")
    tips: List[str] = Field(..., description="Best practices and tips")


# ============================================================================
# FILE SYSTEM ENDPOINTS
# ============================================================================

@router.get("/files/browse", response_model=List[FileNode])
async def browse_files(
    path: str = Query("/", description="Path to browse (relative to pydantic_library)")
):
    """Browse pydantic_library directory structure.

    Returns a tree of files and directories starting from the given path.

    Args:
        path: Relative path from pydantic_library root (default: "/")

    Returns:
        List of FileNode objects representing directory contents
    """
    try:
        pydantic_library_path = Path(settings.pydantic_library_path)

        # Sanitize path - remove leading slash and resolve relative to library root
        clean_path = path.lstrip("/").lstrip("\\")
        target_path = pydantic_library_path / clean_path if clean_path else pydantic_library_path

        # Security check - ensure we're not escaping pydantic_library
        target_path = target_path.resolve()
        if not str(target_path).startswith(str(pydantic_library_path.resolve())):
            raise HTTPException(status_code=403, detail="Access denied: Path escapes pydantic_library")

        if not target_path.exists():
            raise HTTPException(status_code=404, detail=f"Path not found: {clean_path}")

        if not target_path.is_dir():
            raise HTTPException(status_code=400, detail="Path must be a directory")

        # Build file tree
        nodes = []
        for item in sorted(target_path.iterdir()):
            relative_path = str(item.relative_to(pydantic_library_path)).replace("\\", "/")

            if item.is_dir():
                nodes.append(FileNode(
                    name=item.name,
                    path=relative_path,
                    type="directory",
                    size=None,
                    extension=None,
                    children=None  # Don't recurse - let frontend request children
                ))
            else:
                nodes.append(FileNode(
                    name=item.name,
                    path=relative_path,
                    type="file",
                    size=item.stat().st_size,
                    extension=item.suffix,
                    children=None
                ))

        return nodes

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error browsing files: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to browse files: {str(e)}")


@router.get("/files/read", response_model=FileContentResponse)
async def read_file(
    path: str = Query(..., description="File path (relative to pydantic_library)")
):
    """Read file contents from pydantic_library.

    Returns file content with metadata for display/download.

    Args:
        path: Relative path from pydantic_library root

    Returns:
        FileContentResponse with file content and metadata
    """
    try:
        pydantic_library_path = Path(settings.pydantic_library_path)

        # Sanitize path
        clean_path = path.lstrip("/").lstrip("\\")
        target_path = pydantic_library_path / clean_path

        # Security check
        target_path = target_path.resolve()
        if not str(target_path).startswith(str(pydantic_library_path.resolve())):
            raise HTTPException(status_code=403, detail="Access denied: Path escapes pydantic_library")

        if not target_path.exists():
            raise HTTPException(status_code=404, detail=f"File not found: {clean_path}")

        if not target_path.is_file():
            raise HTTPException(status_code=400, detail="Path must be a file")

        # Determine language for syntax highlighting
        extension = target_path.suffix.lower()
        language_map = {
            ".py": "python",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".json": "json",
            ".md": "markdown",
            ".txt": "text",
            ".log": "text"
        }
        language = language_map.get(extension, "text")

        # Read file content
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()

        return FileContentResponse(
            path=clean_path,
            content=content,
            size=target_path.stat().st_size,
            extension=extension,
            language=language
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")


# ============================================================================
# CONTEXTUAL HELP ENDPOINTS
# ============================================================================

# Step-specific help content
STEP_HELP_CONTENT = {
    1: {
        "step_name": "Business Outcome Input",
        "description": "Define your business outcome in natural language. The system will analyze your text to identify key entities and relationships.",
        "files_used": [
            "frontend/components/workflow/Step1Input.tsx"
        ],
        "libraries": ["React", "Next.js", "shadcn/ui"],
        "tips": [
            "Be specific about what data you need to track",
            "Mention any relationships between entities",
            "Include business rules or constraints",
            "Describe the desired queries or reports"
        ]
    },
    2: {
        "step_name": "Ontology Research",
        "description": "Claude AI analyzes your outcome and maps entities to canonical ontologies (DoCO, FaBiO, PROV-O, FIBO, SKOS).",
        "files_used": [
            "backend/app/routers/research.py",
            "backend/app/services/claude_service.py",
            "backend/app/prompts/templates.py (ONTOLOGY_RESEARCH_TASK)"
        ],
        "libraries": ["Anthropic Claude API", "FastAPI"],
        "tips": [
            "Review confidence scores - low scores may need refinement",
            "Check ontology URI mappings for accuracy",
            "Claude's reasoning explains each mapping choice",
            "Enable MCP tools for domain-specific research"
        ]
    },
    3: {
        "step_name": "OutcomeSpec Generation",
        "description": "Generate an OutcomeSpec YAML defining outcome questions, target entities, and validation queries.",
        "files_used": [
            "backend/app/routers/generation.py",
            "pydantic_library/schemas/overlays/{name}_outcomespec.yaml"
        ],
        "libraries": ["Anthropic Claude API", "PyYAML"],
        "tips": [
            "OutcomeSpec defines WHAT you want to achieve",
            "Validation queries are Cypher queries for testing",
            "Outcome questions guide schema design",
            "This file serves as documentation for developers"
        ]
    },
    4: {
        "step_name": "LinkML Schema Generation",
        "description": "Generate a LinkML schema YAML that defines classes, slots, and enums for Pydantic model generation.",
        "files_used": [
            "backend/app/routers/generation.py",
            "backend/app/prompts/templates.py (LINKML_SCHEMA_TASK)",
            "pydantic_library/schemas/overlays/{name}_overlay.yaml"
        ],
        "libraries": ["LinkML", "Anthropic Claude API"],
        "tips": [
            "Every slot MUST be defined in the slots: section",
            "All classes should have ProvenanceFields mixin",
            "Check that enum ranges are defined in enums: section",
            "Validate schema before proceeding to Step 5",
            "Class URIs should point to ontology classes from Step 2"
        ]
    },
    5: {
        "step_name": "Pydantic Model Generation",
        "description": "Execute gen-pydantic to convert LinkML schema into Pydantic V2 Python models.",
        "files_used": [
            "backend/app/routers/generation.py",
            "backend/app/services/subprocess_service.py",
            "pydantic_library/schemas/overlays/{name}_overlay.yaml (input)",
            "pydantic_library/generated/pydantic/overlays/{name}_models.py (output)"
        ],
        "libraries": ["gen-pydantic CLI", "Pydantic V2", "LinkML"],
        "tips": [
            "gen-pydantic runs as subprocess - check stderr for errors",
            "Common errors: missing slot definitions, invalid enum ranges",
            "Generated models include validation and provenance fields",
            "Models are ready for use in your application",
            "If gen-pydantic fails, go back to Step 4 and fix schema"
        ]
    },
    6: {
        "step_name": "Testing & Validation",
        "description": "Auto-generate pytest tests and validate generated Pydantic models.",
        "files_used": [
            "backend/app/routers/testing.py",
            "backend/app/services/test_generator.py",
            "backend/app/services/subprocess_service.py",
            "pydantic_library/tests/test_{name}.py (generated)",
            "pydantic_library/generated/pydantic/overlays/{name}_models.py"
        ],
        "libraries": ["pytest", "pytest-json-report", "Pydantic V2"],
        "tips": [
            "Tests are auto-generated from your models",
            "Tests validate entity creation, enums, fields, and provenance",
            "Check test output for validation errors",
            "Failed tests indicate schema issues - fix in Step 4",
            "Passing tests mean models are ready for production"
        ]
    }
}


@router.get("/help/step/{step_number}", response_model=StepHelpResponse)
async def get_step_help(step_number: int):
    """Get contextual help for a specific workflow step.

    Args:
        step_number: Step number (1-6)

    Returns:
        StepHelpResponse with step-specific guidance
    """
    if step_number not in STEP_HELP_CONTENT:
        raise HTTPException(status_code=404, detail=f"No help content for step {step_number}")

    content = STEP_HELP_CONTENT[step_number]
    return StepHelpResponse(
        step_number=step_number,
        **content
    )


@router.get("/help/all", response_model=List[StepHelpResponse])
async def get_all_step_help():
    """Get help content for all workflow steps.

    Returns:
        List of StepHelpResponse objects for steps 1-6
    """
    return [
        StepHelpResponse(step_number=num, **content)
        for num, content in STEP_HELP_CONTENT.items()
    ]


@router.get("/health")
async def learning_center_health():
    """Health check for learning center endpoints."""
    return {
        "status": "healthy",
        "service": "learning_center",
        "library_path": settings.pydantic_library_path
    }


# ============================================================================
# LOG STREAMING ENDPOINTS
# ============================================================================

@router.websocket("/logs/stream")
async def stream_logs(websocket: WebSocket):
    """WebSocket endpoint for real-time log streaming.

    Clients can connect to this endpoint to receive real-time logs from the backend.
    Logs are formatted as JSON with timestamp, level, logger, message, and optional step number.

    Example log entry:
    {
        "timestamp": "2024-01-15T12:30:45.123456",
        "level": "INFO",
        "logger": "app.routers.research",
        "message": "Starting ontology research...",
        "module": "research",
        "function": "research_ontologies",
        "line": 42,
        "step": 2  // Optional - only if step can be detected
    }

    Frontend can filter by:
    - level (INFO, WARNING, ERROR, DEBUG)
    - step (1-6)
    - search text in message
    """
    await log_broadcaster.connect(websocket)

    try:
        # Keep connection alive and handle client messages (if any)
        while True:
            # Wait for client messages (e.g., ping/pong)
            data = await websocket.receive_text()

            # Handle special commands
            if data == "ping":
                await websocket.send_text("pong")
            elif data == "clear":
                # Client requests to clear log buffer
                log_broadcaster.clear_buffer()
                await websocket.send_json({"type": "system", "message": "Log buffer cleared"})

    except WebSocketDisconnect:
        log_broadcaster.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)
        log_broadcaster.disconnect(websocket)


@router.post("/logs/clear")
async def clear_logs():
    """Clear the log buffer.

    This endpoint clears the buffered logs without disconnecting WebSocket clients.
    Useful for starting fresh when beginning a new workflow.

    Returns:
        Dict with success status and message
    """
    try:
        log_broadcaster.clear_buffer()
        logger.info("Log buffer cleared via API")
        return {
            "success": True,
            "message": "Log buffer cleared successfully"
        }
    except Exception as e:
        logger.error(f"Failed to clear log buffer: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to clear logs: {str(e)}")


@router.get("/logs/count")
async def get_log_count():
    """Get the current number of buffered log entries.

    Returns:
        Dict with log count and active connections
    """
    return {
        "log_count": len(log_broadcaster.log_buffer),
        "active_connections": len(log_broadcaster.active_connections),
        "max_buffer_size": log_broadcaster.max_buffer_size
    }
