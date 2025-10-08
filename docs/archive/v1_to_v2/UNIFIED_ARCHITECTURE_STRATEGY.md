# Unified Pydantic Model Architecture Strategy

## Executive Summary

This document consolidates four strategic decisions:
1. **Organization Strategy**: **Outcome-driven** schema generation via agents (not static domain hierarchies)
2. **Episode-Based Provenance**: Track information source via Episode model
3. **Ontology Mapping**: Dynamic retrieval of ontology snippets for semantic alignment
4. **Plugin Architecture**: Runtime plugin system for generated schemas

**Critical Insight**: Don't organize statically by "domain" or "information type." Use the **agent-driven pipeline** to generate minimal, outcome-specific schemas on-demand. Each OutcomeSpec creates its own focused schema with only the entities/edges needed to answer specific questions.

**Key Principle**: Define **outcomes** (questions to answer), retrieve **ontologies** (semantic context), generate **schemas** (minimal LinkML), produce **Pydantic models** (with provenance + ontology URIs).

---

## 1. The Outcome-Driven Architecture

**OLD THINKING** ❌: Organize by static domains (business/, aaoifi/)
**NEW THINKING** ✅: Generate schemas dynamically per outcome

```
┌──────────────────────────────────────────────────────────┐
│                     OUTCOME-DRIVEN                       │
│              (Agent Pipeline Generates)                  │
│                                                          │
│  OutcomeSpec                                             │
│  ┌─────────────────────────────────────────┐           │
│  │ Questions: What standards cite FAS 28?  │           │
│  │ Ontologies: doco, fibo, aaoifi          │           │
│  │ Entities: AAOIFIStandard, Fatwa         │           │
│  │ Relations: Cites, Supersedes            │           │
│  └─────────────────────────────────────────┘           │
│                      ↓                                   │
│        ┌─────────────────────────────┐                  │
│        │  OntologyRetriever Agent    │                  │
│        │  (Exa + Firecrawl)          │                  │
│        │  - Fetches doco classes     │                  │
│        │  - Fetches fibo properties  │                  │
│        │  - Fetches aaoifi terms     │                  │
│        └─────────────────────────────┘                  │
│                      ↓                                   │
│        ┌─────────────────────────────┐                  │
│        │  SchemaSynthesizer (LLM)    │                  │
│        │  + Instructor Validation    │                  │
│        │  - Max 12 classes           │                  │
│        │  - Max 10 edges             │                  │
│        │  - Ontology URIs included   │                  │
│        └─────────────────────────────┘                  │
│                      ↓                                   │
│  Generated Schema: aaoifi_standards_overlay.yaml        │
│  Generated Pydantic: aaoifi_models.py                   │
│  Evidence Query Plan: eqp.json                          │
└──────────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────┐
│                   EPISODE PROVENANCE                     │
│               (Universal Tracking Layer)                 │
│                                                          │
│  Episode Model (core/episodes.yaml)                     │
│  - source_type: conversation | document                 │
│  - source_system: slack | email | upload | aaoifi_db   │
│  - Tracks WHERE data came from                          │
│                                                          │
│  ALL entities link to episodes via episode_ids          │
└──────────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────┐
│                 ONTOLOGY ALIGNMENT                       │
│              (Semantic Interoperability)                 │
│                                                          │
│  class_uri: fabio:Standard, schema:Action               │
│  slot_uri: cito:cites, prov:wasDerivedFrom             │
│  - Retrieved dynamically per outcome                    │
│  - LLM sees actual ontology definitions                 │
│  - Correct semantic URIs in generated models            │
└──────────────────────────────────────────────────────────┘
```

**Key Insight**: Don't create `domains/business/` and `domains/aaoifi/` upfront. Instead, create **OutcomeSpecs** that generate focused schemas:

- `specs/aaoifi_standards_extraction.yaml` → generates AAOIFIStandard, Fatwa, Cites edge
- `specs/business_outcomes_tracking.yaml` → generates BusinessOutcome, BusinessTask, Requires edge
- `specs/contract_compliance_check.yaml` → generates Contract, Requirement, ComplianceCheck edge

Each spec is minimal (max 12 classes, max 10 edges) and question-driven.

---

## 2. Directory Structure (Outcome-Driven)

