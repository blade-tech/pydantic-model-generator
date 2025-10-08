# Quick Recovery Handoff - Modular Pydantic Library

**Last Updated**: 2025-10-06
**Status**: ✅ 49/49 tests passing
**Location**: `D:\projects\Pydantic Model Generator\v1_to_v2_migration`

---

## 🚀 Quick Start (5 minutes)

### Run Tests
```bash
cd "D:\projects\Pydantic Model Generator\v1_to_v2_migration"
pytest tests/ -v
```

**Expected**: 49/49 passing (18 V1/V2 compatibility + 31 AAOIFI standards)

### Generate Models from Schema
```bash
cd "D:\projects\Pydantic Model Generator\v1_to_v2_migration"
gen-pydantic schemas/overlays/your_overlay.yaml > generated/pydantic/overlays/your_overlay.py
```

### Add New Overlay (8-Step Workflow)
**See**: `MIGRATION_GUIDE.md` for complete workflow

---

## 📂 Directory Structure

```
v1_to_v2_migration/
├── README.md                          # Library overview + architecture
├── MIGRATION_GUIDE.md                 # ⬅️ COMPLETE 8-STEP WORKFLOW
├── DECOMPOSITION_REPORT.md            # Final validation metrics
├── HANDOFF.md                         # ⬅️ YOU ARE HERE (quick recovery)
├── AGENT_DRIVEN_ONTOLOGY_PIPELINE.md
├── GRAPHITI_INGESTION_METHODS.md
├── ONTOLOGY_MAPPING_STRATEGY.md
│
├── schemas/
│   ├── core/
│   │   └── provenance.yaml            # Universal provenance fields
│   ├── shared/
│   │   └── shared_types.yaml          # Cross-outcome types
│   └── overlays/
│       ├── business_outcomes_overlay.yaml    # 4 entities, 6 edges
│       └── aaoifi_standards_overlay.yaml     # 7 entities, 4 edges
│
├── generated/
│   └── pydantic/
│       ├── core/
│       │   ├── provenance.py          # ProvenanceFields, EdgeProvenanceFields
│       │   └── __init__.py
│       ├── shared/
│       │   ├── shared_types.py        # Deliverable, Milestone, Team
│       │   └── __init__.py
│       └── overlays/
│           ├── business_outcomes_overlay.py    # Generated models
│           ├── business_outcomes_glue.py       # Type registries + validation
│           ├── aaoifi_standards_overlay.py     # Generated models
│           ├── aaoifi_standards_glue.py        # Type registries + validation
│           └── __init__.py
│
├── specs/
│   ├── business_outcomes.yaml         # OutcomeSpec with validation queries
│   └── aaoifi_standards.yaml          # OutcomeSpec with validation queries
│
└── tests/
    ├── test_v1_v2_compatibility.py    # 18 tests (V1/V2 field mappings)
    └── test_aaoifi_standards.py       # 31 tests (OutcomeSpec validation)
```

---

## 🎯 Core Principles

### Three-Layer Architecture
1. **Core** (Universal) → ProvenanceFields (13 slots), EdgeProvenanceFields (15 slots)
2. **Shared** (Cross-Outcome) → Deliverable, Milestone, Team
3. **Overlays** (Outcome-Specific) → Business Outcomes, AAOIFI Standards

### Outcome-Driven Design
- Organize schemas by **questions to answer**, not domains
- Max **5-8 entities per overlay** (minimalism principle)
- **OutcomeSpecs** define validation queries
- **Evidence Query Plans (EQP)** test if models answer questions

### Closed-Loop Validation
```
OutcomeSpec (YAML)
  ↓
LinkML Schema
  ↓
Pydantic Models
  ↓
Test Suite (EQP)
  ↓
✅ Pass → Keep schema
❌ Fail → Reject & refine
```

### Universal Provenance
**Every node gets**:
- `node_id` (str, required) - Stable identifier
- `node_created_at` (datetime, optional)
- `node_updated_at` (datetime, optional)
- `source_uri` (str, optional)
- `source_document_id` (str, optional)
- `source_page` (int, optional)
- `extraction_confidence` (float, 0.0-1.0, optional)
- `node_metadata` (dict, optional)
- + 5 more slots (see `schemas/core/provenance.yaml`)

