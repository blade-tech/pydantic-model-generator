# Pydantic V2 Core Foundation

## Overview

The `graphmodels/core/` package provides the foundational Pydantic V2 models and utilities that serve as the base layer for both:
1. **LinkML-generated models** (outcome-driven, minimal schemas)
2. **Hand-crafted domain models** (comprehensive business/AAOIFI models)

This ensures consistency, type safety, and shared provenance tracking across all models.

## Architecture

```
graphmodels/core/
├── __init__.py          # Package exports
├── base.py              # Strict ModelBase + shared enums
├── provenance.py        # NodeProv/EdgeProv mixins
├── id_utils.py          # Deterministic ID generation
├── registry.py          # Type registries (ENTITY_TYPES, EDGE_TYPES)
└── types.py             # GraphAccessor protocol
```

## Core Components

### 1. ModelBase (base.py)

Strict Pydantic base with:
- `extra="forbid"` - Catch typos and schema drift
- `strict=True` - No type coercion (int ≠ "42")
- `use_enum_values=True` - Serialize enum values
- `validate_assignment=True` - Runtime validation

**Shared Enums:**
- `ProvenanceSystem` - System of origin (slack, aaoifi, fibo, etc.)
- `Currency` - Currency codes (USD, EUR, GBP, SAR)
- `PriorityLevel` - Priority levels (HIGH, MEDIUM, LOW)

### 2. Provenance Mixins (provenance.py)

**NodeProv** - For graph nodes:
```python
class NodeProv(ModelBase):
    node_id: str                           # Unique identifier
    entity_type: str                       # Business/logical type
    uri: Optional[str]                     # Canonical ontology URI
    prov_system: ProvenanceSystem          # System of origin
    prov_file_ids: List[str]               # Source file IDs
    prov_rev_ids: List[str]                # Revision tracking
    prov_text_sha1s: List[str]             # Content hashes
    prov_permalinks: List[str]             # Permanent URLs
    doc_paths: List[str]                   # Document hierarchy
    page_nums: List[int]                   # Page numbers
    support_count: int                     # Evidence count
```

**EdgeProv** - For graph edges:
```python
class EdgeProv(ModelBase):
    rel_id: str                            # Unique identifier
    uri: Optional[str]                     # Canonical ontology URI
    derived: bool                          # Inferred vs. stated
    derivation_rule: Optional[str]         # Derivation logic
    prov_system: ProvenanceSystem          # System of origin
    prov_file_ids: List[str]               # Source file IDs
    prov_text_sha1s: List[str]             # Content hashes
    confidence_score: Optional[float]      # Confidence (0.0-1.0)
```

### 3. ID Generation (id_utils.py)

**Deterministic ID Functions:**

```python
# Node IDs
generate_node_id(
    entity_type="Paragraph",
    key_fields={"doc_id": "SS-59", "ordinal": 45},
    group_id="AAOIFI-SS-59-EN-2023"
)
# => "AAOIFI-SS-59-EN-2023:Paragraph:SS-59:45"

# Edge IDs
generate_edge_id(
    edge_type="IsPartOf",
    source_id="Paragraph:P45",
    target_id="Section:S4"
)
# => "IsPartOf:Paragraph:P45=>Section:S4"

# Text hashes (SHA1)
generate_text_hash("The seller must disclose cost and profit.")
# => "163dd646d1d27fda..." (40 hex chars)
```

### 4. Type Registries (registry.py)

**EntityTypeRegistry** - Tracks entity types:
```python
ENTITY_TYPES.register(
    "Paragraph",
    ParagraphModel,
    canonical_uri="http://purl.org/spar/doco/Paragraph"
)

model = ENTITY_TYPES.get_model("Paragraph")
uri = ENTITY_TYPES.get_uri("Paragraph")
types = ENTITY_TYPES.list_types()
```

**EdgeTypeRegistry** - Tracks edge types and valid combinations:
```python
EDGE_TYPES.register(
    "IsPartOf",
    source_type="Paragraph",
    target_type="Section",
    canonical_uri="http://purl.org/dc/terms/isPartOf"
)

is_valid = EDGE_TYPES.is_valid("IsPartOf", "Paragraph", "Section")
valid_targets = EDGE_TYPES.get_valid_targets("IsPartOf", "Paragraph")
```

### 5. Graph Protocol (types.py)

**GraphAccessor** - Interface for graph adapters:
```python
class GraphAccessor(Protocol):
    async def add_node(...) -> None
    async def add_edge(...) -> None
    async def search(...) -> List[Dict[str, Any]]
    async def get_node(...) -> Optional[Dict[str, Any]]
```

Implementations:
- `GraphitiAdapter` - Real Neo4j-backed graph
- `MockGraphAdapter` - In-memory mock for offline mode

## Usage Patterns

### Defining a Domain Model

```python
from graphmodels.core import NodeProv, generate_node_id, ProvenanceSystem

class Paragraph(NodeProv):
    text: str
    ordinal: int
    section_id: str
    page_from: int
    page_to: int

# Create instance
para = Paragraph(
    node_id=generate_node_id(
        "Paragraph",
        {"doc_id": "SS-59", "ordinal": 45},
        group_id="AAOIFI-SS-59-EN-2023"
    ),
    entity_type="Paragraph",
    text="The seller must disclose cost and profit.",
    ordinal=45,
    section_id="S4",
    page_from=27,
    page_to=27,
    prov_system=ProvenanceSystem.AAOIFI,
    prov_file_ids=["ss-59-en.json"],
    page_nums=[27],
)
```

### Registering Models

```python
from graphmodels.core import ENTITY_TYPES, EDGE_TYPES

# Register entity type
ENTITY_TYPES.register(
    "Paragraph",
    Paragraph,
    canonical_uri="http://purl.org/spar/doco/Paragraph"
)

# Register edge type
EDGE_TYPES.register(
    "IsPartOf",
    "Paragraph",
    "Section",
    canonical_uri="http://purl.org/dc/terms/isPartOf"
)
```

### LinkML Integration

LinkML-generated models will extend these base classes:

```yaml
# schemas/overlays/overlay.yaml
imports:
  - ../../core.yaml  # LinkML version

classes:
  Paragraph:
    mixins:
      - NodeProv     # Inherits all provenance fields
    attributes:
      text: string
      ordinal: integer
```

Generated Pydantic:
```python
from graphmodels.core import NodeProv

class Paragraph(NodeProv):
    text: str
    ordinal: int
```

## Testing

Run core foundation tests:
```bash
python test_core_foundation.py
```

Tests validate:
- ✓ Deterministic ID generation
- ✓ Provenance model instantiation
- ✓ Registry operations
- ✓ Strict validation (extra fields, type coercion)

## Design Principles

1. **Strict Validation** - No surprises, fail fast
2. **Deterministic IDs** - Reproducible, content-addressable
3. **Full Provenance** - Track all origins and derivations
4. **Type Safety** - Leverage Pydantic V2 strict mode
5. **Modular** - Core foundation independent of pipeline

## Next Steps

With core foundation complete:
1. ✓ Pydantic V2 base layer established
2. → Build LinkML pipeline agents (ontology retriever, schema synthesizer)
3. → Generate outcome-specific overlays extending this base
4. → Implement Graphiti adapter using registries
5. → Build evaluation pipeline

The foundation ensures all models (LinkML-generated and hand-crafted) share:
- Consistent provenance tracking
- Deterministic identification
- Type-safe validation
- Registry-based type management
