# Pydantic Model Generator Demo App

**Live demonstration of outcome-first Pydantic modeling pipeline with human-in-the-loop workflow**

---

## 🎯 What This Is

A **real, working application** that shows the complete transformation pipeline:

```
Business Outcome (free text)
  ↓
AI Ontology Research (Claude)
  ↓
OutcomeSpec Generation (Instructor)
  ↓
LinkML Schema Generation (Instructor)
  ↓
Pydantic Models (gen-pydantic)
  ↓
Testing & Validation (pytest)
  ↓
Graphiti Knowledge Graph (Neo4j)
```

**Human-in-the-loop**: User approves each transformation step with live AI reasoning logs.

---

## ⚠️ What This Is NOT

- ❌ Not a mockup with hardcoded responses
- ❌ Not a prototype with fake API calls
- ❌ Not a demo with test data only

**✅ This app uses REAL API keys, makes REAL calls to Claude/OpenAI/Neo4j, writes REAL files to the pydantic_library.**

---

## 🏗️ Architecture

### Frontend (Next.js 14 + TypeScript)
- **UI Framework**: Next.js App Router with Server Components
- **Styling**: Tailwind CSS + shadcn/ui components
- **Key Features**:
  - 6-step workflow with progress tracking
  - Live Claude reasoning log panel (Server-Sent Events)
  - Human approval gates at each step
  - Library coverage dashboard
  - Settings panel for environment variables

### Backend (FastAPI + Python 3.11+)
- **API Framework**: FastAPI with async support
- **Key Features**:
  - Real Claude SDK integration (streaming)
  - Real Instructor for structured outputs
  - Real subprocess execution (gen-pydantic, pytest)
  - Real Graphiti ingestion
  - Real Neo4j connection
  - Server-Sent Events for streaming logs

### Data Flow
```
Next.js Frontend
  ↕ HTTP/SSE
FastAPI Backend
  ↕ Real API calls
Claude (Anthropic) + OpenAI + Neo4j
  ↕ File writes
../pydantic_library/
```

---

## 📋 Prerequisites

### Required Software
- **Python 3.11+** (for backend)
- **Node.js 18+** (for frontend)
- **Neo4j Desktop** or Docker container
- **LinkML** (`pip install linkml`)

### Required API Keys
- **Anthropic API Key** - Get at https://console.anthropic.com/
- **OpenAI API Key** - Get at https://platform.openai.com/api-keys
- **Neo4j Credentials** - Setup during Neo4j installation

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
cd "D:\projects\Pydantic Model Generator"
```

### 2. Setup Backend

```bash
cd demo-app/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your real API keys
# ANTHROPIC_API_KEY=sk-ant-api03-xxx
# OPENAI_API_KEY=sk-xxx
# NEO4J_PASSWORD=your-password
```

### 3. Setup Frontend

```bash
cd demo-app/frontend

# Install dependencies
npm install

# Copy environment template
cp .env.local.example .env.local

# Edit .env.local if needed (API URL)
```

### 4. Start Neo4j

**Option A: Neo4j Desktop**
1. Open Neo4j Desktop
2. Create new database (or use existing)
3. Start the database
4. Note the connection URI (usually `neo4j://localhost:7687`)

**Option B: Docker**
```bash
docker run \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your-password \
  neo4j:latest
```

### 5. Start Backend

```bash
cd demo-app/backend
python -m uvicorn app.main:app --reload --port 8000
```

Backend will be available at: http://localhost:8000

### 6. Start Frontend

```bash
cd demo-app/frontend
npm run dev
```

Frontend will be available at: http://localhost:3000

---

## 📖 Usage

### Step-by-Step Workflow

**Step 1: Enter Business Outcome**
```
Example input:
"We need to track customer support tickets with priority levels,
assigned agents, response times, and resolution status."
```

**Step 2: AI Ontology Research**
- Claude analyzes text and identifies entities
- Maps to canonical ontologies (DoCO, FaBiO, PROV-O, FIBO, SKOS)
- Displays confidence scores
- Shows live reasoning in Claude log panel
- **Human approval required**

**Step 3: Generate OutcomeSpec**
- Creates YAML specification with:
  - Outcome questions
  - Target entities
  - Validation queries
- Uses Instructor for structured output
- **Human approval required** (can edit YAML)

**Step 4: Generate LinkML Schema**
- Creates LinkML schema with:
  - Entity classes
  - Slots (fields)
  - Relationships
  - Canonical URIs
- Uses Instructor for structured output
- **Human approval required** (can edit YAML)

**Step 5: Generate Pydantic Models**
- Executes `gen-pydantic` subprocess
- Writes files to `../pydantic_library/`
- Shows generated Python code
- **Human approval required**