**Every edge gets**:
- `rel_id` (str, required) - Stable relationship identifier
- `rel_created_at` (datetime, optional)
- `rel_updated_at` (datetime, optional)
- `source_uri` (str, optional)
- `confidence_score` (float, 0.0-1.0, optional)
- + 10 more slots (see `schemas/core/provenance.yaml`)

### Canonical Ontology URIs
All entities map to standard ontology classes:
- **DoCO** (Document Components): http://purl.org/spar/doco/
- **FaBiO** (Bibliographic): http://purl.org/spar/fabio/
- **PROV-O** (Provenance): http://www.w3.org/ns/prov#
- **FIBO** (Finance): https://spec.edmcouncil.org/fibo/ontology/
- **SKOS** (Knowledge Organization): http://www.w3.org/2004/02/skos/core#

Example:
```yaml
classes:
  Document:
    class_uri: fabio:SpecificationDocument  # Maps to FaBiO ontology
```

---

## 📊 Current Status

### Test Results
```
✅ 49/49 tests passing (100% pass rate)

tests/test_v1_v2_compatibility.py  18 passed
tests/test_aaoifi_standards.py     31 passed
```

### Implemented Overlays

**1. Business Outcomes Overlay**
- **Entities**: Deliverable, Milestone, Team, Outcome (4 total)
- **Edges**: Depends_on, Produces, Assigned_to, Contributes_to, Leads_to, Supports (6 total)
- **OutcomeSpec**: `specs/business_outcomes.yaml`
- **Schema**: `schemas/overlays/business_outcomes_overlay.yaml`
- **Models**: `generated/pydantic/overlays/business_outcomes_overlay.py`
- **Glue**: `generated/pydantic/overlays/business_outcomes_glue.py`

**2. AAOIFI Standards Overlay**
- **Entities**: Document, Section, Paragraph, Concept, ContractType, Rule, Agent (7 total)
- **Edges**: HasComponent, About, EvidenceOf, AttributedTo (4 total)
- **OutcomeSpec**: `specs/aaoifi_standards.yaml`
- **Schema**: `schemas/overlays/aaoifi_standards_overlay.yaml`
- **Models**: `generated/pydantic/overlays/aaoifi_standards_overlay.py`
- **Glue**: `generated/pydantic/overlays/aaoifi_standards_glue.py`

---

## 🔑 Key Files to Read

### For Quick Start
1. **This file** (`HANDOFF.md`) - Quick recovery instructions
2. `README.md` - Library overview + architecture diagrams
3. `MIGRATION_GUIDE.md` - Complete 8-step workflow for adding overlays

### For Deep Dive
4. `DECOMPOSITION_REPORT.md` - Final validation metrics + decomposition analysis
5. `schemas/core/provenance.yaml` - Universal provenance field definitions
6. `specs/aaoifi_standards.yaml` - Example OutcomeSpec with validation queries
7. `tests/test_aaoifi_standards.py` - Example Evidence Query Plan (EQP)

---

## 🚀 Common Tasks

### 1. Add New Overlay (Full Workflow)

**See**: `MIGRATION_GUIDE.md` (8-step workflow with examples)

**Quick Steps**:
1. Create OutcomeSpec: `specs/your_outcome.yaml`
2. Create overlay schema: `schemas/overlays/your_overlay.yaml`
3. Generate Pydantic models: `gen-pydantic schemas/overlays/your_overlay.yaml > generated/pydantic/overlays/your_overlay.py`
4. Create glue code: `generated/pydantic/overlays/your_glue.py` (type registries + edge validation)
5. Write tests: `tests/test_your_outcome.py` (Evidence Query Plan)
6. Run tests: `pytest tests/test_your_outcome.py -v`
7. Update documentation: README.md, MIGRATION_GUIDE.md
8. Commit changes

### 2. Run All Tests
```bash
cd "D:\projects\Pydantic Model Generator\v1_to_v2_migration"
pytest tests/ -v
```

### 3. Run Specific Test File
```bash
pytest tests/test_aaoifi_standards.py -v
```

### 4. Run Single Test
```bash
pytest tests/test_aaoifi_standards.py::TestOutcomeSpecValidation::test_rule_provenance -v
```

### 5. Regenerate Models After Schema Changes
```bash
gen-pydantic schemas/overlays/your_overlay.yaml > generated/pydantic/overlays/your_overlay.py
```

