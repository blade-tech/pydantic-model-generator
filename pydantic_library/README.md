# Outcome-Driven Modular Pydantic Library

A modular, outcome-first architecture for generating Pydantic models from LinkML schemas with closed-loop validation against business requirements.

## Quick Start

### Installation

```bash
# Install LinkML
pip install linkml

# Install dependencies
pip install pydantic pytest
```

### Generate Models

```bash
cd "D:\projects\Pydantic Model Generator\v1_to_v2_migration"

# Generate from overlay schema
gen-pydantic schemas/overlays/business_outcomes_overlay.yaml \
  --template-dir templates \
  > generated/pydantic/overlays/business_outcomes_models.py
```

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific overlay tests
pytest tests/test_aaoifi_standards.py -v
```

## Architecture Overview

### Outcome-First Design

Schemas are organized by **questions to answer**, not by static domains:

```yaml
# specs/business_outcomes_tracking.yaml
outcome_questions:
  - question: "What business outcomes are we tracking and what is their status?"
    target_entities: [BusinessOutcome]
    required_attributes: [name, status, priority, owner, due_date]
```

This enables:
- **Closed-loop validation**: Test if generated models can answer the original questions
- **Minimalism**: Only 5-8 entities per overlay (not 10+)
- **Testability**: Validate queries execute against OutcomeSpecs

### Three-Layer Architecture

```
Core (universal infrastructure)
  ↓
Shared (cross-outcome components)
  ↓
Overlays (outcome-specific entities and edges)
```

**Core Layer** (`schemas/core/`):
- `base.yaml`: ConfiguredBaseModel with Pydantic v2 settings
- `provenance.yaml`: ProvenanceFields and EdgeProvenanceFields mixins
- `types.yaml`: Custom validation types (Email, E164Phone, Confidence01)

**Shared Layer** (`schemas/shared/`):
- `identity.yaml`: Actor, Customer, Project (used across overlays)

**Overlay Layer** (`schemas/overlays/`):
- `business_outcomes_overlay.yaml`: Business outcome tracking (4 entities, 6 edges)
- `aaoifi_standards_overlay.yaml`: Islamic finance standards (7 entities, 4 edges)

## Available Overlays

### Business Outcomes Overlay

**OutcomeSpec**: `specs/business_outcomes_tracking.yaml`
**Schema**: `schemas/overlays/business_outcomes_overlay.yaml`
**Models**: `generated/pydantic/overlays/business_outcomes_models.py`
**Glue**: `generated/pydantic/overlays/business_outcomes_glue.py`

**Core Questions**:
- What business outcomes are we tracking and what is their status?
- What tasks are required to complete each outcome?
- What decisions are blocking progress?
- What handoffs exist between teams?

**Entities**: BusinessOutcome, BusinessTask, BusinessDecision, BusinessHandoff
**Test Coverage**: 18 V1/V2 compatibility tests

### AAOIFI Standards Overlay

**OutcomeSpec**: `specs/aaoifi_standards_extraction.yaml`
**Schema**: `schemas/overlays/aaoifi_standards_overlay.yaml`
**Models**: `generated/pydantic/overlays/aaoifi_standards_models.py`
**Glue**: `generated/pydantic/overlays/aaoifi_standards_glue.py`

**Core Questions**:
- What AAOIFI standard documents exist and who issued them?
- What is the structural hierarchy of a standard document?
- What topical concepts are covered in each section?
- What normative rules exist and where are they sourced from?
- What contract types are defined and what rules apply to them?

**Entities**: Document, Section, Paragraph, Concept, ContractType, Rule, Agent
**Canonical Ontologies**: DoCO, FaBiO, PROV-O, FIBO, SKOS
**Test Coverage**: 31 OutcomeSpec validation tests

## Usage Examples

### Business Outcomes

```python
from datetime import date
from generated.pydantic.overlays.business_outcomes_models import (
    BusinessOutcome,
    BusinessTask,
)
from generated.pydantic.shared.identity import Actor, Customer

# Create a business outcome
outcome = BusinessOutcome(
    name="Launch MVP",
    status="in_progress",
    priority="high",
    owner="alice@example.com",
    due_date=date(2025, 12, 31),
    completion_confidence=0.85,
    node_id="outcome_001",
)

# Create a task
task = BusinessTask(
    name="Implement authentication",
    status="in_progress",
    priority="high",
    estimated_effort=8.0,  # hours
    node_id="task_001",
)
```

### AAOIFI Standards

```python
from datetime import date
from generated.pydantic.overlays.aaoifi_standards_models import (
    Document,
    Section,
    Paragraph,
    Rule,
    EvidenceOf,
)
from generated.pydantic.overlays.aaoifi_standards_glue import (
    get_entity_uri,
    validate_edge_type,
)

# Create a document
doc = Document(
    title="AAOIFI Sharia Standard No. 59",
    edition="2023",
    issued=date(2023, 1, 1),
    node_id="AAOIFI-SS-59",
)

# Get canonical URI
uri = get_entity_uri("Document")
# Returns: "http://purl.org/spar/fabio/SpecificationDocument"

# Validate edge type
valid = validate_edge_type("Rule", "Paragraph", "EvidenceOf")
# Returns: True
```

## Adding New Overlays

Follow the 8-step workflow documented in [`MIGRATION_GUIDE.md`](MIGRATION_GUIDE.md#adding-new-overlays):

1. **Create OutcomeSpec** in `specs/`
2. **Create Overlay Schema** in `schemas/overlays/`
3. **Generate Pydantic Models** using `gen-pydantic`
4. **Create Graphiti Glue File** with type registries
5. **Create Tests** for OutcomeSpec validation queries
6. **Run Tests** with pytest
7. **Update Documentation**
8. **Validate Closed-Loop** - all questions answerable

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

## Key Features

✅ **Outcome-driven design**: Schemas organized by questions, not domains
✅ **Closed-loop validation**: Test if models answer original questions
✅ **Minimalism**: Only 5-8 entities per overlay (not 10+)
✅ **Canonical URIs**: Semantic interoperability via standard ontologies
✅ **Universal provenance**: Track data lineage across all entities
✅ **Graphiti integration**: Type registries and edge validation
✅ **Testability**: 49 tests covering compatibility and OutcomeSpecs

## Test Results

```bash
$ pytest tests/ -v

============================= 49 passed in 0.14s ==============================
```

**Test Coverage**:
- 18 V1/V2 compatibility tests
- 31 AAOIFI standards tests (OutcomeSpec validation)

## Documentation

- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)**: Comprehensive migration guide from monolithic to modular structure
- **OutcomeSpecs**: `specs/` directory contains validation questions and queries
- **Schemas**: `schemas/` directory contains LinkML schema definitions

## Canonical Ontologies

AAOIFI overlay uses standard ontology URIs for semantic interoperability:

- **DoCO**: Document Components Ontology (structure)
- **FaBiO**: FRBR-aligned Bibliographic Ontology (document types)
- **PROV-O**: Provenance Ontology (attribution, derivation)
- **FIBO**: Financial Industry Business Ontology (contracts)
- **SKOS**: Simple Knowledge Organization System (concepts)

## Links

- **LinkML Documentation**: https://linkml.io/
- **Pydantic V2 Documentation**: https://docs.pydantic.dev/
- **Graphiti**: Knowledge graph integration (type registries)
- **OutcomeSpec Pattern**: Closed-loop validation methodology

## License

This is a teaching artifact demonstrating outcome-driven Pydantic model generation.
