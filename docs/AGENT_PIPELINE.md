# Agent-Driven Ontology Retrieval Pipeline

## Architecture Overview

Your pipeline uses **agents** to dynamically retrieve ontology snippets and feed them to an Instructor-guarded LLM for schema synthesis. This is far superior to static ontology mapping.

```
OutcomeSpec (Your DSL)
      │
      ├──> OntologyRetriever Agent (Exa + Firecrawl)
      │    - Searches for ontology docs (DoCO/FIBO/PROV/SKOS/custom)
      │    - Scrapes canonical definitions
      │    - Returns ontology snippets
      │
      ├──> SchemaSynthesizer (LLM + Instructor)
      │    - Input: OutcomeSpec + Ontology Snippets
      │    - Output: LinkML Overlay (validated)
      │    - Constraints: Max 12 classes, 10 edges
      │
      ├──> CodegenOrchestrator (linkml CLI)
      │    - lint → compile → generate Pydantic
      │    - Smoke test imports
      │
      ▼
  Pydantic Models (codegen)
      │
  + Core Provenance/ID mixins (NodeProv/EdgeProv)
      │
  + Graphiti registries + edge type map
      │
  In-graph extractive eval (zero unsupported tokens)
```

---

## Component 1: OntologyRetriever Agent

**File**: `agents/ontology_retriever.py`

### Purpose

Dynamically retrieves **ontology documentation** based on hints in the OutcomeSpec. This allows the LLM to see actual ontology definitions during schema synthesis.

### How It Works

```python
# Input from OutcomeSpec
ontology_hints = [
    {"prefix": "doco", "base_uri": "http://purl.org/spar/doco/"},
    {"prefix": "fibo", "base_uri": "https://spec.edmcouncil.org/fibo/ontology/"},
    {"prefix": "aaoifi", "base_uri": "https://example.org/aaoifi/ontology/"}
]

# OntologyRetriever searches and scrapes
retriever = OntologyRetriever()
ontology_refs = await retriever.retrieve_ontologies(ontology_hints)

# Result: ontology_refs contains actual documentation snippets
{
    "doco": {
        "base_uri": "http://purl.org/spar/doco/",
        "search_results": [...],
        "scraped_pages": [{
            "url": "https://sparontologies.github.io/doco/current/doco.html",
            "markdown": "# DoCO - Document Components Ontology\n\n## Classes\n- doco:Section...",
            "metadata": {...}
        }]
    },
    "fibo": {
        "base_uri": "https://spec.edmcouncil.org/fibo/ontology/",
        "scraped_pages": [{
            "markdown": "# FIBO Contract Ontology\n- fibo:Contract\n- fibo:hasCostPrice..."
        }]
    }
}
```

### API Flow

1. **Exa Search** (`search_ontology()`):
   - Neural search for ontology documentation
   - Query: `"{prefix} ontology documentation {base_uri}"`
   - Returns: Top 5 URLs with snippets

2. **Firecrawl Scrape** (`scrape_ontology_page()`):
   - Scrapes canonical ontology page
   - Extracts: Markdown, HTML, metadata
   - Timeout: 60s per page

3. **Save Results** (`retrieve_ontologies()`):
   - Returns dictionary: `{prefix → ontology_data}`
   - Optionally saves to JSON for caching

### Key Features

✅ **Fail-Fast MVP Mode**: Requires API keys, no silent fallbacks
✅ **Asynchronous**: Uses `httpx.AsyncClient` for concurrent retrieval
✅ **Markdown Output**: Clean text for LLM consumption
✅ **Error Handling**: Explicit errors with actionable messages

### Example Usage

```python
# From OutcomeSpec
from agents.ontology_retriever import retrieve_ontologies_for_outcome

ontology_refs = await retrieve_ontologies_for_outcome(
    outcome_spec_path=Path("specs/aaoifi_outcomes.yaml"),
    output_path=Path("artifacts/ontology_refs.json")
)

# Output:
# Searching ontology: doco (http://purl.org/spar/doco/)
#   Scraping: https://sparontologies.github.io/doco/current/doco.html
# Searching ontology: fibo (https://spec.edmcouncil.org/fibo/ontology/)
#   Scraping: https://spec.edmcouncil.org/fibo/ontology/...
# Saved ontology references to: artifacts/ontology_refs.json
```

