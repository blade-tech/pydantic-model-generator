# Schema Alignment Analysis: Current V1 vs. Recommended Pydantic V2

## Summary: Gap Analysis

Your **current Pydantic V1** (entities - Pydantiv V1.py) and the **Pydantic V2 upgrade we just completed** are **NOT yet aligned** with the recommended tightening advice. Here's what needs to be done:

---

## Current State vs. Recommendations

### ❌ **GAP 1: No Strict ConfigDict**

**Current V1:**
```python
class BusinessOutcome(BaseModel):
    outcome_type: Optional[str] = Field(None, ...)
```

**Problem:** No `model_config` with strict validation

**Recommended V2:**
```python
class BusinessOutcome(NodeProv):
    model_config = ConfigDict(
        extra="forbid",              # Reject unknown fields
        validate_assignment=True,    # Validate on updates
        arbitrary_types_allowed=False
    )
```

**Status:** ✅ Already implemented in `lib/provenance_fields.py` (NodeProv/EdgeProv have this)

---

### ❌ **GAP 2: No Provenance Mixins**

**Current V1:**
- No `node_id`, `entity_type`, `episode_ids`, temporal tracking
- Each entity is independent, no shared provenance pattern

**Recommended V2:**
```python
class BusinessOutcome(NodeProv):  # ← Inherits provenance
    # Business fields
    outcome_type: Optional[str] = None

    # Inherited from NodeProv:
    # - node_id: str (required)
    # - entity_type: str (required)
    # - episode_ids: Optional[List[str]]
    # - created_at, valid_at, invalid_at
```

**Status:** ✅ NodeProv/EdgeProv created, but **NOT yet applied to Business entities**

---

### ❌ **GAP 3: String Enums Instead of Proper Enums**

**Current V1:**
```python
status: Optional[str] = Field(None, description="Status (proposed, approved, rejected)")
priority: Optional[str] = Field(None, description="Priority (low, medium, high)")
```

**Problem:** No type safety, can accept any string

**Recommended V2:**
```python
from enum import Enum

class OutcomeStatus(str, Enum):
    proposed = 'proposed'
    in_progress = 'in_progress'
    completed = 'completed'
    blocked = 'blocked'

class Priority(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'
    critical = 'critical'

class BusinessOutcome(NodeProv):
    status: Optional[OutcomeStatus] = None
    priority: Optional[Priority] = None
```

**Status:** ❌ **NOT implemented** - all enums are still strings

---

### ❌ **GAP 4: String Dates Instead of Datetime**

**Current V1:**
```python
due_date: Optional[str] = Field(None, description="ISO format: YYYY-MM-DD or natural language")
approved_at: Optional[str] = Field(None, ...)
```

**Problem:** No type safety, no date validation

**Recommended V2:**
```python
from datetime import datetime

class BusinessOutcome(NodeProv):
    due_date: Optional[datetime] = Field(None, description="Deadline for completion")
    approved_at: Optional[datetime] = None
```

**Status:** ❌ **NOT implemented** - all dates are still strings

---

### ❌ **GAP 5: No Field Constraints on Numerics**

**Current V1:**
```python
confidence_score: Optional[float] = Field(None, description="Confidence (0-1)")
contract_value: Optional[float] = Field(None, description="Annual contract value")
```

**Problem:** No validation that confidence is actually 0-1, contract_value is non-negative

**Recommended V2:**
```python
class BusinessOutcome(NodeProv):
    confidence: Optional[float] = Field(None, ge=0, le=1)  # ← Enforces 0-1 range

class Customer(NodeProv):
    contract_value: Optional[float] = Field(None, ge=0)  # ← Enforces non-negative
```

**Status:** ❌ **NOT implemented** - no numeric constraints

---

### ❌ **GAP 6: Edge Classes Don't Inherit EdgeProv**

