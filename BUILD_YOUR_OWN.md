# Build Your Own Version (1 Hour)

## What to Copy vs What to Change

### ✅ Copy These Concepts (Keep Forever)

#### 1. Outcome-First Design
- **What**: Start with business questions, generate only needed models
- **Why**: Prevents over-modeling
- **How**: Define questions → Generate schema → Test if schema answers questions

#### 2. Structured LLM Outputs
- **What**: Use Instructor (or similar) to get typed responses
- **Why**: No text parsing, no validation errors
- **How**: Define Pydantic response schema → LLM fills it

#### 3. Provenance Tracking
- **What**: Every entity knows its source
- **Why**: Debugging, deduplication, audit trail
- **How**: NodeProv mixin with deterministic IDs

#### 4. Fail-Fast Evaluation
- **What**: Test schema before deployment
- **Why**: Reject bad models early
- **How**: Golden set of questions → Test retrieval → Pass/Fail gates

---

### ❌ Don't Copy These (Choose Your Own)

#### 1. LinkML
**This repo uses**: LinkML YAML → Python codegen

**You might use**:
- Direct Pydantic generation (simpler)
- TypeScript types (if JS stack)
- Protocol Buffers (if cross-language)
- JSON Schema (if API-first)

**Choose based on**: Your team's skills, existing stack

#### 2. OpenAI
**This repo uses**: GPT-4 via Instructor

**You might use**:
- Claude (Anthropic) - better reasoning
- Gemini (Google) - multimodal
- Local LLMs (Ollama) - privacy/cost
- Azure OpenAI - enterprise

**Choose based on**: Budget, privacy needs, performance

#### 3. Neo4j/Graphiti
**This repo uses**: Neo4j graph database + Graphiti

**You might use**:
- PostgreSQL - relational, simpler
- MongoDB - document store
- Elasticsearch - search-first
- Your existing database

**Choose based on**: Your data structure, query patterns

---

## Your Architecture Decision Checklist

Before building, answer these questions:

### 1. Schema Format?
- [ ] LinkML (like this repo) - YAML, multi-target
- [ ] Direct Pydantic - simpler, Python-only
- [ ] TypeScript - if JS/TS stack
- [ ] JSON Schema - API-first
- [ ] Other: __________

**My choice**: __________ **Why**: __________

### 2. LLM Provider?
- [ ] OpenAI (like this repo) - GPT-4, GPT-4o
- [ ] Claude - better reasoning, longer context
- [ ] Gemini - multimodal capabilities
- [ ] Local (Ollama) - privacy, no API costs
- [ ] Other: __________

**My choice**: __________ **Why**: __________

### 3. Structured Output Tool?
- [ ] Instructor (like this repo) - Pydantic-first
- [ ] Native function calling - provider-specific
- [ ] JSON mode - simpler, less reliable
- [ ] Guidance/Outlines - local LLMs
- [ ] Other: __________

**My choice**: __________ **Why**: __________

### 4. Database?
- [ ] Neo4j (like this repo) - graph
- [ ] PostgreSQL - relational
- [ ] MongoDB - documents
- [ ] Elasticsearch - search
- [ ] Other: __________

**My choice**: __________ **Why**: __________

---

## Minimal Implementation (Start Simple)

### Step 1: Input Format (15 minutes)

Define how users specify needs.

**Option A: Simple Dict**
```python
need = {
    "questions": [
        "Can invoice be approved?",
        "Which invoices are blocked?"
    ],
    "entities": ["Invoice", "Budget", "Vendor"]
}
```

**Option B: YAML (like this repo)**
```yaml
outcome_name: "Invoice Validation"
queries_we_must_answer:
  - "Can invoice be approved?"
  - "Which invoices are blocked?"
target_entities:
  - name: Invoice
    must_have_slots: [amount, vendor_id]
```

**Option C: Natural Language**
```python
need = """
I need to approve invoices based on:
- Budget availability
- Vendor approval status
- Purchase order existence
"""
```