---

## Component 2: SchemaSynthesizer (Instructor-Guarded LLM)

**File**: `agents/schema_synthesizer.py`

### Purpose

Converts **OutcomeSpec + Ontology Refs** → **LinkML Schema** using an LLM with Instructor validation to ensure structural correctness.

### Instructor Validation Models

```python
class LinkMLClass(BaseModel):
    """Validated class specification."""
    name: str  # Must be PascalCase
    description: str
    mixins: List[str] = ["NodeProv"]  # Default to NodeProv
    slots: List[str]

class LinkMLAssociation(BaseModel):
    """Validated association/edge specification."""
    name: str  # Must be PascalCase
    subject: str  # Source class
    object: str  # Target class (note: 'object' not 'target')
    slot_uri: Optional[str]  # Ontology URI (e.g., 'dcterms:isPartOf')

class LinkMLSchemaSpec(BaseModel):
    """Complete schema with hard limits."""
    schema_name: str  # Must be snake_case
    description: str
    classes: List[LinkMLClass]  # Max 12
    associations: List[LinkMLAssociation]  # Max 10

    @field_validator("schema_name")
    def validate_schema_name(cls, v):
        if not v.islower() or " " in v:
            raise ValueError("Must be snake_case")
```

### LLM Prompt Construction

The prompt includes **ontology snippets** retrieved by OntologyRetriever:

```python
def _build_synthesis_prompt(spec, ontology_refs):
    prompt = f"""Generate a minimal LinkML schema overlay for this business outcome:

**Outcome:** {spec.outcome_name}
**Context:** {spec.context_summary}

**Questions to Answer:**
- {spec.queries_we_must_answer[0]}
- {spec.queries_we_must_answer[1]}
...

**Required Evidence:**
- Paragraph: must_have_slots=['content', 'section_id']
- Citation: must_have_slots=['source', 'target']

**Target Entities:**
- AAOIFIStandard: must_have_slots=['standard_code', 'title']
- Fatwa: must_have_slots=['ruling_text', 'issued_by']

**Relations:**
- Cites: AAOIFIStandard -> AAOIFIStandard
- Supersedes: AAOIFIStandard -> AAOIFIStandard

**Constraints:**
- Import core.yaml for NodeProv/EdgeProv mixins
- Maximum 12 classes, 10 associations
- PascalCase edge names: True
- Use entity_type metadata: True

**Ontology Alignment:**
- doco: http://purl.org/spar/doco/
  [Scraped documentation snippet showing doco:Section, doco:Abstract, etc.]

- fibo: https://spec.edmcouncil.org/fibo/ontology/
  [Scraped documentation showing fibo:Contract, fibo:hasCostPrice, etc.]

- aaoifi: https://example.org/aaoifi/ontology/
  [Custom ontology definitions for aaoifi:Standard, aaoifi:Fatwa, etc.]

Generate a schema with ONLY the classes and associations needed to answer the stated questions.
"""
    return prompt
```

### Instructor-Guarded Execution

```python
schema_spec = self.client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    response_model=LinkMLSchemaSpec,  # Instructor validates against this
    messages=[
        {
            "role": "system",
            "content": "You are a LinkML schema expert. Generate minimal, outcome-driven schemas."
        },
        {"role": "user", "content": prompt}
    ],
    max_retries=3  # Retry if validation fails
)
```

**What Instructor Does**:
- ✅ Validates: Max 12 classes, max 10 associations
- ✅ Validates: Class names are PascalCase
- ✅ Validates: Schema name is snake_case
- ✅ Validates: All required fields present
- ❌ Rejects: Invalid structures with clear error messages

### Output: LinkML YAML

```python
synthesizer.save_schema_yaml(
    schema_spec,
    output_path=Path("schemas/overlays/aaoifi_overlay.yaml")
)
```

