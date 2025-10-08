# Developer Handoff Guide

**Project:** Pydantic Model Generator
**Repository:** https://github.com/blade-tech/pydantic-model-generator
**Handoff Date:** October 8, 2025

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Project Overview](#project-overview)
3. [Current Status](#current-status)
4. [Architecture](#architecture)
5. [Local Deployment](#local-deployment)
6. [Configuration](#configuration)
7. [Known Issues](#known-issues)
8. [Next Steps](#next-steps)

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+**
- **Node.js 18+**
- **Neo4j** (Desktop or Docker)
- **API Keys:**
  - Anthropic API Key (Claude)
  - OpenAI API Key
  - Neo4j credentials

### Setup Commands

```bash
# 1. Clone repository
git clone https://github.com/blade-tech/pydantic-model-generator.git
cd pydantic-model-generator

# 2. Backend setup
cd demo-app/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys

# 3. Frontend setup
cd ../frontend
npm install
cp .env.local.example .env.local
# Edit .env.local if needed

# 4. Start services
# Terminal 1 - Backend (use port 8001 to avoid conflicts)
cd demo-app/backend
python -m uvicorn app.main:app --reload --port 8001

# Terminal 2 - Frontend
cd demo-app/frontend
npm run dev

# 5. Open browser
# http://localhost:3001
```

---

## 📊 Project Overview

### What This Is

An **outcome-first Pydantic modeling pipeline** that transforms business requirements into validated, graph-ready Pydantic models through a 6-step workflow:

```
Business Outcome → AI Research → OutcomeSpec → LinkML Schema → Pydantic Models → Testing & Graph Ingestion
```

### Key Features

- **Human-in-the-loop workflow** - User approves each transformation step
- **Real AI integration** - Uses Claude (Anthropic) and OpenAI APIs
- **Live reasoning logs** - Shows AI thinking in real-time via SSE
- **Knowledge graph integration** - Ingests to Neo4j via Graphiti
- **Customizable prompts** - Edit AI prompts for each step
- **Full-stack demo app** - Next.js frontend + FastAPI backend

---

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS + shadcn/ui
- Server-Sent Events (SSE) for streaming

**Backend:**
- FastAPI (Python 3.11+)
- Anthropic Claude SDK (streaming)
- OpenAI Instructor (structured outputs)
- LinkML (schema generation)
- Graphiti (knowledge graph)
- Neo4j (graph database)

**Core Pipeline:**
1. `pipeline/` - Main generation logic
2. `pydantic_library/` - Generated Pydantic models
3. `demo-app/` - Full-stack demo application

### Directory Structure

```
pydantic-model-generator/
├── demo-app/              # Full-stack demo application
│   ├── backend/           # FastAPI backend
│   │   ├── app/
│   │   │   ├── routers/   # API endpoints
│   │   │   ├── services/  # Business logic (Claude, Instructor)
│   │   │   ├── prompts/   # AI prompt templates
│   │   │   └── main.py    # FastAPI app
│   │   ├── requirements.txt
│   │   └── .env.example
│   │
│   └── frontend/          # Next.js frontend
│       ├── app/           # Next.js App Router
│       ├── components/    # React components
│       ├── lib/           # API client, utilities
│       ├── package.json
│       └── .env.local.example
│
├── pydantic_library/      # Generated Pydantic models (v2)
│   ├── core/              # Base classes, provenance
│   └── domains/           # Domain-specific models
│       ├── aaoifi/
│       ├── business/
│       └── murabaha_audit/
│
├── pipeline/              # Core generation pipeline
│   ├── agents/            # AI agents (research, synthesis)
│   ├── generators/        # Code generators
│   └── orchestrators/     # Workflow orchestration
│
├── docs/                  # Comprehensive documentation
│   ├── GRAPHITI_INTEGRATION.md
│   ├── ONTOLOGY_MAPPING.md
│   └── ...
│
└── README.md              # Main project documentation
```

---

## ✅ Current Status

### What's Working

✅ **Backend API (FastAPI)**
- All 6 workflow steps implemented
- Real Claude streaming integration
- Instructor for structured outputs
- Prompts API for customization
- CORS configured for localhost:3000-3001

✅ **Frontend (Next.js)**
- Complete 6-step workflow UI
- Live Claude reasoning logs (SSE)
- Prompt editor with default/custom prompts
- Human approval gates at each step
- Error handling and validation

✅ **Pydantic Models**
- Modular architecture (core + domains)
- Pydantic v2 compatible
- Graphiti-compatible annotations
- Provenance tracking
- Multiple domain overlays working

✅ **Documentation**
- Comprehensive README
- API documentation (Swagger at /docs)
- Architecture diagrams
- Deployment guides

### Known Issues

⚠️ **Port Conflicts**
- Backend should run on **port 8001** (not 8000)
- Frontend runs on **port 3001** (if 3000 is busy)
- Update `.env.local` if backend port changes:
  ```
  NEXT_PUBLIC_API_URL=http://localhost:8001
  ```

⚠️ **Log Broadcasting Error**
- AsyncIO warning in learning_center.py:129
- Non-blocking, doesn't affect functionality
- Fix: Use `asyncio.ensure_future()` instead of `create_task()`

⚠️ **Environment Variables**
- Frontend needs hard refresh (Ctrl+Shift+R) after .env.local changes
- Backend auto-reloads on .env changes

---

## 🚀 Local Deployment

### Step-by-Step Deployment

#### 1. Backend Setup

```bash
cd demo-app/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

**Edit `.env` file:**
```bash
# Required
ANTHROPIC_API_KEY=sk-ant-api03-xxx
OPENAI_API_KEY=sk-xxx
NEO4J_PASSWORD=your-password

# Optional (defaults shown)
NEO4J_URI=neo4j://localhost:7687
NEO4J_USER=neo4j
PYDANTIC_LIBRARY_PATH=../../pydantic_library
CLAUDE_MODEL=claude-sonnet-4-5-20250929
API_PORT=8001  # Use 8001 to avoid conflicts
```

**Start backend:**
```bash
python -m uvicorn app.main:app --reload --port 8001
```

**Verify:** http://localhost:8001/docs

#### 2. Frontend Setup

```bash
cd demo-app/frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
```

**Edit `.env.local` file:**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
```

**Start frontend:**
```bash
npm run dev
```

**Verify:** http://localhost:3001

#### 3. Neo4j Setup

**Option A: Neo4j Desktop**
1. Download from https://neo4j.com/download/
2. Create new database
3. Set password (use in .env)
4. Start database
5. Note connection URI (usually neo4j://localhost:7687)

**Option B: Docker**
```bash
docker run \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your-password \
  neo4j:latest
```

#### 4. Verify Everything

1. Backend health: http://localhost:8001/health
2. Frontend: http://localhost:3001
3. API docs: http://localhost:8001/docs
4. Neo4j Browser: http://localhost:7474

---

## ⚙️ Configuration

### Environment Variables

**Backend (.env):**
| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| ANTHROPIC_API_KEY | ✅ | Claude API key | - |
| OPENAI_API_KEY | ✅ | OpenAI API key | - |
| NEO4J_PASSWORD | ✅ | Neo4j password | - |
| NEO4J_URI | ❌ | Neo4j connection | neo4j://localhost:7687 |
| NEO4J_USER | ❌ | Neo4j username | neo4j |
| PYDANTIC_LIBRARY_PATH | ❌ | Models output path | ../../pydantic_library |
| CLAUDE_MODEL | ❌ | Claude model | claude-sonnet-4-5-20250929 |
| API_PORT | ❌ | Backend port | 8001 |

**Frontend (.env.local):**
| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| NEXT_PUBLIC_API_URL | ❌ | Backend API URL | http://localhost:8000 |

### API Keys Setup

**Anthropic (Claude):**
1. Go to https://console.anthropic.com/
2. Create account / Login
3. Settings → API Keys → Create Key
4. Copy key (starts with `sk-ant-`)

**OpenAI:**
1. Go to https://platform.openai.com/api-keys
2. Create account / Login
3. Create new secret key
4. Copy key (starts with `sk-`)

---

## 🐛 Known Issues & Fixes

### Issue 1: "Failed to get default prompt: Not Found"

**Symptom:** Step 2 shows "Not Found" error when loading prompts.

**Cause:** Wrong backend running on port 8000 (Islamic Finance API instead of Pydantic Generator).

**Fix:**
```bash
# Stop all Python processes on port 8000
taskkill /F /PID <process_id>

# Start correct backend on port 8001
cd demo-app/backend
python -m uvicorn app.main:app --reload --port 8001

# Update frontend .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8001

# Hard refresh browser (Ctrl+Shift+R)
```

### Issue 2: AsyncIO Event Loop Warning

**Symptom:** `RuntimeError: no running event loop` in logs.

**Location:** `demo-app/backend/app/routers/learning_center.py:129`

**Impact:** Non-blocking warning, doesn't affect functionality.

**Fix (optional):**
```python
# Change from:
asyncio.create_task(self.broadcaster.broadcast(log_entry))

# To:
asyncio.ensure_future(self.broadcaster.broadcast(log_entry))
```

### Issue 3: Frontend Cache Issues

**Symptom:** Changes to .env.local not reflected.

**Fix:** Hard refresh browser:
- Windows/Linux: `Ctrl + Shift + R`
- Mac: `Cmd + Shift + R`

---

## 🔄 Next Steps

### Immediate Priorities

1. **Fix Event Loop Warning**
   - Update learning_center.py logging handler
   - Test with concurrent requests

2. **Add Production Config**
   - Create production .env templates
   - Add Railway/Vercel deployment configs
   - Set up environment variable management

3. **Improve Error Handling**
   - Add retry logic for Claude API
   - Better error messages in UI
   - Graceful degradation

4. **Testing**
   - Add E2E tests (Playwright configured)
   - Unit tests for API endpoints
   - Integration tests for pipeline

### Future Enhancements

1. **Authentication**
   - Add user login/signup
   - Secure API with JWT tokens
   - Multi-tenant support

2. **Model Management**
   - Version control for generated models
   - Diff viewer for model changes
   - Rollback capabilities

3. **Workflow Extensions**
   - Custom workflow steps
   - Conditional branching
   - Parallel processing

4. **Monitoring**
   - API usage tracking
   - Performance metrics
   - Error logging dashboard

---

## 📚 Additional Resources

### Documentation Files

- **README.md** - Main project overview
- **demo-app/README.md** - Demo app specifics
- **docs/GRAPHITI_INTEGRATION.md** - Knowledge graph integration
- **docs/ONTOLOGY_MAPPING.md** - Ontology mapping guide
- **pydantic_library/README.md** - Generated models documentation

### API Documentation

- **Swagger UI:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc

### External Resources

- [Next.js Docs](https://nextjs.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Claude API Docs](https://docs.anthropic.com/)
- [LinkML Docs](https://linkml.io/)
- [Graphiti Docs](https://github.com/getzep/graphiti)

---

## 🆘 Troubleshooting

### Backend Won't Start

**Error:** `Settings validation error`

**Fix:** Ensure .env file exists with all required variables (see Configuration section).

### Claude API Errors

**Error:** `401 Unauthorized`

**Fix:**
- Check ANTHROPIC_API_KEY in .env
- Verify key starts with `sk-ant-`
- Check API usage limits at https://console.anthropic.com/

### Neo4j Connection Failed

**Error:** `Unable to connect to Neo4j`

**Fix:**
1. Ensure Neo4j is running
2. Verify credentials in .env
3. Test connection in Neo4j Browser first
4. Check firewall/ports (7687, 7474)

### Frontend Build Errors

**Error:** `Module not found`

**Fix:**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## 📞 Contact

For questions or issues:
- Create GitHub issue: https://github.com/blade-tech/pydantic-model-generator/issues
- Check existing documentation in `/docs`
- Review API docs at /docs endpoint

---

**Last Updated:** October 8, 2025
**Handoff Completed By:** Claude Code Assistant
**Repository:** https://github.com/blade-tech/pydantic-model-generator
