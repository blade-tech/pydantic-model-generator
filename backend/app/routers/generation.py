"""Generation router for OutcomeSpec, LinkML, and Pydantic generation (Steps 3-5).

Provides endpoints for:
- OutcomeSpec generation with streaming (Step 3)
- LinkML schema generation with streaming (Step 4)
- Pydantic model generation with subprocess (Step 5)
"""
# Updated 10:14

import logging
import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.models.schemas import (
    OutcomeSpecRequest,
    OutcomeSpecResponse,
    LinkMLSchemaRequest,
    LinkMLSchemaResponse,
    PydanticGenerationRequest,
    PydanticGenerationResponse,
    ErrorResponse
)
from app.services.claude_service import ClaudeService
from app.services.subprocess_service import SubprocessService
from app.services.test_generator import TestGenerator
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


def get_subprocess_service() -> SubprocessService:
    """Dependency to get subprocess service instance."""
    return SubprocessService(
        pydantic_library_path=settings.pydantic_library_path
    )


@router.post("/generate-outcome-spec")
async def generate_outcome_spec(
    request: OutcomeSpecRequest,
    claude_service: ClaudeService = Depends(get_claude_service)
):
    """Generate OutcomeSpec with Claude streaming (Step 3).

    **Flow**:
    1. Take business text and identified entities
    2. Generate OutcomeSpec YAML with:
       - Outcome questions
       - Target entities
       - Validation queries (Cypher)
    3. Stream Claude's thinking process

    Args:
        request: Business text and entities
        claude_service: Claude AI service

    Returns:
        StreamingResponse with Server-Sent Events
    """
    logger.info(f"Starting OutcomeSpec generation with {len(request.entities)} entities")

    async def event_generator():
        """Generate SSE events from Claude stream."""
        try:
            # Convert entities dict to EntityMapping objects
            from app.models.schemas import EntityMapping
            entities = [EntityMapping(**e) for e in request.entities]

            # Stream Claude's generation
            response_chunks = []
            async for chunk in claude_service.generate_outcome_spec(
                request.text,
                entities,
                custom_prompt=request.custom_prompt
            ):
                response_chunks.append(chunk)
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"

            # Extract YAML from response
            full_response = "".join(response_chunks)
            yaml_start = full_response.find("```yaml")
            yaml_end = full_response.find("```", yaml_start + 7)

            if yaml_start >= 0 and yaml_end > yaml_start:
                yaml_content = full_response[yaml_start + 7:yaml_end].strip()
            else:
                yaml_content = full_response

            # Send final result
            final_result = OutcomeSpecResponse(
                outcome_spec={"raw": yaml_content},
                yaml_content=yaml_content
            )

            yield f"data: {json.dumps({'type': 'complete', 'result': final_result.model_dump(mode='json')})}\n\n"

        except Exception as e:
            logger.error(f"Error generating OutcomeSpec: {e}", exc_info=True)
            error_response = ErrorResponse(
                error="OutcomeSpec generation failed",
                detail=str(e)
            )
            yield f"data: {json.dumps({'type': 'error', 'error': error_response.model_dump(mode='json')})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.post("/generate-linkml")
