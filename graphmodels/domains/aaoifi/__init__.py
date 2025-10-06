"""
AAOIFI Domain Plugin

Provides Islamic finance standards document models:
- Document, Section, Paragraph, Concept, Term
- Contains, Defines, Mentions, References, Supersedes relationships
"""

import sys
from pathlib import Path

# Add generated models to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from generated.pydantic.aaoifi_glue import (
    AAOIFI_ENTITIES,
    AAOIFI_EDGES,
)

# Export registries for plugin loader
ENTITIES = AAOIFI_ENTITIES
EDGES = AAOIFI_EDGES

__all__ = ["ENTITIES", "EDGES"]
