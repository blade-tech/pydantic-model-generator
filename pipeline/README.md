# Pipeline: Business Outcome → Pydantic Module

**Purpose**: Repeatable pipeline to add new overlays to the Pydantic library.

## Quick Start

### Add New Overlay (Automated)

```bash
python pipeline/add_overlay.py \
    --name "customer_support" \
    --outcome-doc "docs/customer_support_requirements.md"
```

This will:
1. Generate OutcomeSpec from your business document
2. Create LinkML overlay schema
3. Generate Pydantic models with `gen-pydantic`
4. Create glue code (type registries + edge validation)
5. Generate test template
6. Run tests to validate

### Add New Overlay (Manual - 8 Steps)

See: `../pydantic_library/MIGRATION_GUIDE.md`

## Templates

### 1. OutcomeSpec Template
**File**: `templates/outcome_spec_template.yaml`

Copy and fill in your business questions:
```yaml
id: https://example.org/specs/your-outcome
outcome_name: "Your Outcome Name"

outcome_questions:
  - question: "What entities do I need to track?"
    target_entities: [YourEntity]

validation_queries:
  - name: "test_your_query"
    cypher: |
      MATCH (e:YourEntity)
      RETURN e.field1
```

### 2. Overlay Schema Template
**File**: `templates/overlay_schema_template.yaml`

Copy and customize for your entities:
```yaml
id: https://example.org/schemas/your-overlay
name: your_overlay
imports:
  - ../core/provenance

classes:
  YourEntity:
    class_uri: ontology:YourClass
    mixins:
      - ProvenanceFields
    slots:
      - field1
```

### 3. Test Template
**File**: `templates/test_template.py`

Copy and adapt for your overlay validation queries.

## Examples

### Example 1: Business Outcomes
**File**: `examples/example_business_outcome.md`

Shows how to model:
- Deliverables, milestones, teams, outcomes
- Task assignments, handoffs, decisions

### Example 2: AAOIFI Standards
**File**: `examples/example_aaoifi_standard.md`

Shows how to model:
- Documents, sections, paragraphs, rules
- Provenance from source documents

## Pipeline Script Usage

### Basic Usage
```bash
python pipeline/add_overlay.py --name "your_overlay"
```

### With Business Document (AI-assisted)
```bash
python pipeline/add_overlay.py \
    --name "your_overlay" \
    --outcome-doc "path/to/requirements.md"
```

The script will:
- Parse the business document
- Generate OutcomeSpec with AI assistance
- Create LinkML schema
- Generate Pydantic models
- Create glue code
- Generate tests

### Manual Mode (Interactive)
```bash
python pipeline/add_overlay.py --name "your_overlay" --interactive
```

Prompts you for:
- Outcome questions
- Target entities
- Validation queries
- Canonical ontology URIs

## Output Structure

After running the pipeline, you'll have:

```
pydantic_library/
├── specs/
│   └── your_overlay.yaml              # OutcomeSpec (questions + queries)
├── schemas/overlays/
│   └── your_overlay.yaml              # LinkML schema
├── generated/pydantic/overlays/
│   ├── your_overlay.py                # Generated Pydantic models
│   └── your_glue.py                   # Type registries + validation
└── tests/
    └── test_your_overlay.py           # Evidence Query Plan tests
```

## Validation

After creating your overlay, validate it:

```bash
cd pydantic_library
pytest tests/test_your_overlay.py -v
```

All tests must pass before the overlay is considered complete.

## Tips

### 1. Keep Overlays Small
- Max 5-8 entities per overlay
- Focus on answering specific business questions
- Don't try to model entire domains

### 2. Use Canonical Ontology URIs
- DoCO (Documents): http://purl.org/spar/doco/
- FaBiO (Bibliography): http://purl.org/spar/fabio/
- PROV-O (Provenance): http://www.w3.org/ns/prov#
- FIBO (Finance): https://spec.edmcouncil.org/fibo/ontology/
- SKOS (Concepts): http://www.w3.org/2004/02/skos/core#

### 3. Write Tests First
- Start with OutcomeSpec validation queries
- Write tests that validate your queries work
- Generate schema to pass the tests

### 4. Use Provenance Mixins
- Always include `ProvenanceFields` mixin for entities
- Always include `EdgeProvenanceFields` mixin for edges
- This enables full provenance tracking in Graphiti

## Next Steps

1. **Read examples** in `examples/` directory
2. **Copy a template** from `templates/`
3. **Run the pipeline** with `add_overlay.py`
4. **Test your overlay** with pytest
5. **Update documentation** (MIGRATION_GUIDE.md)

## Troubleshooting

### gen-pydantic fails
- Check LinkML schema syntax with `linkml lint schemas/overlays/your_overlay.yaml`
- Verify imports are correct (must import `../core/provenance`)

### Tests fail
- Verify all fields from validation queries exist in models
- Check that edge types are defined in glue code
- Ensure ProvenanceFields mixins are included

### Import errors
- Make sure to run from correct directory
- Check that `__init__.py` files exist in all Python packages
- Verify PYTHONPATH includes `pydantic_library/`

## See Also

- `../pydantic_library/MIGRATION_GUIDE.md` - Complete 8-step workflow
- `../pydantic_library/README.md` - Library architecture
- `../docs/GRAPHITI_INTEGRATION.md` - How to use with Graphiti
- `../docs/ONTOLOGY_MAPPING.md` - Canonical URI reference
