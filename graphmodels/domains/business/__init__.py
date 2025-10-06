"""
Business Domain Plugin

Provides business workflow models:
- BusinessOutcome, BusinessDecision, BusinessTask, etc.
- Requires, Fulfills, BlockedBy relationships
"""

import sys
from pathlib import Path

# Add generated models to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from generated.pydantic.business_glue import (
    BUSINESS_ENTITIES,
    BUSINESS_EDGES,
)

# Export registries for plugin loader
ENTITIES = BUSINESS_ENTITIES
EDGES = BUSINESS_EDGES

__all__ = ["ENTITIES", "EDGES"]