async def generate_linkml_schema(
    request: LinkMLSchemaRequest,
    claude_service: ClaudeService = Depends(get_claude_service)
):
    """Generate LinkML schema with Claude streaming (Step 4).

    **Flow**:
    1. Take OutcomeSpec and entities
    2. Generate LinkML schema YAML with:
       - Class definitions
       - Canonical ontology URIs (class_uri)
       - ProvenanceFields mixin
       - Slots (fields)
       - Relationships
    3. Stream Claude's thinking process

    Args:
        request: OutcomeSpec and entities
        claude_service: Claude AI service

    Returns:
        StreamingResponse with Server-Sent Events
    """
    logger.info("Starting LinkML schema generation")

    async def event_generator():
        """Generate SSE events from Claude stream."""
        try:
            from app.models.schemas import EntityMapping
            entities = [EntityMapping(**e) for e in request.entities]

            # Stream Claude's generation
            response_chunks = []
            async for chunk in claude_service.generate_linkml_schema(
                request.outcome_spec,
                entities,
                custom_prompt=request.custom_prompt
            ):
                response_chunks.append(chunk)
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"

            # Extract YAML from response
            full_response = "".join(response_chunks)
            yaml_start = full_response.find("```yaml")
            yaml_end = full_response.find("```", yaml_start + 7)

            if yaml_start >= 0 and yaml_end > yaml_start:
                yaml_content = full_response[yaml_start + 7:yaml_end].strip()
            else:
                yaml_content = full_response

            # Validate schema completeness
            logger.info("🔍 Starting schema validation")
            from app.utils.linkml_validator import validate_linkml_schema, get_schema_completeness_report, auto_repair_schema

            try:
                is_valid, validation_errors = validate_linkml_schema(yaml_content)
                completeness = get_schema_completeness_report(yaml_content)
                logger.info(f"📊 Validation complete - Valid: {is_valid}, Completeness: {completeness}")

                if not is_valid:
                    logger.warning(f"⚠️  LinkML schema has validation errors: {len(validation_errors)} issues found")
                    logger.warning(f"📈 Completeness: {completeness}")
                    for error in validation_errors[:5]:  # Log first 5 errors
                        logger.warning(f"  ❌ {error}")

                    # Attempt auto-repair
                    logger.info("🔧 Attempting auto-repair of common issues...")
                    repaired_yaml, repairs_made = auto_repair_schema(yaml_content)

                    if repairs_made:
                        logger.info(f"✅ Auto-repair successful: {len(repairs_made)} repairs made")
                        for repair in repairs_made:
                            logger.info(f"  {repair}")

                        # Re-validate after repair
                        is_valid_after_repair, remaining_errors = validate_linkml_schema(repaired_yaml)
                        if is_valid_after_repair:
                            logger.info("✅ Schema is now valid after auto-repair")
                            yaml_content = repaired_yaml  # Use repaired schema
                            yield f"data: {json.dumps({'type': 'info', 'content': f'Auto-repaired schema: {len(repairs_made)} fixes applied'})}\n\n"
                        else:
                            logger.warning(f"⚠️  Schema still has {len(remaining_errors)} errors after auto-repair")
                            yaml_content = repaired_yaml  # Still use repaired schema (partial fix is better than none)
                            yield f"data: {json.dumps({'type': 'warning', 'content': f'Partial auto-repair: {len(repairs_made)} fixes applied, {len(remaining_errors)} issues remain'})}\n\n"
                    else:
                        logger.info("ℹ️  No auto-repairable issues found")
                        yield f"data: {json.dumps({'type': 'warning', 'content': f'Schema validation found {len(validation_errors)} issues. Check logs for details.'})}\n\n"
                else:
                    logger.info("✅ Schema validation passed")
            except Exception as e:
                logger.error(f"❌ Validation failed with exception: {e}", exc_info=True)

            # Count entities
            entity_count = yaml_content.count("class_uri:")

            # Send final result with validation info
            final_result = LinkMLSchemaResponse(
                schema={
                    "raw": yaml_content,
                    "validation": {
                        "is_valid": is_valid,
                        "errors": validation_errors if not is_valid else [],
                        "completeness": completeness
                    }
                },
                yaml_content=yaml_content,
                entity_count=entity_count
            )

            yield f"data: {json.dumps({'type': 'complete', 'result': final_result.model_dump(mode='json')})}\n\n"

        except Exception as e:
            logger.error(f"Error generating LinkML schema: {e}", exc_info=True)
            error_response = ErrorResponse(
                error="LinkML schema generation failed",
                detail=str(e)
            )
            yield f"data: {json.dumps({'type': 'error', 'error': error_response.model_dump(mode='json')})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.post("/generate-pydantic", response_model=PydanticGenerationResponse)