**Current V1:**
```python
class Requires(BaseModel):
    criticality: Optional[str] = Field(None, ...)
    deadline: Optional[str] = Field(None, ...)
```

**Problem:** No edge provenance (rel_id, source episodes, temporal tracking)

**Recommended V2:**
```python
class Requires(EdgeProv):  # ← Inherits edge provenance
    criticality: Optional[Severity] = None  # ← Enum, not string
    deadline: Optional[datetime] = None     # ← Datetime, not string

    # Inherited from EdgeProv:
    # - rel_id: str (required)
    # - relation_type: str (required)
    # - episode_ids, created_at, valid_at, expired_at
```

**Status:** ✅ EdgeProv created, but **NOT yet applied to Business edges**

---

### ❌ **GAP 7: Deprecated Back-References Still Present**

**Current V1:**
```python
class BusinessOutcome(BaseModel):
    for_customer: Optional[str] = Field(None, description="Customer or client name")
    in_project: Optional[str] = Field(None, ...)
    owner: Optional[str] = Field(None, ...)
```

**Problem:** These should be **edges** (Customer→Outcome, Project→Outcome, Actor→Outcome), not embedded strings

**Recommended V2:**
```python
class BusinessOutcome(NodeProv):
    # NO for_customer, in_project, owner fields
    # Use edges instead:
    # - (Customer)-[:Requires]->(BusinessOutcome)
    # - (Project)-[:Fulfills]->(BusinessOutcome)
    # - (Actor)-[:ResponsibleFor]->(BusinessOutcome)
```

**Status:** ❌ **NOT removed** - deprecated fields still in V1

---

## What We've Completed So Far

✅ **Created Foundation:**
- `lib/provenance_fields.py` with NodeProv/EdgeProv
- `lib/id_utils.py` with deterministic ID generation
- LinkML core schema with provenance mixins

✅ **Validated Pattern on Invoice Example:**
- Invoice overlay schema uses NodeProv correctly
- Generated Pydantic models inherit provenance
- All 6 validation tests pass

❌ **NOT Yet Applied to Business Entities:**
- Business entities still use old V1 pattern
- No enums, no datetime fields, no constraints
- No NodeProv/EdgeProv inheritance

---

## Required Changes to Align V1 with V2 Recommendations

### 1. **Create Business Domain LinkML Schema**

Create `schemas/overlays/business_overlay.yaml`:

```yaml
id: https://example.org/graphmodels/business
name: business_validation
imports:
  - ../core

# Define enums at schema level
enums:
  OutcomeStatus:
    permissible_values:
      proposed: {}
      in_progress: {}
      completed: {}
      blocked: {}

  Priority:
    permissible_values:
      low: {}
      medium: {}
      high: {}
      critical: {}

  Severity:
    permissible_values:
      low: {}
      medium: {}
      high: {}

slots:
  outcome_type: { range: string }
  status: { range: OutcomeStatus }
  priority: { range: Priority }
  due_date: { range: datetime }
  confidence: { range: float, minimum_value: 0, maximum_value: 1 }
  # ... etc for all fields

classes:
  BusinessOutcome:
    mixins: [NodeProv]
    slots:
      - outcome_type
      - status
      - priority
      - due_date
      - confidence
```

### 2. **Generate Pydantic V2 Models**

```bash
linkml generate pydantic schemas/overlays/business_overlay.yaml > generated/pydantic/business_models.py
```

### 3. **Replace V1 Entities File**

Replace `entities - Pydantiv V1.py` with generated models + glue:

```python
# generated/pydantic/business_models.py (auto-generated by LinkML)
from lib.provenance_fields import NodeProv, EdgeProv

class BusinessOutcome(NodeProv):
    # Auto-generated with:
    # - Proper enums (OutcomeStatus, Priority)
    # - Datetime fields (not strings)
    # - Numeric constraints (ge=0, le=1)
    # - Inherited provenance (node_id, entity_type, episode_ids)
    ...

# business_glue.py (handwritten registries)
BUSINESS_ENTITY_TYPES = {
    "BusinessOutcome": BusinessOutcome,
    # ... etc
}
```