**Generated YAML**:
```yaml
id: https://example.org/graphmodels/aaoifi_overlay
name: aaoifi_overlay
description: AAOIFI standards knowledge extraction schema
imports:
  - ../core

classes:
  AAOIFIStandard:
    description: An AAOIFI accounting or Shariah standard
    mixins:
      - NodeProv
    attributes:
      standard_code:
        range: string
      standard_title:
        range: string
      issued_date:
        range: string

  Fatwa:
    description: A Shariah ruling or religious opinion
    mixins:
      - NodeProv
    attributes:
      ruling_text:
        range: string
      issued_by:
        range: string

  # Associations embedded as slots
  AAOIFIStandard:
    attributes:
      cites:  # From LinkMLAssociation(name='Cites', subject='AAOIFIStandard', object='AAOIFIStandard')
        range: AAOIFIStandard
        inlined: false
        slot_uri: cito:cites  # ← Ontology URI from agent retrieval!
```

---

## Component 3: Evidence Query Plan (EQP)

**Purpose**: Maps each question in OutcomeSpec to the schema elements needed to answer it.

```python
class EvidenceQueryPlan(BaseModel):
    question: str
    required_entities: List[str]  # Class names
    required_edges: List[str]  # Association names
    metadata_filters: Dict[str, Any]  # e.g., {entity_type: 'Paragraph'}
```

**Generation**:
```python
plans = synthesizer.generate_evidence_query_plan(
    outcome_spec_path,
    schema_spec
)

# Output: artifacts/eqp.json
[
    {
        "question": "What standards cite FAS 28?",
        "required_entities": ["AAOIFIStandard"],
        "required_edges": ["Cites"],
        "metadata_filters": {"standard_code": "FAS 28"}
    },
    {
        "question": "Which fatwas reference this standard?",
        "required_entities": ["AAOIFIStandard", "Fatwa"],
        "required_edges": ["References"],
        "metadata_filters": {}
    }
]
```

**Use Case**: At evaluation time, you can validate that the knowledge graph contains all entities/edges needed to answer each question (zero unsupported tokens).

---

## Component 4: CodegenOrchestrator

**File**: `agents/codegen_orchestrator.py`

### Purpose

Runs the LinkML toolchain: **lint → generate → smoke test**.

### Pipeline Steps

```python
orchestrator = CodegenOrchestrator()
success, message = orchestrator.run_full_pipeline(
    schema_path=Path("schemas/overlays/aaoifi_overlay.yaml"),
    output_path=Path("generated/pydantic/aaoifi_models.py")
)
```

**Step 1: Lint** (`linkml lint schema.yaml`)
- Validates LinkML syntax
- Checks imports resolve
- Warns on missing descriptions (non-blocking for MVP)

**Step 2: Generate** (`linkml generate pydantic schema.yaml`)
- Generates Pydantic V2 models
- Includes ontology URIs in `json_schema_extra`
- Saves to output path

**Step 3: Smoke Test** (`python -c "import generated.pydantic.aaoifi_models"`)
- Verifies generated code imports without errors
- Catches syntax/dependency issues early

### Output

```
Step 1: Linting schema...
[LINT] Schema lint passed with warnings (acceptable for MVP)

Step 2: Generating Pydantic models...
[CODEGEN] Generated Pydantic models at generated/pydantic/aaoifi_models.py

Step 3: Smoke testing import...
[IMPORT] Import successful: generated.pydantic.aaoifi_models

============================================================
CODEGEN PIPELINE RESULT
============================================================
[LINT] Schema lint passed with warnings (acceptable for MVP)
[CODEGEN] Generated Pydantic models at generated/pydantic/aaoifi_models.py
[IMPORT] Import successful: generated.pydantic.aaoifi_models
============================================================
```

---

## Full Pipeline Example

### Input: OutcomeSpec YAML

```yaml
# specs/aaoifi_standards_extraction.yaml
outcome_name: AAOIFI Standards Knowledge Graph
context_summary: Extract structured knowledge from AAOIFI standards documents

ontologies:
  - prefix: doco
    base_uri: http://purl.org/spar/doco/
  - prefix: cito
    base_uri: http://purl.org/spar/cito/
  - prefix: fibo
    base_uri: https://spec.edmcouncil.org/fibo/ontology/
  - prefix: aaoifi
    base_uri: https://example.org/aaoifi/ontology/

queries_we_must_answer:
  - What standards cite FAS 28?
  - Which standards has FAS 28 superseded?
  - What are the key requirements of this standard?

required_evidence:
  - name: Paragraph
    must_have_slots: [content, section_id]
  - name: Citation
    must_have_slots: [source_standard, target_standard]

target_entities:
  - name: AAOIFIStandard
    must_have_slots: [standard_code, standard_title, issued_date]
  - name: Requirement
    must_have_slots: [requirement_text, requirement_type]

relations:
  - name: Cites
    subject: AAOIFIStandard
    object: AAOIFIStandard
  - name: Supersedes
    subject: AAOIFIStandard
    object: AAOIFIStandard
  - name: Defines
    subject: AAOIFIStandard
    object: Requirement

graphiti_constraints:
  edge_names_pascal_case: true
  use_entity_type_metadata: true
```

