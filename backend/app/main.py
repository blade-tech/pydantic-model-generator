"""
FastAPI Backend for Pydantic Model Generator Demo App

This backend provides real API integrations for:
- Claude (Anthropic) for ontology research and generation
- Instructor for structured LLM outputs
- gen-pydantic subprocess execution
- pytest subprocess execution
- Graphiti for knowledge graph ingestion
- Neo4j for graph storage

NO MOCKS - All API calls are real.
"""

import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os
from pathlib import Path


# ============================================================================
# CONFIGURATION
# ============================================================================

class Settings(BaseSettings):
    """Application settings from environment variables."""

    # AI API Keys
    anthropic_api_key: str
    openai_api_key: str

    # Neo4j Connection
    neo4j_uri: str = "neo4j://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str

    # Pydantic Library Path
    pydantic_library_path: str = "../pydantic_library"

    # FastAPI Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:3000,http://localhost:3001"

    # Claude Configuration
    claude_model: str = "claude-3-5-sonnet-20241022"
    claude_max_tokens: int = 16384  # Increased for complete LinkML schema generation
    claude_temperature: float = 0.7

    # Logging
    log_level: str = "INFO"

    # Development
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Load settings
try:
    settings = Settings()
except Exception as e:
    print(f"❌ Error loading settings: {e}")
    print("⚠️  Make sure .env file exists and contains all required variables")
    print("    Copy .env.example to .env and fill in your API keys")
    raise


# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ============================================================================
# LIFESPAN MANAGEMENT
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events."""

    # Startup
    logger.info("🚀 Starting Pydantic Model Generator Demo App Backend")
    logger.info(f"📚 Pydantic library path: {settings.pydantic_library_path}")

    # Validate pydantic library path exists
    pydantic_path = Path(settings.pydantic_library_path)
    if not pydantic_path.exists():
        logger.error(f"❌ Pydantic library not found at: {pydantic_path}")
        raise FileNotFoundError(
            f"Pydantic library not found at: {pydantic_path}\n"
            "Please set PYDANTIC_LIBRARY_PATH in .env"
        )

    logger.info("✅ Pydantic library found")

    # Add pydantic_library to Python path for dynamic imports
    pydantic_lib_abs = str(pydantic_path.resolve())
    if pydantic_lib_abs not in sys.path:
        sys.path.insert(0, pydantic_lib_abs)
        logger.info(f"📦 Added pydantic_library to Python path: {pydantic_lib_abs}")

    # Validate API keys (basic check)
    if not settings.anthropic_api_key.startswith("sk-ant-"):
        logger.warning("⚠️  ANTHROPIC_API_KEY may be invalid (should start with sk-ant-)")

    if not settings.openai_api_key.startswith("sk-"):
        logger.warning("⚠️  OPENAI_API_KEY may be invalid (should start with sk-)")

    logger.info("🔑 API keys configured")
    logger.info("🗄️  Neo4j URI: {settings.neo4j_uri}")

    yield

    # Shutdown
    logger.info("👋 Shutting down Pydantic Model Generator Demo App Backend")
    # Force reload


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="Pydantic Model Generator Demo API",
    description=(
        "Real API backend for outcome-first Pydantic modeling pipeline.\n\n"
        "Features:\n"
        "- Claude AI for ontology research\n"
        "- Instructor for structured outputs\n"
        "- gen-pydantic subprocess execution\n"
        "- pytest subprocess execution\n"
        "- Graphiti knowledge graph ingestion\n"
        "- Neo4j graph database\n\n"
        "⚠️  NO MOCKS - All API calls are real."
    ),
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.debug
)


# ============================================================================
# CORS MIDDLEWARE
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Pydantic Model Generator Demo API is running",
        "version": "1.0.0"
    }


@app.get("/debug/syspath")
async def debug_syspath():
    """Debug endpoint to check sys.path."""
    pydantic_lib_path = str(Path(settings.pydantic_library_path).resolve())
    return {
        "sys_path": sys.path[:10],  # First 10 entries
        "pydantic_library_path": pydantic_lib_path,
        "in_sys_path": pydantic_lib_path in sys.path
    }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Pydantic Model Generator Demo API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "research": "POST /api/research",
            "outcome_spec": "POST /api/generate-outcome-spec",
            "linkml": "POST /api/generate-linkml",
            "pydantic": "POST /api/generate-pydantic",
            "tests": "POST /api/run-tests",
            "library": "GET /api/library-coverage",
            "graphiti_ingest": "POST /api/graphiti/ingest",
            "graphiti_status": "GET /api/graphiti/status"
        }
    }


# ============================================================================
# ROUTERS
# ============================================================================

from app.routers import research, generation, testing, prompts, learning_center

app.include_router(research.router, prefix="/api", tags=["Research"])
app.include_router(generation.router, prefix="/api", tags=["Generation"])
app.include_router(testing.router, prefix="/api", tags=["Testing"])
app.include_router(prompts.router, prefix="/api", tags=["Prompts"])
app.include_router(learning_center.router, prefix="/api/learning-center", tags=["Learning Center"])

# Note: Graphiti router to be added in future iteration
# from app.routers import graphiti
# app.include_router(graphiti.router, prefix="/api/graphiti", tags=["Graphiti"])


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.debug else "An error occurred",
            "type": type(exc).__name__
        }
    )


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info(f"🚀 Starting server on {settings.api_host}:{settings.api_port}")

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