---

## Action Items (Priority Order)

### **HIGH PRIORITY - Foundation Alignment**

1. ✅ **DONE:** Create provenance mixins (`lib/provenance_fields.py`)
2. ✅ **DONE:** Create ID utilities (`lib/id_utils.py`)
3. ✅ **DONE:** Validate pattern on Invoice example

### **NEXT STEP - Business Schema Upgrade**

4. ❌ **TODO:** Create `schemas/overlays/business_overlay.yaml` with:
   - Proper enum definitions (OutcomeStatus, Priority, Severity, etc.)
   - Datetime fields (not strings)
   - Numeric constraints (ge, le for confidence, contract_value)
   - Remove deprecated back-references (for_customer, in_project, owner)
   - Add proper edge associations

5. ❌ **TODO:** Generate Business Pydantic V2 models from LinkML

6. ❌ **TODO:** Create `business_glue.py` with registries and edge maps

7. ❌ **TODO:** Update Graphiti integration to use new Business V2 models

---

## Comparison Table: V1 vs. V2 Features

| Feature | Current V1 | Our V2 (lib/) | Recommended V2 (Advice) | Status |
|---------|-----------|---------------|------------------------|---------|
| **Provenance Tracking** | ❌ None | ✅ NodeProv/EdgeProv | ✅ NodeProv/EdgeProv | ✅ Foundation ready, not applied to Business |
| **Deterministic IDs** | ❌ None | ✅ SHA1-based | ✅ SHA1-based | ✅ Utilities ready |
| **Strict Validation** | ❌ No ConfigDict | ✅ extra="forbid" | ✅ extra="forbid" | ✅ In mixins |
| **Enums for Status** | ❌ Strings | ❌ Not yet | ✅ Enums | ❌ Need to implement |
| **Datetime Fields** | ❌ Strings | ❌ Not yet | ✅ datetime | ❌ Need to implement |
| **Numeric Constraints** | ❌ None | ❌ Not yet | ✅ ge, le | ❌ Need to implement |
| **Edge Provenance** | ❌ BaseModel | ✅ EdgeProv | ✅ EdgeProv | ✅ Foundation ready, not applied |
| **LinkML as Source** | ❌ Handwritten | ✅ Invoice only | ✅ All schemas | ⚠️ Partial |

---

## Recommended Next Action

**Option 1: Apply V2 Pattern to Business Entities NOW**
- Create `business_overlay.yaml` with proper enums, datetime, constraints
- Generate V2 Business models
- Replace V1 entities file
- Update Graphiti integration

**Option 2: Continue with Graphiti Integration Using V1**
- Keep V1 entities working with Graphiti
- Upgrade to V2 Business models later as separate task
- Focus on Graphiti adapter first

**My Recommendation:** Option 1 - apply V2 pattern to Business entities now before Graphiti integration, because:
1. Easier to migrate while Graphiti integration is fresh
2. Avoid double-migration later (V1→Graphiti, then V1→V2→Graphiti)
3. Foundation is already complete (NodeProv/EdgeProv ready)
4. Invoice example proves the pattern works

---

## Answer to Your Question

> "Is our current 'Pydantic V2' already aligned with this?"

**Short Answer:** **Partially aligned**

**What's Aligned:**
✅ Foundation complete (NodeProv/EdgeProv with strict ConfigDict)
✅ Deterministic ID utilities ready
✅ Pattern validated on Invoice example

**What's NOT Aligned:**
❌ Business entities still use V1 pattern (no enums, string dates, no constraints)
❌ No LinkML schema for Business domain yet
❌ Deprecated back-references still present
❌ Edge classes don't inherit EdgeProv

**Gap:** Foundation is ready, but **not yet applied** to your working Business entities.
