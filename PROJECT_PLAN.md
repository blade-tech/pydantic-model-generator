# Outcome-First Pydantic Model Generator - Project Plan

## Executive Summary

**Mission:** Build a repeatable pipeline that converts business outcomes into minimal, evaluated Pydantic models through LinkML, with built-in quality gates ensuring models actually support retrieval and answer generation.

**North Star:** *Schema as search intent* - Only accept schemas whose metadata fields demonstrably enable evidence retrieval for stated business outcomes.

## Core Architecture

```
OutcomeSpec (DSL)
    ↓ (LLM + Instructor guards)
LinkML Overlay (minimal)
    ↓ (lint → compile)
Pydantic Models (codegen)
    ↓
Graphiti Ingestion (+ metadata stamping)
    ↓
Retrieval + Extractive Eval (zero unsupported tokens)
    ↓
Pass/Fail Report (DoD gates)
```

## Definition of Done (DoD)

A schema overlay is **accepted** only if:

✅ **Gate A - Build Hygiene:** `linkml lint` passes; Pydantic codegen succeeds; smoke import passes
✅ **Gate B - Evidence Retrieval Fitness:** Evidence Recall@8 ≥ 0.9 on GoldenSet
✅ **Gate C - Extractive Answer Gate:** GAR ≥ 0.9, Coverage ≥ 0.98 (quotes only)
✅ **Gate D - Metadata Utility:** MDI > 0 (each metadata family measurably helps via ablation)
✅ **Gate E - Structure & Provenance:** 0 violations on deterministic edges and entity_type stamping
✅ **Gate F - Performance:** P95 Time-to-Evidence < 800ms (mock acceptable for v1)

**Fail closed:** If any gate fails, reject overlay with concrete improvement suggestions.

## Milestones & Timeline

### Phase 1: Foundation (Days 1-2)
- **M1.1:** Repo scaffold with proper structure ✓
- **M1.2:** Python environment (pyproject.toml, dependencies) ✓
- **M1.3:** Core LinkML schemas (core.yaml with NodeProv/EdgeProv mixins) ✓
- **M1.4:** OutcomeSpec DSL schema and validator ✓
- **M1.5:** Example OutcomeSpecs for both use cases ✓

### Phase 2: Schema Pipeline (Days 2-3)
- **M2.1:** Ontology retriever (Exa/Firecrawl + offline fallback) ✓
- **M2.2:** Schema synthesizer (Instructor-guarded LLM → LinkML JSON/YAML) ✓
- **M2.3:** Codegen orchestrator (lint + LinkML → Pydantic + smoke test) ✓
- **M2.4:** Generated models for Resource Allocation & AAOIFI outcomes ✓

### Phase 3: Graph Integration (Days 3-4)
- **M3.1:** Graphiti adapter with mock fallback ✓
- **M3.2:** Type registries (ENTITY_TYPES, EDGE_TYPES, EDGE_TYPE_MAP) ✓
- **M3.3:** Ingestion helpers (entity_type stamping, edge URI mapping) ✓
- **M3.4:** Fixture ingestion (Slack + AAOIFI samples) ✓

### Phase 4: Evaluation Loop (Days 4-5)
- **M4.1:** GoldenSets for both outcomes ✓
- **M4.2:** Retrieval facade (metadata filters + keyword + ablation toggles) ✓
- **M4.3:** Extractive gate (zero unsupported tokens, coverage checks) ✓
- **M4.4:** Evaluation runner (Recall@K, GAR, Coverage, MDI metrics) ✓
- **M4.5:** Report generation (Markdown + JSON) ✓

### Phase 5: Integration & Demo (Day 5)
- **M5.1:** CLI with all commands (Typer-based) ✓
- **M5.2:** Makefile targets ✓
- **M5.3:** Test suite (pytest: codegen, ingest, eval) ✓
- **M5.4:** End-to-end demo run ✓
- **M5.5:** Documentation (README, GLOSSARY, TOOLS) ✓

## Technical Stack

