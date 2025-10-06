# Tech Stack - How It Works (1 Hour)

## Overview

This pipeline uses 4 key technologies:

1. **Instructor** - LLM returns typed Python objects
2. **LinkML** - Schema language (YAML)
3. **Pydantic** - Data validation
4. **Provenance** - Track data sources

---

## 1. Instructor (LLM → Structured Data)

### What It Does
Forces LLM to return valid Python objects (no text parsing needed).

### Code Example
```python
import instructor
from pydantic import BaseModel
from openai import OpenAI

# Define what you want
class Schema(BaseModel):
    entity_name: str
    fields: list[str]

# LLM returns EXACTLY this structure
client = instructor.from_openai(OpenAI())
result = client.chat.completions.create(
    model="gpt-4",
    response_model=Schema,  # ← Forces this structure
    messages=[{
        "role": "user",
        "content": "Design a model for invoices"
    }]
)

# Guaranteed to work
print(result.entity_name)  # str (guaranteed)
print(result.fields)       # list[str] (guaranteed)
```

### Why We Use It
- ✅ No parsing LLM text
- ✅ No validation errors
- ✅ Auto-retry if LLM returns wrong format

### Where to Find It
**File**: `agents/schema_synthesizer.py` (lines 45-89)

### Try It
```python
# Run the schema synthesizer
python run_llm_synthesis.py dsl/examples/invoice_validation.yaml

# See: LLM generates valid LinkML schema automatically
```

---

## 2. LinkML (Schema Language)

### What It Does
YAML format for defining data models. Can generate Python, GraphQL, JSON-LD, etc.

### Example Schema
```yaml
# schemas/overlays/invoice_overlay.yaml
classes:
  Invoice:
    attributes:
      invoice_id:
        range: string
        required: true
      amount:
        range: float
        required: true
      approved:
        range: boolean
```

### Generates This Python
```python
class Invoice(BaseModel):
    invoice_id: str
    amount: float
    approved: bool
```

### Why We Use It
- ✅ LLM writes YAML easily
- ✅ Convert to many formats (Pydantic, GraphQL, etc)
- ✅ Schema separate from code

### Commands
```bash
# Validate schema
linkml lint schemas/overlays/invoice_overlay.yaml

# Generate Python
linkml generate pydantic schemas/overlays/invoice_overlay.yaml > models.py
```

### Where to Find It
**Files**:
- `schemas/core.yaml` - Base schema (NodeProv, EdgeProv)
- `schemas/overlays/*.yaml` - Generated schemas

### Try It
```bash
# Create your own schema
nano schemas/overlays/my_schema.yaml

# Add:
# classes:
#   Product:
#     attributes:
#       name: string
#       price: float

# Generate Python
linkml generate pydantic schemas/overlays/my_schema.yaml

# See the generated code
```

---

## 3. Pydantic (Data Validation)

### What It Does
Python models with automatic validation.

### Example
```python
from pydantic import BaseModel, Field

class Invoice(BaseModel):
    amount: float = Field(ge=0)  # Must be >= 0
    status: str = Field(
        pattern="^(pending|approved|rejected)$"
    )

# This works ✅
invoice = Invoice(
    amount=100,
    status="approved"
)

# This fails ❌
invoice = Invoice(
    amount=-50,      # Negative not allowed
    status="banana"  # Invalid status
)
# ValidationError: amount must be >= 0
```

### Why We Use It
- ✅ Auto validation
- ✅ Type safety
- ✅ Works with Instructor

### Where to Find It
**Files**:
- `generated/pydantic/invoice_models.py` - Generated models
- `generated/pydantic/murabaha_audit_models.py` - Complex example

### Try It
```python
# Import generated model
from generated.pydantic.invoice_models import Invoice

# Create valid invoice
invoice = Invoice(
    node_id="inv_001",
    entity_type="Invoice",
    invoice_id="INV-001",
    amount=1000.0
)

print(invoice.amount)  # 1000.0

# Try invalid
invoice = Invoice(
    node_id="inv_002",
    entity_type="Invoice",
    invoice_id="INV-002",
    amount="not_a_number"  # ❌ Will fail
)
```

---

## 4. Provenance Mixins (Track Data Source)

### What It Does
Every model remembers WHERE it came from.

### Example
```python
from lib.provenance_fields import NodeProv

class Invoice(NodeProv):  # ← Inherit tracking
    amount: float
    vendor: str

# Create with provenance
invoice = Invoice(
    # Required provenance fields
    node_id="invoice_INV001_abc123",
    entity_type="Invoice",

    # Optional provenance
    prov_system="slack",
    prov_file_ids=["msg-456"],
    prov_page_num=1,

    # Your fields
    amount=1000,
    vendor="ACME Corp"
)

# Now you know:
# - This invoice came from Slack
# - From message msg-456
# - On page 1
```

### Why We Use It
- ✅ Know source of every entity
- ✅ Deduplicate data (same ID = same entity)
- ✅ Debug data issues
- ✅ Audit trail