```
project_root/
├── specs/                             # OutcomeSpecs (input to agent pipeline)
│   ├── aaoifi_standards_extraction.yaml
│   ├── business_outcomes_tracking.yaml
│   ├── contract_compliance_check.yaml
│   ├── slack_decision_tracking.yaml
│   └── murabaha_audit.yaml
│
├── schemas/                           # LinkML schemas (generated + core)
│   ├── core/                          # Universal infrastructure (hand-written)
│   │   ├── base.yaml                  # Base classes, ConfigDict
│   │   ├── provenance.yaml            # ProvenanceFields (prov:Entity)
│   │   ├── episodes.yaml              # Episode model (source tracking)
│   │   └── types.yaml                 # Custom types (Email, Confidence01)
│   │
│   ├── shared/                        # Cross-outcome reusable (hand-written)
│   │   ├── temporal.yaml              # DateRange, Period
│   │   ├── identity.yaml              # Person, Organization (schema:Person)
│   │   ├── geography.yaml             # Address, Location
│   │   └── financial.yaml             # Money, Currency (fibo:MonetaryAmount)
│   │
│   └── overlays/                      # GENERATED by agent pipeline
│       ├── aaoifi_standards_overlay.yaml   # From aaoifi_standards_extraction spec
│       ├── business_outcomes_overlay.yaml  # From business_outcomes_tracking spec
│       ├── contract_compliance_overlay.yaml
│       └── slack_decisions_overlay.yaml
│
├── generated/                         # GENERATED Pydantic models
│   └── pydantic/
│       ├── core/                      # Hand-written, not generated
│       │   ├── base.py
│       │   ├── provenance.py
│       │   ├── episodes.py
│       │   └── types.py
│       │
│       ├── shared/                    # Hand-written, not generated
│       │   ├── temporal.py
│       │   ├── identity.py
│       │   └── financial.py
│       │
│       └── overlays/                  # GENERATED from overlays/
│           ├── aaoifi_standards_models.py       # From aaoifi_standards_overlay.yaml
│           ├── aaoifi_standards_glue.py         # AAOIFI_ENTITIES, AAOIFI_EDGES
│           ├── business_outcomes_models.py      # From business_outcomes_overlay.yaml
│           ├── business_outcomes_glue.py        # BUSINESS_ENTITIES, BUSINESS_EDGES
│           └── ...
│
├── graphmodels/                       # Runtime plugin system
│   ├── core/
│   │   ├── __init__.py
│   │   ├── registries.py              # Global _ENTITY_REGISTRY, _EDGE_REGISTRY
│   │   ├── plugin_loader.py           # Auto-discover overlay plugins
│   │   ├── ids.py                     # ID generation
│   │   └── episodes.py                # Episode runtime utilities
│   │
│   └── overlays/                      # Plugin per outcome (auto-discovered)
│       ├── aaoifi_standards/
│       │   └── __init__.py            # Exports ENTITIES, EDGES
│       ├── business_outcomes/
│       │   └── __init__.py
│       └── contract_compliance/
│           └── __init__.py
│
├── artifacts/                         # Agent pipeline outputs
│   ├── ontology_refs/
│   │   ├── aaoifi_standards_ontology_refs.json
│   │   └── business_outcomes_ontology_refs.json
│   └── eqp/
│       ├── aaoifi_standards_eqp.json  # Evidence Query Plans
│       └── business_outcomes_eqp.json
│
├── v1_to_v2_migration/
│   ├── templates/                     # Custom LinkML→Pydantic templates
│   └── tests/
│       └── test_v1_v2_compatibility.py
│
└── agents/                            # Agent-driven schema generation
    ├── ontology_retriever.py          # Fetch ontology docs dynamically
    ├── schema_synthesizer.py          # LLM + Instructor → LinkML
    ├── codegen_orchestrator.py        # LinkML → Pydantic pipeline
    └── run_pipeline.py                # Main orchestration script
```

**Key Changes from Static to Outcome-Driven**:

1. **`specs/`** (NEW): OutcomeSpecs define what questions to answer
2. **`schemas/overlays/`** (GENERATED): One overlay per outcome, not per domain
3. **`generated/pydantic/overlays/`** (GENERATED): Pydantic models per outcome
4. **`graphmodels/overlays/`**: Runtime plugins per outcome (not domains)
5. **`artifacts/`** (NEW): Agent pipeline outputs (ontology refs, EQPs)

---

## 3. How The Three Dimensions Work Together

### Example 1: Business Outcome from Slack Conversation

**Dimension 1 (Domain)**: Business domain
**Dimension 2 (Source)**: Conversation from Slack
**Dimension 3 (Ontology)**: Schema.org Action + PROV-O Entity

```python
# Step 1: Create Episode (Dimension 2)
slack_episode = Episode(
    episode_id="episode_slack_20250106_001",
    source_type=SourceType.conversation,      # Dimension 2
    source_system=SourceSystem.slack,         # Dimension 2
    content="@john we need to launch payment feature by Q2. High priority.",
    channel_id="C123ABC",
    participants=["john@example.com", "alice@example.com"],
    timestamp=datetime(2025, 1, 6, 14, 30)
)

# Step 2: Extract BusinessOutcome (Dimension 1)
outcome = BusinessOutcome(                    # Domain: business
    node_id="outcome_payment_feature",
    outcome_type="deliverable",
    status=OutcomeStatus.proposed,
    priority=Priority.high,
    due_date=datetime(2025, 6, 30),
    episode_ids=["episode_slack_20250106_001"],  # Link to Episode
    prov_system="slack"
)

# Dimension 3 (Ontology URIs - in metadata)
# model_config['json_schema_extra']['class_uri'] == 'schema:Action'
# model_config['json_schema_extra']['mixins'] == ['prov:Entity']
```

**Queries You Can Do**:
```python
# By domain: "All business outcomes"
outcomes = get_entities(entity_type="BusinessOutcome")

# By source type: "Outcomes from conversations"
outcomes = get_entities_from_episodes(source_type="conversation")

# By source system: "Outcomes from Slack"
outcomes = get_entities_from_episodes(source_system="slack")

# By ontology: "All Schema.org Actions"
actions = sparql_query("SELECT ?x WHERE { ?x rdf:type schema:Action }")
```

### Example 2: AAOIFI Standard from PDF Document

**Dimension 1 (Domain)**: AAOIFI domain
**Dimension 2 (Source)**: Document (PDF upload)
**Dimension 3 (Ontology)**: FaBiO Standard + DoCO Document + PROV-O Entity

```python
# Step 1: Create Episode (Dimension 2)
pdf_episode = Episode(
    episode_id="episode_aaoifi_fas_28",
    source_type=SourceType.document,          # Dimension 2
    source_system=SourceSystem.aaoifi_db,     # Dimension 2
    content="FAS 28: Murabaha and Other Deferred Payment Sales\n\n[full text]",
    document_title="FAS 28 - Murabaha.pdf",
    document_url="https://aaoifi.com/standards/fas-28",
    timestamp=datetime(2018, 11, 1)
)

# Step 2: Extract AAOIFIStandard (Dimension 1)
standard = AAOIFIStandard(                    # Domain: aaoifi
    node_id="aaoifi_fas_28",
    standard_code="FAS 28",
    standard_title="Murabaha and Other Deferred Payment Sales",
    standard_type=StandardType.accounting,
    status=StandardStatus.active,
    issued_date=datetime(2018, 11, 1),
    episode_ids=["episode_aaoifi_fas_28"],
    prov_system="aaoifi_db"
)

# Dimension 3 (Ontology URIs)
# class_uri: fabio:Standard
# slot_uri (standard_code): aaoifi:standardCode
# slot_uri (issued_date): schema:datePublished
```

