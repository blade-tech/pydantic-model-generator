# 🎓 Learning Center: Pydantic Model Generator

**Welcome, Developer!** This Learning Center is your complete guide to understanding, extending, and productionizing the Pydantic Model Generator application.

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [The "Why" - Problem Statement](#the-why---problem-statement)
3. [The "What" - Solution Overview](#the-what---solution-overview)
4. [The "How" - Technical Architecture](#the-how---technical-architecture)
5. [Visual Walkthrough (with Screenshots)](#visual-walkthrough-with-screenshots)
6. [Deep Dive: Key Components](#deep-dive-key-components)
7. [Production Readiness Guide](#production-readiness-guide)
8. [Developer Onboarding](#developer-onboarding)
9. [Troubleshooting & FAQs](#troubleshooting--faqs)

---

## Executive Summary

**What is this?** An AI-powered pipeline that transforms business requirements into production-ready Pydantic V2 models with full provenance tracking and Neo4j compatibility.

**The Magic**: From plain English text to validated, tested, graph-ready Python models in 6 automated steps.

**Tech Stack**:
- **Frontend**: Next.js 14 (App Router), TypeScript, TailwindCSS, shadcn/ui
- **Backend**: FastAPI (Python 3.12), Anthropic Claude 4.5 Sonnet, OpenAI GPT-4
- **Pipeline**: LinkML → Pydantic V2 → Neo4j (via Graphiti)
- **Testing**: Pytest (auto-generated)
- **Infrastructure**: Neo4j Aura (graph database)

**Key Innovation**: Canonical ontology preservation throughout the pipeline using LinkML `class_uri` annotations, enabling semantic interoperability.

---

## The "Why" - Problem Statement

### 🎯 The Core Challenge

Traditional data modeling workflows are:
1. **Disconnected**: Business requirements → ER diagrams → Code → Database (lossy transformations)
2. **Manual**: Schema changes require updating multiple systems
3. **Semantically Opaque**: Lost connection to canonical ontologies (PROV-O, DOCO, Schema.org)
4. **Hard to Test**: Models often lack validation tests
5. **Graph-Incompatible**: SQL-first thinking doesn't map to Neo4j naturally

### 💡 The Vision

What if you could:
- Start with business text describing an outcome
- Automatically generate semantically-grounded models
- Preserve ontology URIs for interoperability
- Get validated tests for free
- Deploy directly to Neo4j knowledge graphs

**This app makes that vision real.**

---

## The "What" - Solution Overview

### 🚀 The 6-Step Pipeline

```
Business Text
    ↓
[Step 1] Entity Extraction (Graphiti + GPT-4)
    ↓
[Step 2] Ontology Mapping (Claude 4.5 + Semantic Web)
    ↓
[Step 3] OutcomeSpec Generation (YAML specification)
    ↓
[Step 4] LinkML Schema (Canonical ontology preservation)
    ↓
[Step 5] Pydantic V2 Models (Auto-generate pytest tests)
    ↓
[Step 6] Neo4j Deployment (via Graphiti client)
```

### 🎨 User Experience

**Interface**: Clean, step-by-step wizard with:
- Real-time streaming (see Claude "thinking")
- Editable outputs at each step
- Visual progress tracking
- Code syntax highlighting
- One-click copying

**Feedback Loop**: Edit any step's output → regenerate downstream artifacts

---

## The "How" - Technical Architecture

### 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐       │
│  │  Step Card │  │  Step Card │  │  Step Card │  ...  │
│  │   (1-6)    │  │   (1-6)    │  │   (1-6)    │       │
│  └────────────┘  └────────────┘  └────────────┘       │
│         │                │                │             │
│         └────────────────┴────────────────┘             │
│                          │                              │
└──────────────────────────┼──────────────────────────────┘
                           │ HTTP/SSE
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                       │
│                                                          │
│  ┌─────────────────────────────────────────────┐       │
│  │         Router Layer                         │       │
│  │  /entity-extraction  /generate-outcome-spec │       │
│  │  /generate-linkml    /generate-pydantic     │       │
│  │  /deploy-neo4j                              │       │
│  └─────────────────────────────────────────────┘       │
│                          │                              │
│  ┌─────────────────────────────────────────────┐       │
│  │         Service Layer                        │       │
│  │  - ClaudeService (Anthropic API)            │       │
│  │  - GraphitiService (OpenAI + Neo4j)         │       │
│  │  - SubprocessService (gen-pydantic)         │       │
│  │  - TestGenerator (pytest automation)        │       │
│  └─────────────────────────────────────────────┘       │
│                          │                              │
└──────────────────────────┼──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              External Services                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Anthropic   │  │    OpenAI    │  │  Neo4j Aura  │ │
│  │  Claude 4.5  │  │    GPT-4     │  │ (Knowledge   │ │
│  │   Sonnet     │  │              │  │   Graph)     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              Pydantic Library                            │
│  schemas/overlays/        → LinkML schemas              │
│  generated/pydantic/      → Generated models            │
│  tests/                   → Auto-generated pytest       │
└─────────────────────────────────────────────────────────┘
```

### 🔄 Data Flow

**Step 1: Entity Extraction**
```
User Input (text) → GraphitiService → OpenAI Embedding → Neo4j Temp Storage
                                    ↓
                            Entity/Relation Extraction (GPT-4)
                                    ↓
                            Return: EntityMapping[]
```

**Step 2: Ontology Mapping**
```
EntityMapping[] → ClaudeService (streaming)
                       ↓
        Semantic Web Research (Claude 4.5)
                       ↓
        Match to Canonical URIs (PROV-O, DOCO, etc.)
                       ↓
        Return: OntologyMapping[]
```

**Step 3-4: OutcomeSpec → LinkML**
```
Text + Entities → Claude (OutcomeSpec YAML)
                       ↓
   OutcomeSpec + Ontologies → Claude (LinkML YAML)
                       ↓
               Save to pydantic_library/schemas/overlays/
```

**Step 5: Pydantic Generation**
```
LinkML YAML → SubprocessService (gen-pydantic subprocess)
                       ↓
            Generated Pydantic V2 Models
                       ↓
   Save to pydantic_library/generated/pydantic/overlays/
                       ↓
            TestGenerator (automatic pytest generation)
                       ↓
      Save to pydantic_library/tests/
```

**Step 6: Neo4j Deployment**
```
Pydantic Models → GraphitiService
                       ↓
        Neo4j Client (entity creation)
                       ↓
          Graph Database (persisted nodes/edges)
```

---

## Visual Walkthrough (with Screenshots)

### 🖼️ Screenshot Guide Structure

Below is the planned structure for visual documentation. Screenshots will be captured using Playwright automation:

#### 1. **Landing Page & Workflow Overview**
   - Screenshot: `screenshots/01-landing-page.png`
   - **What**: Initial app state with 6-step cards
   - **Why**: Shows the complete pipeline at a glance
   - **How**: User sees progress through visual step indicators

#### 2. **Step 1: Entity Extraction**
   - Screenshot: `screenshots/02-step1-input.png`
   - **What**: Text input area + "Extract Entities" button
   - **Why**: User provides business requirements in plain English
   - **How**: Graphiti processes text → extracts entities

   - Screenshot: `screenshots/03-step1-output.png`
   - **What**: Table of extracted entities (name, type, description)
   - **Why**: Validates AI understood the domain
   - **How**: User can edit entities before proceeding

#### 3. **Step 2: Ontology Mapping**
   - Screenshot: `screenshots/04-step2-streaming.png`
   - **What**: Claude's thinking process (streaming text)
   - **Why**: Transparency in AI decision-making
   - **How**: Real-time Server-Sent Events (SSE)

   - Screenshot: `screenshots/05-step2-output.png`
   - **What**: Table of entities → canonical ontology URIs
   - **Why**: Semantic grounding (Schema.org, PROV-O, etc.)
   - **How**: Editable mappings for correction

#### 4. **Step 3: OutcomeSpec Generation**
   - Screenshot: `screenshots/06-step3-yaml.png`
   - **What**: Generated YAML with outcome questions
   - **Why**: Bridges business intent to technical schema
   - **How**: Editable YAML before LinkML generation

#### 5. **Step 4: LinkML Schema**
   - Screenshot: `screenshots/07-step4-linkml.png`
   - **What**: Full LinkML schema with class_uri annotations
   - **Why**: Schema includes canonical ontology references
   - **How**: This is what feeds into Pydantic generation

#### 6. **Step 5: Pydantic Models**
   - Screenshot: `screenshots/08-step5-pydantic.png`
   - **What**: Generated Python code with Pydantic V2 models
   - **Why**: Production-ready models with validation
   - **How**: Includes ProvenanceFields mixin, LinkMLMeta

   - Screenshot: `screenshots/09-step5-tests.png`
   - **What**: Auto-generated pytest test file
   - **Why**: Every model gets validation tests automatically
   - **How**: TestGenerator service creates comprehensive tests

#### 7. **Step 6: Neo4j Deployment**
   - Screenshot: `screenshots/10-step6-deploy.png`
   - **What**: Deployment status + Neo4j connection info
   - **Why**: Models are now in graph database
   - **How**: Graphiti client handles Cypher generation

#### 8. **Code Viewer Features**
   - Screenshot: `screenshots/11-code-viewer.png`
   - **What**: Syntax highlighting + copy button
   - **Why**: Developer-friendly output viewing
   - **How**: Monaco editor integration

---

## Deep Dive: Key Components

### 🧩 Component Breakdown

#### Frontend Components (`demo-app/frontend/`)

**1. `app/page.tsx` - Main Orchestrator**
```typescript
// Manages workflow state across all 6 steps
const [step1Data, setStep1Data] = useState<Step1Data>({ ... })
const [step2Data, setStep2Data] = useState<Step2Data>({ ... })
// ... etc for steps 3-6

// Step execution handlers
const handleStep1Execute = async () => {
  const response = await fetch('/api/extract-entities', {
    method: 'POST',
    body: JSON.stringify({ text: step1Data.input })
  })
  // Process response → update state
}
```

**Key Pattern**: Lift state to parent, pass setters to children

**2. `components/StepCard.tsx` - Reusable Step Container**
```typescript
interface StepCardProps {
  stepNumber: number
  title: string
  status: 'pending' | 'in-progress' | 'completed'
  children: React.ReactNode
}
```

**Design**: Consistent UI wrapper for all steps

**3. `components/CodeViewer.tsx` - Syntax Highlighting**
```typescript
// Uses Monaco Editor for code display
<MonacoEditor
  language={language} // yaml, python, json
  value={code}
  options={{ readOnly: true }}
/>
```

**Why Monaco**: Same editor as VS Code, familiar to developers

#### Backend Services (`demo-app/backend/app/services/`)

**1. `ClaudeService` - Anthropic API Wrapper**
```python
class ClaudeService:
    async def generate_outcome_spec(
        self,
        text: str,
        entities: List[EntityMapping],
        custom_prompt: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """Stream Claude's response using SSE."""
        async with self.client.messages.stream(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            async for text_chunk in stream.text_stream:
                yield text_chunk
```

**Key Feature**: Streaming for real-time user feedback

**2. `GraphitiService` - Graphiti Client**
```python
class GraphitiService:
    async def extract_entities(
        self,
        text: str
    ) -> List[EntityMapping]:
        """Use Graphiti to extract entities from text."""
        # Add episode to Graphiti
        await self.client.add_episode(
            name=f"Entity Extraction - {timestamp}",
            episode_body=text,
            episode_type=EpisodeType.text
        )

        # Search for extracted entities
        results = await self.client.search(query=text)
        return self._parse_entities(results)
```

**Critical**: Uses OpenAI embeddings + Neo4j for entity extraction

**3. `SubprocessService` - gen-pydantic Executor**
```python
class SubprocessService:
    def generate_pydantic_models(
        self,
        overlay_name: str,
        linkml_schema_content: str
    ) -> Dict[str, Any]:
        """Execute gen-pydantic subprocess."""
        # Write schema to file
        schema_path = self._write_schema(overlay_name, linkml_schema_content)

        # Run gen-pydantic
        result = subprocess.run(
            ["gen-pydantic", schema_path, "--pydantic-version", "2"],
            capture_output=True,
            text=True
        )

        # Parse and save generated code
        return self._process_output(result.stdout)
```

**Why Subprocess**: LinkML's gen-pydantic is CLI-based

**4. `TestGenerator` - Automatic pytest Generation**
```python
class TestGenerator:
    def generate_test_file(self, overlay_name: str) -> Dict[str, Any]:
        """Generate pytest tests from Pydantic models."""
        # Import generated models
        models_module = importlib.import_module(
            f"generated.pydantic.overlays.{overlay_name}_models"
        )

        # Extract classes and enums
        model_classes = [cls for cls in inspect.getmembers(models_module)
                         if issubclass(cls, BaseModel)]

        # Generate test code
        test_code = self._generate_test_code(model_classes)

        # Write to tests/
        self._write_test_file(test_code)
```

**Innovation**: Introspects generated models → creates comprehensive tests

---

### 🔑 Critical Design Patterns

#### 1. **Ontology Preservation Pattern**

```yaml
# LinkML Schema (step 4)
classes:
  Audit:
    class_uri: prov:Activity  # ← Canonical URI preserved
    slots:
      - audit_id
```

```python
# Generated Pydantic Model (step 5)
class Audit(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        class_uri="prov:Activity",  # ← Same URI available
        tree_root=True
    )
```

**Why It Matters**: Enables semantic interoperability with external systems

#### 2. **Provenance Mixin Pattern**

```yaml
# Core schema (pydantic_library/schemas/core/provenance.yaml)
classes:
  ProvenanceFields:
    mixin: true
    slots:
      - node_id
      - prov_system
      - prov_file_ids
      - support_count
```

```yaml
# Overlay schema (any domain)
classes:
  MyEntity:
    mixins:
      - ProvenanceFields  # ← Automatically includes provenance
```

```python
# Generated Pydantic Model
class MyEntity(ConfiguredBaseModel):
    node_id: str
    prov_system: Optional[str] = None
    prov_file_ids: Optional[List[str]] = None
    support_count: Optional[int] = None
```

**Why It Matters**: Every entity tracks its source automatically

#### 3. **Streaming Response Pattern**

```python
# Backend (FastAPI)
async def generate_outcome_spec():
    async def event_generator():
        async for chunk in claude_service.generate_outcome_spec(...):
            yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
```

```typescript
// Frontend (Next.js)
const response = await fetch('/generate-outcome-spec', { method: 'POST' })
const reader = response.body.getReader()

while (true) {
  const { done, value } = await reader.read()
  if (done) break

  const chunk = new TextDecoder().decode(value)
  setStreamingText(prev => prev + chunk)  // Real-time update
}
```

**Why It Matters**: User sees Claude's thinking process in real-time

---

## Production Readiness Guide

### 🚀 What Works (Keep These)

✅ **Core Pipeline Architecture**
- 6-step workflow is solid and proven
- LinkML → Pydantic conversion is production-ready
- Ontology preservation works correctly

✅ **Automatic Test Generation**
- TestGenerator creates comprehensive pytest suites
- Handles Pydantic V2 correctly
- Enum detection works reliably

✅ **Streaming UX**
- Real-time feedback is excellent for user engagement
- SSE implementation is stable

### ⚠️ What Needs Work (Prioritize These)

#### 1. **Error Handling**

**Current State**: Basic try-catch blocks
**Production Need**: Comprehensive error recovery

```python
# Current (demo-app/backend/app/routers/generation.py)
try:
    result = subprocess_service.generate_pydantic_models(...)
    return PydanticGenerationResponse(**result)
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
```

**Recommended**:
```python
# Add structured error types
class PydanticGenerationError(Exception):
    def __init__(self, step: str, details: dict):
        self.step = step
        self.details = details

# Retry logic for transient failures
@retry(stop=stop_after_attempt(3), wait=wait_exponential())
async def generate_with_retry(...):
    # ... implementation

# Detailed error responses
return ErrorResponse(
    error_code="PYDANTIC_GEN_FAILED",
    step="schema_validation",
    details={"line": 42, "issue": "Invalid YAML syntax"},
    recovery_suggestion="Check YAML indentation in LinkML schema"
)
```

#### 2. **Authentication & Authorization**

**Current State**: None (demo app)
**Production Need**: Multi-user support with API key management

**Recommended**:
- JWT-based authentication
- API key rotation for Anthropic/OpenAI
- User workspace isolation (separate Neo4j graphs per user)

```python
# Add to backend
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = await auth_service.verify_jwt(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

# Protect routes
@router.post("/generate-pydantic")
async def generate_pydantic(
    request: PydanticGenerationRequest,
    current_user: User = Depends(verify_token)
):
    # ... implementation
```

#### 3. **Rate Limiting**

**Current State**: None
**Production Need**: Prevent API abuse (Anthropic charges per token)

**Recommended**:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/generate-outcome-spec")
@limiter.limit("10/minute")  # 10 requests per minute
async def generate_outcome_spec(...):
    # ... implementation
```

#### 4. **Async Job Queue**

**Current State**: Synchronous generation (blocks HTTP request)
**Production Need**: Background jobs for long-running tasks

**Recommended**:
```python
# Use Celery or FastAPI BackgroundTasks
from fastapi import BackgroundTasks

@router.post("/generate-pydantic")
async def generate_pydantic(
    request: PydanticGenerationRequest,
    background_tasks: BackgroundTasks
):
    job_id = str(uuid.uuid4())

    # Queue background task
    background_tasks.add_task(
        generate_pydantic_worker,
        job_id,
        request.overlay_name,
        request.linkml_schema
    )

    return {"job_id": job_id, "status": "queued"}

@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    return await job_service.get_status(job_id)
```

#### 5. **Database Persistence**

**Current State**: File system only (pydantic_library/)
**Production Need**: Proper database for workflow state

**Recommended**:
```python
# Add PostgreSQL for workflow tracking
class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    status = Column(Enum(WorkflowStatus))
    step1_data = Column(JSONB)
    step2_data = Column(JSONB)
    # ... etc
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
```

#### 6. **Frontend Performance**

**Current State**: Client-side rendering only
**Production Need**: Optimize for scale

**Recommended**:
- Server-side rendering (SSR) for initial page load
- Code splitting (dynamic imports for Monaco editor)
- State management library (Zustand or Redux for complex state)
- Virtualized tables (react-window) for large entity lists

```typescript
// Example: Code split Monaco editor
const MonacoEditor = dynamic(() => import('@monaco-editor/react'), {
  ssr: false,
  loading: () => <Skeleton className="h-96" />
})
```

#### 7. **Monitoring & Observability**

**Current State**: Basic logging
**Production Need**: Comprehensive monitoring

**Recommended**:
```python
# Add structured logging with correlation IDs
import structlog

logger = structlog.get_logger()

@router.post("/generate-pydantic")
async def generate_pydantic(request: PydanticGenerationRequest):
    correlation_id = str(uuid.uuid4())
    logger.info(
        "pydantic_generation_started",
        correlation_id=correlation_id,
        overlay_name=request.overlay_name,
        schema_size=len(request.linkml_schema)
    )

    # ... implementation

    logger.info(
        "pydantic_generation_completed",
        correlation_id=correlation_id,
        duration_ms=duration
    )
```

**Add metrics**:
- Request duration histograms
- Error rates by endpoint
- Token usage tracking (cost monitoring)
- Neo4j query performance

### 📊 Production Architecture Recommendations

```
┌─────────────────────────────────────────────────────────┐
│                     Load Balancer (Nginx)                │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
┌───────▼────────┐        ┌────────▼────────┐
│  Next.js App   │        │  Next.js App    │
│   (SSR Mode)   │        │   (SSR Mode)    │
└───────┬────────┘        └────────┬────────┘
        │                           │
        └─────────────┬─────────────┘
                      │
            ┌─────────▼──────────┐
            │  API Gateway       │
            │  (Auth, Rate Limit)│
            └─────────┬──────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
┌───────▼────────┐        ┌────────▼────────┐
│  FastAPI Node  │        │  FastAPI Node   │
│  (Workers)     │        │  (Workers)      │
└───────┬────────┘        └────────┬────────┘
        │                           │
        └─────────────┬─────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼───┐  ┌─────▼──────┐  ┌──▼──────┐
│ Postgres  │  │   Redis    │  │ Neo4j   │
│ (Workflow)│  │  (Cache/   │  │ (Graph) │
│           │  │   Queue)   │  │         │
└───────────┘  └────────────┘  └─────────┘
```

---

## Developer Onboarding

### 🛠️ Setup Guide

#### Prerequisites
```bash
# Required
- Python 3.12+
- Node.js 18+
- Neo4j Aura account (or local Neo4j)
- Anthropic API key
- OpenAI API key

# Optional
- Docker (for containerized development)
- PostgreSQL (for production persistence)
```

#### Step 1: Clone and Setup

```bash
# Clone repository
git clone <repo-url>
cd pydantic-model-generator

# Backend setup
cd demo-app/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

#### Step 2: Environment Configuration

```bash
# Backend .env (demo-app/backend/.env)
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
NEO4J_URI=neo4j+s://your_instance.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
PYDANTIC_LIBRARY_PATH=../../pydantic_library
CLAUDE_MODEL=claude-sonnet-4-5-20250929
CLAUDE_MAX_TOKENS=16384
```

#### Step 3: Run Development Servers

```bash
# Terminal 1: Backend
cd demo-app/backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd demo-app/frontend
npx next dev -p 3002
```

#### Step 4: Verify Installation

```bash
# Test backend
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "anthropic_configured": true,
  "openai_configured": true,
  "neo4j_configured": true
}

# Test frontend
# Open browser: http://localhost:3002
```

### 📚 Code Navigation Guide

#### Where to Find Things

**Frontend**:
```
demo-app/frontend/
├── app/
│   ├── page.tsx                    # Main workflow orchestrator
│   ├── layout.tsx                  # Root layout
│   └── globals.css                 # Global styles
├── components/
│   ├── StepCard.tsx               # Reusable step container
│   ├── CodeViewer.tsx             # Monaco editor wrapper
│   ├── EntityTable.tsx            # Entity display
│   └── ui/                        # shadcn/ui components
├── lib/
│   └── utils.ts                   # Utility functions
└── types/
    └── workflow.ts                # TypeScript types
```

**Backend**:
```
demo-app/backend/
├── app/
│   ├── main.py                    # FastAPI app entry point
│   ├── routers/
│   │   ├── entity_extraction.py  # Step 1 routes
│   │   └── generation.py         # Steps 3-5 routes
│   ├── services/
│   │   ├── claude_service.py     # Claude API wrapper
│   │   ├── graphiti_service.py   # Graphiti client
│   │   ├── subprocess_service.py # gen-pydantic runner
│   │   └── test_generator.py     # pytest auto-generation
│   └── models/
│       └── schemas.py             # Pydantic request/response models
└── requirements.txt
```

**Pydantic Library**:
```
pydantic_library/
├── schemas/
│   ├── core/
│   │   └── provenance.yaml       # Reusable provenance mixin
│   └── overlays/
│       └── *.yaml                # Domain-specific schemas
├── generated/
│   └── pydantic/
│       └── overlays/
│           └── *_models.py       # Generated Pydantic models
└── tests/
    └── test_*.py                 # Auto-generated tests
```

### 🎯 Common Development Tasks

#### Task 1: Add a New Workflow Step

```typescript
// 1. Add state to page.tsx
const [step7Data, setStep7Data] = useState<Step7Data>({ ... })

// 2. Create component
// components/Step7Card.tsx
export function Step7Card({ data, onExecute }: Step7CardProps) {
  return (
    <StepCard stepNumber={7} title="New Step" status={data.status}>
      {/* Your UI */}
    </StepCard>
  )
}

// 3. Add backend route
# app/routers/new_step.py
@router.post("/new-step-endpoint")
async def new_step_handler(request: NewStepRequest):
    # Implementation
    return NewStepResponse(...)
```

#### Task 2: Modify LinkML Schema Templates

```python
# app/services/claude_service.py
async def generate_linkml_schema(...):
    prompt = f"""
    Generate a LinkML schema with the following requirements:

    1. Include canonical ontology URIs (class_uri) for each class
    2. Add ProvenanceFields mixin to all entity classes
    3. Use these prefixes: {prefixes}

    [YOUR CUSTOM REQUIREMENTS HERE]

    Entities to model:
    {entities}
    """
```

#### Task 3: Customize Test Generation

```python
# app/services/test_generator.py

# Add new test class generation
def _generate_performance_tests(self, model_classes: List[tuple]) -> str:
    """Generate performance benchmark tests."""
    tests = []
    for class_name, cls in model_classes:
        test_code = f'''    def test_{class_name.lower()}_serialization_speed(self):
        """Benchmark serialization performance."""
        instance = {class_name}(...)

        import timeit
        duration = timeit.timeit(lambda: instance.model_dump(), number=1000)
        assert duration < 1.0  # Should serialize 1000 instances in < 1s
        '''
        tests.append(test_code)
    return f'''class TestPerformance:\n{chr(10).join(tests)}'''

# Call it in _generate_test_code()
performance_tests = self._generate_performance_tests(model_classes)
```

---

## Troubleshooting & FAQs

### ❓ Common Issues

#### Issue 1: "Module Not Found" Error in Tests

**Problem**:
```
ModuleNotFoundError: No module named 'generated'
```

**Solution**:
```bash
# Run tests from pydantic_library/ directory with PYTHONPATH
cd pydantic_library
set PYTHONPATH=.  # Windows
export PYTHONPATH=.  # Unix/Mac
pytest tests/test_*.py -v
```

**Why**: Python needs to resolve the `generated.pydantic.overlays` import path

---

#### Issue 2: Claude API Rate Limits

**Problem**:
```
429 Too Many Requests: Rate limit exceeded
```

**Solution**:
1. Check your Anthropic dashboard for rate limits
2. Add exponential backoff in `claude_service.py`:
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def _make_api_call(self, ...):
    # API call logic
```

---

#### Issue 3: Neo4j Connection Timeout

**Problem**:
```
Failed to establish connection to Neo4j
```

**Solution**:
1. Verify Neo4j Aura instance is running
2. Check firewall rules (Neo4j uses port 7687)
3. Test connection manually:
```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    uri="neo4j+s://your_instance.databases.neo4j.io",
    auth=("neo4j", "your_password")
)
with driver.session() as session:
    result = session.run("RETURN 1 AS test")
    print(result.single())  # Should print: <Record test=1>
```

---

#### Issue 4: Frontend Not Hot Reloading

**Problem**: Changes to frontend code don't reflect in browser

**Solution**:
```bash
# Clear Next.js cache
cd demo-app/frontend
rm -rf .next
npm run dev
```

---

### 💡 Best Practices

#### 1. **Always Test the Full Pipeline**

After making changes to any step:
```bash
# 1. Start backend and frontend
# 2. Run through all 6 steps with test data
# 3. Verify generated models in pydantic_library/generated/
# 4. Run pytest tests
cd pydantic_library && pytest tests/ -v
```

#### 2. **Use Type Hints Everywhere**

```typescript
// Frontend
interface WorkflowState {
  step1: Step1Data
  step2: Step2Data
  // ...
}

// Backend
def generate_pydantic(
    request: PydanticGenerationRequest
) -> PydanticGenerationResponse:
    # Type checking catches errors early
```

#### 3. **Log Correlation IDs**

```python
import uuid

correlation_id = str(uuid.uuid4())
logger.info("Request started", extra={"correlation_id": correlation_id})
# ... processing
logger.info("Request completed", extra={"correlation_id": correlation_id})
```

Makes debugging distributed traces much easier!

#### 4. **Version Your Schemas**

```yaml
# schemas/overlays/my_domain_v1.yaml
id: https://example.org/schemas/my_domain/v1
name: my_domain_v1
version: 1.0.0

# When schema changes:
# schemas/overlays/my_domain_v2.yaml
id: https://example.org/schemas/my_domain/v2
name: my_domain_v2
version: 2.0.0
```

Allows backward compatibility and migration paths.

---

## 🎓 Learning Resources

### Recommended Reading

1. **LinkML Documentation**: https://linkml.io/linkml/
   - Essential for understanding schema syntax
   - Learn about class_uri, mixins, slots

2. **Pydantic V2 Migration Guide**: https://docs.pydantic.dev/latest/migration/
   - Differences from V1 (important!)
   - New features (computed_field, model_validator, etc.)

3. **Neo4j Cypher Guide**: https://neo4j.com/docs/cypher-manual/
   - Graph query language
   - Understanding nodes and relationships

4. **Anthropic Claude API**: https://docs.anthropic.com/
   - Streaming responses
   - Prompt engineering best practices

### Hands-On Exercises

#### Exercise 1: Create a Custom Domain Schema

Try modeling a "Project Management" domain:
- Entities: Project, Task, Developer, Sprint
- Relationships: assigned_to, belongs_to, depends_on
- Ontologies: Use PROV-O for activities, Schema.org for persons

#### Exercise 2: Add Validation Rules

Extend TestGenerator to add custom validation:
```python
def _generate_business_rule_tests(self, model_classes):
    """Generate tests for business logic."""
    # Example: Task due_date must be after created_at
    return '''
    def test_task_date_consistency(self):
        with pytest.raises(ValidationError):
            Task(
                task_id="TEST-001",
                created_at=date(2024, 1, 15),
                due_date=date(2024, 1, 10)  # Invalid: before created_at
            )
    '''
```

#### Exercise 3: Optimize Streaming UX

Add progress indicators to streaming responses:
```python
async def event_generator():
    total_steps = 5
    current_step = 0

    for chunk in response_chunks:
        current_step += 1
        yield f"data: {json.dumps({
            'type': 'progress',
            'progress': current_step / total_steps,
            'content': chunk
        })}\n\n"
```

---

## 📞 Support & Next Steps

### Getting Help

1. **Check this Learning Center first** - Most answers are here
2. **Review the troubleshooting section** - Common issues covered
3. **Inspect the code** - Well-commented and structured
4. **Test incrementally** - Isolate issues step by step

### Production Deployment Checklist

- [ ] Set up authentication (JWT + API keys)
- [ ] Configure rate limiting (per user/IP)
- [ ] Add PostgreSQL for workflow persistence
- [ ] Implement background job queue (Celery)
- [ ] Set up monitoring (Prometheus + Grafana)
- [ ] Add structured logging (correlation IDs)
- [ ] Configure CORS for production domain
- [ ] Set up SSL/TLS certificates
- [ ] Enable Neo4j backups
- [ ] Create CI/CD pipeline (GitHub Actions)
- [ ] Write API documentation (Swagger/OpenAPI)
- [ ] Load test critical endpoints
- [ ] Set up error tracking (Sentry)
- [ ] Create runbooks for common issues

### Future Enhancements

1. **Multi-Model Support**: Allow users to choose between Claude/GPT-4/Gemini
2. **Schema Versioning**: Track schema changes over time
3. **Collaborative Editing**: Multiple users working on same workflow
4. **Visual Schema Editor**: Drag-and-drop interface for LinkML schemas
5. **Export Options**: Generate TypeScript types, GraphQL schemas, JSON Schema
6. **Template Library**: Pre-built schemas for common domains (e-commerce, healthcare, etc.)

---

## 🎉 Conclusion

You now have everything you need to:
- ✅ Understand the app's architecture
- ✅ Run and test the full pipeline
- ✅ Extend functionality
- ✅ Deploy to production

**Next steps**: Run through the visual walkthrough (screenshots coming next), then start building your production version!

Welcome to the team, and happy coding! 🚀

---

**Document Version**: 1.0
**Last Updated**: 2025-10-07
**Maintained By**: Original Development Team
