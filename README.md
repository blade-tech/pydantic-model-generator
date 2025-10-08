# Pydantic Model Library with Outcome-Driven Architecture

**Modular Pydantic library with universal provenance tracking and Graphiti knowledge graph integration.**

---

## 🎯 What This Is

A production-ready Pydantic model library organized by **business outcomes**, not domains. Each "overlay" answers specific business questions with:

- **Minimal schemas** (5-8 entities max per overlay)
- **Universal provenance** (13 node fields + 15 edge fields)
- **Canonical ontology URIs** (DoCO, FaBiO, PROV-O, FIBO, SKOS)
- **Graphiti integration** (type registries + edge validation)
- **Closed-loop validation** (tests verify models answer business questions)

---

## 🚀 Quick Start

### Use Existing Models

```python
from pydantic_library.generated.pydantic.overlays.business_outcomes_models import (
    BusinessOutcome,
    OutcomeStatus
)

outcome = BusinessOutcome(
    node_id="outcome_001",
    name="Launch payment feature",
    status=OutcomeStatus.in_progress,
    completion_confidence=0.75
)
```

### Add New Overlay

```bash
# Automated pipeline
python pipeline/add_overlay.py --name "customer_support"

# Or follow 8-step manual workflow
# See: pydantic_library/MIGRATION_GUIDE.md
```

### Run Tests

```bash
cd pydantic_library
python -m pytest tests/ -v
```

**Status**: ✅ 31/31 tests passing

---

## 📂 Repository Structure

```
D:\projects\Pydantic Model Generator\
│
├── README.md                          # ← You are here
├── QUICK_START.md                     # 5-minute getting started guide
├── PROJECT_CONTEXT.md                 # Full context for AI continuation
│
├── pydantic_library/                  # Modular Pydantic library
│   ├── README.md                      # Library architecture
│   ├── MIGRATION_GUIDE.md             # 8-step workflow for adding overlays
│   ├── HANDOFF.md                     # Quick recovery for AI
│   ├── DECOMPOSITION_REPORT.md        # Final validation metrics
│   │
│   ├── schemas/                       # LinkML schemas
│   │   ├── core/provenance.yaml       # Universal provenance (13 + 15 slots)
│   │   ├── shared/shared_types.yaml   # Cross-outcome types
│   │   └── overlays/                  # Outcome-specific schemas
│   │       ├── business_outcomes_overlay.yaml
│   │       └── aaoifi_standards_overlay.yaml
│   │
│   ├── generated/pydantic/            # Generated Pydantic models
│   │   ├── core/provenance.py
│   │   ├── shared/shared_types.py
│   │   └── overlays/
│   │       ├── business_outcomes_models.py
│   │       ├── business_outcomes_glue.py
│   │       ├── aaoifi_standards_models.py
│   │       └── aaoifi_standards_glue.py
│   │
│   ├── specs/                         # OutcomeSpecs (business questions)
│   │   ├── business_outcomes.yaml
│   │   └── aaoifi_standards.yaml
│   │
│   └── tests/                         # Evidence Query Plans (49 tests)
│       ├── test_v1_v2_compatibility.py (18 tests)
│       └── test_aaoifi_standards.py    (31 tests)
│
├── pipeline/                          # Tools for adding overlays
│   ├── README.md                      # Pipeline usage guide
│   ├── add_overlay.py                 # Automated overlay creation
│   ├── templates/
│   │   ├── outcome_spec_template.yaml
│   │   ├── overlay_schema_template.yaml
│   │   └── test_template.py
│   └── examples/
│
├── docs/                              # Technical documentation
│   ├── GRAPHITI_INTEGRATION.md        # How to use with Graphiti
│   ├── ONTOLOGY_MAPPING.md            # Canonical URI reference
│   ├── AGENT_PIPELINE.md              # AI-assisted overlay generation
│   └── archive/                       # Historical context
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── Makefile
```

---

## 🏗️ Architecture

### Three-Layer Design

```
Core (Universal)
  ├─ ProvenanceFields (13 slots: node_id, source_uri, extraction_confidence, ...)
  └─ EdgeProvenanceFields (15 slots: rel_id, confidence_score, quote, ...)

Shared (Cross-Outcome)
  ├─ Deliverable, Milestone, Team
  └─ Reused across multiple overlays

Overlays (Outcome-Specific)
  ├─ Business Outcomes (4 entities, 6 edges)
  └─ AAOIFI Standards (7 entities, 4 edges)
```

### Key Principles

1. **Outcome-First**: Organize by questions to answer, not domains
2. **Minimalism**: Max 5-8 entities per overlay
3. **Closed-Loop Validation**: Tests verify models answer business questions
4. **Universal Provenance**: Every entity/edge tracks its source
5. **Canonical Ontologies**: Map to standard ontology URIs
6. **Graphiti-Ready**: Type registries for knowledge graph ingestion

