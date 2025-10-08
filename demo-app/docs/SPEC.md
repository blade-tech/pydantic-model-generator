# Demo App Specification: Pydantic Library Generator

**Version:** 1.0
**Date:** 2025-10-07
**Status:** In Development

---

## 🎯 Project Overview

### Purpose
Real working mini-application that demonstrates the complete AI-powered transformation pipeline from business requirements to production-ready Pydantic models with knowledge graph integration.

### Key Objectives
1. Show live AI reasoning and ontology research (Claude + Instructor)
2. Generate real OutcomeSpecs, LinkML schemas, and Pydantic models
3. Write files to actual pydantic_library/ directory
4. Execute real tests with pytest
5. Ingest data to Graphiti/Neo4j knowledge graph
6. Provide human-in-the-loop approval at each step

### What This Is NOT
- ❌ Not a mockup with hardcoded responses
- ❌ Not using placeholder data
- ❌ Not simulating API calls
- ✅ Real API keys, real LLM calls, real file operations

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                   Next.js Frontend (Port 3000)              │
│  - React 18 + TypeScript                                   │
│  - shadcn/ui components + Tailwind CSS                     │
│  - Server-sent events for streaming                        │
│  - Form validation and state management                    │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/SSE
                       ↓
┌─────────────────────────────────────────────────────────────┐
│              Python FastAPI Backend (Port 8000)             │
│  - FastAPI with async support                              │
│  - Real service integrations                               │
│  - File system operations                                  │
│  - Subprocess management (gen-pydantic, pytest)            │
└──────────────────────┬──────────────────────────────────────┘
                       │
      ┌────────────────┼────────────────┐
      ↓                ↓                ↓
┌──────────┐  ┌─────────────┐  ┌──────────────┐
│ Claude   │  │  Graphiti   │  │   Neo4j      │
│ (Anthro) │  │  (OpenAI)   │  │  localhost   │
│ Real API │  │  Real API   │  │  :7687       │
└──────────┘  └─────────────┘  └──────────────┘
                       │
                       ↓
         ┌─────────────────────────┐
         │  pydantic_library/      │
         │  - Real file writes     │
         │  - Real test execution  │
         └─────────────────────────┘
