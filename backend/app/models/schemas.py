"""Pydantic schemas for API request/response models."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ============================================================================
# REQUEST MODELS
# ============================================================================

class BusinessOutcomeRequest(BaseModel):
    """Request model for business outcome input (Step 1) and research (Step 2)."""
    text: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Business outcome description in natural language"
    )
    user_context: Optional[str] = Field(
        None,
        description="Optional context or instructions from user to guide Claude's research"
    )
    use_mcp_tools: bool = Field(
        False,
        description="Whether to enable MCP tools (web search, documentation lookup) for research"
    )
    custom_prompt: Optional[str] = Field(
        None,
        description="Optional custom prompt template (overrides default prompt)"
    )


class OutcomeSpecRequest(BaseModel):
    """Request model for OutcomeSpec generation (Step 3)."""
    text: str = Field(..., description="Business outcome text")
    entities: List[Dict[str, Any]] = Field(..., description="Identified entities from research step")
    custom_prompt: Optional[str] = Field(
        None,
        description="Optional custom prompt template (overrides default prompt)"
    )


class LinkMLSchemaRequest(BaseModel):
    """Request model for LinkML schema generation (Step 4)."""
    outcome_spec: str = Field(..., description="Generated OutcomeSpec YAML content")
    entities: List[Dict[str, Any]] = Field(..., description="Entity definitions")
    custom_prompt: Optional[str] = Field(
        None,
        description="Optional custom prompt template (overrides default prompt)"
    )


class PydanticGenerationRequest(BaseModel):
    """Request model for Pydantic model generation (Step 5)."""
    overlay_name: str = Field(..., description="Name of the overlay (e.g., 'customer_support')")
    linkml_schema: str = Field(..., description="LinkML schema YAML content")


class TestExecutionRequest(BaseModel):
    """Request model for test execution (Step 6)."""
    overlay_name: str = Field(..., description="Name of the overlay to test")


class GraphitiIngestionRequest(BaseModel):
    """Request model for Graphiti ingestion (Step 6)."""
    overlay_name: str = Field(..., description="Name of the overlay to ingest")
    episode_name: str = Field(..., description="Name for the episode")
    episode_body: str = Field(..., description="Content to ingest")


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class EntityMapping(BaseModel):
    """Entity mapped to canonical ontology."""
    entity_name: str = Field(..., description="Name of the entity")
    entity_type: str = Field(..., description="Type of entity (e.g., 'Document', 'Person')")
    ontology_uri: str = Field(..., description="Canonical ontology URI")
    ontology_source: str = Field(..., description="Ontology source (DoCO, FaBiO, PROV-O, FIBO, SKOS)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Mapping confidence (0.0-1.0)")
    reasoning: str = Field(..., description="Why this mapping was chosen")


class OntologyResearchResponse(BaseModel):
    """Response model for ontology research (Step 2)."""
    entities: List[EntityMapping] = Field(..., description="Identified entities with ontology mappings")
    reasoning_log: List[str] = Field(..., description="Claude's reasoning steps")
    total_entities: int = Field(..., description="Total entities identified")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class OutcomeSpecResponse(BaseModel):
    """Response model for OutcomeSpec generation (Step 3)."""
    outcome_spec: Dict[str, Any] = Field(..., description="Generated OutcomeSpec")
    yaml_content: str = Field(..., description="YAML representation")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class LinkMLSchemaResponse(BaseModel):
    """Response model for LinkML schema generation (Step 4)."""
    schema: Dict[str, Any] = Field(..., description="Generated LinkML schema")
    yaml_content: str = Field(..., description="YAML representation")
    entity_count: int = Field(..., description="Number of entities defined")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PydanticGenerationResponse(BaseModel):
    """Response model for Pydantic model generation (Step 5)."""
    success: bool = Field(..., description="Whether generation succeeded")
    output_path: Optional[str] = Field(None, description="Path to generated Python file (None if failed)")
    python_code: Optional[str] = Field(None, description="Generated Python code (None if failed)")
    stderr: Optional[str] = Field(None, description="Error output if any")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TestResult(BaseModel):
    """Individual test result."""
    test_name: str
    status: str  # "passed", "failed", "skipped"
    duration: float
    error_message: Optional[str] = None


class TestExecutionResponse(BaseModel):
    """Response model for test execution (Step 6)."""
    success: bool = Field(..., description="Whether tests passed")
    total_tests: int = Field(..., description="Total tests run")
    passed: int = Field(..., description="Tests passed")
    failed: int = Field(..., description="Tests failed")
    skipped: int = Field(..., description="Tests skipped")
    duration: float = Field(..., description="Total duration in seconds")
    tests: List[TestResult] = Field(..., description="Individual test results")
    stdout: str = Field(..., description="Test output")
    stderr: Optional[str] = Field(None, description="Test error output (if any)")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class GraphitiIngestionResponse(BaseModel):
    """Response model for Graphiti ingestion (Step 6)."""
    success: bool = Field(..., description="Whether ingestion succeeded")
    episode_id: str = Field(..., description="Graphiti episode ID")
    entities_created: int = Field(..., description="Number of entities created")
    edges_created: int = Field(..., description="Number of edges created")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class LibraryCoverageStats(BaseModel):
    """Statistics about pydantic_library coverage."""
    total_overlays: int = Field(..., description="Total number of overlays")
    total_entities: int = Field(..., description="Total entities across all overlays")
    total_edges: int = Field(..., description="Total edge types")
    overlays: List[Dict[str, Any]] = Field(..., description="List of overlays with details")
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Health status")
    message: str = Field(..., description="Status message")
    version: str = Field(..., description="API version")