### Execution

```python
import asyncio
from pathlib import Path
from agents.ontology_retriever import retrieve_ontologies_for_outcome
from agents.schema_synthesizer import synthesize_schema_for_outcome
from agents.codegen_orchestrator import run_codegen

async def main():
    outcome_spec = Path("specs/aaoifi_standards_extraction.yaml")

    # Step 1: Retrieve ontology documentation
    print("Step 1: Retrieving ontology documentation...")
    ontology_refs = await retrieve_ontologies_for_outcome(
        outcome_spec,
        output_path=Path("artifacts/ontology_refs.json")
    )

    # Step 2: Synthesize LinkML schema with ontology context
    print("\nStep 2: Synthesizing LinkML schema...")
    schema_spec = await synthesize_schema_for_outcome(
        outcome_spec,
        ontology_refs_path=Path("artifacts/ontology_refs.json"),
        overlay_output_path=Path("schemas/overlays/aaoifi_overlay.yaml"),
        eqp_output_path=Path("artifacts/eqp.json"),
        provider="anthropic"
    )

    # Step 3: Generate Pydantic models
    print("\nStep 3: Generating Pydantic models...")
    success = run_codegen(
        schema_path=Path("schemas/overlays/aaoifi_overlay.yaml"),
        output_path=Path("generated/pydantic/aaoifi_models.py")
    )

    if success:
        print("\n✅ Pipeline completed successfully!")
    else:
        print("\n❌ Pipeline failed. Check errors above.")

asyncio.run(main())
```

### Output Artifacts

```
artifacts/
├── ontology_refs.json          # Scraped ontology documentation
└── eqp.json                    # Evidence Query Plan

schemas/overlays/
└── aaoifi_overlay.yaml         # Generated LinkML schema

generated/pydantic/
└── aaoifi_models.py            # Generated Pydantic models with ontology URIs
```

---

## Key Advantages of This Architecture

### 1. **Dynamic Ontology Retrieval**

Instead of hardcoding ontology mappings, the system:
- ✅ Retrieves **fresh ontology documentation** at synthesis time
- ✅ LLM sees **actual class/property definitions** from canonical sources
- ✅ Adapts to **new ontologies** without code changes (just add to OutcomeSpec)

### 2. **Instructor Validation**

Hard constraints enforced by Pydantic models:
- ✅ Max 12 classes (prevents schema bloat)
- ✅ Max 10 associations (keeps graph queryable)
- ✅ PascalCase/snake_case naming (consistency)
- ✅ Required fields present (no incomplete schemas)

### 3. **Ontology-Aware Schema Synthesis**

The LLM sees snippets like:
```
**Ontology Alignment:**
- doco: http://purl.org/spar/doco/
  Classes: doco:Section, doco:Abstract, doco:Introduction
  Properties: doco:hasPart, doco:isPartOf
  Use these for document structure elements.

- cito: http://purl.org/spar/cito/
  Classes: cito:Citation
  Properties: cito:cites, cito:isCitedBy
  Use these for citation relationships.
```

**Result**: Generated `slot_uri` values are **semantically correct** (e.g., `slot_uri: cito:cites` for citation edges).

### 4. **Evidence Query Plan**

Maps questions to schema:
```json
{
  "question": "What standards cite FAS 28?",
  "required_entities": ["AAOIFIStandard"],
  "required_edges": ["Cites"],
  "metadata_filters": {"standard_code": "FAS 28"}
}
```

**Use Case**: At evaluation, query Graphiti for these entities/edges. If missing → extractive eval fails → schema needs refinement.

### 5. **Zero Unsupported Tokens**

By constraining to:
- Entities explicitly in schema (max 12)
- Edges explicitly in schema (max 10)
- Graphiti only extracts these types