### Core Pipeline
- **Python 3.12** (current environment)
- **LinkML** - Schema language + Pydantic generator
- **Instructor** - Structured LLM output validation
- **Pydantic v2** - Type models and validation

### Graph & Storage
- **Graphiti** - Neo4j-backed graph with hybrid search (mock fallback available)
- **Neo4j** - Optional; can run fully mocked

### APIs & Tools
- **Exa** - Ontology search (optional, offline fallback)
- **Firecrawl** - Web scraping (optional, offline fallback)
- **OpenAI/Anthropic** - LLM providers (configurable)

### DevX
- **Typer + Rich** - CLI with nice output
- **pytest** - Testing
- **Poetry/uv** - Dependency management

## Repository Structure

```
outcome-first/
├── README.md                          # Main documentation
├── PROJECT_PLAN.md                    # This file
├── GLOSSARY.md                        # Acronym reference
├── TOOLS.md                           # Tool usage guide
├── pyproject.toml                     # Dependencies
├── Makefile                           # Common tasks
├── .env.example                       # Environment template
│
├── dsl/                               # Outcome specification DSL
│   ├── outcome_spec_schema.py         # Pydantic schema for OutcomeSpec
│   └── examples/
│       ├── resource_allocation.yaml   # Business use case
│       └── aaoifi_qa.yaml            # Standards use case
│
├── schemas/                           # LinkML schemas
│   ├── core.yaml                      # Core mixins (NodeProv, EdgeProv)
│   └── overlays/                      # Generated per-outcome overlays
│
├── generated/                         # Generated code (DO NOT EDIT)
│   └── pydantic/                      # LinkML → Pydantic models
│
├── agents/                            # Pipeline subagents
│   ├── ontology_retriever.py          # Fetch ontology snippets
│   ├── schema_synthesizer.py          # LLM → LinkML (Instructor-guarded)
│   ├── codegen_orchestrator.py        # Lint + codegen + validation
│   ├── graphiti_adapter.py            # Graph registries & ingestion
│   ├── retriever.py                   # Hybrid retrieval facade
│   └── eval_gate.py                   # Extractive answer validation
│
├── graphiti/                          # Graph layer
│   ├── registries.py                  # Type registries from generated models
│   ├── ingestion.py                   # Ingestion helpers
│   └── constraints.cypher             # Neo4j constraints (optional)
│
├── eval/                              # Evaluation framework
│   ├── goldenset_resource_allocation.yaml
│   ├── goldenset_aaoifi.yaml
│   └── runner.py                      # Eval orchestrator
│
├── fixtures/                          # Sample data
│   ├── slack/
│   │   └── channel-alloc-planning.json
│   └── aaoifi/
│       └── ss-59-en.json
│
├── reports/                           # Evaluation outputs
│   ├── eval_*.json
│   └── eval_*.md
│
├── tests/                             # Test suite
│   ├── test_codegen.py
│   ├── test_ingest.py
│   └── test_eval_gate.py
│
└── main.py                            # CLI entrypoint
```

## Risk Assessment & Mitigation

### High-Risk Items

1. **LLM Schema Generation Quality**
   - Risk: LLM produces invalid or oversized LinkML schemas
   - Mitigation: Hard Instructor validation, class/association caps (≤12/≤10), comprehensive linting
   - Rollback: Use handcrafted schemas if LLM quality poor

2. **Graphiti Integration Complexity**
   - Risk: Graphiti has breaking changes or unexpected behavior
   - Mitigation: Mock adapter with same interface, can run fully offline
   - Rollback: Continue with mock, integrate real Graphiti later

3. **Evaluation Gate Tuning**
   - Risk: Thresholds too strict (nothing passes) or too loose (poor quality accepted)
   - Mitigation: Start with provided fixtures that should pass; tune thresholds empirically
   - Rollback: Make thresholds configurable via env vars

### Medium-Risk Items

4. **External API Dependencies**
   - Risk: Exa/Firecrawl rate limits or downtime
   - Mitigation: Offline fixtures as fallback, cache ontology responses
   - Rollback: Run fully offline mode