**Queries You Can Do**:
```python
# By domain: "All AAOIFI standards"
standards = get_entities(entity_type="AAOIFIStandard")

# By source type: "Standards from documents"
standards = get_entities_from_episodes(source_type="document")

# By ontology: "All FaBiO Standards"
standards = sparql_query("SELECT ?x WHERE { ?x rdf:type fabio:Standard }")

# By document structure: "All documents with sections"
docs = sparql_query("SELECT ?x WHERE { ?x doco:hasPart ?section }")
```

---

## 4. Core Episode Model (NEW)

### schemas/core/episodes.yaml

```yaml
id: https://example.com/schemas/core/episodes
name: episodes
description: Source episodes from which entities are extracted

imports:
  - provenance
  - types

prefixes:
  prov: http://www.w3.org/ns/prov#
  schema: http://schema.org/

enums:
  SourceType:
    permissible_values:
      conversation:
        description: Extracted from conversations (Slack, email, chat)
        meaning: prov:Communication
      document:
        description: Extracted from documents (PDFs, standards, files)
        meaning: schema:DigitalDocument

  SourceSystem:
    permissible_values:
      slack:
        description: Slack workspace
        meaning: schema:SoftwareApplication
      email:
        description: Email system
        meaning: schema:EmailMessage
      upload:
        description: User-uploaded documents
        meaning: schema:DigitalDocument
      aaoifi_db:
        description: AAOIFI standard database
        meaning: schema:Dataset

classes:
  Episode:
    class_uri: prov:Entity  # Episode is a provenance entity
    description: A source episode from which knowledge is extracted
    attributes:
      episode_id:
        identifier: true
        range: string
        slot_uri: prov:identifier

      source_type:
        range: SourceType
        required: true
        slot_uri: prov:type
        description: Whether this is a conversation or document

      source_system:
        range: SourceSystem
        required: true
        slot_uri: prov:wasAttributedTo
        description: System from which episode originated

      content:
        range: string
        slot_uri: schema:text
        description: Raw content of the episode

      metadata:
        range: string
        slot_uri: schema:additionalProperty
        description: JSON metadata (channel_id, file_name, etc.)

      timestamp:
        range: datetime
        required: true
        slot_uri: prov:generatedAtTime
        description: When episode occurred/was created

      # Document-specific fields (optional)
      document_title:
        range: string
        slot_uri: schema:name

      document_url:
        range: string
        slot_uri: schema:url

      # Conversation-specific fields (optional)
      channel_id:
        range: string
        slot_uri: schema:identifier
        description: Slack/Teams channel ID

      participants:
        range: string
        multivalued: true
        slot_uri: schema:participant
        description: Conversation participants
```

---

## 5. Domain Models Stay Clean

### ✅ GOOD: Domain models focus on business logic

```yaml
# schemas/domains/business/entities.yaml
classes:
  BusinessOutcome:
    class_uri: schema:Action              # Ontology (Dimension 3)
    mixins:
      - ProvenanceFields                  # Includes episode_ids (Dimension 2)
    slots:
      - outcome_type
      - status                            # Business domain logic
      - priority
      - due_date
      - confidence
```

**Key Points**:
- ✅ No `channel_id` or `document_url` fields (those are on Episode)
- ✅ No `source_type` field (tracked via Episode)
- ✅ Business logic only: status, priority, due_date
- ✅ Links to source via `episode_ids` (from ProvenanceFields mixin)

### ❌ BAD: Mixing source metadata with domain logic

```yaml
# ❌ DON'T DO THIS
classes:
  BusinessOutcome:
    slots:
      - outcome_type
      - status
      - slack_channel_id          # ❌ Source-specific field
      - document_page_number      # ❌ Source-specific field
      - source_type               # ❌ Provenance, not business logic
```

---

## 6. Ontology Mapping Strategy

### By Domain (Dimension 1)

| Domain | Primary Ontology | Example Classes | Example Slots |
|--------|------------------|-----------------|---------------|
| **Business** | Schema.org | `schema:Action`, `schema:Person`, `schema:Organization` | `schema:priority`, `schema:endDate` |
| **AAOIFI** | FIBO + custom AAOIFI | `fabio:Standard`, `aaoifi:Fatwa`, `aaoifi:MurabahaContract` | `aaoifi:standardCode`, `fibo:hasCostPrice` |
| **Core** | PROV-O | `prov:Entity`, `prov:Activity` | `prov:wasDerivedFrom`, `prov:generatedAtTime` |

### By Information Type (Dimension 2)

| Information Type | Primary Ontology | Applied To | Example URIs |
|------------------|------------------|-----------|--------------|
| **Documents** | DoCO, FaBiO, CiTO | Episode model, document-specific entities | `doco:Section`, `fabio:Standard`, `cito:cites` |
| **Conversations** | Schema.org, PROV-O | Episode model | `schema:Message`, `prov:Communication` |
| **Provenance** | PROV-O | All entities via ProvenanceFields | `prov:Entity`, `prov:wasDerivedFrom` |

### Combination Matrix

| Entity | Domain | Source Type | Ontology URIs |
|--------|--------|-------------|---------------|
| `BusinessOutcome` | Business | Any | `schema:Action` + `prov:Entity` |
| `AAOIFIStandard` | AAOIFI | Document | `fabio:Standard` + `doco:Document` + `prov:Entity` |
| `Fatwa` | AAOIFI | Document | `aaoifi:Fatwa` + `doco:Document` + `prov:Entity` |
| `MurabahaContract` | AAOIFI | Structured data | `fibo:Contract` + `aaoifi:MurabahaContract` + `prov:Entity` |
| `BusinessTask` | Business | Any | `schema:Action` + `prov:Activity` |
| `Episode` (conversation) | Core | N/A | `prov:Entity` + `prov:Communication` |
| `Episode` (document) | Core | N/A | `prov:Entity` + `schema:DigitalDocument` |

---

## 7. Query Patterns (All Three Dimensions)