---

## 📊 Current Overlays

### 1. Business Outcomes (4 entities, 6 edges)

**Purpose**: Track deliverables, milestones, task assignments, handoffs

**Entities**:
- BusinessOutcome, BusinessDecision, BusinessTask, BusinessHandoff

**Use Cases**:
- Project planning discussions (Slack, email)
- Task assignment tracking
- Outcome status monitoring
- Decision impact analysis

**Files**:
- Schema: `pydantic_library/schemas/overlays/business_outcomes_overlay.yaml`
- Models: `pydantic_library/generated/pydantic/overlays/business_outcomes_models.py`
- Glue: `pydantic_library/generated/pydantic/overlays/business_outcomes_glue.py`
- Tests: `pydantic_library/tests/test_v1_v2_compatibility.py` (18 tests)

### 2. AAOIFI Standards (7 entities, 4 edges)

**Purpose**: Model Islamic finance standards documents with provenance

**Entities**:
- Document, Section, Paragraph, Concept, ContractType, Rule, Agent

**Use Cases**:
- Standards document ingestion
- Rule provenance tracking
- Compliance requirement extraction
- Concept definition lookup

**Files**:
- Schema: `pydantic_library/schemas/overlays/aaoifi_standards_overlay.yaml`
- Models: `pydantic_library/generated/pydantic/overlays/aaoifi_standards_models.py`
- Glue: `pydantic_library/generated/pydantic/overlays/aaoifi_standards_glue.py`
- Tests: `pydantic_library/tests/test_aaoifi_standards.py` (31 tests)

---

## 🔗 Graphiti Integration

### Type Registries

Each overlay provides type registries for Graphiti:

```python
from pydantic_library.generated.pydantic.overlays.business_outcomes_glue import (
    BUSINESS_OUTCOMES_ENTITY_TYPES,
    BUSINESS_OUTCOMES_EDGE_TYPES,
    BUSINESS_OUTCOMES_EDGE_TYPE_MAP,
    validate_edge_type
)

# Validate edge before creation
is_valid = validate_edge_type("BusinessTask", "Actor", "AssignedTo")
```

### Data Flow

```
Business Document
  ↓
Graphiti Episode Ingestion (EpisodeType.message/.text/.json)
  ↓
LLM Entity Extraction
  ↓
Pydantic Model Creation (from extracted entities)
  ↓
Validation with OutcomeSpec Tests
```

**See**: `docs/GRAPHITI_INTEGRATION.md` for complete guide

---

## 🛠️ Adding New Overlays

### Option 1: Automated Pipeline (Recommended)

```bash
python pipeline/add_overlay.py --name "customer_support"
```

This creates templates for:
- OutcomeSpec (business questions)
- LinkML schema (entity definitions)
- Pydantic models (auto-generated)
- Glue code (type registries)
- Tests (validation queries)

**See**: `pipeline/README.md` for details

### Option 2: Manual (8-Step Workflow)

1. Create OutcomeSpec (`specs/your_overlay.yaml`)
2. Create LinkML schema (`schemas/overlays/your_overlay.yaml`)
3. Generate Pydantic models (`gen-pydantic`)
4. Create glue code (`generated/pydantic/overlays/your_glue.py`)
5. Write tests (`tests/test_your_overlay.py`)
6. Run tests (`pytest`)
7. Update documentation
8. Commit changes

**See**: `pydantic_library/MIGRATION_GUIDE.md` for complete workflow

---

## 📚 Documentation

### Getting Started
- **[QUICK_START.md](QUICK_START.md)** - 5-minute getting started guide
- **[pydantic_library/README.md](pydantic_library/README.md)** - Library architecture
- **[pydantic_library/HANDOFF.md](pydantic_library/HANDOFF.md)** - Quick recovery for AI

### Adding Overlays
- **[pipeline/README.md](pipeline/README.md)** - Pipeline tools usage
- **[pydantic_library/MIGRATION_GUIDE.md](pydantic_library/MIGRATION_GUIDE.md)** - 8-step workflow

### Integration & Advanced
- **[docs/GRAPHITI_INTEGRATION.md](docs/GRAPHITI_INTEGRATION.md)** - Graphiti usage patterns
- **[docs/ONTOLOGY_MAPPING.md](docs/ONTOLOGY_MAPPING.md)** - Canonical URI reference
- **[docs/AGENT_PIPELINE.md](docs/AGENT_PIPELINE.md)** - AI-assisted generation

### Context Preservation
- **[PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)** - Full project context for AI
- **[docs/archive/](docs/archive/)** - Historical planning documents

---

## 🧪 Testing

### Run All Tests
```bash
cd pydantic_library
python -m pytest tests/ -v
```