5. **LinkML Toolchain Issues**
   - Risk: LinkML version incompatibilities or bugs
   - Mitigation: Pin versions tightly, extensive testing
   - Rollback: Direct Pydantic code generation as escape hatch

6. **Performance at Scale**
   - Risk: Evaluation too slow on larger datasets
   - Mitigation: Start with tiny fixtures (10-20 questions), optimize later
   - Rollback: Sample evaluation instead of exhaustive

### Low-Risk Items

7. **Neo4j Setup Complexity**
   - Risk: Local Neo4j difficult to configure
   - Mitigation: Docker compose file + clear docs, mock works without it
   - Rollback: Pure mock mode

8. **CLI UX Issues**
   - Risk: Commands confusing or hard to use
   - Mitigation: Rich output, clear help text, sensible defaults
   - Rollback: Simple shell scripts as alternative

## Success Criteria

### Technical Success
- ✅ End-to-end pipeline runs: OutcomeSpec → Pydantic → Ingestion → Eval → Report
- ✅ All DoD gates pass for both demo outcomes (Resource Allocation + AAOIFI)
- ✅ Zero-dependency fallback mode works (offline, mocked)
- ✅ Test suite covers critical paths and passes
- ✅ Pipeline completes in <5 minutes on demo fixtures

### Quality Success
- ✅ Evidence Recall@8 ≥ 0.9 for both GoldenSets
- ✅ Grounded Answer Rate ≥ 0.9 (extractive only, no hallucination)
- ✅ MDI > 0 (metadata demonstrably improves retrieval)
- ✅ Generated schemas are minimal (≤12 classes, ≤10 edges)

### Usability Success
- ✅ Single command demo: `make run-demo`
- ✅ Clear, actionable error messages on failure
- ✅ Documentation enables new developer to run pipeline in <30 min
- ✅ Eval reports are executive-readable (one-page Markdown)

## Constraints & Guardrails

### Hard Constraints
- **Extractive answers only** - No paraphrasing until GAR consistently high
- **Schema size limits** - ≤12 classes, ≤10 associations per overlay
- **Provenance required** - All nodes must have entity_type; edges need URIs when known
- **Group discipline** - Wrong group/edition = automatic failure
- **Fail closed** - Reject schema if any DoD gate fails

### Architectural Principles
- **Configuration over code** - Prefer YAML/env vars to hardcoding
- **Mock-friendly** - Can run without network or external services
- **Outcome-first** - Only model what's needed for stated questions
- **Evidence-driven** - Schemas judged by retrieval effectiveness, not completeness

## Rollback Plan

If at any point the pipeline becomes unworkable:

1. **Immediate Rollback** - Revert to last working commit
2. **Component Isolation** - Disable problematic component (e.g., switch to mock)
3. **Simplification** - Remove optional features (Langfuse, real Neo4j, etc.)
4. **Handcrafted Fallback** - Use manually written Pydantic models for demo
5. **Re-planning** - Reassess scope with user, potentially phase features

**Rollback Triggers:**
- Any component blocking progress >4 hours
- DoD gates impossible to meet with current approach
- External dependencies consistently unavailable
- Performance degradation beyond acceptable limits

## Next Steps

1. ✅ Review and approve this plan
2. → Create repository scaffold
3. → Set up Python environment
4. → Implement core pipeline components
5. → Build evaluation framework
6. → Run end-to-end demo
7. → Iterate based on DoD gate results

## Questions for User

Before proceeding, please confirm:

1. **LLM Provider Preference:** Anthropic (Claude) or OpenAI? (Default: Anthropic since you're using Claude Code)
2. **Network Access:** Should we attempt Exa/Firecrawl calls or start purely offline? (Recommend: offline first)
3. **Neo4j:** Do you want to run real Neo4j or just use mocks? (Recommend: mock for v1)
4. **Langfuse:** Enable observability from start or add later? (Recommend: later)
5. **CI Platform:** GitHub Actions or local scripts? (Can use GitHub MCP if desired)

---

**Status:** Planning complete, awaiting approval to proceed with implementation.
