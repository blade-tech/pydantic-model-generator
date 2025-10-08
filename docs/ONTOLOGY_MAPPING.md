# Ontology Mapping Strategy for Pydantic Models

## Executive Summary

**Strategy**: Use LinkML's `class_uri` and `slot_uri` annotations to map your Pydantic models to standard ontologies. This maintains **semantic alignment with standards** while keeping your Pydantic models clean and domain-focused.

**Key Insight**: Ontology choice depends on **information type AND domain**:
- **Documents**: DoCO (Document Components Ontology) - for structural elements
- **Islamic Finance**: FIBO (Financial Industry Business Ontology) - for financial concepts
- **General Business**: Schema.org - for common business entities
- **Provenance**: PROV-O - for tracking data lineage

LinkML acts as the bridge: **YAML schemas** contain ontology URIs → generate **Pydantic models** + **RDF/OWL exports** with full semantic alignment.

---

## Why Ontology Mapping Matters

### Problem Without Ontologies

```python
# Your internal model
class MurabahaContract(BaseModel):
    contract_id: str
    seller: str
    buyer: str
    asset: str
    cost_price: float
    profit_margin: float
```

**Issues**:
- ❌ Not interoperable with AAOIFI systems
- ❌ Can't validate against FIBO concepts
- ❌ Can't query across heterogeneous data sources
- ❌ No semantic reasoning (e.g., "Murabaha is a type of sale")

### Solution With Ontology Mapping

```yaml
# LinkML schema with ontology URIs
classes:
  MurabahaContract:
    class_uri: fibo:MurabahaContract
    is_a: IslamicFinancialContract
    slots:
      - contract_id
      - seller
      - buyer
      - asset
      - cost_price
      - profit_margin

slots:
  seller:
    slot_uri: fibo:hasSeller
    range: Organization

  buyer:
    slot_uri: fibo:hasBuyer
    range: Organization

  cost_price:
    slot_uri: fibo:hasCostPrice
    range: MonetaryAmount
```

**Benefits**:
- ✅ Interoperable with FIBO-compliant systems
- ✅ Validatable against AAOIFI ontologies
- ✅ Queryable via SPARQL across data sources
- ✅ Enables semantic reasoning

---

## Ontology Selection Strategy

### By Information Type

| Information Type | Primary Ontology | URI Prefix | Use Case |
|------------------|------------------|------------|----------|
| **Documents** | DoCO | `doco:` | Document structure, sections, rhetorical elements |
| **Citations** | CiTO | `cito:` | Citation relationships |
| **Bibliographic** | FaBiO | `fabio:` | Publications, articles, books |
| **Provenance** | PROV-O | `prov:` | Data lineage, attribution, derivation |

### By Domain

| Domain | Primary Ontology | URI Prefix | Use Case |
|--------|------------------|------------|----------|
| **Islamic Finance** | FIBO | `fibo:` | Financial instruments, contracts, parties |
| **General Business** | Schema.org | `schema:` | Organizations, people, events, places |
| **AAOIFI Standards** | Custom AAOIFI | `aaoifi:` | Standards, Shariah rulings, compliance |
| **Legal** | LegalRuleML | `lrml:` | Rules, regulations, compliance |

### Combined Example Matrix

| Entity Type | Information Source | Ontology Mapping |
|-------------|-------------------|------------------|
| **BusinessOutcome** from Slack | Conversation | `schema:Action` + `prov:Entity` |
| **AAOIFIStandard** from PDF | Document | `doco:Document` + `aaoifi:Standard` |
| **MurabahaContract** from database | Structured data | `fibo:Contract` + `aaoifi:MurabahaContract` |
| **Fatwa** from document | Document | `doco:Document` + `aaoifi:Fatwa` |
| **BusinessTask** from conversation | Conversation | `schema:Action` + `prov:Activity` |

---

## LinkML Ontology Mapping Patterns

### Pattern 1: Class URI Mapping

Maps entire class to ontology concept:

```yaml
prefixes:
  schema: http://schema.org/
  fibo: https://spec.edmcouncil.org/fibo/ontology/
  aaoifi: https://example.org/aaoifi/ontology/
  doco: http://purl.org/spar/doco/
  prov: http://www.w3.org/ns/prov#

classes:
  BusinessOutcome:
    class_uri: schema:Action  # Maps to Schema.org Action
    description: A business outcome or deliverable
    mixins:
      - ProvenanceFields
    slots:
      - outcome_type
      - status
      - priority

  AAOIFIStandard:
    class_uri: doco:Standard  # Maps to DoCO Standard (document type)
    description: An AAOIFI accounting or Shariah standard
    mixins:
      - ProvenanceFields
    slots:
      - standard_code
      - standard_title
      - standard_type
```

**What This Does**:
- Generates Pydantic model with `model_config = ConfigDict(json_schema_extra={'class_uri': 'schema:Action'})`
- Enables RDF export: `<entity> rdf:type schema:Action`
- Supports SPARQL queries: `SELECT ?x WHERE { ?x rdf:type schema:Action }`

### Pattern 2: Slot URI Mapping

Maps individual fields to ontology properties:

```yaml
slots:
  outcome_type:
    slot_uri: schema:actionType
    range: string
    description: Type of business outcome

  priority:
    slot_uri: schema:priority
    range: Priority
    description: Priority level

  due_date:
    slot_uri: schema:endDate
    range: datetime
    description: Expected completion date

  confidence:
    slot_uri: schema:probability
    range: Confidence01
    description: Confidence score for outcome
```

**What This Does**:
- Adds semantic meaning to each field
- RDF export: `<entity> schema:actionType "deliverable"`
- Enables property-level SPARQL queries

### Pattern 3: Multiple Ontology Mappings

Use `exact_mappings`, `close_mappings`, `related_mappings` for alignment:

```yaml
slots:
  email:
    slot_uri: schema:email
    exact_mappings:
      - foaf:mbox  # Friend of a Friend ontology
    range: Email

  standard_code:
    slot_uri: aaoifi:standardCode
    close_mappings:
      - doco:documentIdentifier
      - schema:identifier
    range: string
```

**Mapping Types**:
- `exact_mappings`: Semantically identical
- `close_mappings`: Similar but not identical
- `related_mappings`: Related concepts
- `narrow_mappings`: More specific concept
- `broad_mappings`: More general concept

### Pattern 4: Mixin Inheritance with Ontology URIs

```yaml
classes:
  ProvenanceFields:
    mixin: true
    class_uri: prov:Entity
    slots:
      - node_id
      - episode_ids
      - created_at
      - valid_at

  BusinessOutcome:
    mixins:
      - ProvenanceFields  # Inherits prov:Entity class_uri
    class_uri: schema:Action
    slots:
      - outcome_type
```

**Result**: `BusinessOutcome` is both `schema:Action` and `prov:Entity` in RDF

---

## Domain-Specific Ontology Mappings

### Islamic Finance Domain (FIBO + Custom AAOIFI)

```yaml
# schemas/domains/aaoifi/ontology_config.yaml
prefixes:
  fibo: https://spec.edmcouncil.org/fibo/ontology/
  aaoifi: https://example.org/aaoifi/ontology/
  schema: http://schema.org/

classes:
  IslamicFinancialContract:
    class_uri: fibo:Contract
    abstract: true
    slots:
      - contract_id
      - effective_date
      - parties

  MurabahaContract:
    is_a: IslamicFinancialContract
    class_uri: aaoifi:MurabahaContract
    description: Murabaha sale contract
    slots:
      - cost_price
      - profit_margin
      - deferred_payment_terms

  AAOIFIStandard:
    class_uri: aaoifi:Standard
    mixins:
      - doco:Document  # Also a document
    slots:
      - standard_code
      - standard_type
      - issued_date
      - supersedes

slots:
  cost_price:
    slot_uri: fibo:hasCostPrice
    range: MonetaryAmount

  profit_margin:
    slot_uri: aaoifi:hasProfitMargin
    range: float
    unit:
      ucum_code: '%'

  standard_code:
    slot_uri: aaoifi:standardCode
    exact_mappings:
      - schema:identifier
    pattern: '^(FAS|GSIFI|AAOIFI) \\d+$'

  supersedes:
    slot_uri: aaoifi:supersedes
    range: AAOIFIStandard
    multivalued: true
```