```

---

## 📋 Functional Requirements

### FR-1: Business Text Input
- **ID:** FR-1
- **Priority:** P0 (Critical)
- **Description:** User provides business requirements as free-form text
- **Acceptance Criteria:**
  - Text area supports multi-line input (min 500 chars)
  - Load sample data from `public/sample-data/*.txt`
  - Upload `.md` or `.txt` files
  - Input validation: minimum 50 characters
- **Dependencies:** None

### FR-2: AI Ontology Research
- **ID:** FR-2
- **Priority:** P0 (Critical)
- **Description:** Claude analyzes text and researches canonical ontologies
- **Acceptance Criteria:**
  - Real Anthropic API call with streaming
  - Identify 2-8 entities from business text
  - Map entities to DoCO, FaBiO, PROV-O, FIBO, or SKOS ontologies
  - Display confidence scores (0.0-1.0) for each mapping
  - Stream thinking process to UI in real-time
- **Dependencies:** FR-1
- **API Requirements:**
  - Anthropic SDK with streaming
  - Model: `claude-3-5-sonnet-20241022`
  - Max tokens: 4096

### FR-3: Structured Output via Instructor
- **ID:** FR-3
- **Priority:** P0 (Critical)
- **Description:** Generate structured `OntologyAnalysis` and `OutcomeSpec` objects
- **Acceptance Criteria:**
  - Real Instructor integration with Anthropic
  - Pydantic models: `OntologyAnalysis`, `OutcomeSpec`
  - Type-safe structured output
  - Validation errors displayed to user
- **Dependencies:** FR-2
- **Data Models:**
  - `EntityMapping`: name, description, canonical_uri, confidence, reasoning
  - `RelationshipMapping`: name, source, target, canonical_uri, confidence
  - `OutcomeQuestion`: question, target_entities, reasoning
  - `ValidationQuery`: name, cypher, description

### FR-4: OutcomeSpec YAML Generation
- **ID:** FR-4
- **Priority:** P0 (Critical)
- **Description:** Convert structured output to YAML OutcomeSpec
- **Acceptance Criteria:**
  - Valid YAML syntax
  - Editable in-app YAML editor
  - Syntax highlighting
  - Real-time validation
  - Write to `pydantic_library/specs/{overlay_name}.yaml`
- **Dependencies:** FR-3
- **File Location:** `../pydantic_library/specs/`

### FR-5: LinkML Schema Generation
- **ID:** FR-5
- **Priority:** P0 (Critical)
- **Description:** Generate LinkML schema from OutcomeSpec
- **Acceptance Criteria:**
  - Valid LinkML YAML with imports
  - Include canonical ontology URIs
  - Add `ProvenanceFields` mixin to all entities
  - Write to `pydantic_library/schemas/overlays/{overlay_name}_overlay.yaml`
  - Display schema in code viewer
- **Dependencies:** FR-4
- **Schema Requirements:**
  - Import: `../core/provenance`
  - Prefixes: linkml, doco, fabio, prov, fibo, skos
  - Classes with class_uri, mixins, slots

### FR-6: Pydantic Model Generation
- **ID:** FR-6
- **Priority:** P0 (Critical)
- **Description:** Run gen-pydantic to create Pydantic V2 models
- **Acceptance Criteria:**
  - Real subprocess call: `gen-pydantic schema.yaml`
  - Write to `pydantic_library/generated/pydantic/overlays/{overlay_name}_models.py`
  - Display generated Python code with syntax highlighting
  - Handle gen-pydantic errors gracefully
- **Dependencies:** FR-5
- **Subprocess:** `gen-pydantic {schema_path}`

### FR-7: Test Generation & Execution
- **ID:** FR-7
- **Priority:** P1 (High)
- **Description:** Generate test file and run pytest
- **Acceptance Criteria:**
  - Generate test file from OutcomeSpec validation_queries
  - Write to `pydantic_library/tests/test_{overlay_name}.py`
  - Real subprocess call: `pytest test_file.py -v`
  - Display test results (pass/fail/error)
  - Show stdout/stderr
- **Dependencies:** FR-6
- **Subprocess:** `pytest {test_file} -v --tb=short`

### FR-8: Graphiti Ingestion
- **ID:** FR-8
- **Priority:** P1 (High)
- **Description:** Ingest sample data to Graphiti/Neo4j
- **Acceptance Criteria:**
  - Real Graphiti initialization with credentials
  - Load sample data (user-provided or from files)
  - Call `graphiti.add_episode()` with real OpenAI API
  - Create nodes in Neo4j
  - Display ingestion stats (nodes, edges created)
  - Provide "Open Neo4j Browser" button
- **Dependencies:** FR-6
- **External Dependencies:**
  - Graphiti Core >= 0.3.0
  - OpenAI API for entity extraction
  - Neo4j running on localhost:7687

### FR-9: Library Coverage Dashboard
- **ID:** FR-9
- **Priority:** P2 (Medium)
- **Description:** Display current pydantic_library statistics
- **Acceptance Criteria:**
  - Scan `pydantic_library/schemas/overlays/` directory
  - Count total overlays, entities, edges
  - List ontology usage (DoCO, FaBiO, etc.)
  - Update in real-time after new overlay added
- **Dependencies:** None (read-only)
- **Update Frequency:** On page load + after Step 6

### FR-10: Human-in-the-Loop Approvals
- **ID:** FR-10
- **Priority:** P0 (Critical)
- **Description:** User must approve each step before proceeding
- **Acceptance Criteria:**
  - Clear "Approve" and "Edit" buttons at each step
  - Cannot proceed without approval
  - Edit mode allows modifications before approval
  - "Regenerate" option for Steps 2-4
- **Dependencies:** All FRs
- **Checkpoints:**
  - Step 2: Approve ontology mappings
  - Step 3: Approve OutcomeSpec YAML
  - Step 4: Approve LinkML schema
  - Step 5: Approve Pydantic models
  - Step 6: Review test results
  - Step 7: Confirm Graphiti ingestion

### FR-11: Claude Streaming Log Panel
- **ID:** FR-11
- **Priority:** P1 (High)
- **Description:** Display Claude's reasoning process in real-time
- **Acceptance Criteria:**
  - Server-sent events from backend
  - Auto-scroll to bottom
  - Timestamps for each log entry
  - Export log as `.txt` file
  - Clear log button
- **Dependencies:** FR-2
- **Display:** Right-side panel, always visible

---

## 🔧 Technical Requirements

### TR-1: Frontend Stack
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript 5.x
- **UI Library:** shadcn/ui (Radix UI primitives)
- **Styling:** Tailwind CSS 3.x
- **State Management:** React hooks + Context API
- **Code Editor:** react-syntax-highlighter or Monaco Editor
- **Dependencies:**
  ```json
  {
    "next": "^14.1.0",
    "@radix-ui/react-*": "latest",
    "tailwindcss": "^3.4.0",
    "react-syntax-highlighter": "^15.5.0",
    "yaml": "^2.3.4",
    "eventsource": "^2.0.2"
  }
  ```

### TR-2: Backend Stack
- **Framework:** FastAPI 0.110+
- **Language:** Python 3.11+
- **Async:** asyncio + async/await
- **API Docs:** Auto-generated (Swagger UI)
- **Dependencies:**
  ```txt
  anthropic>=0.25.0
  instructor>=1.3.0
  openai>=1.0.0
  graphiti-core>=0.3.0
  neo4j>=5.17.0
  linkml>=1.7.0
  pydantic>=2.6.0
  fastapi>=0.110.0
  uvicorn>=0.29.0
  sse-starlette>=2.0.0
  pyyaml>=6.0.0
  ```

### TR-3: External Services
- **Claude API:**
  - Provider: Anthropic
  - Model: `claude-3-5-sonnet-20241022`
  - Features: Streaming, 200K context window
  - Rate limits: Respect API limits

- **OpenAI API:**
  - Used by: Graphiti for entity extraction
  - Model: `gpt-4-turbo-preview` (Graphiti default)
  - Fallback: `gpt-3.5-turbo`

- **Neo4j:**
  - Version: 5.x
  - Protocol: Bolt (neo4j://)
  - Port: 7687
  - Authentication: Username + password
  - Database: Default database

### TR-4: File System Operations
- **Read Access:**
  - `pydantic_library/schemas/overlays/*.yaml`
  - `pydantic_library/specs/*.yaml`
  - `public/sample-data/*.txt`

- **Write Access:**
  - `pydantic_library/specs/{overlay_name}.yaml`
  - `pydantic_library/schemas/overlays/{overlay_name}_overlay.yaml`
  - `pydantic_library/generated/pydantic/overlays/{overlay_name}_models.py`
  - `pydantic_library/generated/pydantic/overlays/{overlay_name}_glue.py`
  - `pydantic_library/tests/test_{overlay_name}.py`

### TR-5: Environment Variables
```bash
# Required - User must provide
ANTHROPIC_API_KEY=sk-ant-api03-xxx
OPENAI_API_KEY=sk-xxx
NEO4J_URI=neo4j://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Optional - Defaults provided
PYDANTIC_LIBRARY_PATH=../pydantic_library
NEXT_PUBLIC_API_URL=http://localhost:8000
BACKEND_PORT=8000
FRONTEND_PORT=3000
```

### TR-6: Security Requirements
- Store API keys in `.env` file (not committed to git)
- `.env` in `.gitignore`
- Backend validates all file paths (no directory traversal)
- Rate limiting on API endpoints (10 req/min per IP)
- CORS configured for localhost only in dev

---

## 🎨 User Interface Requirements

### UI-1: Layout
- **Structure:** Two-column layout
  - Left: Main workflow (70% width)
  - Right: Claude log panel (30% width)
- **Navigation:** Step indicator (1/6, 2/6, etc.)
- **Responsive:** Desktop only (min-width: 1280px)

### UI-2: Components
1. **WorkflowStepper**
   - Visual progress indicator
   - Disable future steps
   - Allow back navigation

2. **ClaudeLogPanel**
   - Auto-scroll streaming logs
   - Timestamps
   - Export button
   - Clear button

3. **LibraryCoverageDashboard**
   - Top bar, always visible
   - Overlay cards with stats
   - Refresh button

4. **CodeViewer**
   - Syntax highlighting (Python, YAML)
   - Line numbers
   - Copy to clipboard button
   - Download button

5. **ApprovalControls**
   - Approve button (primary)
   - Edit button (secondary)
   - Regenerate button (tertiary)
   - Cancel button

### UI-3: Color Scheme
- **Primary:** Blue (#3b82f6)
- **Success:** Green (#10b981)
- **Warning:** Orange (#f59e0b)
- **Error:** Red (#ef4444)
- **Neutral:** Gray (#6b7280)

### UI-4: Typography
- **Headings:** Inter font family
- **Code:** JetBrains Mono
- **Body:** Inter

---

## 📊 Data Flow

### Workflow Sequence

```
┌─────────────────┐
│ 1. Input Text   │ User enters business requirements
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Research     │ Claude analyzes + researches ontologies
│    (Claude API) │ → OntologyAnalysis (Instructor)
└────────┬────────┘
         │ [Human Approval]
         ▼
┌─────────────────┐
│ 3. OutcomeSpec  │ Claude generates OutcomeSpec
│    (Instructor) │ → YAML file written
└────────┬────────┘
         │ [Human Approval]
         ▼
┌─────────────────┐
│ 4. LinkML       │ Generate LinkML schema
│    (YAML gen)   │ → schema_overlay.yaml written
└────────┬────────┘
         │ [Human Approval]
         ▼
┌─────────────────┐
│ 5. Pydantic     │ Run gen-pydantic subprocess
│    (gen-pydantic)│ → models.py written
└────────┬────────┘
         │ [Human Approval]
         ▼
┌─────────────────┐
│ 6. Tests        │ Generate + run pytest
│    (pytest)     │ → test results displayed
└────────┬────────┘
         │ [Human Approval]
         ▼
┌─────────────────┐
│ 7. Graphiti     │ Ingest to Neo4j via Graphiti
│    (OpenAI+Neo4j)│ → Nodes created
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Complete ✓      │ Open Neo4j Browser
└─────────────────┘
```

---

## 🧪 Testing Requirements

### Test Coverage
- **Backend Unit Tests:** 80% coverage minimum
  - Service layer tests
  - Mocked external API calls
  - File operation tests

- **Integration Tests:**
  - End-to-end pipeline test
  - Mock Claude/OpenAI responses
  - Real file writes to temp directory

- **Manual Testing:**
  - Real API calls with valid keys
  - Graphiti ingestion
  - Neo4j node verification

### Test Data
- Sample business requirements:
  - `public/sample-data/customer_support.txt`
  - `public/sample-data/business_outcomes.md`
  - `public/sample-data/inventory_tracking.txt`

---

## 📝 Documentation Requirements

### User Documentation
1. **README.md** - Setup instructions
2. **GETTING_STARTED.md** - Quick start guide
3. **API_KEYS.md** - How to get API keys
4. **TROUBLESHOOTING.md** - Common issues

### Developer Documentation
1. **ARCHITECTURE.md** - System design
2. **API.md** - Backend API reference
3. **CONTRIBUTING.md** - Development guidelines

---

## 🚀 Deployment Requirements

### Development
- **Frontend:** `npm run dev` (Port 3000)
- **Backend:** `uvicorn main:app --reload` (Port 8000)
- **Neo4j:** Docker or local install

### Production (Future)
- Frontend: Vercel deployment
- Backend: Docker container
- Neo4j: Neo4j AuraDB or self-hosted

---

## 🎯 Success Criteria

### Minimum Viable Product (MVP)
1. ✅ Complete 6-step workflow functional
2. ✅ Real Claude API integration with streaming
3. ✅ Real Instructor structured output
4. ✅ Real file writes to pydantic_library/
5. ✅ Real gen-pydantic execution
6. ✅ Real pytest execution
7. ✅ Real Graphiti ingestion
8. ✅ Human approval at each step
9. ✅ Claude log streaming visible
10. ✅ Library coverage dashboard

### Definition of Done
- All functional requirements implemented
- Manual end-to-end test passes
- README with setup instructions
- .env.example provided
- No hardcoded API keys
- Code commented
- Error handling in place

---

## 📅 Timeline

### Phase 1: Foundation (Day 1)
- Project setup
- Directory structure
- Backend skeleton (FastAPI)
- Frontend skeleton (Next.js)
- Environment configuration

### Phase 2: Core Services (Day 1-2)
- Claude service with streaming
- Instructor integration
- Ontology service
- LinkML service
- File system service

### Phase 3: Pipeline (Day 2)
- gen-pydantic integration
- pytest integration
- Graphiti service
- Neo4j connection

### Phase 4: UI (Day 2-3)
- Workflow components
- Log panel
- Code viewers
- Coverage dashboard

### Phase 5: Integration (Day 3)
- API routes
- SSE streaming
- Error handling
- End-to-end testing

---

## 🔒 Constraints & Assumptions

### Constraints
1. Desktop only (no mobile responsive)
2. Requires Neo4j running locally
3. Requires valid API keys
4. Internet connection required
5. Linux/Mac environment (Windows WSL acceptable)

### Assumptions
1. User has Neo4j installed and running
2. User has valid Anthropic and OpenAI API keys
3. User has Python 3.11+ and Node.js 18+ installed
4. User has basic understanding of Pydantic and Neo4j
5. `pydantic_library/` directory exists at `../pydantic_library/`

---

## 📚 References

- [Anthropic API Docs](https://docs.anthropic.com/)
- [Instructor Documentation](https://python.useinstructor.com/)
- [Graphiti Documentation](https://github.com/getzep/graphiti)
- [LinkML Documentation](https://linkml.io/)
- [Neo4j Documentation](https://neo4j.com/docs/)
- [shadcn/ui Documentation](https://ui.shadcn.com/)

---

**Document Version History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-07 | AI | Initial specification |

