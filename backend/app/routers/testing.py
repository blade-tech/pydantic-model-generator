"""Testing router for pytest execution and library coverage (Step 6).

Provides endpoints for:
- Auto-generating test files from Pydantic models
- Running pytest on generated models
- Getting library coverage statistics
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import (
    TestExecutionRequest,
    TestExecutionResponse,
    LibraryCoverageStats,
    ErrorResponse
)
from app.services.subprocess_service import SubprocessService
from app.services.test_generator import TestGenerator
from app.main import settings

logger = logging.getLogger(__name__)

router = APIRouter()


def get_subprocess_service() -> SubprocessService:
    """Dependency to get subprocess service instance."""
    return SubprocessService(
        pydantic_library_path=settings.pydantic_library_path
    )


@router.post("/run-tests", response_model=TestExecutionResponse)
async def run_tests(
    request: TestExecutionRequest,
    subprocess_service: SubprocessService = Depends(get_subprocess_service)
):
    """Run pytest on generated models (Step 6).

    **Flow**:
    1. Auto-generate test file from Pydantic models
    2. Execute pytest subprocess with JSON output
    3. Parse results (passed/failed/skipped counts)
    4. Return formatted results

    Args:
        request: Overlay name to test
        subprocess_service: Subprocess service

    Returns:
        TestExecutionResponse with test results
    """
    logger.info(f"Running tests for overlay: {request.overlay_name}")

    try:
        # Step 1: Auto-generate test file
        logger.info(f"Generating test file for {request.overlay_name}")
        test_generator = TestGenerator(settings.pydantic_library_path)
        gen_result = test_generator.generate_test_file(request.overlay_name)

        if not gen_result["success"]:
            logger.error(f"Test generation failed: {gen_result.get('error')}")
            raise HTTPException(
                status_code=500,
                detail=f"Test generation failed: {gen_result.get('error')}"
            )

        logger.info(f"Generated test file: {gen_result['test_file_path']} with {gen_result['num_tests']} tests")

        # Step 2: Run tests
        result = subprocess_service.run_tests(
            overlay_name=request.overlay_name
        )

        return TestExecutionResponse(**result)

    except Exception as e:
        logger.error(f"Error running tests: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Test execution failed: {str(e)}"
        )


@router.get("/library-coverage", response_model=LibraryCoverageStats)
async def get_library_coverage(
    subprocess_service: SubprocessService = Depends(get_subprocess_service)
):
    """Get pydantic_library coverage statistics.

    Scans schemas/overlays/ directory and counts:
    - Total overlays
    - Total entities
    - Total edges
    - Per-overlay details

    Args:
        subprocess_service: Subprocess service

    Returns:
        LibraryCoverageStats with coverage data
    """
    logger.info("Getting library coverage statistics")

    try:
        result = subprocess_service.get_library_coverage()
        return LibraryCoverageStats(**result)

    except Exception as e:
        logger.error(f"Error getting library coverage: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get library coverage: {str(e)}"
        )


@router.get("/health")
async def testing_health():
    """Health check for testing endpoints."""
    return {
        "status": "healthy",
        "service": "testing",
        "library_path": settings.pydantic_library_path
    }

