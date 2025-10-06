# Outcome-First Pydantic Model Generator

---
**🎓 TEACHING ARTIFACT - STUDY THE PATTERN, BUILD YOUR OWN**

👉 **New here? Start with**: [`START_HERE.md`](START_HERE.md) (30 minutes)
👉 **Understand how**: [`TECH_STACK.md`](TECH_STACK.md) (1 hour)
👉 **Build your version**: [`BUILD_YOUR_OWN.md`](BUILD_YOUR_OWN.md) (1 hour)

**Goal**: Learn outcome-first modeling → Build your own implementation with your stack
---

**Schema as Search Intent** — A pipeline that converts business outcomes into minimal, evaluated Pydantic models through LinkML, with built-in quality gates ensuring models actually support retrieval and answer generation.

## 🎯 Mission

Build a repeatable pipeline that:
1. Takes a business **OutcomeSpec** (YAML) describing what questions need answering
2. Uses an LLM (Instructor-guarded) to generate a minimal **LinkML schema** overlay
3. Compiles to **Pydantic models** with full provenance tracking
4. Ingests data into **Graphiti** (Neo4j-backed graph) with metadata stamping
5. **Evaluates** the schema by testing retrieval effectiveness
6. Only accepts schemas that pass all **Definition of Done (DoD) gates**

## 🏗️ Architecture

```
OutcomeSpec (DSL)
    ↓ (LLM + Instructor guards)
LinkML Overlay (minimal, imports core.yaml)
    ↓ (linkml generate pydantic)
Pydantic Models (with provenance mixins)
    ↓ (registries + ingestion)
Graphiti Graph (entity_type metadata stamped)
    ↓ (hybrid retrieval + extractive gate)
Evaluation Report (DoD: Recall@K, GAR, Coverage, MDI)
```

## ✅ Definition of Done (DoD)

A schema overlay is **accepted** only if ALL gates pass:

| Gate | Metric | Threshold | What It Validates |
|------|--------|-----------|-------------------|
| **A - Build Hygiene** | Lint + Codegen | Pass | LinkML valid, Pydantic compiles, imports work |
| **B - Evidence Retrieval** | Recall@8 | ≥ 0.9 | Schema metadata enables finding evidence for 90%+ questions |
| **C - Extractive Answers** | GAR, Coverage | ≥ 0.9, ≥ 0.98 | Answers are quotes-only, no hallucination |
| **D - Metadata Utility** | MDI | > 0 | Each metadata family measurably improves retrieval (ablation test) |
| **E - Structure & Provenance** | Violations | 0 | Deterministic edges exist, entity_type stamped |
| **F - Performance** | P95 Time-to-Evidence | < 800ms | Retrieval is fast enough (mock OK for v1) |

**Fail closed:** If any gate fails, reject the overlay with concrete suggestions.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- (Optional) Neo4j for real Graphiti; works with mocks otherwise
- (Optional) API keys for Exa/Firecrawl; works offline otherwise

### Installation

```bash
# Clone and setup
cd "Pydantic Model Generator"

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys (or leave blank for offline mode)

# Test installation
python -m dsl.loader dsl/examples/resource_allocation.yaml
```

### Run Demo

```bash
# Full pipeline (when implemented)
make run-demo SPEC=dsl/examples/resource_allocation.yaml

# Individual steps
make search-ontologies SPEC=...
make synthesize-schema SPEC=...
make codegen OVERLAY=schemas/overlays/overlay.yaml
make ingest-demo
make eval GOLDEN=eval/goldenset_resource_allocation.yaml
```

## 📁 Repository Structure