### Document Domain (DoCO + FaBiO)

```yaml
# schemas/core/documents.yaml
prefixes:
  doco: http://purl.org/spar/doco/
  fabio: http://purl.org/spar/fabio/
  cito: http://purl.org/spar/cito/

classes:
  Document:
    class_uri: doco:Document
    abstract: true
    slots:
      - document_id
      - title
      - abstract
      - sections

  AAOIFIStandard:
    is_a: Document
    class_uri: fabio:Standard
    description: AAOIFI standard document
    slots:
      - standard_code
      - issued_date

  Section:
    class_uri: doco:Section
    slots:
      - section_number
      - section_title
      - content

  Citation:
    class_uri: cito:Citation
    slots:
      - citing_document
      - cited_document
      - citation_type

slots:
  abstract:
    slot_uri: doco:Abstract
    range: string

  sections:
    slot_uri: doco:hasPart
    range: Section
    multivalued: true

  citation_type:
    slot_uri: cito:hasCitationCharacterization
    range: CitationType
```

**Key DoCO Classes** (from research):
- `doco:Document` - Any document
- `doco:Section` - Document section
- `doco:Abstract` - Abstract/summary
- `doco:Introduction` - Introduction section
- `doco:Methods` - Methods section
- `doco:Results` - Results section
- `doco:Discussion` - Discussion section
- `doco:Conclusion` - Conclusion section
- `doco:Figure` - Figure in document
- `doco:Table` - Table in document
- `doco:Reference` - Bibliographic reference

### General Business Domain (Schema.org)

```yaml
# schemas/domains/business/ontology_config.yaml
prefixes:
  schema: http://schema.org/
  prov: http://www.w3.org/ns/prov#

classes:
  Actor:
    class_uri: schema:Person
    slots:
      - name
      - role
      - email
      - phone

  Organization:
    class_uri: schema:Organization
    slots:
      - name
      - industry
      - size
      - tier

  BusinessTask:
    class_uri: schema:Action
    mixins:
      - prov:Activity
    slots:
      - title
      - description
      - task_status
      - assigned_to

  BusinessDecision:
    class_uri: schema:Action
    slots:
      - decision_summary
      - rationale
      - approved_by

slots:
  role:
    slot_uri: schema:jobTitle
    range: string

  industry:
    slot_uri: schema:industry
    range: string

  assigned_to:
    slot_uri: schema:agent
    range: Actor
```

---

## Complete Example: AAOIFI Standard with Full Ontology Mapping