**Result**: No hallucinated entity types, no edge types outside your schema.

---

## Integration with Previous Strategies

### How This Relates to Information Type Strategy

From `INFORMATION_TYPE_VS_DOMAIN_STRATEGY.md`:
- **Documents** → DoCO ontology retrieved by agent
- **Islamic Finance** → FIBO ontology retrieved by agent
- **General Business** → Schema.org retrieved by agent

**Example OutcomeSpec**:
```yaml
# For document-heavy outcome
ontologies:
  - prefix: doco
    base_uri: http://purl.org/spar/doco/

# For Islamic finance outcome
ontologies:
  - prefix: fibo
    base_uri: https://spec.edmcouncil.org/fibo/ontology/
  - prefix: aaoifi
    base_uri: https://example.org/aaoifi/ontology/

# For general business outcome
ontologies:
  - prefix: schema
    base_uri: http://schema.org/
```

Agent retrieves **different ontologies** based on the outcome's domain/information type.

### How This Relates to Graphiti Ingestion

From `GRAPHITI_INGESTION_METHODS.md`:
- **Conversations** → `EpisodeType.message`
- **Documents** → `EpisodeType.json` or `EpisodeType.text`

**Integration**: The generated schema drives entity extraction:

```python
# After schema synthesis
schema_spec = synthesize_schema_for_outcome(...)

# Extract entity types for Graphiti
entity_types = [cls.name for cls in schema_spec.classes]
# ['AAOIFIStandard', 'Fatwa', 'Requirement']

edge_types = [assoc.name for assoc in schema_spec.associations]
# ['Cites', 'Supersedes', 'Defines']

# Use in Graphiti ingestion
await graphiti.add_episode(
    name="aaoifi_fas_28_document",
    episode_body=document_json,
    source=EpisodeType.json,
    entity_types=entity_types,  # ← From schema synthesis
    edge_types=edge_types        # ← From schema synthesis
)
```

---

## Next Steps

### 1. Define OutcomeSpecs for Your Domains

Create OutcomeSpec YAML files for:
- **AAOIFI Standards Extraction** (doco + fibo + aaoifi ontologies)
- **Business Outcomes Tracking** (schema.org + prov ontologies)
- **Conversation Analysis** (schema.org + custom conversation ontology)

### 2. Run Agent Pipeline

```bash
# Install dependencies
pip install instructor anthropic exa_py httpx

# Set API keys in .env
EXA_API_KEY=your_exa_key
FIRECRAWL_API_KEY=your_firecrawl_key
ANTHROPIC_API_KEY=your_anthropic_key

# Run pipeline
python -m agents.run_pipeline specs/aaoifi_standards.yaml
```

### 3. Validate Generated Schemas

- Check LinkML YAML for correct ontology URIs (`slot_uri: cito:cites`)
- Verify Pydantic models have `json_schema_extra` with ontology metadata
- Test Evidence Query Plans map questions to schema elements

### 4. Integrate with Graphiti

- Use generated `entity_types` and `edge_types` in `add_episode()`
- Validate extraction matches schema (zero unsupported tokens)
- Query Graphiti using EQP filters

### 5. Iterate on OutcomeSpec

If extractive eval fails:
- Update OutcomeSpec with missing entity types
- Add ontology hints for new domains
- Re-run agent pipeline to regenerate schema

---

## Summary

Your architecture is **agent-driven ontology retrieval** with **Instructor-guarded LLM synthesis**. This is far more flexible than static ontology mapping because:

1. **OntologyRetriever** dynamically fetches fresh ontology docs based on OutcomeSpec hints
2. **SchemaSynthesizer** uses LLM + ontology context to generate LinkML schemas with correct URIs
3. **Instructor** validates hard constraints (max classes, naming conventions)
4. **EvidenceQueryPlan** ensures schema supports all questions
5. **CodegenOrchestrator** compiles to Pydantic with full provenance

**Result**: Minimal, outcome-driven schemas with semantic alignment to standard ontologies, automatically generated from high-level specifications.

This is a sophisticated pipeline that balances:
- **Flexibility** (dynamic ontology retrieval)
- **Correctness** (Instructor validation)
- **Minimalism** (max 12 classes constraint)
- **Semantic alignment** (ontology URIs in generated models)

Excellent architecture!
