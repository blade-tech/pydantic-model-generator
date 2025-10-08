"""Business outcomes overlay - Graphiti type registries and edge mappings.

This module provides type registries for Graphiti integration, enabling
the knowledge graph to validate and route business outcome entities and edges.

Driven by: specs/business_outcomes_tracking.yaml
"""
from __future__ import annotations

from typing import Dict, List
from pydantic import BaseModel

# Import all entity and edge classes
from .business_outcomes_models import (
    BusinessOutcome,
    BusinessDecision,
    BusinessTask,
    BusinessHandoff,
    BlockedBy,
    Fulfills,
    Requires,
    AssignedTo,
    ResponsibleFor,
    Transfers,
)

# Import shared identity entities
from generated.pydantic.shared.identity import Actor

# ==================================================================
# GRAPHITI TYPE REGISTRIES
# ==================================================================

BUSINESS_OUTCOMES_ENTITY_TYPES: Dict[str, type[BaseModel]] = {
    "BusinessOutcome": BusinessOutcome,
    "BusinessDecision": BusinessDecision,
    "BusinessTask": BusinessTask,
    "BusinessHandoff": BusinessHandoff,
    "Actor": Actor,  # From shared identity
}

BUSINESS_OUTCOMES_EDGE_TYPES: Dict[str, type[BaseModel]] = {
    "BlockedBy": BlockedBy,
    "Fulfills": Fulfills,
    "Requires": Requires,
    "AssignedTo": AssignedTo,
    "ResponsibleFor": ResponsibleFor,
    "Transfers": Transfers,
}

# ==================================================================
# CANONICAL EDGE TYPE MAPPINGS
# ==================================================================
# Maps (source_type, target_type) tuples to allowed edge types
# Graphiti uses this to validate and route edge creation

BUSINESS_OUTCOMES_EDGE_TYPE_MAP: Dict[tuple, List[str]] = {
    # Decision impact on outcomes
    ("BusinessOutcome", "BusinessDecision"): ["BlockedBy"],
    ("BusinessDecision", "BusinessOutcome"): ["Fulfills"],

    # Task relationships
    ("BusinessOutcome", "BusinessTask"): ["Requires"],
    ("BusinessTask", "Actor"): ["AssignedTo"],

    # Responsibility tracking
    ("Actor", "BusinessOutcome"): ["ResponsibleFor"],

    # Handoff tracking
    ("BusinessHandoff", "Actor"): ["Transfers"],
}

# ==================================================================
# VALIDATION HELPERS
# ==================================================================

def validate_edge_type(source_type: str, target_type: str, edge_type: str) -> bool:
    """Validate if an edge type is allowed between two entity types.

    Args:
        source_type: Source entity type name
        target_type: Target entity type name
        edge_type: Edge type name

    Returns:
        bool: True if edge type is valid for this entity pair
    """
    allowed_edges = BUSINESS_OUTCOMES_EDGE_TYPE_MAP.get((source_type, target_type), [])
    return edge_type in allowed_edges


def get_allowed_edges(source_type: str, target_type: str) -> List[str]:
    """Get allowed edge types between two entity types.

    Args:
        source_type: Source entity type name
        target_type: Target entity type name

    Returns:
        List of allowed edge type names (empty if no edges allowed)
    """
    return BUSINESS_OUTCOMES_EDGE_TYPE_MAP.get((source_type, target_type), [])


# ==================================================================
# OUTCOME SPEC METADATA
# ==================================================================

OUTCOME_SPEC_ID = "https://example.org/specs/business-outcomes-tracking"
OUTCOME_SPEC_NAME = "business_outcomes_tracking"

OUTCOME_QUESTIONS = [
    "What business outcomes are we tracking and what is their status?",
    "What decisions block or enable specific outcomes?",
    "What tasks are assigned to deliver each outcome?",
    "Who is responsible for each outcome and what is their availability?",
    "What handoffs are needed and what is their status?",
]

# Validation query names from OutcomeSpec
VALIDATION_QUERIES = [
    "test_outcome_status_retrieval",
    "test_decision_blocking_outcomes",
    "test_task_assignment",
    "test_responsibility_tracking",
    "test_handoff_tracking",
]