```yaml
# schemas/domains/aaoifi/entities.yaml
id: https://example.org/schemas/aaoifi/entities
name: aaoifi_entities
description: AAOIFI domain entities with ontology mappings

prefixes:
  linkml: https://w3id.org/linkml/
  schema: http://schema.org/
  doco: http://purl.org/spar/doco/
  fabio: http://purl.org/spar/fabio/
  fibo: https://spec.edmcouncil.org/fibo/ontology/
  aaoifi: https://example.org/aaoifi/ontology/
  prov: http://www.w3.org/ns/prov#

default_prefix: aaoifi

imports:
  - ../../core/provenance
  - ../../core/types
  - ../shared/temporal

classes:
  AAOIFIStandard:
    class_uri: fabio:Standard  # It's a standard document
    description: An AAOIFI accounting or Shariah standard
    mixins:
      - ProvenanceFields  # Inherits prov:Entity
    slots:
      - standard_code
      - standard_title
      - standard_type
      - issued_date
      - status
      - scope
      - key_requirements
      - references_standards
      - supersedes_standards

  Fatwa:
    class_uri: aaoifi:Fatwa
    description: A Shariah ruling or religious opinion
    mixins:
      - ProvenanceFields
      - doco:Document
    slots:
      - fatwa_id
      - fatwa_title
      - issued_by
      - issued_date
      - ruling_text
      - references_standards

  ShariaBoard:
    class_uri: schema:Organization
    description: Shariah supervisory board
    slots:
      - board_name
      - institution
      - members
      - established_date

slots:
  standard_code:
    slot_uri: aaoifi:standardCode
    exact_mappings:
      - schema:identifier
      - doco:documentIdentifier
    range: string
    required: true
    pattern: '^(FAS|GSIFI|AAOIFI) \\d+$'

  standard_title:
    slot_uri: schema:name
    exact_mappings:
      - doco:title
    range: string
    required: true

  standard_type:
    slot_uri: aaoifi:standardType
    range: StandardType
    required: true

  issued_date:
    slot_uri: schema:datePublished
    exact_mappings:
      - doco:publicationDate
    range: datetime
    required: true

  status:
    slot_uri: aaoifi:standardStatus
    range: StandardStatus
    required: true

  scope:
    slot_uri: aaoifi:scope
    close_mappings:
      - schema:abstract
    range: string
    description: Application scope of the standard

  key_requirements:
    slot_uri: aaoifi:hasRequirement
    range: string
    multivalued: true
    description: Key requirements defined by the standard

  references_standards:
    slot_uri: cito:cites  # Citation Typing Ontology
    range: AAOIFIStandard
    multivalued: true
    description: Other standards referenced by this standard

  supersedes_standards:
    slot_uri: aaoifi:supersedes
    close_mappings:
      - schema:supersededBy
    range: AAOIFIStandard
    multivalued: true
    description: Previous standards that this standard replaces

enums:
  StandardType:
    permissible_values:
      accounting:
        meaning: aaoifi:AccountingStandard
      auditing:
        meaning: aaoifi:AuditingStandard
      governance:
        meaning: aaoifi:GovernanceStandard
      ethics:
        meaning: aaoifi:EthicsStandard
      shariah:
        meaning: aaoifi:ShariahStandard

  StandardStatus:
    permissible_values:
      draft:
        meaning: aaoifi:DraftStatus
      active:
        meaning: aaoifi:ActiveStatus
      withdrawn:
        meaning: aaoifi:WithdrawnStatus
      superseded:
        meaning: aaoifi:SupersededStatus
```

---

## Generated Pydantic Output with Ontology Annotations

```python
# generated/pydantic/aaoifi_entities.py (simplified)
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from enum import Enum

class StandardType(str, Enum):
    """StandardType enum with ontology URIs"""
    accounting = "accounting"
    auditing = "auditing"
    governance = "governance"
    ethics = "ethics"
    shariah = "shariah"

class AAOIFIStandard(BaseModel):
    """
    An AAOIFI accounting or Shariah standard

    Ontology Mapping:
    - class_uri: fabio:Standard
    - mixin: prov:Entity (from ProvenanceFields)
    """

    model_config = ConfigDict(
        json_schema_extra={
            "class_uri": "fabio:Standard",
            "mixins": ["prov:Entity"],
            "$id": "https://example.org/schemas/aaoifi/entities/AAOIFIStandard"
        }
    )

    standard_code: str = Field(
        ...,
        description="Standard code (e.g., FAS 28)",
        pattern="^(FAS|GSIFI|AAOIFI) \\d+$",
        json_schema_extra={
            "slot_uri": "aaoifi:standardCode",
            "exact_mappings": ["schema:identifier", "doco:documentIdentifier"]
        }
    )

    standard_title: str = Field(
        ...,
        description="Full title of the standard",
        json_schema_extra={
            "slot_uri": "schema:name",
            "exact_mappings": ["doco:title"]
        }
    )

    standard_type: StandardType = Field(
        ...,
        json_schema_extra={
            "slot_uri": "aaoifi:standardType"
        }
    )

    issued_date: datetime = Field(
        ...,
        json_schema_extra={
            "slot_uri": "schema:datePublished",
            "exact_mappings": ["doco:publicationDate"]
        }
    )

    references_standards: Optional[List[str]] = Field(
        default=None,
        description="Other standards referenced by this standard",
        json_schema_extra={
            "slot_uri": "cito:cites"
        }
    )

    # Provenance fields (inherited from ProvenanceFields mixin)
    node_id: str = Field(
        ...,
        json_schema_extra={"slot_uri": "prov:identifier"}
    )

    episode_ids: Optional[List[str]] = Field(
        default=None,
        json_schema_extra={"slot_uri": "prov:wasDerivedFrom"}
    )
```

