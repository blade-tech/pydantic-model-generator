# Simplified Developer Handoff Plan (2-3 Hours Total)

## Goal
Understand: Business Outcome → Pydantic Models → Test if Outcomes Achieved

**Learning Time**: 2-3 hours maximum
**Audience**: Non-native English speaker, visual learner

---

## 3 Simple Documents to Create

### 1. `START_HERE.md` (30 minutes reading + running)

```markdown
# Start Here - 30 Minutes

## The Big Idea (2 minutes read)

**Problem**: Writing data models is hard. You might create the wrong models.

**Solution**:
1. Write what you NEED (business questions)
2. LLM generates models automatically
3. Test if models answer your questions
4. If yes → keep models. If no → reject and try again.

## The Pipeline (Visual)

```
┌─────────────────┐
│ Business Need   │  "Can this invoice be approved?"
│ (YAML file)     │  "Which invoices are blocked?"
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ LLM Agent       │  Reads your questions
│ (Instructor)    │  Generates schema automatically
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ LinkML Schema   │  YAML definition of models
│ (YAML file)     │  (Not Python yet)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Code Generator  │  linkml gen-pydantic
│ (LinkML tool)   │  Converts YAML → Python
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Pydantic Models │  Python classes
│ (Python file)   │  With validation
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Test Evaluation │  Run your business questions
│ (pytest)        │  Check if models work
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ ✅ Pass → Keep  │
│ ❌ Fail → Reject│
└─────────────────┘
```

## Run the Demo (15 minutes)

### Step 1: Install
```bash
pip install -r requirements.txt
```

### Step 2: Run Full Pipeline
```bash
python demo_full_pipeline.py
```

**What happens**:
1. Reads business need from `dsl/examples/invoice_validation.yaml`
2. LLM generates schema
3. Creates Pydantic models in `generated/pydantic/`
4. Tests if models answer business questions
5. Shows PASS ✅ or FAIL ❌

### Step 3: Look at Output
```bash
# See what was generated
cat generated/pydantic/invoice_models.py
```

### Step 4: Run Tests
```bash
python validate_outcome.py
```

**Expected**: 6/6 tests pass ✅

## What You Learned (5 minutes)

1. ✅ Business questions → Automatic models
2. ✅ LLM generates code (not humans)
3. ✅ Models tested against original questions
4. ✅ Fail-fast if models don't work

## Next Steps

Read: `TECH_STACK.md` to understand HOW it works
```

---

### 2. `TECH_STACK.md` (1 hour reading + experimenting)

```markdown
# Tech Stack - How It Works (1 Hour)

## The 4 Key Technologies

### 1. Instructor (LLM → Structured Data)

**What**: Forces LLM to return valid Python objects

**Code Example**:
```python
import instructor
from pydantic import BaseModel

class Schema(BaseModel):
    entity_name: str
    fields: list[str]

# LLM will return EXACTLY this structure
client = instructor.from_openai(openai.OpenAI())
result = client.chat.completions.create(
    model="gpt-4",
    response_model=Schema,  # ← Forces this structure
    messages=[{"role": "user", "content": "Design invoice model"}]
)

print(result.entity_name)  # Guaranteed to exist
print(result.fields)       # Guaranteed to be list[str]
```

**Why We Use It**:
- No parsing LLM text ✅
- No validation errors ✅
- Auto-retry if wrong ✅

**File**: `agents/schema_synthesizer.py` (line 45-89)

---

### 2. LinkML (Schema Language)

**What**: YAML language for defining models

**Example**:
```yaml
# schemas/overlays/invoice_overlay.yaml
classes:
  Invoice:
    attributes:
      invoice_id: string
      amount: float
      approved: boolean
```

**Generates Python**:
```python
class Invoice(BaseModel):
    invoice_id: str
    amount: float
    approved: bool
```

**Why We Use It**:
- LLM writes YAML easily ✅
- Convert to many formats (Pydantic, GraphQL, etc) ✅
- Separate schema from code ✅

**Try It**:
```bash
# Validate schema
linkml lint schemas/overlays/invoice_overlay.yaml

# Generate Python
linkml generate pydantic schemas/overlays/invoice_overlay.yaml
```

---

### 3. Pydantic (Data Validation)

**What**: Python models with automatic validation

**Example**:
```python
from pydantic import BaseModel, Field

class Invoice(BaseModel):
    amount: float = Field(ge=0)  # Must be >= 0
    status: str = Field(pattern="^(pending|approved|rejected)$")

# This works
invoice = Invoice(amount=100, status="approved")

# This fails automatically
invoice = Invoice(amount=-50, status="banana")  # ❌ Validation error
```

**Why We Use It**:
- Auto validation ✅
- Type safety ✅
- Works with LLMs (Instructor) ✅

**File**: `generated/pydantic/invoice_models.py`

---

### 4. Provenance Mixins (Track Data Source)

**What**: Every model remembers where it came from

**Example**:
```python
from lib.provenance_fields import NodeProv

