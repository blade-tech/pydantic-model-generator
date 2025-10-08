# Pydantic Model Generator

**Outcome-First AI Pipeline for Dynamic Pydantic Model Generation**

Transform business outcomes into validated Pydantic models using Claude AI, LinkML schemas, and knowledge graph storage.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)

---

## 🚀 Quick Deploy to Railway

### Prerequisites
- [Railway Account](https://railway.app/) (free tier available)
- GitHub account
- API Keys:
  - [Anthropic API Key](https://console.anthropic.com/) (Claude)
  - [OpenAI API Key](https://platform.openai.com/) (for Graphiti)

### One-Click Deployment

1. **Fork this repository** to your GitHub account

2. **Create new Railway project**:
   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `pydantic-model-generator`

3. **Add Neo4j Database**:
   - In Railway project, click "New" → "Database" → "Add Neo4j"
   - Railway will auto-inject connection variables

4. **Configure Backend Service**:
   - Root Directory: `backend`
   - Add environment variables (see below)
   - Railway auto-detects Python and installs dependencies

5. **Configure Frontend Service**:
   - Root Directory: `frontend`
   - Set `NEXT_PUBLIC_API_URL` to Railway backend URL
   - Railway auto-detects Next.js and builds

6. **Deploy**: Railway auto-deploys on every push to main branch

### Environment Variables

**Backend Service:**
```env
ANTHROPIC_API_KEY=sk-ant-...           # Your Claude API key
OPENAI_API_KEY=sk-...                  # Your OpenAI API key
NEO4J_URI=${{Neo4j.NEO4J_URI}}        # Auto-injected by Railway
NEO4J_USER=${{Neo4j.NEO4J_USER}}      # Auto-injected by Railway
NEO4J_PASSWORD=${{Neo4j.NEO4J_PASSWORD}} # Auto-injected by Railway
PYDANTIC_LIBRARY_PATH=../pydantic_library
CORS_ORIGINS=https://your-frontend.railway.app
CLAUDE_MODEL=claude-3-5-sonnet-20241022
CLAUDE_MAX_TOKENS=16384
CLAUDE_TEMPERATURE=0.7
LOG_LEVEL=INFO
DEBUG=false
```

**Frontend Service:**
```env
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

---

## 📐 Architecture

```
┌─────────────────┐
│   Frontend      │  Next.js 14 + TypeScript
│   (Port 3000)   │  - 6-Step Workflow UI
└────────┬────────┘  - Real-time streaming
         │           - State management (Zustand)
         │
         ▼
┌─────────────────┐
│   Backend       │  FastAPI + Python 3.11+
│   (Port 8000)   │  - Claude AI integration
└────────┬────────┘  - Subprocess execution
         │           - Pydantic generation
         │
         ▼
┌─────────────────┐
│   Neo4j Graph   │  Knowledge Graph Storage
│   (Port 7687)   │  - Entity relationships
└─────────────────┘  - Graphiti integration
         │
         ▼
┌─────────────────┐
│ Pydantic Library│  Generated Models
│ (File System)   │  - LinkML schemas
└─────────────────┘  - Pydantic classes
                      - Pytest tests
```

### Service Dependencies

- **Frontend** → **Backend** (API calls via CORS)
- **Backend** → **Neo4j** (Graphiti knowledge graph)
- **Backend** → **pydantic_library** (persistent file storage)

---

## 🔄 6-Step Workflow

### Step 1: Business Context Input
User provides business outcome description in natural language.

### Step 2: Ontology Research
Claude researches relevant domain ontologies and suggests entities.

### Step 3: OutcomeSpec Generation
AI generates YAML specification with:
- Outcome questions
- Target entities
- Validation queries (Cypher)

### Step 4: LinkML Schema Generation
Converts OutcomeSpec to LinkML schema with:
- Entity classes
- Relationships (slots)
- Constraints and types

### Step 5: Pydantic Generation
Executes `gen-pydantic` subprocess to create:
- Pydantic V2 models
- Type-safe Python classes
- Graphiti-compatible entities

### Step 6: Testing & Validation
Runs `pytest` to validate:
- Model instantiation
- Constraint enforcement
- Graphiti compatibility

---

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- Neo4j (Docker or local)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
# Edit .env.local with backend URL
npm run dev
```

### Neo4j Setup (Docker)
```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your-password \
  neo4j:latest
```

---

## 📚 Tech Stack

### Backend
- **FastAPI** - High-performance async API framework
- **Anthropic Claude** - AI for ontology research and generation
- **Instructor** - Structured LLM outputs
- **LinkML** - Schema definition language
- **gen-pydantic** - LinkML → Pydantic conversion
- **Graphiti** - Knowledge graph integration
- **Neo4j** - Graph database
- **pytest** - Testing framework

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Zustand** - State management
- **Radix UI** - Accessible components
- **Tailwind CSS** - Utility-first styling
- **Playwright** - E2E testing

### Infrastructure
- **Railway** - Full-stack deployment platform
- **GitHub** - Version control
- **Nixpacks** - Automatic containerization

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm run test:e2e
```

### Generated Model Tests
```bash
cd pydantic_library
pytest tests/test_*.py -v
```

---

## 📝 Project Structure

```
pydantic-model-generator/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── main.py            # Application entry point
│   │   ├── routers/           # API routes
│   │   │   ├── research.py    # Step 2: Ontology research
│   │   │   ├── generation.py  # Steps 3-5: Generation pipeline
│   │   │   ├── testing.py     # Step 6: Test execution
│   │   │   └── prompts.py     # Prompt management
│   │   ├── services/          # Business logic
│   │   │   ├── claude_service.py      # Claude API
│   │   │   ├── subprocess_service.py  # gen-pydantic/pytest
│   │   │   └── test_generator.py      # Test generation
│   │   └── utils/             # Utilities
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Environment template
│
├── frontend/                  # Next.js application
│   ├── app/                  # App router
│   ├── components/           # React components
│   │   └── workflow/         # 6-step workflow UI
│   ├── lib/                  # Utilities
│   │   ├── api-client.ts    # Backend API client
│   │   └── workflow-store.ts # State management
│   ├── package.json         # Node dependencies
│   └── next.config.js       # Next.js config
│
├── pydantic_library/         # Generated models (persistent)
│   ├── schemas/overlays/    # LinkML schemas
│   ├── generated/pydantic/overlays/  # Pydantic models
│   └── tests/               # Generated pytest tests
│
├── railway.toml              # Railway configuration
├── .gitignore
└── README.md                 # This file
```

---

## 🔐 Security Notes

- **Never commit `.env` files** - Use `.env.example` as template
- **API Keys**: Store in Railway environment variables, not in code
- **Neo4j Credentials**: Use Railway's auto-injected variables
- **CORS**: Configure `CORS_ORIGINS` with your frontend URL only

---

## 📖 Documentation

### API Documentation
- **Interactive Docs**: `https://your-backend.railway.app/docs`
- **OpenAPI Schema**: `https://your-backend.railway.app/openapi.json`

### Workflow Steps
1. [Step 1: Business Input](docs/step1-business-input.md)
2. [Step 2: Ontology Research](docs/step2-ontology-research.md)
3. [Step 3: OutcomeSpec](docs/step3-outcomespec.md)
4. [Step 4: LinkML Schema](docs/step4-linkml.md)
5. [Step 5: Pydantic Generation](docs/step5-pydantic.md)
6. [Step 6: Testing](docs/step6-testing.md)

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Anthropic](https://anthropic.com/) - Claude AI
- [LinkML](https://linkml.io/) - Schema definition framework
- [Graphiti](https://github.com/graphiti-project/graphiti) - Knowledge graph integration
- [Railway](https://railway.app/) - Deployment platform

---

## 🐛 Troubleshooting

### Common Issues

**1. Backend won't start**
- Verify all environment variables are set
- Check Neo4j connection in Railway logs
- Ensure `pydantic_library` path is correct

**2. Frontend can't connect to backend**
- Verify `NEXT_PUBLIC_API_URL` points to Railway backend URL
- Check CORS settings in backend
- Confirm backend health: `curl https://backend-url/health`

**3. gen-pydantic subprocess fails**
- Ensure LinkML is installed: `pip list | grep linkml`
- Check schema validity with `linkml-validate`
- Review logs in Railway dashboard

**4. Tests failing**
- Verify pytest-json-report is installed
- Check PYTHONPATH includes pydantic_library
- Run tests locally first for better error messages

---

## 📬 Support

- **GitHub Issues**: [Report bugs](https://github.com/blade-tech/pydantic-model-generator/issues)
- **Discussions**: [Ask questions](https://github.com/blade-tech/pydantic-model-generator/discussions)

---

**Built with ❤️ using Claude AI and deployed on Railway**
