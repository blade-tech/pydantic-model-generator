"""Research router for Claude ontology research (Step 2).

Provides endpoints for:
- Ontology research with streaming (Server-Sent Events)
"""

import logging
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.models.schemas import (
    BusinessOutcomeRequest,
    EntityMapping,
    OntologyResearchResponse,
    ErrorResponse
)
from app.services.claude_service import ClaudeService
from app.main import settings

logger = logging.getLogger(__name__)

router = APIRouter()


def get_claude_service() -> ClaudeService:
    """Dependency to get Claude service instance."""
    return ClaudeService(
        api_key=settings.anthropic_api_key,
        model=settings.claude_model,
        max_tokens=settings.claude_max_tokens,
        temperature=settings.claude_temperature
    )


@router.post("/research")
async def research_ontologies(
    request: BusinessOutcomeRequest,
    claude_service: ClaudeService = Depends(get_claude_service)
):
    """Research ontologies for business text with Claude streaming.

    This endpoint streams Claude's thinking process via Server-Sent Events.
    The frontend can display the reasoning in real-time.

    **Flow**:
    1. Analyze business text
    2. Identify 2-8 key entities
    3. Map entities to canonical ontology URIs (DoCO, FaBiO, PROV-O, FIBO, SKOS)
    4. Provide confidence scores and reasoning

    **Streaming Format**: Server-Sent Events
    - Each chunk is Claude's thinking text
    - Final chunk contains complete JSON response

    Args:
        request: Business outcome text
        claude_service: Claude AI service

    Returns:
        StreamingResponse with Server-Sent Events
    """
    logger.info(f"Starting ontology research for text: {request.text[:100]}...")

    async def event_generator():
        """Generate SSE events from Claude stream."""
        try:
            # Stream Claude's reasoning
            reasoning_chunks = []
            async for chunk in claude_service.research_ontologies(
                request.text,
                user_context=request.user_context,
                use_mcp_tools=request.use_mcp_tools,
                custom_prompt=request.custom_prompt
            ):
                reasoning_chunks.append(chunk)
                # Send chunk as SSE
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"

            # Parse the complete response to extract entities
            full_response = "".join(reasoning_chunks)
            logger.debug(f"Full Claude response: {full_response}")

            # Extract JSON from response (Claude may wrap it in markdown)
            try:
                # Try to find JSON in response
                json_start = full_response.find("{")
                json_end = full_response.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = full_response[json_start:json_end]
                    result = json.loads(json_str)
                    entities = [EntityMapping(**e) for e in result.get("entities", [])]
                else:
                    logger.error("No JSON found in Claude response")
                    entities = []
            except Exception as e:
                logger.error(f"Error parsing Claude response: {e}")
                entities = []

            # Send final result
            final_result = OntologyResearchResponse(
                entities=entities,
                reasoning_log=reasoning_chunks,
                total_entities=len(entities)
            )

            yield f"data: {json.dumps({'type': 'complete', 'result': final_result.model_dump(mode='json')})}\n\n"

        except Exception as e:
            logger.error(f"Error in ontology research: {e}", exc_info=True)
            error_response = ErrorResponse(
                error="Ontology research failed",
                detail=str(e)
            )
            yield f"data: {json.dumps({'type': 'error', 'error': error_response.model_dump(mode='json')})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )


@router.get("/health")
async def research_health():
    """Health check for research endpoints."""
    return {
        "status": "healthy",
        "service": "research",
        "claude_model": settings.claude_model
    }
