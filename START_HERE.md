# Start Here - 30 Minutes

## The Big Idea (2 minutes)

**Problem**: Writing data models is hard. You might create the wrong models.

**Solution**:
1. Write what you NEED (business questions)
2. LLM generates models automatically
3. Test if models answer your questions
4. If yes → keep models. If no → reject and try again.

---

## The Pipeline (Visual)

```
┌─────────────────────────────┐
│ 1. Business Need (YAML)     │
│                             │  "Can this invoice be approved?"
│ dsl/examples/               │  "Which invoices are blocked?"
│ invoice_validation.yaml     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ 2. LLM Agent                │
│                             │  Reads your questions
│ agents/                     │  Generates schema automatically
│ schema_synthesizer.py       │  (Uses Instructor library)
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ 3. LinkML Schema (YAML)     │
│                             │  Model definition
│ schemas/overlays/           │  (Not Python yet)
│ invoice_overlay.yaml        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ 4. Code Generator           │
│                             │  linkml gen-pydantic
│ LinkML Tool                 │  YAML → Python
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ 5. Pydantic Models          │
│                             │  Python classes
│ generated/pydantic/         │  With validation
│ invoice_models.py           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ 6. Test Evaluation          │
│                             │  Run business questions
│ validate_outcome.py         │  Check if models work
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Result                      │
│                             │
│ ✅ Pass → Keep models       │
│ ❌ Fail → Reject & retry    │
└─────────────────────────────┘
```

---

## Run the Demo (15 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Full Pipeline
```bash
python demo_full_pipeline.py
```

**What happens**:
1. ✅ Reads business need from `dsl/examples/invoice_validation.yaml`
2. ✅ LLM generates schema → `schemas/overlays/invoice_overlay.yaml`
3. ✅ Creates Pydantic models → `generated/pydantic/invoice_models.py`
4. ✅ Tests if models answer business questions
5. ✅ Shows PASS ✅ or FAIL ❌

### Step 3: Look at Generated Code
```bash
# Windows
type generated\pydantic\invoice_models.py

# Mac/Linux
cat generated/pydantic/invoice_models.py
```

You will see Python classes like:
```python
class Invoice(BaseModel):
    invoice_id: str
    amount: float
    vendor_id: str
    has_purchase_order: bool
```

### Step 4: Run Tests
```bash
python validate_outcome.py
```

**Expected Output**:
```
✅ Test 1: Invoice approval logic - PASS
✅ Test 2: Blocked invoices query - PASS
✅ Test 3: Department totals - PASS

SUCCESS: 6/6 tests passed
Models satisfy ALL business requirements!
```

---

## What You Learned (5 minutes)

1. ✅ Business questions → Automatic models
2. ✅ LLM generates code (not humans)
3. ✅ Models tested against original questions
4. ✅ Fail-fast if models don't work

**Key Insight**: The models are VALIDATED by checking if they can answer the original business questions.

---

## What to Read Next

### Option A: Understand HOW (1 hour)
→ Read `TECH_STACK.md` to learn:
- How Instructor works (LLM → typed objects)
- How LinkML works (YAML → Python)
- How Pydantic validates data
- How provenance tracking works

### Option B: Build YOUR Version (1 hour)
→ Read `BUILD_YOUR_OWN.md` to learn:
- What to copy (concepts)
- What to change (your stack)
- Step-by-step plan

---

## Quick Reference - Key Files

| File | What It Is |
|------|-----------|
| `dsl/examples/invoice_validation.yaml` | Business questions (INPUT) |
| `agents/schema_synthesizer.py` | LLM agent that generates schema |
| `schemas/overlays/invoice_overlay.yaml` | Generated schema (LinkML YAML) |
| `generated/pydantic/invoice_models.py` | Generated Python models |
| `validate_outcome.py` | Test if models work |
| `lib/provenance_fields.py` | Track where data came from |

---

## Troubleshooting

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "LinkML command not found"
```bash
pip install linkml
```

### Demo doesn't run
1. Check Python version: `python --version` (need 3.11+)
2. Check if files exist: `ls dsl/examples/`
3. Try: `python demo_pipeline.py` (alternative demo)

---

**Time spent**: ~30 minutes
**Next step**: Choose Option A or B above