**Step 6: Testing & Ingestion**
- Runs pytest on generated models
- Shows pass/fail/skip counts
- Ingests to Graphiti (creates Neo4j nodes/edges)
- **Human approval required**

**Step 7: View in Neo4j Browser**
- Open Neo4j Browser
- Run Cypher queries to explore graph
- Visualize entities and relationships

---

## 🔧 Configuration

### Backend (.env)

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-api03-xxx
OPENAI_API_KEY=sk-xxx
NEO4J_PASSWORD=your-password

# Optional
NEO4J_URI=neo4j://localhost:7687
NEO4J_USER=neo4j
PYDANTIC_LIBRARY_PATH=../pydantic_library
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

### Frontend (.env.local)

```bash
# Optional
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📊 Library Coverage Dashboard

The app includes a dashboard showing:
- Number of overlays in pydantic_library
- Total entities across all overlays
- Total edges (relationships)
- Most recent overlay added
- Coverage by outcome type

---

## 🧪 Testing

### Backend Tests
```bash
cd demo-app/backend
pytest
```

### Frontend Tests
```bash
cd demo-app/frontend
npm test
```

### End-to-End Tests
```bash
# Start backend and frontend
# Then run E2E tests
cd demo-app
npm run test:e2e
```

---

## 📚 API Documentation

### Backend API
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

**Research**
- `POST /api/research` - Claude ontology research with streaming

**Generation**
- `POST /api/generate-outcome-spec` - Generate OutcomeSpec YAML
- `POST /api/generate-linkml` - Generate LinkML schema YAML
- `POST /api/generate-pydantic` - Execute gen-pydantic subprocess
- `POST /api/run-tests` - Execute pytest subprocess

**Library**
- `GET /api/library-coverage` - Get pydantic_library coverage stats

**Graphiti**
- `POST /api/graphiti/ingest` - Ingest to knowledge graph
- `GET /api/graphiti/status` - Get ingestion status

---

## 🐛 Troubleshooting

### Backend won't start
**Error**: `Settings validation error`
**Fix**: Make sure .env file exists with all required variables

### Claude API errors
**Error**: `401 Unauthorized`
**Fix**: Check ANTHROPIC_API_KEY in .env (should start with `sk-ant-`)

### Neo4j connection failed
**Error**: `Unable to connect to Neo4j`
**Fix**:
1. Make sure Neo4j is running
2. Check NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD in .env
3. Test connection in Neo4j Browser first

### gen-pydantic not found
**Error**: `gen-pydantic: command not found`
**Fix**: Install LinkML in backend venv: `pip install linkml`

### File write errors
**Error**: `Permission denied writing to ../pydantic_library/`
**Fix**: Check file permissions, make sure path is correct in PYDANTIC_LIBRARY_PATH

---

## 📁 Directory Structure

```
demo-app/
├── README.md                    # ← You are here
├── docs/
│   ├── SPEC.md                  # Technical specification
│   └── PROGRESS.md              # Progress tracker
│
├── backend/                     # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app
│   │   ├── routers/             # API endpoints
│   │   ├── services/            # Business logic
│   │   └── models/              # Pydantic models
│   ├── requirements.txt
│   ├── .env.example
│   └── .env                     # Your API keys (not committed)
│
└── frontend/                    # Next.js frontend (to be created)
    ├── app/                     # Next.js App Router
    ├── components/              # React components
    ├── lib/                     # Utilities
    ├── package.json
    ├── .env.local.example
    └── .env.local               # Your config (not committed)
```

---

## 🎥 Demo Video

*(Coming soon - video walkthrough of full pipeline)*

---

## 🔗 Related Documentation

- **Main Project**: `../README.md`
- **Pydantic Library**: `../pydantic_library/README.md`
- **Migration Guide**: `../pydantic_library/MIGRATION_GUIDE.md`
- **Graphiti Integration**: `../docs/GRAPHITI_INTEGRATION.md`
- **Ontology Mapping**: `../docs/ONTOLOGY_MAPPING.md`

---

## 🤝 Contributing

This is a teaching artifact and demo app. For contributions to the main pydantic_library, see the parent directory.

---

## 📝 License

Same as parent project.

---

## 🆘 Support

For issues with this demo app:
1. Check troubleshooting section above
2. Review SPEC.md in docs/
3. Check PROGRESS.md for known issues

For issues with pydantic_library:
1. See `../pydantic_library/README.md`
2. Check `../PROJECT_CONTEXT.md`

---

**Built with**: FastAPI • Next.js • Claude (Anthropic) • Instructor • LinkML • Graphiti • Neo4j

**Status**: 🟡 In Development (see docs/PROGRESS.md)