**Usage**:
```python
standard = AAOIFIStandard(
    standard_code="FAS 28",
    standard_title="Murabaha and Other Deferred Payment Sales",
    standard_type=StandardType.accounting,
    issued_date=datetime(2018, 11, 1),
    references_standards=["FAS 1", "FAS 2"],
    node_id="aaoifi_fas_28",
    episode_ids=["episode_doc_fas28_pdf"]
)

# Access ontology metadata
print(standard.model_config['json_schema_extra']['class_uri'])
# Output: fabio:Standard

# Export to RDF (with separate tool)
# <aaoifi_fas_28> rdf:type fabio:Standard .
# <aaoifi_fas_28> aaoifi:standardCode "FAS 28" .
# <aaoifi_fas_28> schema:name "Murabaha..." .
# <aaoifi_fas_28> cito:cites <FAS_1>, <FAS_2> .
```

---

## Benefits of This Approach

### 1. **Standards Compliance**
✅ Models align with international ontologies (FIBO, Schema.org, DoCO)
✅ AAOIFI standards map to recognized semantic concepts
✅ Interoperable with FIBO-compliant financial systems

### 2. **Domain Flexibility**
✅ Different ontologies for different domains (business vs AAOIFI)
✅ Different ontologies for information types (conversations vs documents)
✅ Easy to add new ontologies as needed

### 3. **Clean Pydantic Models**
✅ Ontology URIs stored in metadata, not polluting business logic
✅ Models remain Pythonic and usable
✅ Optional: can ignore ontology annotations entirely

### 4. **RDF/SPARQL Export**
✅ Generate RDF triples from Pydantic instances
✅ Query across heterogeneous data with SPARQL
✅ Semantic reasoning (e.g., "all Contracts")

### 5. **Validation Against Ontologies**
✅ Validate that `standard_type` values exist in AAOIFI ontology
✅ Check that relationships (cites, supersedes) are semantically valid
✅ Enforce ontology constraints

---

## Implementation Checklist

### Phase 1: Define Ontology Prefixes (1 hour)

```yaml
# schemas/prefixes.yaml (shared across all schemas)
prefixes:
  # Core ontologies
  schema: http://schema.org/
  prov: http://www.w3.org/ns/prov#

  # Document ontologies
  doco: http://purl.org/spar/doco/
  fabio: http://purl.org/spar/fabio/
  cito: http://purl.org/spar/cito/

  # Financial ontologies
  fibo: https://spec.edmcouncil.org/fibo/ontology/

  # Custom ontologies
  aaoifi: https://example.org/aaoifi/ontology/
  business: https://example.org/business/ontology/
```

### Phase 2: Add class_uri to Core Classes (2-3 hours)

- [ ] Add `class_uri: prov:Entity` to ProvenanceFields
- [ ] Add `class_uri: schema:Person` to Actor
- [ ] Add `class_uri: schema:Organization` to Organization/Customer

### Phase 3: Add class_uri to Domain Classes (3-4 hours)

**Business Domain**:
- [ ] `BusinessOutcome` → `schema:Action`
- [ ] `BusinessTask` → `schema:Action` + `prov:Activity`
- [ ] `BusinessDecision` → `schema:Action`

**AAOIFI Domain**:
- [ ] `AAOIFIStandard` → `fabio:Standard`
- [ ] `Fatwa` → `aaoifi:Fatwa` + `doco:Document`
- [ ] `MurabahaContract` → `aaoifi:MurabahaContract`

### Phase 4: Add slot_uri to Key Fields (2-3 hours)

- [ ] `email` → `schema:email` (exact_mappings: foaf:mbox)
- [ ] `name` → `schema:name`
- [ ] `due_date` → `schema:endDate`
- [ ] `standard_code` → `aaoifi:standardCode`

