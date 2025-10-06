# Acronym Glossary

Quick reference for all acronyms used in this project.

## Core to the Spec

- **DSL** — Domain-Specific Language (small, purpose-built syntax for describing outcomes)
- **LLM** — Large Language Model
- **MCP** — Model Context Protocol (standard for connecting tools/data to AI agents)
- **LinkML** — Linked Data Modeling Language (YAML schema language generating Pydantic, SHACL, OWL, etc.)
- **Pydantic** — Python data-modeling/validation library (using v2)
- **Graphiti** — Graph+AI framework (Neo4j-backed) for episodes, hybrid search, extraction
- **RAG** — Retrieval-Augmented Generation (LLM answers grounded in retrieved context)

## Web/Semantics & Standards

- **OWL** — Web Ontology Language
- **RDF** — Resource Description Framework (triples)
- **IRI/URI** — Internationalized/Uniform Resource Identifier (global identifiers for concepts/relations)
- **DoCO** — Document Components Ontology (Document/Section/Paragraph)
- **PROV** — W3C Provenance Ontology
- **SKOS** — Simple Knowledge Organization System (Concepts/labels)
- **FIBO** — Financial Industry Business Ontology
- **SHACL** — Shapes Constraint Language (validates RDF graphs)
- **DCTERMS** — Dublin Core Terms (e.g., `dcterms:subject`)

## Tooling & Libraries

- **Instructor** — Library forcing LLM outputs to conform to Pydantic schema
- **Exa** — Search/website content extraction API
- **Firecrawl** — Web crawler/scraper/search API
- **Neo4j** — Graph database used underneath Graphiti
- **LlamaParse** — Parser extracting structured text from PDFs/Docs
- **LlamaIndex** — RAG toolkit (splitters, ingestion pipelines)
- **Pinecone** — Managed vector database (not required for in-graph approach)

## Retrieval/Ranking

- **BM25** — Classic keyword relevance scoring
- **HNSW** — Hierarchical Navigable Small World (fast vector index)
- **RRF** — Reciprocal Rank Fusion (combines multiple ranked lists)
- **MMR** — Maximal Marginal Relevance (diversifies results)
- **HyDE** — Hypothetical Document Embeddings (query expansion technique)
- **Cross-encoder (reranker)** — Model scoring (query, passage) pairs for precise ranking
- **Hybrid search** — Combine sparse (BM25) + dense (embeddings) retrieval

## Evaluation & Guardrails

- **RAGAS** — RAG evaluation library (faithfulness, context recall/precision)
- **Langfuse** — Tracing/experimentation/observability for LLM pipelines
- **TruLens** — Eval toolkit (groundedness, relevance checks)
- **Promptfoo** — Testing/red-teaming for prompts & LLM workflows
- **Giskard** — ML/LLM testing and safety framework
- **GAR** — Grounded Answer Rate (share of answers passing grounding checks)
- **MDI** — Metadata Discriminability Index (ablation metric for metadata utility)

## DevOps & Project

- **CI** — Continuous Integration (automated lint/tests/builds)
- **CLI** — Command-Line Interface
- **ETL** — Extract, Transform, Load (data pipeline)
- **YAML / JSON** — Human-readable data serializations
- **DoD** — Definition of Done (acceptance criteria)

## Domain-Specific

- **AAOIFI** — Accounting and Auditing Organization for Islamic Financial Institutions (Shari'ah standards body)
- **SS** — Shari'ah Standard (e.g., SS-59)

## Key Metrics (This Project)

- **Recall@K** — Percentage of questions with correct evidence in top-K results
- **K@Hit** — Average rank of first correct supporting paragraph
- **GAR** — Grounded Answer Rate (% answers passing extractive gate)
- **Coverage** — Proportion of answer tokens from graph quotes (target ≥0.98)
- **MDI** — Metadata Discriminability Index (min relative uplift from any metadata family)

## Pipeline Components

- **OutcomeSpec** — YAML/JSON specification of desired business outcome
- **EQP** — Evidence Query Plan (how to retrieve evidence for outcome questions)
- **NodeProv** — LinkML mixin for node provenance metadata
- **EdgeProv** — LinkML mixin for edge provenance metadata
- **entity_type** — Metadata field preserving business classification in Graphiti