async def generate_pydantic_models(
    request: PydanticGenerationRequest,
    subprocess_service: SubprocessService = Depends(get_subprocess_service)
):
    """Generate Pydantic models with gen-pydantic subprocess (Step 5).

    **Flow**:
    1. Write LinkML schema to pydantic_library/schemas/overlays/
    2. Execute gen-pydantic subprocess
    3. Write generated Python to pydantic_library/generated/pydantic/overlays/
    4. Return generated code

    Args:
        request: Overlay name and LinkML schema
        subprocess_service: Subprocess service

    Returns:
        PydanticGenerationResponse with generated code
    """
    logger.info(f"Starting Pydantic model generation for overlay: {request.overlay_name}")

    try:
        # Strip markdown code fences if present
        linkml_schema = request.linkml_schema
        logger.info(f"Received schema starting with: {linkml_schema[:50]}...")

        if linkml_schema.startswith("```yaml") or linkml_schema.startswith("```"):
            logger.info("Detected code fences, stripping them")
            # Find the start and end of code fence
            lines = linkml_schema.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]  # Remove opening fence
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]  # Remove closing fence
            linkml_schema = "\n".join(lines)
            logger.info(f"After stripping, schema starts with: {linkml_schema[:50]}...")
        else:
            logger.info("No code fences detected")

        # Validate and auto-repair schema before gen-pydantic
        logger.info("🔍 Validating LinkML schema before Pydantic generation")
        from app.utils.linkml_validator import validate_linkml_schema, auto_repair_schema

        try:
            is_valid, validation_errors = validate_linkml_schema(linkml_schema)

            if not is_valid:
                logger.warning(f"⚠️  Schema has {len(validation_errors)} validation errors")
                for error in validation_errors[:5]:
                    logger.warning(f"  ❌ {error}")

                # Attempt auto-repair
                logger.info("🔧 Attempting auto-repair before gen-pydantic...")
                repaired_schema, repairs_made = auto_repair_schema(linkml_schema)

                if repairs_made:
                    logger.info(f"✅ Auto-repair successful: {len(repairs_made)} repairs made")
                    for repair in repairs_made:
                        logger.info(f"  {repair}")

                    # Re-validate
                    is_valid_after, remaining_errors = validate_linkml_schema(repaired_schema)
                    if is_valid_after:
                        logger.info("✅ Schema is valid after auto-repair, using repaired version")
                        linkml_schema = repaired_schema
                    else:
                        logger.warning(f"⚠️  Schema still has {len(remaining_errors)} errors, using partially repaired version")
                        linkml_schema = repaired_schema
                else:
                    logger.info("ℹ️  No auto-repairable issues found")
            else:
                logger.info("✅ Schema validation passed")
        except Exception as e:
            logger.error(f"❌ Validation/repair failed: {e}", exc_info=True)

        result = subprocess_service.generate_pydantic_models(
            overlay_name=request.overlay_name,
            linkml_schema_content=linkml_schema
        )

        # AUTO-GENERATE TESTS AFTER SUCCESSFUL PYDANTIC GENERATION
        if result.get('success'):
            try:
                logger.info("🧪 Auto-generating test file...")
                test_generator = TestGenerator(settings.pydantic_library_path)
                test_result = test_generator.generate_test_file(request.overlay_name)

                if test_result.get('success'):
                    logger.info(f"✅ Auto-generated test file: {test_result['test_file_path']}")
                    logger.info(f"   Generated tests for {test_result['num_model_classes']} models and {test_result['num_enum_classes']} enums")
                    logger.info(f"   Total tests: {test_result['num_tests']}")
                else:
                    logger.warning(f"⚠️  Test generation failed: {test_result.get('error')}")
            except Exception as e:
                logger.error(f"❌ Error in test generation: {e}", exc_info=True)
                # Don't fail the whole request if test generation fails

        return PydanticGenerationResponse(**result)

    except Exception as e:
        logger.error(f"Error generating Pydantic models: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Pydantic model generation failed: {str(e)}"
        )


@router.get("/health")
async def generation_health():
    """Health check for generation endpoints."""
    # Force reload
    return {
        "status": "healthy",
        "service": "generation",
        "claude_model": settings.claude_model
    }