### Phase 5: Test Ontology Alignment (1-2 hours)

```python
# Test script: validate_ontology_mappings.py
from generated.pydantic.aaoifi_entities import AAOIFIStandard

# Check ontology metadata present
standard = AAOIFIStandard(...)
assert 'class_uri' in standard.model_config['json_schema_extra']
assert standard.model_config['json_schema_extra']['class_uri'] == 'fabio:Standard'

# Check field ontology mappings
field_info = AAOIFIStandard.model_fields['standard_code']
assert 'slot_uri' in field_info.json_schema_extra
assert field_info.json_schema_extra['slot_uri'] == 'aaoifi:standardCode'
```

### Phase 6: Generate RDF Exports (Optional, 2-4 hours)

```python
# Use LinkML's RDF generator
from linkml.generators.rdfgen import RDFGenerator

generator = RDFGenerator("schemas/domains/aaoifi/entities.yaml")
rdf_output = generator.serialize(format="turtle")

# Output:
# @prefix aaoifi: <https://example.org/aaoifi/ontology/> .
# @prefix fabio: <http://purl.org/spar/fabio/> .
#
# <aaoifi_fas_28> a fabio:Standard ;
#     aaoifi:standardCode "FAS 28" ;
#     schema:name "Murabaha..." .
```

---

## Query Examples with Ontology URIs

### SPARQL Query Across Domains

```sparql
PREFIX schema: <http://schema.org/>
PREFIX fabio: <http://purl.org/spar/fabio/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX aaoifi: <https://example.org/aaoifi/ontology/>

# Find all entities derived from document episodes
SELECT ?entity ?type ?episode
WHERE {
  ?entity a ?type .
  ?entity prov:wasDerivedFrom ?episode .
  ?episode a prov:Entity .

  # Filter to standards only
  FILTER(?type = fabio:Standard || ?type = aaoifi:Standard)
}
```

### Python Query Using Ontology Mappings

```python
# Query Graphiti using ontology-aware search
results = await graphiti.search(
    query="Find all AAOIFI standards about Murabaha",
    entity_types=["fabio:Standard", "aaoifi:Standard"],
    num_results=10
)

# Filter results by ontology type
standards = [
    r for r in results
    if r.entity_type in ["fabio:Standard", "aaoifi:Standard"]
]
```

---

## Next Steps

1. **Define Your Custom AAOIFI Ontology** (if not exists)
   - Create `ontologies/aaoifi.ttl` with AAOIFI-specific concepts
   - Define: `aaoifi:Standard`, `aaoifi:Fatwa`, `aaoifi:MurabahaContract`
   - Host at: `https://example.org/aaoifi/ontology/`

2. **Add Ontology URIs to LinkML Schemas**
   - Start with core classes (ProvenanceFields, Actor)
   - Add domain-specific mappings (AAOIFI, business)
   - Use multiple ontologies where appropriate (fabio + aaoifi)

3. **Generate Pydantic Models with Ontology Metadata**
   - Run `gen-pydantic` on updated schemas
   - Verify `class_uri` and `slot_uri` in generated models

4. **Test Semantic Queries**
   - Export Pydantic instances to RDF
   - Query with SPARQL across domains
   - Validate ontology alignment with reasoners

5. **Document Ontology Choices**
   - Create mapping table: Entity → Ontology URIs
   - Explain rationale for each mapping
   - Provide SPARQL query examples

**Total Effort**: ~10-15 hours to add full ontology mapping layer

---

## Summary

**Yes, ontologies depend on information type AND domain**:

- **Documents** (regardless of domain) → DoCO, FaBiO, CiTO
- **Islamic Finance** (regardless of source) → FIBO, custom AAOIFI
- **General Business** → Schema.org
- **Provenance** (universal) → PROV-O

Use LinkML's `class_uri` and `slot_uri` to maintain semantic alignment while keeping Pydantic models clean and Pythonic. This enables:
- Interoperability with standard systems
- SPARQL querying across heterogeneous data
- Validation against ontology constraints
- Semantic reasoning

The ontology layer is **metadata** - it enriches your models without polluting business logic.