**Important**: Always run tests after regenerating models!

### 6. Check Field Name Mappings (V1 → V2)
**See**: `MIGRATION_GUIDE.md` Section 4 (Field Name Changes)

Quick reference:
- `outcome_type` → `name`
- `confidence_score` → `completion_confidence`
- `created_at` → `node_created_at`
- `updated_at` → `node_updated_at`
- `source` → `source_uri`
- `metadata` → `node_metadata`

---

## 🧬 Architecture Details

### Core Layer (Universal)
**File**: `schemas/core/provenance.yaml`

**ProvenanceFields** (13 slots):
```yaml
slots:
  node_id:                    # Required, stable identifier
  node_created_at:            # Optional datetime
  node_updated_at:            # Optional datetime
  source_uri:                 # Optional URI
  source_document_id:         # Optional document ID
  source_page:                # Optional page number
  extraction_confidence:      # Optional 0.0-1.0
  extraction_method:          # Optional method name
  extraction_timestamp:       # Optional datetime
  validated_at:               # Optional datetime
  validated_by:               # Optional agent ID
  validation_status:          # Optional status
  node_metadata:              # Optional dict
```

**EdgeProvenanceFields** (15 slots):
```yaml
slots:
  rel_id:                     # Required, stable relationship ID
  rel_created_at:             # Optional datetime
  rel_updated_at:             # Optional datetime
  source_uri:                 # Optional URI
  source_document_id:         # Optional document ID
  source_page:                # Optional page number
  confidence_score:           # Optional 0.0-1.0
  extraction_method:          # Optional method name
  extraction_timestamp:       # Optional datetime
  validated_at:               # Optional datetime
  validated_by:               # Optional agent ID
  validation_status:          # Optional status
  rel_metadata:               # Optional dict
  quote:                      # Optional supporting quote
  reasoning:                  # Optional reasoning
```

### Shared Layer (Cross-Outcome)
**File**: `schemas/shared/shared_types.yaml`

**Types**:
- `Deliverable` - Work products (code, documents, designs)
- `Milestone` - Project milestones with dates
- `Team` - Organizational units

### Overlays Layer (Outcome-Specific)
**Files**:
- `schemas/overlays/business_outcomes_overlay.yaml` (4 entities, 6 edges)
- `schemas/overlays/aaoifi_standards_overlay.yaml` (7 entities, 4 edges)

---

## 🔍 Example: Understanding OutcomeSpec → EQP Flow

### 1. OutcomeSpec (`specs/aaoifi_standards.yaml`)
```yaml
outcome_questions:
  - question: "Which paragraphs provide evidence for a specific rule?"
    target_entities: [Rule, Paragraph]
    expected_relations: [EvidenceOf]

validation_queries:
  - name: "test_rule_provenance"
    description: "Verify Rule provenance fields from supporting paragraphs"
    cypher: |
      MATCH (r:Rule)-[e:EvidenceOf]->(p:Paragraph)
      RETURN r.article_no, r.normative_effect,
             e.quote, e.page_from, e.page_to,
             p.section_id, p.ordinal
    expected_fields:
      Rule: [article_no, normative_effect, text, title]
      Paragraph: [section_id, ordinal, text, page_from, page_to]
      EvidenceOf: [quote, page_from, page_to]
```

### 2. LinkML Schema (`schemas/overlays/aaoifi_standards_overlay.yaml`)
```yaml
classes:
  Rule:
    class_uri: fibo:ContractualElement
    mixins:
      - ProvenanceFields  # Inherits 13 provenance slots
    slots:
      - title
      - text
      - article_no
      - normative_effect

  Paragraph:
    class_uri: doco:Paragraph
    mixins:
      - ProvenanceFields
    slots:
      - section_id
      - ordinal
      - text
      - page_from
      - page_to

edges:
  EvidenceOf:
    source: Rule
    target: Paragraph
    description: "Rule derived from paragraph"
    mixins:
      - EdgeProvenanceFields  # Inherits 15 edge provenance slots
    slots:
      - quote
      - page_from
      - page_to
```

