# Migration Guide: Monolithic to Modular Outcome-Driven Architecture

This guide documents the migration from a single monolithic `entities_v2.py` file to a modular, outcome-driven Pydantic library structure.

## Table of Contents

1. [Migration Overview](#migration-overview)
2. [Architecture Principles](#architecture-principles)
3. [Directory Structure](#directory-structure)
4. [Key Changes](#key-changes)
5. [Import Path Changes](#import-path-changes)
6. [Testing Strategy](#testing-strategy)
7. [Adding New Overlays](#adding-new-overlays)

---

## Migration Overview

### What Changed

**Before (Monolithic):**
- Single file: `entities_v2.py` (1195 lines)
- 10 entity classes + 10 edge classes
- Domain-organized (all business models together)
- No formal validation against business requirements

**After (Modular):**
- **Core infrastructure** (3 files): base, provenance, types
- **Shared components** (1 file): identity (Actor, Customer, Project)
- **Outcome-driven overlays** (2 overlays):
  - `business_outcomes_overlay`: 4 entities, 6 edges
  - `aaoifi_standards_overlay`: 7 entities, 4 edges
- **OutcomeSpecs** drive each overlay design
- **Closed-loop validation** via Evidence Query Plans (EQP)

### Why Outcome-Driven?

The modular structure organizes schemas by **questions we need to answer**, not by static domains:

```yaml
# specs/business_outcomes_tracking.yaml
outcome_questions:
  - question: "What business outcomes are we tracking and what is their status?"
    target_entities: [BusinessOutcome]
    required_attributes: [name, status, priority, owner, due_date]
```

This enables:
- **Closed-loop validation**: Test if generated models can answer the original questions
- **Minimalism**: Only create entities needed for specific outcomes (5-8 entities max per overlay)
- **Testability**: Validate queries execute against OutcomeSpecs

---

## Architecture Principles

### 1. Outcome-First Design

**Start with questions, not entities:**

1. Define `outcome_questions` in an OutcomeSpec
2. Extract `target_entities` and `required_relations` from questions
3. Create minimal overlay schema with only necessary classes
4. Generate Pydantic models
5. Validate with Evidence Query Plans (validation_queries)

### 2. Three-Layer Structure

```
Core (universal infrastructure)
  ↓
Shared (cross-outcome components)
  ↓
Overlays (outcome-specific entities and edges)
```

**Core Layer:**
- `base.yaml`: ConfiguredBaseModel with Pydantic v2 settings
- `provenance.yaml`: ProvenanceFields and EdgeProvenanceFields mixins
- `types.yaml`: Custom validation types (Email, E164Phone, Confidence01)

**Shared Layer:**
- `identity.yaml`: Actor, Customer, Project (used across multiple overlays)

**Overlay Layer:**
- `business_outcomes_overlay.yaml`: Business outcome tracking
- `aaoifi_standards_overlay.yaml`: Islamic finance standards extraction

### 3. Graphiti Integration

Each overlay includes a `*_glue.py` file for knowledge graph integration:

```python
# Entity type registries
ENTITY_TYPES: Dict[str, type[BaseModel]] = {
    "BusinessOutcome": BusinessOutcome,
    # ...
}

# Edge type mappings (validates allowed relationships)
EDGE_TYPE_MAP: Dict[tuple, List[str]] = {
    ("BusinessOutcome", "BusinessDecision"): ["BlockedBy"],
    # ...
}

# Canonical ontology URIs (for RDF export)
NODE_URI: Dict[str, str] = {
    "Document": "http://purl.org/spar/fabio/SpecificationDocument",
    # ...
}
```

---

## Directory Structure

```
v1_to_v2_migration/
├── specs/                                # OutcomeSpec definitions
│   ├── business_outcomes_tracking.yaml   # Business outcomes questions
│   └── aaoifi_standards_extraction.yaml  # AAOIFI standards questions
│
├── schemas/                              # LinkML schemas
│   ├── core/                             # Universal infrastructure
│   │   ├── base.yaml                     # ConfiguredBaseModel
│   │   ├── provenance.yaml               # Provenance mixins
│   │   └── types.yaml                    # Custom validation types
│   │
│   ├── shared/                           # Cross-outcome components
│   │   └── identity.yaml                 # Actor, Customer, Project
│   │
│   └── overlays/                         # Outcome-specific schemas
│       ├── business_outcomes_overlay.yaml
│       └── aaoifi_standards_overlay.yaml
│
├── generated/pydantic/                   # Generated Pydantic models
│   ├── core/
│   │   ├── base.py                       # Manually created
│   │   ├── provenance.py                 # Generated via gen-pydantic
│   │   └── types.py                      # Manually created
│   │
│   ├── shared/
│   │   └── identity.py                   # Generated via gen-pydantic
│   │
│   └── overlays/
│       ├── business_outcomes_models.py   # Generated via gen-pydantic
│       ├── business_outcomes_glue.py     # Manually created
│       ├── aaoifi_standards_models.py    # Generated via gen-pydantic
│       └── aaoifi_standards_glue.py      # Manually created
│
├── templates/                            # Jinja2 templates for generation
│   ├── base_model.py.jinja               # Base model template
│   └── class.py.jinja                    # Class generation template
│
└── tests/                                # Test suite
    ├── test_v1_v2_compatibility.py       # V1/V2 compatibility tests
    └── test_aaoifi_standards.py          # AAOIFI standards tests
```

---

## Key Changes

### Field Name Changes

**BusinessOutcome:**

| V1 (Monolithic)      | V2 (Modular)            | Notes                          |
|----------------------|-------------------------|--------------------------------|
| `outcome_type`       | *(removed)*             | Not in minimal overlay         |
| `confidence_score`   | `completion_confidence` | Renamed for clarity            |
| `for_customer`       | *(removed)*             | Use edges to Customer entity   |

**BusinessTask:**

| V1 (Monolithic)         | V2 (Modular)        | Notes                          |
|-------------------------|---------------------|--------------------------------|
| `description`           | `name`              | Simplified to universal `name` |
| `task_status`           | `status`            | Aligned with other entities    |
| `estimated_effort`      | `estimated_effort`  | Now float (hours)              |

### Provenance Tracking

Universal provenance via **ProvenanceFields** mixin (13 slots):

```python
class ProvenanceFields(ConfiguredBaseModel):
    node_id: Optional[str]               # Stable citation id
    prov_system: Optional[str]           # Source system (slack, gdrive, etc.)
    prov_channel_ids: Optional[list[str]]  # Slack channels
    prov_tss: Optional[list[str]]        # Slack timestamps
    prov_file_ids: Optional[list[str]]   # Document identifiers
    doco_types: Optional[list[str]]      # Document component types
    page_nums: Optional[list[int]]       # Page numbers
    support_count: Optional[int]         # Number of supporting evidences
    # ... and 5 more slots
```

Edges get **EdgeProvenanceFields** with additional fields:
- `derived`: Whether derived vs directly extracted
- `derivation_rule`: Rule or method used for derivation

### Canonical Ontology URIs

AAOIFI models use standard ontology URIs for semantic interoperability:

```python
AAOIFI_NODE_URI = {
    "Document": "http://purl.org/spar/fabio/SpecificationDocument",  # FaBiO
    "Section": "http://purl.org/spar/doco/Section",                  # DoCO
    "Paragraph": "http://purl.org/spar/doco/Paragraph",              # DoCO
    "Concept": "http://www.w3.org/2004/02/skos/core#Concept",        # SKOS
    "Agent": "http://www.w3.org/ns/prov#Agent",                      # PROV-O
    # ...
}
```

**Ontologies used:**
- **DoCO**: Document Components Ontology (structure)
- **FaBiO**: FRBR-aligned Bibliographic Ontology (document types)
- **PROV-O**: Provenance Ontology (attribution, derivation)
- **FIBO**: Financial Industry Business Ontology (contracts)
- **SKOS**: Simple Knowledge Organization System (concepts)

---

## Import Path Changes

### Before (Monolithic)

```python
from entities_v2 import (
    BusinessOutcome,
    BusinessTask,
    Actor,
    Customer,
)
```

### After (Modular)

```python
# Overlay-specific entities
from generated.pydantic.overlays.business_outcomes_models import (
    BusinessOutcome,
    BusinessTask,
    BusinessDecision,
    BusinessHandoff,
)

# Shared components
from generated.pydantic.shared.identity import (
    Actor,
    Customer,
    Project,
)

# Graphiti integration
from generated.pydantic.overlays.business_outcomes_glue import (
    BUSINESS_OUTCOMES_ENTITY_TYPES,
    BUSINESS_OUTCOMES_EDGE_TYPE_MAP,
    validate_edge_type,
)
```

### AAOIFI Standards

```python
from generated.pydantic.overlays.aaoifi_standards_models import (
    Document,
    Section,
    Paragraph,
    Concept,
    ContractType,
    Rule,
    Agent,
)

from generated.pydantic.overlays.aaoifi_standards_glue import (
    AAOIFI_NODE_URI,
    AAOIFI_EDGE_URI,
    get_entity_uri,
    get_edge_uri,
    validate_edge_type,
)
```

---

## Testing Strategy

### 1. V1/V2 Compatibility Tests

`tests/test_v1_v2_compatibility.py` validates:
- V1 models work with legacy data
- V2 models work with adapted data
- Provenance fields function correctly
- ConfiguredBaseModel settings (extra='ignore', str_strip_whitespace, etc.)

**Key adaptations:**
```python
# V1 format
v1_data = {
    "outcome_type": "deliverable",
    "confidence_score": 0.85,
}

# V2 format (simplified)
v2_data = {
    "name": "Deliverable outcome",
    "completion_confidence": 0.85,
}
```

### 2. AAOIFI Standards Tests

`tests/test_aaoifi_standards.py` validates:
- Entity creation with required fields
- Edge relationships
- Canonical URI mappings
- Graphiti type registries
- Edge type validation functions
- **OutcomeSpec validation queries** (EQP)

**OutcomeSpec Validation Example:**
```python
def test_rule_provenance(self):
    """Validation query: test_rule_provenance

    Expected fields: article_no, normative_effect, page_from, page_to
    Expected relations: EvidenceOf (Rule→Paragraph)
    """
    rule = Rule(
        article_no="Art. 1",
        normative_effect="requires",
        # ...
    )
    # Verify all required fields exist
    assert hasattr(rule, 'article_no')
    assert hasattr(rule, 'normative_effect')
```

### 3. Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_aaoifi_standards.py -v

# Run with short traceback
pytest tests/ -v --tb=short
```

**Current test coverage:**
- 18 V1/V2 compatibility tests
- 31 AAOIFI standards tests
- **49 total tests, all passing**

---

## Adding New Overlays

Follow this 8-step workflow to add a new overlay:

### Step 1: Create OutcomeSpec

Create `specs/your_outcome.yaml`:

```yaml
id: https://example.org/specs/your-outcome
name: your_outcome
description: |
  What business questions does this overlay answer?

outcome_questions:
  - question: "What entities do I need to track?"
    target_entities: [YourEntity]
    required_relations: [YourEdge]
    required_attributes: [YourEntity.field1, YourEntity.field2]

# Define entities needed to answer questions
core_entities:
  YourEntity:
    description: "Description of entity"
    required_for: ["answering question 1"]

# Define relationships
core_relations:
  YourEdge:
    description: "Relationship description"
    source: YourEntity1
    target: YourEntity2

# Create validation queries (Evidence Query Plan)
validation_queries:
  - name: "test_your_query"
    description: "Can we answer the question?"
    cypher: |
      MATCH (e:YourEntity)
      RETURN e.field1, e.field2
    expected_fields: [field1, field2]
```

### Step 2: Create Overlay Schema

Create `schemas/overlays/your_overlay.yaml`:

```yaml
id: https://example.org/overlays/your-overlay
name: your_overlay
description: |
  Overlay description driven by OutcomeSpec.

  Core question: "What is the primary question?"

imports:
  - ../core/provenance
  - ../core/types
  - ../shared/identity

classes:
  YourEntity:
    description: "Entity description"
    class_uri: canonical:URI  # Use standard ontology URI
    mixins:
      - ProvenanceFields
    slots:
      - field1
      - field2

  YourEdge:
    description: "Edge description"
    class_uri: canonical:EdgeURI
    mixins:
      - EdgeProvenanceFields
    slots:
      - edge_specific_field
```

### Step 3: Generate Pydantic Models

```bash
cd "D:\projects\Pydantic Model Generator\v1_to_v2_migration"

# Generate models
gen-pydantic schemas/overlays/your_overlay.yaml \
  --template-dir templates \
  > generated/pydantic/overlays/your_models.py
```

### Step 4: Create Graphiti Glue File

Create `generated/pydantic/overlays/your_glue.py`:

```python
from typing import Dict, List
from pydantic import BaseModel
from .your_models import YourEntity, YourEdge

# Entity type registry
YOUR_ENTITY_TYPES: Dict[str, type[BaseModel]] = {
    "YourEntity": YourEntity,
}

# Edge type registry
YOUR_EDGE_TYPES: Dict[str, type[BaseModel]] = {
    "YourEdge": YourEdge,
}

# Edge type mappings (source, target) → allowed edges
YOUR_EDGE_TYPE_MAP: Dict[tuple, List[str]] = {
    ("YourEntity1", "YourEntity2"): ["YourEdge"],
}

# Canonical URI mappings
YOUR_NODE_URI: Dict[str, str] = {
    "YourEntity": "https://canonical.ontology/YourEntity",
}

# Validation helpers
def validate_edge_type(source_type: str, target_type: str, edge_type: str) -> bool:
    allowed = YOUR_EDGE_TYPE_MAP.get((source_type, target_type), [])
    return edge_type in allowed
```

### Step 5: Create Tests

Create `tests/test_your_overlay.py`:

```python
import pytest
from generated.pydantic.overlays.your_models import YourEntity
from generated.pydantic.overlays.your_glue import validate_edge_type

class TestOutcomeSpecValidation:
    """Test models support OutcomeSpec validation queries."""

    def test_your_query(self):
        """Validation query: test_your_query

        Expected fields: field1, field2
        """
        entity = YourEntity(field1="value1", field2="value2")
        assert hasattr(entity, 'field1')
        assert hasattr(entity, 'field2')
```

### Step 6: Run Tests

```bash
pytest tests/test_your_overlay.py -v
```

### Step 7: Update Documentation

Add your overlay to `README.md`:

```markdown
## Available Overlays

### Your Overlay
- **OutcomeSpec**: `specs/your_outcome.yaml`
- **Schema**: `schemas/overlays/your_overlay.yaml`
- **Models**: `generated/pydantic/overlays/your_models.py`
- **Core Questions**:
  - "What entities do I need to track?"
```

### Step 8: Validate Closed-Loop

Ensure all `outcome_questions` from your OutcomeSpec have corresponding:
1. Entity classes in overlay schema
2. Required attributes as slots
3. Validation tests in test suite

**Checklist:**
- [ ] OutcomeSpec created with outcome_questions
- [ ] Overlay schema created with all target_entities
- [ ] Pydantic models generated successfully
- [ ] Graphiti glue file created
- [ ] Tests created for all validation_queries
- [ ] All tests pass
- [ ] Documentation updated

---

## Summary

The modular migration enables:

✅ **Outcome-driven design**: Schemas organized by questions, not domains
✅ **Closed-loop validation**: Test if models answer original questions
✅ **Minimalism**: Only 5-8 entities per overlay (not 10+)
✅ **Canonical URIs**: Semantic interoperability via standard ontologies
✅ **Universal provenance**: Track data lineage across all entities
✅ **Graphiti integration**: Type registries and edge validation
✅ **Testability**: 49 tests covering compatibility and OutcomeSpecs

**Next Steps:**
1. Archive monolithic `entities_v2.py` to `archive/`
2. Add more overlays following the 8-step workflow
3. Integrate with Graphiti knowledge graph
4. Export to RDF using canonical URIs
