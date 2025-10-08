# Project Context: Outcome-Driven Pydantic Model Generator

## Project Purpose
This is a **teaching artifact** demonstrating outcome-driven Pydantic V2 model generation from natural language conversations.

## Key Bug Fixes Applied

### 1. Datetime Validation (test_generator.py)
- **Issue:** ValidationError for datetime fields receiving strings
- **Fix:** Type annotation inspection + field name pattern matching
- **Lines:** 171 (import), 247-251 (type check), 267 (pattern match)

### 2. Hyphenated Overlay Names
- **Issue:** Python modules cannot contain hyphens
- **Fix:** Automatic normalization (replace '-' with '_')
- **Files:**
  - subprocess_service.py: Lines 191-194, 235, 273
  - test_generator.py: Lines 48-49, 78

## Test Results
All overlays passing: 16 tests each (entity creation, enums, validation, provenance, serialization, URIs)

## Production Improvements Needed
1. Frontend validation (prevent hyphens in overlay names)
2. Error handling UI (display gen-pydantic errors)
3. Schema versioning
4. Authentication/authorization
5. Database persistence (replace file-based storage)
6. CI/CD pipeline
7. Docker containerization
8. Monitoring/logging infrastructure

## Documentation
- QUICK_START.md: How to run the application
- LEARNING_CENTER.md: 700+ lines comprehensive guide
- docs/AGENT_PIPELINE.md: Agent orchestration
- docs/GRAPHITI_INTEGRATION.md: Knowledge graph integration
- docs/ONTOLOGY_MAPPING.MD: Ontology alignment

## Verified Working
- Conversation → LinkML schema generation
- LinkML → Pydantic V2 models
- Automatic test generation
- Datetime field handling
- Hyphenated name normalization
- Enum validation
- Provenance tracking