```
outcome-first/
├── PROJECT_PLAN.md              # Detailed project plan
├── GLOSSARY.md                  # Acronym reference
├── TOOLS.md                     # Tool usage guide
├── pyproject.toml               # Dependencies
├── requirements.txt             # Pip fallback
├── Makefile                     # Command shortcuts
│
├── dsl/                         # OutcomeSpec DSL
│   ├── outcome_spec_schema.py   # Pydantic schema
│   ├── loader.py                # YAML loader + validation
│   └── examples/
│       ├── resource_allocation.yaml
│       └── aaoifi_qa.yaml
│
├── schemas/                     # LinkML schemas
│   ├── core.yaml                # Core mixins (NodeProv, EdgeProv, entity_type)
│   └── overlays/                # Generated per-outcome (gitignored)
│
├── generated/pydantic/          # LinkML → Pydantic models (gitignored)
│
├── agents/                      # Pipeline subagents
│   ├── ontology_retriever.py   # Exa/Firecrawl + offline fallback
│   ├── schema_synthesizer.py   # Instructor → LinkML
│   ├── codegen_orchestrator.py # Lint + codegen
│   ├── graphiti_adapter.py     # Graph integration
│   ├── retriever.py            # Hybrid retrieval
│   └── eval_gate.py            # Extractive validation
│
├── graphiti/                    # Graph layer
│   ├── registries.py           # ENTITY_TYPES, EDGE_TYPES, EDGE_TYPE_MAP
│   ├── ingestion.py            # Ingestion helpers
│   └── constraints.cypher      # Neo4j constraints
│
├── eval/                        # Evaluation
│   ├── goldenset_*.yaml        # Test questions + expected evidence
│   └── runner.py               # Eval orchestrator
│
├── fixtures/                    # Sample data
│   ├── slack/channel-alloc-planning.json
│   └── aaoifi/ss-59-en.json
│
├── reports/                     # Eval outputs (gitignored)
├── tests/                       # Test suite
└── main.py                      # CLI entrypoint
```

## 🔧 Core Components

### OutcomeSpec DSL

Define what you need in YAML:

```yaml
outcome_name: "Client Brief: Resource Allocation"
context_summary: "Shows allocations given capacity, budgets, priorities"

required_evidence:
  - name: TeamCapacity
    must_have_slots: [team_id, period, capacity_hours]
  - name: BudgetConstraint
    must_have_slots: [project_id, currency, amount]

queries_we_must_answer:
  - "Which allocations exceed team capacity?"
  - "Pending decisions blocking reallocation?"

target_entities:
  - name: Allocation
    must_have_slots: [team_id, project_id, period, hours]

relations:
  - {name: BasedOn, subject: Allocation, object: TeamCapacity}
  - {name: ConstrainedBy, subject: Allocation, object: BudgetConstraint}

ontologies:
  - {prefix: dcterms, base_uri: "http://purl.org/dc/terms/"}

graphiti_constraints:
  use_entity_type_metadata: true
  edge_names_pascal_case: true
  stamp_uri_on_edges: true
```

### Core LinkML Schema (`schemas/core.yaml`)

Provides foundational mixins all overlays must import:

- **NodeProv**: node_id, uri, entity_type, provenance fields
- **EdgeProv**: rel_id, uri, derivation tracking
- **entity_type**: Metadata field for Graphiti label workaround

### Schema Synthesizer (Agent)

- Uses **Instructor** to constrain LLM outputs
- Generates LinkML JSON conforming to `LinkMLSchemaSpec`
- Enforces: ≤12 classes, ≤10 associations, PascalCase edges, imports core.yaml
- Outputs: `overlay.yaml` + `eqp.json` (Evidence Query Plan)

### Codegen Orchestrator (Agent)

```bash
linkml lint schemas/overlays/overlay.yaml
linkml generate pydantic schemas/overlays/overlay.yaml > generated/pydantic/models.py
python -c "import generated.pydantic.models"  # smoke test
```

### Graphiti Adapter

- Builds `ENTITY_TYPES`, `EDGE_TYPES`, `EDGE_TYPE_MAP` from generated Pydantic models
- Stamps `entity_type = ClassName` on all nodes (Graphiti metadata workaround)
- Sets `edge.uri` when association has `slot_uri` (e.g., `dcterms:subject`)
- Mock adapter available if Neo4j not configured

### Extractive Evaluation Gate

- **Zero unsupported tokens** — answers are quotes + tiny connectives
- Coverage ≥ 0.98 (98%+ of answer from graph)
- Wrong group/edition = automatic failure
- Refuse with top-K quotes if insufficient evidence

### Evaluation Runner

Computes all DoD metrics:

- **Recall@K**: % questions with correct evidence in top-K
- **K@Hit**: Average rank of first correct support
- **GAR**: Grounded Answer Rate (% passing extractive gate)
- **Coverage**: Quote proportion in answers
- **MDI**: Metadata Discriminability Index (ablation per metadata family)

Outputs: Markdown report + JSON artifact

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/test_codegen.py
pytest tests/test_ingest.py
pytest tests/test_eval_gate.py

