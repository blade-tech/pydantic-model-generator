# Quick Start Guide

## 🚀 Running the Application

### Prerequisites
- Python 3.12+
- Node.js 18+
- gen-pydantic CLI tool
- pytest

### Start Backend
```bash
cd demo-app/backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend
```bash
cd demo-app/frontend
npx next dev -p 3002
```

### Access Application
- Frontend: http://localhost:3002
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📝 How It Works

### 1. Conversation Input
Users provide natural language conversations about business outcomes.

**Example:**
```
Manager: "We need to track content creation tasks from our weekly meetings."

Developer: "I can build a system that ingests conversations via Graphiti
and generates content based on inferred tasks."

Manager: "Make sure we have full provenance tracking - who created what, when,
and from which source conversation."
```

### 2. Outcome Specification
Users specify the desired business outcome or use case.

**Example:**
```
Track content creation pipeline from conversations
```

### 3. Schema Generation (LinkML)
- LLM synthesizes LinkML schema from conversation + outcome
- Schema includes entities, relationships, enums, and constraints
- Saved to: `pydantic_library/schemas/overlays/{overlay_name}_overlay.yaml`

### 4. Pydantic Model Generation
- `gen-pydantic` converts LinkML → Pydantic V2 models
- Automatic handling of:
  - Datetime fields
  - Enum validation
  - Provenance tracking
  - Graphiti compatibility
- Saved to: `pydantic_library/generated/pydantic/overlays/{overlay_name}_models.py`

### 5. Test Generation
- Automatically creates comprehensive pytest suite
- Tests:
  - Entity creation with required fields
  - Enum validation
  - Field validation (required/optional)
  - Provenance tracking
  - Model serialization (Pydantic V2)
  - Canonical URIs (LinkMLMeta)
- Saved to: `pydantic_library/tests/test_{overlay_name}.py`

### 6. Test Execution
- Runs pytest on generated models
- Returns detailed test results (passed/failed counts, duration, error messages)

---

## 🔧 Key Implementation Details

### Hyphenated Overlay Names
**Problem:** Python modules cannot contain hyphens.

**Solution:** All services automatically normalize overlay names:
- `business-contradiction-adjudication` → `business_contradiction_adjudication`

**Files Updated:**
- `demo-app/backend/app/services/subprocess_service.py`
  - Line 192: Normalize in `generate_pydantic_models()`
  - Line 273: Normalize in `run_tests()`
- `demo-app/backend/app/services/test_generator.py`
  - Line 49: Normalize in `generate_test_file()`

### Datetime Field Handling
**Problem:** Pydantic V2 requires datetime objects, not strings.

**Solution:** `TestGenerator._generate_sample_value()` uses:
1. Type annotation inspection (lines 247-251)
2. Field name pattern matching (line 267):
   - `timestamp` fields → `datetime(2024, 1, 15, 12, 0, 0)`
   - Fields ending with `_at` → `datetime(2024, 1, 15, 12, 0, 0)`

### Duplicate Slot Detection
`SubprocessService._fix_duplicate_slots()` automatically:
1. Detects duplicate slot names in LinkML schemas
2. Adds class-specific prefixes to resolve conflicts
3. Updates slot references in all classes

---

## 📂 Project Structure

```
Pydantic Model Generator/
├── demo-app/
│   ├── backend/          # FastAPI application
│   │   └── app/
│   │       ├── services/
│   │       │   ├── schema_synthesizer.py  # LLM → LinkML
│   │       │   ├── subprocess_service.py  # gen-pydantic execution
│   │       │   └── test_generator.py      # Pytest generation
│   │       └── main.py
│   └── frontend/         # Next.js application
├── pydantic_library/     # Generated code library
│   ├── schemas/overlays/ # LinkML schemas
│   ├── generated/
│   │   └── pydantic/
│   │       └── overlays/ # Pydantic models
│   └── tests/            # Auto-generated tests
└── docs/
    ├── AGENT_PIPELINE.md
    ├── GRAPHITI_INTEGRATION.md
    └── ONTOLOGY_MAPPING.md
```

---

## 🧪 Testing

### Run All Tests
```bash
cd pydantic_library
set PYTHONPATH=.
pytest tests/ -v --tb=short
```

### Run Specific Overlay Tests
```bash
cd pydantic_library
set PYTHONPATH=.
pytest tests/test_business_contradiction_adjudication.py -v
```

### Expected Test Output
```
=================== 16 passed in 0.10s ====================
```

---

## 🐛 Common Issues

### 1. ImportError: No module named 'generated'
**Fix:** Set PYTHONPATH to pydantic_library root:
```bash
set PYTHONPATH=D:\projects\Pydantic Model Generator\pydantic_library
```

### 2. ValidationError: datetime parsing
**Fix:** Already handled in TestGenerator. If you see this, verify:
- datetime imported in test file (line 171)
- `_generate_sample_value()` uses datetime constructors (not strings)

### 3. Test file not found
**Fix:** Already handled - overlay names are normalized. If you see this:
1. Check file exists: `pydantic_library/generated/pydantic/overlays/{name}_models.py`
2. Verify name uses underscores (not hyphens)

---

## 📖 Further Reading

- **Architecture:** [docs/AGENT_PIPELINE.md](docs/AGENT_PIPELINE.md)
- **Graphiti Integration:** [docs/GRAPHITI_INTEGRATION.md](docs/GRAPHITI_INTEGRATION.md)
- **Ontology Mapping:** [docs/ONTOLOGY_MAPPING.md](docs/ONTOLOGY_MAPPING.md)
- **Learning Center:** [LEARNING_CENTER.md](LEARNING_CENTER.md) (700+ lines)

---

## 🎯 Production Readiness Checklist

### ✅ Completed
- [x] Automatic test generation (16+ tests per overlay)
- [x] Datetime field handling
- [x] Hyphenated name normalization
- [x] Enum validation
- [x] Provenance tracking
- [x] Duplicate slot detection/fixing
- [x] Pydantic V2 compatibility
- [x] Comprehensive documentation

### 🚧 Production Improvements Needed
- [ ] Frontend input validation (prevent hyphens in overlay names)
- [ ] Error handling UI (display gen-pydantic errors to user)
- [ ] Schema versioning (track changes over time)
- [ ] Authentication/authorization
- [ ] Database persistence (currently file-based)
- [ ] CI/CD pipeline
- [ ] Docker containerization
- [ ] Monitoring/logging infrastructure

---

## 🤝 Contributing

This is a teaching artifact demonstrating outcome-driven Pydantic model generation.

For production deployment, consider:
1. Adding input validation on frontend
2. Implementing schema version control
3. Adding user authentication
4. Setting up proper logging/monitoring
5. Containerizing with Docker
6. Creating CI/CD workflows

---

## 📧 Support

See `PROJECT_CONTEXT.md` for detailed system architecture and design decisions.