### Query by Domain (Dimension 1)

```python
# Get all business outcomes
outcomes = get_entities(entity_type="BusinessOutcome")

# Get all AAOIFI standards
standards = get_entities(entity_type="AAOIFIStandard")
```

### Query by Source Type (Dimension 2)

```cypher
# Cypher: Find outcomes extracted from conversations
MATCH (o:BusinessOutcome)-[:FROM_EPISODE]->(e:Episode)
WHERE e.source_type = "conversation"
RETURN o.node_id, o.status, e.source_system, e.channel_id
```

```python
# Python: Find standards from documents
episodes = get_episodes(source_type=SourceType.document)
episode_ids = [e.episode_id for e in episodes]
standards = get_entities_by_episodes(episode_ids)
```

### Query by Ontology (Dimension 3)

```sparql
# SPARQL: Find all Schema.org Actions (outcomes + tasks)
PREFIX schema: <http://schema.org/>

SELECT ?entity ?type
WHERE {
  ?entity rdf:type schema:Action .
  ?entity rdf:type ?type .
}
```

```sparql
# SPARQL: Find documents with citations
PREFIX cito: <http://purl.org/spar/cito/>
PREFIX fabio: <http://purl.org/spar/fabio/>

SELECT ?doc ?cited
WHERE {
  ?doc rdf:type fabio:Standard .
  ?doc cito:cites ?cited .
}
```

### Cross-Dimensional Queries

```cypher
# Cypher: Find AAOIFI standards (domain) from PDFs (source) with citations (ontology)
MATCH (s:AAOIFIStandard)-[:FROM_EPISODE]->(e:Episode)
WHERE e.source_type = "document"
  AND e.source_system = "aaoifi_db"
MATCH (s)-[:CITES]->(cited)
RETURN s.standard_code, e.document_title, COUNT(cited) as citation_count
ORDER BY citation_count DESC
```

```python
# Python: Find business outcomes (domain) from Slack (source)
# that are Schema.org Actions (ontology)
outcomes = await graphiti.search(
    query="high priority outcomes",
    entity_types=["schema:Action"],
    filters={
        "source_system": "slack",
        "source_type": "conversation"
    }
)
```

---

## 8. Plugin Registration (Unified)

### Domain Plugin Structure

```python
# graphmodels/domains/business/__init__.py
"""
Business Domain Plugin

Exports:
- Entity models (Dimension 1): BusinessOutcome, BusinessTask, etc.
- Edge models (Dimension 1): Requires, Fulfills, etc.
- Ontology URIs (Dimension 3): class_uri, slot_uri in metadata
- Episode linking (Dimension 2): via ProvenanceFields.episode_ids
"""

from generated.pydantic.domains.business.models import (
    BusinessOutcome,
    BusinessTask,
    BusinessDecision,
    Requires,
    Fulfills,
)
from generated.pydantic.domains.business.glue import (
    BUSINESS_ENTITIES,
    BUSINESS_EDGES,
)

# Export for plugin loader
ENTITIES = BUSINESS_ENTITIES
EDGES = BUSINESS_EDGES

__all__ = [
    "BusinessOutcome",
    "BusinessTask",
    "BusinessDecision",
    "Requires",
    "Fulfills",
    "ENTITIES",
    "EDGES",
]
```

### Global Registry (All Dimensions)

```python
# graphmodels/core/registries.py
from typing import Dict, Type
from pydantic import BaseModel

# Dimension 1: Domain entities and edges
_ENTITY_REGISTRY: Dict[str, Type[BaseModel]] = {}  # "BusinessOutcome" → class
_EDGE_REGISTRY: Dict[str, Type[BaseModel]] = {}    # "REQUIRES" → class

# Dimension 3: Ontology URI → entity type mapping
_ONTOLOGY_URI_TO_ENTITY: Dict[str, str] = {}  # "schema:Action" → ["BusinessOutcome", "BusinessTask"]

def register_domain(domain_name: str, entities: dict, edges: dict):
    """Register domain models (Dimension 1)."""
    for entity_type, model_cls in entities.items():
        if entity_type in _ENTITY_REGISTRY:
            raise ValueError(f"Duplicate entity type: {entity_type}")
        _ENTITY_REGISTRY[entity_type] = model_cls

        # Register ontology URI mapping (Dimension 3)
        class_uri = model_cls.model_config.get('json_schema_extra', {}).get('class_uri')
        if class_uri:
            if class_uri not in _ONTOLOGY_URI_TO_ENTITY:
                _ONTOLOGY_URI_TO_ENTITY[class_uri] = []
            _ONTOLOGY_URI_TO_ENTITY[class_uri].append(entity_type)

    for relation_type, model_cls in edges.items():
        if relation_type in _EDGE_REGISTRY:
            raise ValueError(f"Duplicate relation type: {relation_type}")
        _EDGE_REGISTRY[relation_type] = model_cls

def get_entities_by_ontology_uri(uri: str) -> List[str]:
    """Get entity types by ontology URI (Dimension 3)."""
    return _ONTOLOGY_URI_TO_ENTITY.get(uri, [])
```

---

## 9. Implementation Phases

### Phase 1: Create Episode Model (1-2 hours)
- [ ] Create `schemas/core/episodes.yaml` with SourceType, SourceSystem enums
- [ ] Add Episode class with ontology URIs (`prov:Entity`)
- [ ] Generate Pydantic: `gen-pydantic schemas/core/episodes.yaml`
- [ ] Add Episode to `graphmodels/core/__init__.py`

### Phase 2: Update Domain Models (NO changes needed!)
- [ ] Verify `BusinessOutcome` uses `ProvenanceFields` mixin (✅ already does)
- [ ] Verify `AAOIFIStandard` uses `ProvenanceFields` mixin
- [ ] No new fields on domain entities (episode_ids already exists)