**Your choice**: __________

### Step 2: LLM Call (30 minutes)

Generate schema from needs.

**Using Instructor** (recommended):
```python
import instructor
from pydantic import BaseModel
from openai import OpenAI

class GeneratedSchema(BaseModel):
    entities: list[str]
    fields: dict[str, list[str]]
    relationships: list[dict[str, str]]

client = instructor.from_openai(OpenAI())

schema = client.chat.completions.create(
    model="gpt-4",
    response_model=GeneratedSchema,
    messages=[{
        "role": "user",
        "content": f"Generate data model for: {need}"
    }]
)

print(schema.entities)  # ['Invoice', 'Budget', 'Vendor']
print(schema.fields)    # {'Invoice': ['id', 'amount'], ...}
```

**Alternative: Function Calling**
```python
tools = [{
    "type": "function",
    "function": {
        "name": "generate_schema",
        "parameters": {
            "type": "object",
            "properties": {
                "entities": {"type": "array", "items": {"type": "string"}},
                "fields": {"type": "object"}
            }
        }
    }
}]

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": f"Generate schema: {need}"}],
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "generate_schema"}}
)

schema = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
```

**Your choice**: __________

### Step 3: Generate Models (15 minutes)

Convert schema to code.

**Option A: Dynamic Pydantic**
```python
from pydantic import create_model

models = {}
for entity in schema.entities:
    models[entity] = create_model(
        entity,
        **{field: (str, ...) for field in schema.fields[entity]}
    )

# Use it
Invoice = models["Invoice"]
invoice = Invoice(id="INV-001", amount="1000")
```

**Option B: Code Generation (like this repo)**
```python
# Generate Python code as string
code = ""
for entity in schema.entities:
    code += f"class {entity}(BaseModel):\n"
    for field in schema.fields[entity]:
        code += f"    {field}: str\n"
    code += "\n"

# Write to file
with open("models.py", "w") as f:
    f.write(code)

# Import dynamically
import importlib.util
spec = importlib.util.spec_from_file_location("models", "models.py")
models = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models)
```

**Option C: Template Engine**
```python
from jinja2 import Template

template = Template("""
{% for entity in entities %}
class {{ entity }}(BaseModel):
{% for field in fields[entity] %}
    {{ field }}: str
{% endfor %}

{% endfor %}
""")

code = template.render(entities=schema.entities, fields=schema.fields)
```

**Your choice**: __________

### Step 4: Test (30 minutes)

Validate models answer business questions.

```python
def test_business_outcome(models, questions, test_data):
    results = []

    for question in questions:
        # Simple rule-based check (expand later)
        if "approved" in question.lower():
            # Can we determine approval?
            Invoice = models["Invoice"]
            try:
                # Try to use approval logic
                invoice = Invoice(**test_data["invoice"])
                approved = (
                    invoice.amount <= test_data["budget"]["limit"] and
                    invoice.vendor_approved == True
                )
                results.append(("PASS", question))
            except Exception as e:
                results.append(("FAIL", question, str(e)))

    return results

# Run test
test_data = {
    "invoice": {"id": "1", "amount": "1000", "vendor_approved": "true"},
    "budget": {"limit": "5000"}
}

results = test_business_outcome(
    models=models,
    questions=["Can invoice be approved?"],
    test_data=test_data
)

for result in results:
    print(result)
```

**Your approach**: __________

---

## 4-Week Implementation Plan

### Week 1: Learn & Setup
- [ ] Day 1-2: Run demo from this repo, understand pipeline
- [ ] Day 3: Read TECH_STACK.md, understand components
- [ ] Day 4-5: Make architecture decisions (checklist above)

**Deliverable**: Architecture decision document

### Week 2: Build MVP
- [ ] Day 1: Implement LLM call with Instructor
- [ ] Day 2: Generate simple models (dynamic Pydantic)
- [ ] Day 3: Add basic tests
- [ ] Day 4-5: Test with real business case