### Deterministic IDs
```python
from lib.id_utils import generate_node_id

node_id = generate_node_id(
    entity_type="Invoice",
    business_keys={"invoice_id": "INV-001", "vendor": "ACME"},
    file_sha1="abc123",
    page_number=1
)

# Produces: invoice_INV-001_ACME_abc123_p1_<hash>
# Same input → Same ID → Deduplication
```

### Where to Find It
**Files**:
- `lib/provenance_fields.py` - NodeProv, EdgeProv mixins
- `lib/id_utils.py` - ID generation

### Try It
```python
from lib.provenance_fields import NodeProv
from pydantic import BaseModel

class MyEntity(NodeProv):
    name: str
    value: float

entity = MyEntity(
    node_id="test_001",
    entity_type="MyEntity",
    name="Example",
    value=42.0
)

print(entity.node_id)      # test_001
print(entity.entity_type)  # MyEntity
print(entity.name)         # Example
```

---

## How They Connect

```
Business YAML ──→ Instructor ──→ LinkML YAML ──→ gen-pydantic ──→ Pydantic Models
    ↑                  ↑              ↑                ↑                ↑
  Human           LLM call      Schema format     CLI tool         Python code
                 (typed)        (YAML)            (codegen)        (validated)
```

**Step by Step**:
1. **Human writes**: Business questions in YAML
2. **Instructor calls LLM**: Generate schema (typed response)
3. **LLM returns**: LinkML YAML schema
4. **LinkML generates**: Pydantic Python code
5. **Pydantic validates**: Data at runtime

---

## Files to Study (30 minutes)

Read these files in order:

### 1. Input (5 min)
```bash
cat dsl/examples/invoice_validation.yaml
```
See: Business questions we need to answer

### 2. LLM Agent (10 min)
```bash
cat agents/schema_synthesizer.py
```
See: How Instructor calls LLM and gets typed response

### 3. Schema (5 min)
```bash
cat schemas/overlays/invoice_overlay.yaml
```
See: LinkML schema (YAML format)

### 4. Generated Code (5 min)
```bash
cat generated/pydantic/invoice_models.py
```
See: Python models with validation

### 5. Tests (5 min)
```bash
cat validate_outcome.py
```
See: How we test if models work

---

## Experiments (30 minutes)

### Experiment 1: Change Business Question

**Goal**: See how pipeline responds to new requirements

```bash
# 1. Edit input
nano dsl/examples/invoice_validation.yaml

# 2. Add new question:
#    queries_we_must_answer:
#      - "What is the average invoice amount per department?"

# 3. Re-run pipeline
python demo_full_pipeline.py

# 4. Check if new model supports averaging
cat generated/pydantic/invoice_models.py | grep -i "department\|average"
```

### Experiment 2: Modify Schema

**Goal**: Add new field manually

```bash
# 1. Edit schema
nano schemas/overlays/invoice_overlay.yaml

# 2. Add field:
#    Invoice:
#      attributes:
#        tax_amount:
#          range: float

# 3. Regenerate Python
linkml generate pydantic schemas/overlays/invoice_overlay.yaml > generated/pydantic/invoice_models.py

# 4. Test import
python -c "from generated.pydantic.invoice_models import Invoice; print(Invoice.model_fields.keys())"
```

### Experiment 3: Break It (Learn from Errors)

**Goal**: Understand error messages

```bash
# 1. Edit schema with INVALID YAML
nano schemas/overlays/invoice_overlay.yaml
# (Add syntax error - wrong indentation)

# 2. Run lint
linkml lint schemas/overlays/invoice_overlay.yaml
# (See error message)

# 3. Fix it
# (Correct indentation)

# 4. Re-run lint
linkml lint schemas/overlays/invoice_overlay.yaml
# (Should pass)
```

### Experiment 4: Test Provenance

**Goal**: Track data source

```python
# test_provenance.py
from lib.provenance_fields import NodeProv

class Invoice(NodeProv):
    amount: float

invoice = Invoice(
    node_id="inv_001",
    entity_type="Invoice",
    prov_system="email",
    prov_file_ids=["email_123.pdf"],
    prov_page_num=2,
    amount=500.0
)

print(f"Source: {invoice.prov_system}")
print(f"File: {invoice.prov_file_ids}")
print(f"Page: {invoice.prov_page_num}")
```

```bash
python test_provenance.py
# Output:
# Source: email
# File: ['email_123.pdf']
# Page: 2
```

---

## Summary

### The Stack
1. **Instructor** = LLM returns typed objects
2. **LinkML** = Schema language (YAML → code)
3. **Pydantic** = Python validation models
4. **Provenance** = Track data sources

### The Flow
```
Business Need → LLM (Instructor) → Schema (LinkML) → Models (Pydantic) → Test
```

### Key Insight
Models are generated from business questions, then TESTED against those questions.

If models can't answer the questions → Reject and regenerate.

---

## What's Next?

### Option 1: Deep Dive (2-3 hours)
Study the full codebase:
- `graphmodels/` - Domain plugins
- `eval/` - Evaluation metrics
- `tests/` - Test suite

### Option 2: Build Your Own (see next doc)
Read `BUILD_YOUR_OWN.md` for:
- What to copy (concepts)
- What to change (your stack)
- Implementation plan

---

**Time spent**: ~1 hour
**Next**: BUILD_YOUR_OWN.md