### 3. Generated Pydantic Models (`generated/pydantic/overlays/aaoifi_standards_overlay.py`)
```python
class Rule(ConfiguredBaseModel):
    node_id: str = Field(..., description="Stable identifier")
    title: Optional[str] = Field(None)
    text: Optional[str] = Field(None)
    article_no: Optional[str] = Field(None)
    normative_effect: Optional[str] = Field(None)
    # ... + 12 more provenance fields

class EvidenceOf(ConfiguredBaseModel):
    rel_id: str = Field(..., description="Stable relationship identifier")
    quote: Optional[str] = Field(None)
    page_from: Optional[int] = Field(None)
    page_to: Optional[int] = Field(None)
    # ... + 14 more edge provenance fields
```

### 4. Evidence Query Plan (`tests/test_aaoifi_standards.py`)
```python
def test_rule_provenance(self):
    """Validation query: test_rule_provenance

    Expected fields: article_no, normative_effect, page_from, page_to
    Expected relations: EvidenceOf (Rule→Paragraph)
    """
    rule = Rule(
        title="Test Rule",
        article_no="Art. 1",
        normative_effect="requires",
        text="Test text",
        node_id="RULE"
    )
    para = Paragraph(
        section_id="SEC",
        ordinal=1,
        text="Source text",
        page_from=10,
        page_to=11,
        node_id="PARA"
    )
    evidence = EvidenceOf(
        quote="Source text",
        page_from=10,
        page_to=11,
        rel_id="RULE-PARA"
    )

    # Verify all required fields exist
    assert hasattr(rule, 'article_no')
    assert hasattr(rule, 'normative_effect')
    assert hasattr(para, 'page_from')
    assert hasattr(para, 'page_to')
    assert hasattr(evidence, 'quote')
```

**Result**: ✅ Test passes → Schema validates OutcomeSpec query

---

## 🛠️ Graphiti Integration

### Type Registries (`*_glue.py` files)

**Purpose**: Map Pydantic types to canonical ontology URIs and define allowed edge types.

**Example** (`business_outcomes_glue.py`):
```python
BUSINESS_NODE_URI: Dict[str, str] = {
    "Deliverable": "http://www.w3.org/ns/prov#Entity",
    "Milestone": "http://www.w3.org/ns/prov#Entity",
    "Team": "http://www.w3.org/ns/prov#Agent",
    "Outcome": "http://www.w3.org/ns/prov#Entity",
}

BUSINESS_EDGE_TYPE_MAP: Dict[tuple, List[str]] = {
    ("Deliverable", "Milestone"): ["Depends_on"],
    ("Deliverable", "Outcome"): ["Produces"],
    ("Team", "Deliverable"): ["Assigned_to"],
    ("Team", "Milestone"): ["Contributes_to"],
    ("Outcome", "Milestone"): ["Leads_to"],
    ("Deliverable", "Deliverable"): ["Supports"],
}

def validate_edge_type(source_type: str, target_type: str, edge_type: str) -> bool:
    """Validate that an edge type is allowed between two node types."""
    allowed_edges = BUSINESS_EDGE_TYPE_MAP.get((source_type, target_type), [])
    return edge_type in allowed_edges
```

**Usage**:
```python
from generated.pydantic.overlays.business_outcomes_glue import (
    BUSINESS_NODE_URI,
    BUSINESS_EDGE_TYPE_MAP,
    validate_edge_type
)

# Validate edge before ingestion
is_valid = validate_edge_type("Deliverable", "Milestone", "Depends_on")
assert is_valid == True

# Get canonical URI for node
uri = BUSINESS_NODE_URI["Deliverable"]
assert uri == "http://www.w3.org/ns/prov#Entity"
```

---

## 📝 Important Notes

### Field Name Changes (V1 → V2)
| V1 Field | V2 Field | Reason |
|----------|----------|--------|
| `outcome_type` | `name` | Clarity |
| `confidence_score` | `completion_confidence` | Precision |
| `created_at` | `node_created_at` | Namespace collision avoidance |
| `updated_at` | `node_updated_at` | Namespace collision avoidance |
| `source` | `source_uri` | Type clarity (URI string) |
| `metadata` | `node_metadata` | Namespace collision avoidance |

**Why namespace prefixes?** Prevents collisions with domain-specific fields (e.g., `created_at` for document creation vs node creation).

### Test Suite Structure