# With coverage
pytest --cov=agents --cov=dsl --cov=graphiti --cov=eval
```

## 📊 Example Use Cases

### 1. Resource Allocation Brief (Business)
- **Input**: Slack messages about team capacity, budgets, project priorities
- **Output**: Answers like "Team Alpha allocated 480h to Daytona (520h capacity), budget $120K/$150K remaining"
- **GoldenSet**: `eval/goldenset_resource_allocation.yaml`

### 2. AAOIFI Standards QA (Compliance)
- **Input**: Shari'ah standard documents (SS-59 Gold)
- **Output**: Answers like "Murabaha requires disclosing cost and profit (SS-59, P045)"
- **GoldenSet**: `eval/goldenset_aaoifi.yaml`

## 🔒 Guardrails

### Hard Constraints
- **Extractive only**: No paraphrasing until GAR consistently high
- **Size limits**: ≤12 classes, ≤10 associations per overlay
- **Provenance required**: All nodes have entity_type; edges have URIs when known
- **Group discipline**: Wrong group/edition = failure
- **Fail closed**: Reject schema if any DoD gate fails

### Architectural Principles
- **Configuration > code**: Prefer YAML/env vars
- **Mock-friendly**: Can run without network
- **Outcome-first**: Only model what's needed for stated questions
- **Evidence-driven**: Schemas judged by retrieval effectiveness

## 🔌 Optional Integrations

### Exa (Ontology Search)
```bash
EXA_API_KEY=your_key
# Fetches canonical IRIs/definitions for ontology classes
```

### Firecrawl (Web Scraping)
```bash
FIRECRAWL_API_KEY=your_key
# Scrapes official ontology documentation pages
```

### Langfuse (Observability)
```bash
USE_LANGFUSE=true
LANGFUSE_HOST=https://cloud.langfuse.com
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_SECRET_KEY=...
# Traces: synthesize_schema, codegen, retrieve, quote_select
```

### Neo4j (Real Graph)
```bash
USE_MOCK_GRAPHITI=false
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS=password
```

## 🎬 Demo Storyline

1. **Define Outcome**: Create `OutcomeSpec` YAML with questions and evidence
2. **Synthesize Schema**: LLM (Instructor-guarded) generates LinkML overlay
3. **Generate Models**: LinkML compiles to Pydantic with provenance
4. **Ingest Fixtures**: Slack messages + AAOIFI paragraphs → Graphiti
5. **Evaluate**: Run retrieval on GoldenSet questions
6. **Report**: Markdown summary shows Recall@8, GAR, Coverage, MDI
7. **Answer Questions**: Extractive answers with citations, or refusal with quotes

Example output:
```
Evidence Recall@8: 0.95 ✓
Grounded Answer Rate: 0.93 ✓
Coverage: 0.99 ✓
MDI: 0.18 ✓ (removing entity_type dropped Recall by 18%)
Violations: 0 ✓
P95 Latency: 650ms ✓

DoD Status: PASS
```

## 📚 Documentation

- **[PROJECT_PLAN.md](PROJECT_PLAN.md)** - Milestones, risks, rollback plan
- **[GLOSSARY.md](GLOSSARY.md)** - All acronyms explained
- **[TOOLS.md](TOOLS.md)** - Tool-by-tool usage guide
- **[OutcomeSpec Examples](dsl/examples/)** - Reference YAML files
- **[GoldenSets](eval/)** - Evaluation test cases

## 🤝 Contributing

This is an MVP. Core principles:

1. **Outcome-first**: Don't add features that don't serve stated outcomes
2. **Evidence-driven**: Every schema must pass DoD gates
3. **Mock-friendly**: Keep the loop runnable without external dependencies
4. **Clear failures**: Better to fail with actionable errors than succeed with poor quality

## 📝 License

[Your License Here]

## 🆘 Troubleshooting

### Schema synthesis produces oversized overlays
- Check class/association caps in `schema_synthesizer.py`
- Simplify OutcomeSpec (fewer entities, tighter queries)

### Recall@K failing
- Review GoldenSet expected_support IDs match ingested data
- Check metadata fields are properly stamped during ingestion
- Run ablation to see which metadata families aren't helping

### Import errors on generated models
- Run `linkml lint` on overlay before codegen
- Check core.yaml is properly imported
- Verify Python 3.11+ and pydantic>=2.6

### Extractive gate rejecting valid answers
- Check Coverage threshold (0.98 may be too strict for some cases)
- Verify group_id matches between answer and evidence
- Review quote span extraction logic

## 🔗 Related Projects

- **LinkML**: https://linkml.io
- **Instructor**: https://python.useinstructor.com
- **Graphiti**: https://github.com/getzep/graphiti
- **Model Context Protocol**: https://modelcontextprotocol.io

---

**Status**: Foundation complete. Implementing pipeline agents next.

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for detailed roadmap.