class Invoice(NodeProv):  # ← Inherit tracking
    amount: float

invoice = Invoice(
    node_id="invoice_123",
    entity_type="Invoice",
    prov_system="slack",
    prov_file_ids=["msg-456"],
    amount=1000
)

# Now you know: This invoice came from Slack message msg-456
```

**Why We Use It**:
- Know source of every entity ✅
- Deduplicate data ✅
- Debug data issues ✅

**File**: `lib/provenance_fields.py`

---

## How They Connect

```
Business YAML ──→ Instructor ──→ LinkML YAML ──→ gen-pydantic ──→ Pydantic Models
    ↑                  ↑              ↑                ↑                ↑
  Human           LLM call      Schema format     Tool command      Python code
```

## Files to Study (30 minutes)

1. **Input**: `dsl/examples/invoice_validation.yaml` (business questions)
2. **Agent**: `agents/schema_synthesizer.py` (LLM call with Instructor)
3. **Schema**: `schemas/overlays/invoice_overlay.yaml` (LinkML definition)
4. **Generated**: `generated/pydantic/invoice_models.py` (final Python)
5. **Test**: `validate_outcome.py` (prove models work)

## Try It Yourself (30 minutes)

### Experiment 1: Change Business Question
```bash
# Edit this file
nano dsl/examples/invoice_validation.yaml

# Add new question
queries_we_must_answer:
  - "What is the average invoice amount?"

# Re-run pipeline
python demo_full_pipeline.py

# See if new model supports averaging
```

### Experiment 2: Modify Schema
```bash
# Edit generated schema
nano schemas/overlays/invoice_overlay.yaml

# Add field:
#   tax_amount: float

# Regenerate Python
linkml generate pydantic schemas/overlays/invoice_overlay.yaml > generated/pydantic/invoice_models.py

# Test
python -c "from generated.pydantic.invoice_models import Invoice; print(Invoice.__fields__.keys())"
```

### Experiment 3: Break It (Learn by Failing)
```bash
# Edit schema with invalid YAML
nano schemas/overlays/invoice_overlay.yaml
# (Make syntax error on purpose)

# Run lint
linkml lint schemas/overlays/invoice_overlay.yaml
# (See error message - this is how you debug)

# Fix it
# Re-run
```

## Summary

**The Stack**:
1. Instructor = LLM returns typed objects
2. LinkML = Schema language (YAML)
3. Pydantic = Python validation models
4. Provenance = Track data sources

**The Flow**:
Business Need → LLM (Instructor) → Schema (LinkML) → Models (Pydantic) → Test

**Key Insight**:
Models are tested against ORIGINAL business questions.
If models can't answer → Reject and regenerate.
```

---

### 3. `BUILD_YOUR_OWN.md` (1 hour reading)

```markdown
# Build Your Own Version (1 Hour)

## What to Copy vs What to Change

### ✅ Copy These Concepts

1. **Outcome-First Design**
   - Start with business questions
   - Generate only needed models
   - Test against original questions

2. **Structured LLM Outputs**
   - Use Instructor (or similar)
   - Define response schema
   - No text parsing

3. **Provenance Tracking**
   - Every entity knows its source
   - Deterministic IDs for deduplication
   - Track file/page/system

4. **Fail-Fast Evaluation**
   - Test before deployment
   - Reject bad models early
   - Metrics: Does it answer questions?

### ❌ Don't Copy These (Choose Your Own)

1. **LinkML** → You might use:
   - Direct Pydantic generation
   - TypeScript types
   - Protocol Buffers
   - JSON Schema

2. **OpenAI** → You might use:
   - Claude
   - Gemini
   - Local LLMs (Ollama)
   - Different provider

3. **Neo4j/Graphiti** → You might use:
   - PostgreSQL
   - MongoDB
   - Elasticsearch
   - Different graph DB

## Your Architecture Decision Checklist

Ask yourself:

### 1. Schema Format?
- [ ] LinkML (like this repo)
- [ ] Direct Pydantic (simpler)
- [ ] TypeScript (if JS stack)
- [ ] Other: __________

**Why?** ___________________

### 2. LLM Provider?
- [ ] OpenAI (like this repo)
- [ ] Claude (better reasoning)
- [ ] Local (privacy/cost)
- [ ] Other: __________

**Why?** ___________________

### 3. Validation Library?
- [ ] Pydantic (like this repo)
- [ ] Zod (TypeScript)
- [ ] Marshmallow (Python)
- [ ] Other: __________

**Why?** ___________________

### 4. Storage?
- [ ] Neo4j (like this repo)
- [ ] PostgreSQL (simpler)
- [ ] Your existing DB
- [ ] Other: __________

**Why?** ___________________

## Minimal Implementation (Your First Version)

### Step 1: Input Format (15 min)
Define how users specify needs:
```python
# Option A: Simple dict
need = {
    "questions": ["Can invoice be approved?"],
    "entities": ["Invoice", "Budget"]
}