### Phase 3: Add Ontology URIs (2-4 hours)
- [ ] Add `class_uri` to all core classes (ProvenanceFields, Actor)
- [ ] Add `class_uri` to business domain (BusinessOutcome → schema:Action)
- [ ] Add `class_uri` to AAOIFI domain (AAOIFIStandard → fabio:Standard)
- [ ] Add `slot_uri` to key fields (email → schema:email, etc.)

### Phase 4: Update Ingestion Pipeline (2-3 hours)
- [ ] Slack bot: Create Episode with `source_type=conversation`, `source_system=slack`
- [ ] Document processor: Create Episode with `source_type=document`, `source_system=upload`
- [ ] AAOIFI importer: Create Episode with `source_type=document`, `source_system=aaoifi_db`
- [ ] Entity extraction: Always populate `episode_ids` with source episode

### Phase 5: Update Global Registry (1 hour)
- [ ] Add ontology URI → entity type mapping in `registries.py`
- [ ] Add `get_entities_by_ontology_uri()` helper
- [ ] Update plugin loader to register ontology mappings

### Phase 6: Add Tests (2-3 hours)
- [ ] Test Episode creation (conversation vs document)
- [ ] Test entity → episode linking
- [ ] Test ontology URI lookups
- [ ] Test cross-dimensional queries

**Total Effort**: ~8-15 hours

---

## 10. Benefits of Unified Architecture

### Dimension 1 (Domain): Clean Business Logic
✅ One `BusinessOutcome` class, not N variants per source type
✅ One `AAOIFIStandard` class, not N variants per source type
✅ Domain count stays manageable (business, aaoifi, etc.)
✅ Clear separation of concerns

### Dimension 2 (Source): Flexible Provenance
✅ Query by source type: "Outcomes from conversations"
✅ Query by source system: "Outcomes from Slack"
✅ Query by source metadata: "Outcomes from channel C123"
✅ Same entity can have multiple sources (multiple episode_ids)

### Dimension 3 (Ontology): Semantic Interoperability
✅ Standards compliance (FIBO, Schema.org, DoCO)
✅ SPARQL queries across heterogeneous data
✅ RDF export with full semantic context
✅ Ontology-based reasoning

### All Three Together: Maximum Flexibility
✅ Query any combination: "AAOIFI standards (D1) from documents (D2) that cite other standards (D3)"
✅ No model sprawl: Organize by domain, track source via Episode, enrich with ontology URIs
✅ Easy to extend: Add new domain → auto-discovered; add new source system → new enum value

---

## 11. Decision Framework

### When to organize by DOMAIN (Dimension 1)?
✅ **Always** - Primary organization principle
- Different domains have different business logic
- Different domains have different relationships (REQUIRES vs CITES)
- Different domains have different query patterns
- Different domains have different validation rules

### When to organize by SOURCE TYPE (Dimension 2)?
❌ **Never** - Use Episode model instead
- Source type is provenance metadata, not structure
- Same domain entity can come from any source
- Episode model tracks source-specific fields (channel_id, document_url)

### When to use ONTOLOGY URIs (Dimension 3)?
✅ **Always** - For semantic alignment
- Standards compliance (FIBO, AAOIFI, Schema.org)
- Interoperability with external systems
- RDF export and SPARQL queries
- Semantic reasoning

---

## 12. Answer: Domain vs Information Type vs Ontology?

### The Question

> "Should we stick to domain based or information based or maybe even 'ontology' based?"

### The Answer: **OUTCOME-BASED** (None of the Above!)

**Don't organize by**:
- ❌ **Domain** (business/, aaoifi/) - Too static, requires upfront taxonomy
- ❌ **Information Type** (conversations/, documents/) - Wrong abstraction (provenance, not structure)
- ❌ **Ontology** (schema_org/, fibo/) - Ontologies are semantic context, not organizational principle

**Instead, organize by OUTCOME**:
✅ **OutcomeSpec** → Agent Pipeline → Minimal Schema → Pydantic Models

### Why Outcome-Driven Wins

| Approach | Problem | Solution |
|----------|---------|----------|
| **Domain-Based** | Requires knowing all domains upfront; creates rigid taxonomy; domains overlap (AAOIFI is both "finance" and "compliance") | OutcomeSpec specifies exactly what's needed; no taxonomy required |
| **Information Type-Based** | Same entity (AAOIFIStandard) appears in both conversations/ and documents/; causes duplication | Episode model tracks source; entities stay clean |
| **Ontology-Based** | Ontologies describe semantics, not use cases; one entity may map to multiple ontologies (AAOIFIStandard → fabio:Standard + doco:Document + prov:Entity) | Ontologies retrieved dynamically per outcome; multiple URIs per entity |

### The Outcome-Driven Architecture

```yaml
# Input: OutcomeSpec (specs/aaoifi_standards_extraction.yaml)
outcome_name: AAOIFI Standards Knowledge Graph
questions:
  - What standards cite FAS 28?
  - What requirements does FAS 28 define?

ontologies:
  - prefix: doco      # Documents
  - prefix: fibo      # Finance
  - prefix: aaoifi    # Domain-specific

target_entities:
  - AAOIFIStandard
  - Requirement

relations:
  - Cites (AAOIFIStandard → AAOIFIStandard)
  - Defines (AAOIFIStandard → Requirement)
```

↓ **Agent Pipeline** ↓

```yaml
# Output: Generated LinkML Schema (schemas/overlays/aaoifi_standards_overlay.yaml)
classes:
  AAOIFIStandard:
    class_uri: fabio:Standard  # ← Ontology (retrieved dynamically)
    mixins:
      - ProvenanceFields        # ← Includes episode_ids (source tracking)
    slots:
      - standard_code
      - cites  # slot_uri: cito:cites (from ontology retrieval)

  Requirement:
    class_uri: aaoifi:Requirement
    mixins:
      - ProvenanceFields
    slots:
      - requirement_text
```

### The Three Layers (Outcome-Driven)

1. **Core Infrastructure** (Universal, Hand-Written)
   - `core/provenance.yaml` - ProvenanceFields with episode_ids
   - `core/episodes.yaml` - Episode model (tracks source type/system)
   - `core/types.yaml` - Reusable types (Email, Confidence01)

