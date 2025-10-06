"""
Murabaha Audit Domain Plugin

Provides Shariah compliance audit models for Murabaha transactions:
- MurabahaAuditOutcome: Complete audit result with 89 checkpoints
- AuditCheckpoint: Individual checkpoint verification
- AuditEvidence: Supporting documentation
- VerifiedBy, RequiresEvidence, CitesStandard: Audit relationships
"""

import sys
from pathlib import Path

# Add generated models to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from generated.pydantic.murabaha_audit_glue import (
    MURABAHA_ENTITIES,
    MURABAHA_EDGES,
)

# Export registries for plugin loader
ENTITIES = MURABAHA_ENTITIES
EDGES = MURABAHA_EDGES

__all__ = ["ENTITIES", "EDGES"]