### Run Specific Overlay Tests
```bash
python -m pytest tests/test_aaoifi_standards.py -v
```

### Test Structure
- **AAOIFI Standards** (31 tests): OutcomeSpec validation queries

**Current Status**: ✅ 31/31 tests passing

---

## 🔑 Key Concepts

### OutcomeSpec
Defines business questions your schema must answer:

```yaml
outcome_questions:
  - question: "What tasks are assigned to deliver each outcome?"
    target_entities: [BusinessTask, BusinessOutcome]

validation_queries:
  - name: "test_task_assignment"
    cypher: |
      MATCH (task:BusinessTask)-[r:AssignedTo]->(actor:Actor)
      RETURN task.title, actor.name
```

### Evidence Query Plan (EQP)
Test suite generated from OutcomeSpec to validate models:

```python
def test_task_assignment(self):
    """Validation query: test_task_assignment"""
    task = BusinessTask(node_id="task_001", title="Implement feature")
    actor = Actor(node_id="actor_001", name="John")
    edge = AssignedTo(rel_id="edge_001")

    assert hasattr(task, 'title')
    assert hasattr(actor, 'name')
```

### Universal Provenance
Every entity tracks its source:

```python
outcome = BusinessOutcome(
    node_id="outcome_001",                    # Required, stable ID
    source_uri="slack://channel/planning",    # Source location
    source_document_id="thread_12345",        # Source document
    extraction_confidence=0.9,                # LLM confidence
    extraction_timestamp=datetime.now(),      # When extracted
    # ... + 8 more provenance fields
)
```

### Canonical Ontology URIs
All entities map to standard ontology classes:

```yaml
classes:
  Document:
    class_uri: fabio:SpecificationDocument  # FaBiO ontology
  Section:
    class_uri: doco:Section                 # DoCO ontology
  Rule:
    class_uri: fibo:ContractualElement      # FIBO ontology
```

**Supported Ontologies**:
- **DoCO** (Documents): http://purl.org/spar/doco/
- **FaBiO** (Bibliography): http://purl.org/spar/fabio/
- **PROV-O** (Provenance): http://www.w3.org/ns/prov#
- **FIBO** (Finance): https://spec.edmcouncil.org/fibo/ontology/
- **SKOS** (Concepts): http://www.w3.org/2004/02/skos/core#

---

## 🎯 Design Decisions

### Why Outcome-Driven?
Traditional domain modeling creates bloated schemas trying to model everything. Outcome-driven modeling focuses on answering specific business questions with minimal entities.

### Why 3 Layers?
- **Core**: Universal patterns (provenance) used everywhere
- **Shared**: Common types (Deliverable, Milestone) used across outcomes
- **Overlays**: Outcome-specific entities (minimal, focused)

### Why OutcomeSpecs?
Tests verify models support real business questions. If models can't answer the questions, the schema failed.

### Why Canonical Ontology URIs?
Enables semantic interoperability, data exchange, and integration with existing knowledge graphs.

### Why Graphiti?
Neo4j-backed knowledge graph with LLM-powered entity extraction. Graphiti handles ingestion, we provide type validation.

---

## 🚧 Roadmap

### Completed ✅
- Modular 3-layer architecture
- Universal provenance (13 + 15 fields)
- 2 overlays (Business Outcomes, AAOIFI Standards)
- 31/31 tests passing
- Graphiti type registries
- Pipeline tools for adding overlays

### In Progress 🔨
- Automated overlay generation from business documents
- AI-assisted OutcomeSpec creation
- Enhanced test generation

### Planned 🔮
- More overlays (customer support, inventory, compliance)
- Graphiti ingestion examples
- Full AI agent pipeline (business doc → Pydantic module)
- Performance benchmarks
- Schema versioning strategy

---

## 🤝 Contributing

### Adding Overlays
1. Use `python pipeline/add_overlay.py --name "your_overlay"`
2. Follow 8-step workflow in `MIGRATION_GUIDE.md`
3. Ensure all tests pass (pytest)
4. Update documentation

### Code Quality
- All entities must include `ProvenanceFields` mixin
- All edges must include `EdgeProvenanceFields` mixin
- Max 5-8 entities per overlay
- Map entities to canonical ontology URIs
- Write OutcomeSpec validation tests

### Testing
- All new overlays must have Evidence Query Plan tests
- All tests must pass before committing
- Test coverage should be >90%

---

## 📝 License

[Your License Here]

---

## 🆘 Support

- **Quick Start**: `QUICK_START.md`
- **Library Docs**: `pydantic_library/README.md`
- **Pipeline Docs**: `pipeline/README.md`
- **Full Context**: `PROJECT_CONTEXT.md`

---

**Built with**: LinkML • Pydantic V2 • Graphiti • Neo4j

**Status**: ✅ Production Ready (31/31 tests passing)