2. **Outcome Specs** (Business Requirements, Hand-Written)
   - `specs/aaoifi_standards_extraction.yaml`
   - `specs/business_outcomes_tracking.yaml`
   - `specs/murabaha_audit.yaml`

3. **Generated Overlays** (Agent-Generated, Minimal)
   - `schemas/overlays/aaoifi_standards_overlay.yaml` (max 12 classes, 10 edges)
   - `generated/pydantic/overlays/aaoifi_standards_models.py`
   - `graphmodels/overlays/aaoifi_standards/__init__.py` (plugin)

### Benefits Over Static Organization

| Static Approach | Outcome-Driven Approach |
|-----------------|-------------------------|
| Create `domains/business/` with 50+ entities | Create `specs/slack_decisions.yaml` with 8 entities (only what's needed) |
| Guess which entities belong in "business" vs "compliance" | Let questions drive entity selection |
| Manually write LinkML schemas with ontology URIs | Agent retrieves ontologies dynamically based on spec |
| All entities loaded at startup (heavy) | Plugin loader discovers only active outcomes (lazy) |
| Hard to change taxonomy (requires refactoring) | Easy to add new outcomes (just write new spec) |

### Summary

**Organize by OUTCOME, not domain/information-type/ontology**:

- **Outcome**: The questions you need to answer (business requirement)
- **Episode**: Where data came from (provenance, tracked universally)
- **Ontology**: What it means semantically (retrieved dynamically per outcome)

**Result**: Minimal, question-driven schemas with automatic ontology alignment and universal source tracking.

**Your agent pipeline already implements this!** The architecture docs were written assuming static organization, but your actual implementation is outcome-driven. Update your process to embrace this.

---

## 11. The Closed-Loop Validation Architecture (CRITICAL)

### Why Outcome-Driven Enables Testing

**The Key Insight**: Because schemas are generated FROM outcomes (questions), you can validate that the schema is SUFFICIENT by testing if those questions can be answered.

```
┌─────────────────────────────────────────────────────────┐
│                    CLOSED LOOP                          │
│                                                         │
│  OutcomeSpec (Input)                                    │
│  ┌───────────────────────────────┐                     │
│  │ Questions:                    │                     │
│  │ - What standards cite FAS 28? │                     │
│  │ - What requirements defined?  │                     │
│  └───────────────────────────────┘                     │
│                ↓                                        │
│         Agent Pipeline                                  │
│      (Generate Schema)                                  │
│                ↓                                        │
│  Generated Schema                                       │
│  ┌───────────────────────────────┐                     │
│  │ Classes:                      │                     │
│  │ - AAOIFIStandard              │                     │
│  │ - Requirement                 │                     │
│  │ Edges:                        │                     │
│  │ - Cites                       │                     │
│  │ - Defines                     │                     │
│  └───────────────────────────────┘                     │
│                ↓                                        │
│  Evidence Query Plan (EQP)                             │
│  ┌───────────────────────────────┐                     │
│  │ Question 1:                   │                     │
│  │   required_entities: [AAOIFIStandard]              │
│  │   required_edges: [Cites]     │                     │
│  │                               │                     │
│  │ Question 2:                   │                     │
│  │   required_entities: [AAOIFIStandard, Requirement] │
│  │   required_edges: [Defines]   │                     │
│  └───────────────────────────────┘                     │
│                ↓                                        │
│  Graphiti Extraction                                    │
│  (Extract entities using schema)                       │
│                ↓                                        │
│  Validation (Close the Loop!)                          │
│  ┌───────────────────────────────┐                     │
│  │ For each question in EQP:     │                     │
│  │   1. Query Graphiti           │                     │
│  │   2. Check entities exist     │                     │
│  │   3. Check edges exist        │                     │
│  │   4. Attempt to answer        │                     │
│  │                               │                     │
│  │ If answerable: ✅ Schema sufficient                │
│  │ If not: ❌ Schema incomplete → regenerate          │
│  └───────────────────────────────┘                     │
│                ↓                                        │
│         Feedback Loop                                   │
│  (Update OutcomeSpec, re-run pipeline)                 │
└─────────────────────────────────────────────────────────┘
```

### The Evidence Query Plan (EQP) - The Test Suite

The `schema_synthesizer.py` generates an **Evidence Query Plan** alongside the schema:

```json
// artifacts/eqp/aaoifi_standards_eqp.json
[
  {
    "question": "What standards cite FAS 28?",
    "required_entities": ["AAOIFIStandard"],
    "required_edges": ["Cites"],
    "metadata_filters": {
      "standard_code": "FAS 28"
    },
    "cypher_template": "MATCH (s:AAOIFIStandard)-[:CITES]->(target:AAOIFIStandard {standard_code: 'FAS 28'}) RETURN s.standard_code"
  },
  {
    "question": "What requirements does FAS 28 define?",
    "required_entities": ["AAOIFIStandard", "Requirement"],
    "required_edges": ["Defines"],
    "metadata_filters": {
      "standard_code": "FAS 28"
    },
    "cypher_template": "MATCH (s:AAOIFIStandard {standard_code: 'FAS 28'})-[:DEFINES]->(r:Requirement) RETURN r.requirement_text"
  }
]
```

**This is your test suite!** Each question becomes a testable assertion.

### Zero Unsupported Tokens Enforcement

From `AGENT_DRIVEN_ONTOLOGY_PIPELINE.md`:

> By constraining to:
> - Entities explicitly in schema (max 12)
> - Edges explicitly in schema (max 10)
> - Graphiti only extracts these types
>
> **Result**: No hallucinated entity types, no edge types outside your schema.

**Why This Matters**:
```python
# Graphiti extraction constrained by schema
entity_types = [cls.name for cls in schema_spec.classes]
# ['AAOIFIStandard', 'Requirement']

edge_types = [assoc.name for assoc in schema_spec.associations]
# ['Cites', 'Defines']

# If LLM tries to extract "Footnote" entity → REJECTED (not in schema)
# If LLM tries to create "References" edge → REJECTED (not in schema)
```

### Closed-Loop Validation Script

```python
# tests/test_outcome_validation.py
import json
from pathlib import Path
from graphiti import Graphiti

def validate_outcome(outcome_name: str, eqp_path: Path):
    """
    Validate that extracted knowledge graph can answer outcome questions.

    This is the CLOSED LOOP: Questions (input) → Schema → Extraction → Answer Questions (output)
    """
    # Load Evidence Query Plan
    with open(eqp_path) as f:
        eqp = json.load(f)

    graphiti = Graphiti()
    results = []

    for query_plan in eqp:
        question = query_plan["question"]
        required_entities = query_plan["required_entities"]
        required_edges = query_plan["required_edges"]
        cypher = query_plan.get("cypher_template")

        print(f"\n{'='*60}")
        print(f"Testing Question: {question}")
        print(f"{'='*60}")

        # Step 1: Check required entities exist in graph
        missing_entities = []
        for entity_type in required_entities:
            count = graphiti.count_entities(entity_type)
            if count == 0:
                missing_entities.append(entity_type)
                print(f"❌ Missing entity type: {entity_type}")
            else:
                print(f"✅ Found {count} {entity_type} entities")

        # Step 2: Check required edges exist in graph
        missing_edges = []
        for edge_type in required_edges:
            count = graphiti.count_edges(edge_type)
            if count == 0:
                missing_edges.append(edge_type)
                print(f"❌ Missing edge type: {edge_type}")
            else:
                print(f"✅ Found {count} {edge_type} edges")

        # Step 3: Attempt to execute query
        if not missing_entities and not missing_edges and cypher:
            try:
                answer = graphiti.query(cypher)
                if answer:
                    print(f"✅ Question answerable: {len(answer)} results")
                    results.append({
                        "question": question,
                        "status": "answerable",
                        "result_count": len(answer)
                    })
                else:
                    print(f"⚠️  Query executed but returned 0 results")
                    results.append({
                        "question": question,
                        "status": "no_results",
                        "issue": "Query returned empty"
                    })
            except Exception as e:
                print(f"❌ Query failed: {e}")
                results.append({
                    "question": question,
                    "status": "query_failed",
                    "error": str(e)
                })
        else:
            print(f"❌ Cannot answer: missing prerequisites")
            results.append({
                "question": question,
                "status": "unanswerable",
                "missing_entities": missing_entities,
                "missing_edges": missing_edges
            })

    # Summary
    answerable = sum(1 for r in results if r["status"] == "answerable")
    total = len(results)

    print(f"\n{'='*60}")
    print(f"OUTCOME VALIDATION SUMMARY: {outcome_name}")
    print(f"{'='*60}")
    print(f"Questions Answerable: {answerable}/{total} ({answerable/total*100:.1f}%)")

    if answerable == total:
        print("✅ Schema is SUFFICIENT for outcome")
        return True
    else:
        print("❌ Schema is INSUFFICIENT - regenerate with:")
        for result in results:
            if result["status"] != "answerable":
                print(f"  - Fix: {result['question']}")
                if "missing_entities" in result:
                    print(f"    Add entities: {result['missing_entities']}")
                if "missing_edges" in result:
                    print(f"    Add edges: {result['missing_edges']}")
        return False

# Run validation
if __name__ == "__main__":
    outcome = "aaoifi_standards"
    eqp_path = Path(f"artifacts/eqp/{outcome}_eqp.json")

    success = validate_outcome(outcome, eqp_path)
    exit(0 if success else 1)
```

### Example Validation Output

```
============================================================
Testing Question: What standards cite FAS 28?
============================================================
✅ Found 45 AAOIFIStandard entities
✅ Found 123 Cites edges
✅ Question answerable: 7 results

============================================================
Testing Question: What requirements does FAS 28 define?
============================================================
✅ Found 45 AAOIFIStandard entities
✅ Found 89 Requirement entities
✅ Found 156 Defines edges
✅ Question answerable: 12 results

============================================================
OUTCOME VALIDATION SUMMARY: aaoifi_standards
============================================================
Questions Answerable: 2/2 (100.0%)
✅ Schema is SUFFICIENT for outcome
```

### The Iterative Refinement Loop

```python
# agents/run_pipeline_with_validation.py
async def run_outcome_pipeline_with_validation(outcome_spec_path: Path):
    """
    Run outcome pipeline with closed-loop validation.

    Iterate until schema is sufficient to answer all questions.
    """
    max_iterations = 3
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        print(f"\n{'='*60}")
        print(f"ITERATION {iteration}")
        print(f"{'='*60}")

        # Step 1: Generate schema
        print("\n1. Generating schema...")
        schema_spec = await synthesize_schema_for_outcome(
            outcome_spec_path,
            ontology_refs_path=Path("artifacts/ontology_refs.json"),
            overlay_output_path=Path("schemas/overlays/outcome_overlay.yaml"),
            eqp_output_path=Path("artifacts/eqp/outcome_eqp.json")
        )

        # Step 2: Generate Pydantic
        print("\n2. Generating Pydantic models...")
        run_codegen(
            schema_path=Path("schemas/overlays/outcome_overlay.yaml"),
            output_path=Path("generated/pydantic/overlays/outcome_models.py")
        )

        # Step 3: Extract from test corpus
        print("\n3. Extracting from test corpus...")
        await graphiti.add_episode(
            name="test_extraction",
            episode_body=test_corpus_content,
            source=EpisodeType.json,
            entity_types=[cls.name for cls in schema_spec.classes],
            edge_types=[assoc.name for assoc in schema_spec.associations]
        )

        # Step 4: Validate (CLOSE THE LOOP)
        print("\n4. Validating outcome...")
        success = validate_outcome(
            "outcome",
            Path("artifacts/eqp/outcome_eqp.json")
        )

        if success:
            print(f"\n✅ SUCCESS: Schema sufficient after {iteration} iteration(s)")
            return True
        else:
            print(f"\n⚠️  Schema insufficient, refining...")
            # Agent analyzes failed queries and updates OutcomeSpec hints
            # (could use LLM to suggest additional entities/edges)

    print(f"\n❌ FAILED: Schema still insufficient after {max_iterations} iterations")
    return False
```

### Why This Is Critical

| Without Closed-Loop | With Closed-Loop (Outcome-Driven) |
|---------------------|-----------------------------------|
| ❌ Build schema, hope it works | ✅ Build schema, PROVE it works |
| ❌ Discover missing entities in production | ✅ Discover missing entities during validation |
| ❌ Manual testing required | ✅ Automated testing from OutcomeSpec |
| ❌ Schema drift (over-engineered or under-powered) | ✅ Schema exactly matches requirements |
| ❌ No feedback mechanism | ✅ Iterative refinement until sufficient |

### Integration with CI/CD

```yaml
# .github/workflows/validate_outcomes.yml
name: Validate Outcome Schemas

on:
  push:
    paths:
      - 'specs/**'
      - 'schemas/overlays/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Validate AAOIFI Standards Outcome
        run: python tests/test_outcome_validation.py aaoifi_standards

      - name: Validate Business Outcomes
        run: python tests/test_outcome_validation.py business_outcomes

      - name: Validate Contract Compliance
        run: python tests/test_outcome_validation.py contract_compliance
```

**Result**: Every schema change is validated against the questions it's supposed to answer.

### Summary: Why Closed-Loop Is Critical

**Traditional Approach** (Static Schemas):
```
Requirements → Schema → Implementation → Manual Testing → Hope
```

**Outcome-Driven Approach** (Closed-Loop):
```
Questions → Schema → EQP → Extraction → Validation → Proof
           ↑                                           ↓
           └─────────────── Feedback ─────────────────┘
```

**The Closed Loop Guarantees**:
1. ✅ **Sufficiency**: Schema contains exactly what's needed (no missing entities/edges)
2. ✅ **Minimalism**: Schema contains only what's needed (Instructor limits to max 12/10)
3. ✅ **Testability**: Every question becomes an automated test
4. ✅ **Traceability**: EQP links questions → schema elements → graph queries
5. ✅ **Refinement**: Validation failures inform schema improvements

**This is why outcome-driven beats domain/information-type/ontology organization**: Only outcome-driven enables closed-loop validation from requirements to implementation.

---

## 13. Relationship to Previous Strategy Documents

### Documents Superseded by This Strategy

This unified document **supersedes and corrects** three previous documents:

1. **INFORMATION_TYPE_VS_DOMAIN_STRATEGY.md**
   - **Old Recommendation**: Organize by domain first (business/, aaoifi/)
   - **Correction**: Organize by outcome, not domain
   - **What to Keep**: Episode model for source tracking (✅ correct!)
   - **What to Change**: Don't create static `domains/` hierarchy

2. **MODULAR_PYDANTIC_ARCHITECTURE.md**
   - **Old Recommendation**: Three-layer architecture (core → shared → domains)
   - **Correction**: Three-layer architecture (core → shared → **overlays**)
   - **What to Keep**: Plugin pattern, global registries (✅ correct!)
   - **What to Change**: `domains/` → `overlays/` (generated, not hand-written)

3. **ONTOLOGY_MAPPING_STRATEGY.md**
   - **Old Recommendation**: Manually add `class_uri` and `slot_uri` to schemas
   - **Correction**: Agent retrieves ontologies dynamically and LLM adds URIs
   - **What to Keep**: Understanding of DoCO, FIBO, Schema.org ontologies (✅ correct!)
   - **What to Change**: Don't hardcode ontology mappings; let agent retrieve them

### Why The Change?

The previous documents were written **before reading your agent pipeline code**. Once I read:
- `agents/ontology_retriever.py` - Dynamic ontology retrieval
- `agents/schema_synthesizer.py` - LLM + Instructor validation
- `agents/codegen_orchestrator.py` - Automated pipeline

It became clear your architecture is **outcome-driven**, not domain-driven. The agent pipeline shows you already understand this! The previous docs were based on common patterns (DDD, FastAPI project structure) but didn't account for your sophisticated agent-driven approach.

### What This Means for Implementation

**Don't do this** (from old docs):
```bash
# ❌ Old approach: Create static domain hierarchy
mkdir -p schemas/domains/business
mkdir -p schemas/domains/aaoifi
# ... manually write schemas with ontology URIs
```

**Do this instead** (outcome-driven):
```bash
# ✅ New approach: Write OutcomeSpec, run agent pipeline
cat > specs/aaoifi_standards_extraction.yaml <<EOF
outcome_name: AAOIFI Standards Knowledge Graph
questions:
  - What standards cite FAS 28?
ontologies:
  - prefix: doco
  - prefix: fibo
  - prefix: aaoifi
EOF

python -m agents.run_pipeline specs/aaoifi_standards_extraction.yaml
# Agent retrieves ontologies, LLM generates schema, codegen creates Pydantic
```

### Transition Plan

If you already created `domains/business/` or `domains/aaoifi/` following the old docs:

1. **Move them to examples**: They show what outcome-driven schemas look like
2. **Extract OutcomeSpecs**: Reverse-engineer what questions they answer
3. **Run agent pipeline**: Generate fresh overlays from specs
4. **Compare**: Agent-generated should be more minimal (max 12 classes)

**Your agent architecture is ahead of typical patterns!** Embrace it fully.

---

**Document Version:** 1.0
**Last Updated:** 2025-10-06
**Replaces:** INFORMATION_TYPE_VS_DOMAIN_STRATEGY.md, MODULAR_PYDANTIC_ARCHITECTURE.md, ONTOLOGY_MAPPING_STRATEGY.md
**Status:** ✅ Ready for Implementation (Outcome-Driven Approach)
