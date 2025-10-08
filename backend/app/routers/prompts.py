"""Prompts router for exposing default AI prompts to frontend.

Allows users to view and customize Claude prompts for each step.
"""

import logging
from fastapi import APIRouter
from typing import Dict, Any
from app.prompts import (
    ONTOLOGY_RESEARCH_SYSTEM,
    ONTOLOGY_RESEARCH_TASK,
    OUTCOME_SPEC_SYSTEM,
    OUTCOME_SPEC_TASK,
    LINKML_SCHEMA_SYSTEM,
    LINKML_SCHEMA_TASK,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/default-prompts")
async def get_all_default_prompts() -> Dict[str, Dict[str, Any]]:
    """Get all default prompts for all steps.

    Returns:
        Dictionary with prompts for each step
    """
    return {
        "step2_research": {
            "step": "Step 2: Ontology Research",
            "system": ONTOLOGY_RESEARCH_SYSTEM,
            "task": ONTOLOGY_RESEARCH_TASK,
            "variables": [
                {"name": "business_text", "description": "Business outcome description"},
                {"name": "user_context", "description": "Optional user context or instructions"}
            ],
            "description": "Analyzes business text and maps entities to canonical ontologies"
        },
        "step3_outcome_spec": {
            "step": "Step 3: OutcomeSpec Generation",
            "system": OUTCOME_SPEC_SYSTEM,
            "task": OUTCOME_SPEC_TASK,
            "variables": [
                {"name": "business_text", "description": "Business outcome description"},
                {"name": "entities", "description": "Identified entities from research"}
            ],
            "description": "Generates OutcomeSpec YAML with outcome questions and validation queries"
        },
        "step4_linkml": {
            "step": "Step 4: LinkML Schema Generation",
            "system": LINKML_SCHEMA_SYSTEM,
            "task": LINKML_SCHEMA_TASK,
            "variables": [
                {"name": "outcome_spec", "description": "Generated OutcomeSpec"},
                {"name": "entities", "description": "Entity definitions with ontology mappings"}
            ],
            "description": "Generates LinkML schema YAML with classes, slots, and relationships"
        }
    }


@router.get("/default-prompts/{step_id}")
async def get_default_prompt(step_id: str) -> Dict[str, Any]:
    """Get default prompt for a specific step.

    Args:
        step_id: Step identifier (step2_research, step3_outcome_spec, step4_linkml)

    Returns:
        Prompt details for the specified step
    """
    all_prompts = await get_all_default_prompts()

    if step_id not in all_prompts:
        return {
            "error": f"Unknown step_id: {step_id}",
            "available_steps": list(all_prompts.keys())
        }

    return all_prompts[step_id]


@router.get("/health")
async def prompts_health():
    """Health check for prompts endpoints."""
    return {
        "status": "healthy",
        "service": "prompts",
        "available_steps": ["step2_research", "step3_outcome_spec", "step4_linkml"]
    }