# Option B: YAML (like this repo)
# See: dsl/examples/invoice_validation.yaml

# Option C: Natural language
need = "I need to approve invoices based on budget"
```

**Your choice**: __________

### Step 2: LLM Call (30 min)
Generate schema from need:
```python
import instructor
from pydantic import BaseModel

class GeneratedSchema(BaseModel):
    entities: list[str]
    fields: dict[str, list[str]]

client = instructor.from_openai(openai.OpenAI())
schema = client.chat.completions.create(
    model="gpt-4",
    response_model=GeneratedSchema,
    messages=[{
        "role": "user",
        "content": f"Generate data model for: {need}"
    }]
)

print(schema.entities)  # ['Invoice', 'Budget']
print(schema.fields)    # {'Invoice': ['id', 'amount'], ...}
```

### Step 3: Generate Models (15 min)
Convert schema to code:
```python
# Option A: Dynamic Pydantic
from pydantic import create_model

for entity in schema.entities:
    model = create_model(
        entity,
        **{field: (str, ...) for field in schema.fields[entity]}
    )

# Option B: Code generation (like this repo)
# Use LinkML or jinja2 templates

# Option C: Direct string manipulation (quick and dirty)
code = f"class {entity}(BaseModel):\n"
for field in schema.fields[entity]:
    code += f"    {field}: str\n"
```

**Your choice**: __________

### Step 4: Test (30 min)
Validate models work:
```python
def test_business_outcome(models, questions):
    for question in questions:
        # Can models answer this question?
        result = try_to_answer(question, models)
        assert result is not None, f"Failed: {question}"

# Example
test_business_outcome(
    models={"Invoice": InvoiceModel},
    questions=["Can invoice be approved?"]
)
```

## 4-Week Plan

### Week 1: Learn
- [ ] Run demo from this repo (30 min)
- [ ] Read TECH_STACK.md (1 hour)
- [ ] Understand pipeline (1 hour)

### Week 2: Design
- [ ] Choose your stack (see checklist above)
- [ ] Sketch architecture
- [ ] Define input format

### Week 3: Build MVP
- [ ] Implement LLM call with Instructor
- [ ] Generate models (simple version)
- [ ] Add basic tests

### Week 4: Improve
- [ ] Add provenance tracking
- [ ] Add evaluation metrics
- [ ] Deploy first version

## Key Differences to Make

This repo is a teaching tool. Your version should:

1. **Production Quality**
   - Error handling
   - Logging
   - Monitoring

2. **Your Stack**
   - Your LLM provider
   - Your database
   - Your deployment

3. **Your Use Case**
   - Your business domain
   - Your data sources
   - Your questions

## Questions Before Building?

1. What business questions do you need to answer?
2. What data sources do you have?
3. What's your existing tech stack?
4. What's your team's skill set?

**Answer these first, then design your pipeline.**

## Success Criteria

You've succeeded when:
- [ ] You can explain the pipeline to a colleague
- [ ] You built something DIFFERENT (not a copy)
- [ ] Your version fits YOUR use case better
- [ ] You made conscious tradeoff decisions

---

**Remember**: This repo teaches the pattern.
Your job: Build the solution that fits YOUR needs.
```

---

## Final Handoff Structure (Simple)

```
Repository Root/
├── START_HERE.md          [NEW - 30 min, visual, run demo]
├── TECH_STACK.md          [NEW - 1 hour, how it works]
├── BUILD_YOUR_OWN.md      [NEW - 1 hour, next steps]
├── README.md              [UPDATE - add pointer to START_HERE.md]
└── [existing files...]
```

## Handoff Message (Short)

```
Hi [Developer],

Study this pipeline concept: Business Questions → Auto-Generate Models → Test

📖 Start: START_HERE.md (30 min)
   - Visual pipeline
   - Run demo
   - See it work

🔧 Learn: TECH_STACK.md (1 hour)
   - Instructor + LinkML + Pydantic
   - How they connect
   - Try experiments

🏗️ Build: BUILD_YOUR_OWN.md (1 hour)
   - What to copy (concepts)
   - What to change (your stack)
   - 4-week plan

Total: 2-3 hours to understand, then build YOUR version.

Questions? Let's discuss after you finish the 3 documents.
```

---

## Summary of Changes

**From**: 8-level learning path, 7 documents, complex ADRs
**To**: 3 simple documents, visual diagrams, 2-3 hours

**Key Simplifications**:
1. Visual pipeline diagram (no long text)
2. Code examples (not theory)
3. "Try it yourself" experiments (hands-on)
4. Simple checklists (not essays)
5. Clear "copy this / don't copy that" (no ambiguity)

**Time Breakdown**:
- 30 min: Run demo + see output
- 1 hour: Understand tech stack
- 1 hour: Plan your own version
- **Total: 2.5 hours**

**Outcome**: Developer understands the CORE IDEA:
*Test models against business outcomes, reject if they fail.*

---

**Approval needed**: Is this simple enough for non-native English speaker?