**V1/V2 Compatibility** (`test_v1_v2_compatibility.py`): 18 tests
- TestV1ModelValidation (4 tests) - V1 monolithic models work
- TestV2ModelValidation (5 tests) - V2 modular models work
- TestV1V2Compatibility (5 tests) - Data adapts between versions
- TestV2Enhancements (4 tests) - V2 provenance features

**OutcomeSpec Validation** (`test_aaoifi_standards.py`): 31 tests
- TestOutcomeSpecValidation (7 tests) - Models support validation queries
- TestNodeCreation (7 tests) - All entities instantiate correctly
- TestEdgeCreation (4 tests) - All edges instantiate correctly
- TestProvenanceFields (7 tests) - Provenance slots work
- TestEdgeProvenanceFields (4 tests) - Edge provenance slots work
- TestGraphitiIntegration (2 tests) - Type registries + validation

### Canonical Ontology URI Mapping

**DoCO** (Document Components Ontology):
- `http://purl.org/spar/doco/Section`
- `http://purl.org/spar/doco/Paragraph`

**FaBiO** (FRBR-aligned Bibliographic Ontology):
- `http://purl.org/spar/fabio/SpecificationDocument`

**PROV-O** (Provenance Ontology):
- `http://www.w3.org/ns/prov#Entity`
- `http://www.w3.org/ns/prov#Agent`
- `http://www.w3.org/ns/prov#Activity`

**FIBO** (Financial Industry Business Ontology):
- `https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/Contract`
- `https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/ContractualElement`

**SKOS** (Simple Knowledge Organization System):
- `http://www.w3.org/2004/02/skos/core#Concept`

---

## 🔮 Future Work

### AI Agent Pipeline (Not Yet Implemented)
**Location**: `../agents/` (future directory)

**Goal**: AI agent-assisted pipeline that:
1. Takes high-level business outcome document
2. Uses AI to deconstruct into OutcomeSpec
3. Generates LinkML overlay schema (if needed)
4. Produces new Pydantic module

**Status**: Planned, not implemented

---

## 🎯 Recovery After Context Compaction

**If you're reading this after token limit compaction**:

### 1. Verify Test Status (30 seconds)
```bash
cd "D:\projects\Pydantic Model Generator\v1_to_v2_migration"
pytest tests/ -v
```

**Expected**: 49/49 passing

### 2. Read Essential Docs (5 minutes)
1. This file (`HANDOFF.md`) - Quick recovery
2. `README.md` - Architecture overview
3. `MIGRATION_GUIDE.md` - Complete workflow

### 3. Understand Current State (10 minutes)
- 2 overlays implemented (Business Outcomes, AAOIFI Standards)
- 3-layer architecture (Core → Shared → Overlays)
- Universal provenance (13 node slots + 15 edge slots)
- Canonical ontology URIs (DoCO, FaBiO, PROV-O, FIBO, SKOS)
- Closed-loop validation (OutcomeSpec → Schema → EQP)

### 4. Ready to Work
- Add new overlay: See `MIGRATION_GUIDE.md` (8-step workflow)
- Modify existing overlay: Regenerate models + run tests
- Understand OutcomeSpec flow: See example in this file (Section 8)

---

## 🤝 Developer Handoff Checklist

**Before making changes**:
- [ ] Read this file (`HANDOFF.md`)
- [ ] Run tests to verify 49/49 passing
- [ ] Read `MIGRATION_GUIDE.md` for workflow

**When adding new overlay**:
- [ ] Create OutcomeSpec first (`specs/`)
- [ ] Define max 5-8 entities (minimalism)
- [ ] Map to canonical ontology URIs (`class_uri`)
- [ ] Include ProvenanceFields/EdgeProvenanceFields mixins
- [ ] Generate Pydantic models (`gen-pydantic`)
- [ ] Create glue code (type registries + validation)
- [ ] Write Evidence Query Plan tests
- [ ] Run tests (must pass all 49 + new tests)
- [ ] Update documentation

**Before committing**:
- [ ] All tests passing (49/49 + any new tests)
- [ ] Documentation updated (README.md, MIGRATION_GUIDE.md)
- [ ] Glue code created with type registries
- [ ] OutcomeSpec validation queries tested

---

**End of Handoff Document**

**For full project context**, see: `../PROJECT_CONTEXT.md`