**Deliverable**: Working prototype (1 use case)

### Week 3: Add Features
- [ ] Day 1-2: Add provenance tracking
- [ ] Day 3-4: Add evaluation metrics
- [ ] Day 5: Handle multiple domains

**Deliverable**: Production-ready MVP

### Week 4: Deploy & Iterate
- [ ] Day 1-2: Deploy to production
- [ ] Day 3: Monitor, fix issues
- [ ] Day 4-5: Plan next features

**Deliverable**: Live system, improvement backlog

---

## Key Differences to Make

This repo is a teaching tool. Your version should be:

### 1. Production Quality
```python
# This repo (POC)
schema = llm_call(need)  # No error handling

# Your version (Production)
try:
    schema = llm_call(need)
except LLMError as e:
    logger.error(f"LLM failed: {e}")
    return fallback_schema()
except ValidationError as e:
    logger.error(f"Validation failed: {e}")
    return retry_with_feedback(e)
```

### 2. Your Stack
```python
# This repo
client = instructor.from_openai(OpenAI())  # OpenAI only

# Your version
if config.llm_provider == "claude":
    client = instructor.from_anthropic(Anthropic())
elif config.llm_provider == "local":
    client = instructor.from_ollama(Ollama())
```

### 3. Your Use Case
```python
# This repo (Invoice example)
entities = ["Invoice", "Budget", "Vendor"]

# Your version (E-commerce)
entities = ["Product", "Order", "Customer", "Inventory"]

# Or Healthcare
entities = ["Patient", "Appointment", "Prescription"]

# Or Finance
entities = ["Transaction", "Account", "Portfolio"]
```

---

## Success Criteria

You've succeeded when you can answer YES to:

- [ ] Can you explain the pipeline to a colleague?
- [ ] Did you build something DIFFERENT (not a copy)?
- [ ] Does your version fit YOUR use case better?
- [ ] Did you make conscious tradeoff decisions?
- [ ] Can you modify/extend it easily?

---

## Common Questions

### Q: Should I use LinkML?
**A**: Only if you need multi-target generation (Pydantic + GraphQL + JSON-LD). Otherwise, generate Pydantic directly.

### Q: Do I need a graph database?
**A**: No. Use what fits your query patterns. Relational DB works fine for many cases.

### Q: How do I handle schema evolution?
**A**: Version your schemas. Keep old + new models. Migrate data gradually.

### Q: What if LLM generates wrong schema?
**A**: Use Instructor's retry mechanism. Add validation. Provide examples in prompt.

### Q: How to make it faster?
**A**: Cache LLM responses. Use smaller models. Generate schemas offline, use at runtime.

---

## Next Steps

1. **Fill out the decision checklist** (30 min)
2. **Sketch your architecture** on paper (30 min)
3. **Build Step 1 (Input format)** today
4. **Build Step 2 (LLM call)** tomorrow
5. **Build Step 3 (Generate models)** this week
6. **Build Step 4 (Tests)** next week

---

## Resources

### This Repo
- `START_HERE.md` - Quick start
- `TECH_STACK.md` - How it works
- `agents/` - Reference implementations
- `tests/` - Test patterns

### External
- [Instructor Docs](https://python.useinstructor.com/) - Structured outputs
- [Pydantic Docs](https://docs.pydantic.dev/) - Data validation
- [LinkML Docs](https://linkml.io/) - Schema language (optional)

---

**Time spent**: ~1 hour
**Outcome**: Architecture decisions made, ready to build

---

## Final Reminder

**This repo teaches the PATTERN**:
```
Business Questions → Auto-Generate Models → Test if Models Work
```

**Your job**: Build this pattern YOUR way, for YOUR use case.

Don't copy code. Copy concepts. Build better.

---

**Ready to build?** Start with the decision checklist above ↑
