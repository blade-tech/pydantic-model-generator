# Concrete V1 vs. V2 Comparison Examples

## Example 1: BusinessOutcome Class

### **Current V1 (Working with Graphiti)**
```python
class BusinessOutcome(BaseModel):
    """A business deliverable or goal that needs to be achieved."""
    outcome_type: Optional[str] = Field(None, description="Type of outcome (deliverable, milestone, goal)")
    status: Optional[str] = Field(None, description="Current status (proposed, in_progress, completed, blocked)")
    priority: Optional[str] = Field(None, description="Priority level (low, medium, high, critical)")
    due_date: Optional[str] = Field(None, description="Deadline for completion (ISO format: YYYY-MM-DD or natural language)")
    for_customer: Optional[str] = Field(None, description="Customer or client name")
    in_project: Optional[str] = Field(None, description="Project identifier")
    owner: Optional[str] = Field(None, description="Person responsible")
    confidence_score: Optional[float] = Field(None, description="Confidence in achieving outcome (0-1)")
```

**Problems:**
1. ❌ No `model_config` - accepts unknown fields
2. ❌ No provenance tracking (node_id, entity_type, episode_ids)
3. ❌ `status` is string - can be "banana" instead of "proposed"
4. ❌ `priority` is string - no validation
5. ❌ `due_date` is string - can be "tomorrow" or "2024-13-99"
6. ❌ `confidence_score` is float - can be -5 or 100, not constrained to 0-1
7. ❌ `for_customer`, `in_project`, `owner` are deprecated back-refs (should be edges)

---

### **Recommended V2 (Aligned with Advice)**
```python
from enum import Enum
from datetime import datetime
from lib.provenance_fields import NodeProv

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
    """A business deliverable or goal that needs to be achieved."""

    # Strict validation (inherited from NodeProv)
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        arbitrary_types_allowed=False
    )

    # Business fields with proper types
    outcome_type: Optional[str] = None
    status: Optional[OutcomeStatus] = None  # ✅ Enum, not string
    priority: Optional[Priority] = None      # ✅ Enum, not string
    due_date: Optional[datetime] = None      # ✅ Datetime, not string
    confidence: Optional[float] = Field(None, ge=0, le=1)  # ✅ Constrained 0-1

    # Deprecated fields REMOVED - use edges instead:
    # ❌ for_customer  → Use (Customer)-[:Requires]->(BusinessOutcome)
    # ❌ in_project   → Use (Project)-[:Fulfills]->(BusinessOutcome)
    # ❌ owner        → Use (Actor)-[:ResponsibleFor]->(BusinessOutcome)

    # Inherited from NodeProv:
    # - node_id: str (deterministic SHA1)
    # - entity_type: str (= "BusinessOutcome")
    # - episode_ids: Optional[List[str]]
    # - created_at: Optional[datetime]
    # - valid_at: Optional[datetime]
    # - invalid_at: Optional[datetime]
```

**Improvements:**
1. ✅ Strict validation via `model_config`
2. ✅ Provenance tracking inherited from NodeProv
3. ✅ Status constrained to valid enum values
4. ✅ Priority constrained to valid enum values
5. ✅ Datetime validation on `due_date`
6. ✅ Numeric constraint on confidence (0-1)
7. ✅ Deprecated back-refs removed, use edges instead

---

## Example 2: BusinessDecision Class

### **Current V1**
```python
class BusinessDecision(BaseModel):
    """A crystallized choice or approval that affects business direction."""
    conclusion: Optional[str] = Field(None, description="What was decided")
    rationale: Optional[str] = Field(None, description="Why this decision was made")
    status: Optional[str] = Field(None, description="Status (proposed, approved, rejected, deferred)")
    owner: Optional[str] = Field(None, description="Decision maker")
    approved_by: Optional[str] = Field(None, description="Who approved the decision")
    approved_at: Optional[str] = Field(None, description="When it was approved (ISO format: YYYY-MM-DD or natural language)")
    impact_level: Optional[str] = Field(None, description="Impact level (low, medium, high)")
    reversible: Optional[bool] = Field(None, description="Can this decision be reversed")
```

**Problems:**
- ❌ String dates (`approved_at`)
- ❌ String enums (`status`, `impact_level`)
- ❌ No provenance

---

### **Recommended V2**
```python
class DecisionStatus(str, Enum):
    proposed = 'proposed'
    approved = 'approved'
    rejected = 'rejected'
    deferred = 'deferred'

class Severity(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'

class BusinessDecision(NodeProv):
    """A crystallized choice or approval that affects business direction."""

    title: Optional[str] = None
    conclusion: Optional[str] = None
    rationale: Optional[str] = None
    status: Optional[DecisionStatus] = None  # ✅ Enum
    approvers: Optional[List[str]] = None
    approved_at: Optional[datetime] = None   # ✅ Datetime
    impact_level: Optional[Severity] = None  # ✅ Enum
    reversible: Optional[bool] = None

    # Provenance inherited from NodeProv
```

---

## Example 3: Edge Classes

### **Current V1: Requires Edge**
```python
class Requires(BaseModel):
    """An outcome requires a decision or resource."""
    criticality: Optional[str] = Field(None, description="How critical (low, medium, high)")
    deadline: Optional[str] = Field(None, description="When requirement must be met (ISO format: YYYY-MM-DD or natural language)")
    blocker: Optional[bool] = Field(None, description="Is this blocking progress")
```

**Problems:**
- ❌ No edge provenance (rel_id, episode_ids, created_at)
- ❌ String enum (`criticality`)
- ❌ String date (`deadline`)

---

### **Recommended V2: Requires Edge**
```python
class Requires(EdgeProv):
    """An outcome requires a decision or resource."""

    criticality: Optional[Severity] = None   # ✅ Enum
    deadline: Optional[datetime] = None      # ✅ Datetime
    blocker: Optional[bool] = None

    # Inherited from EdgeProv:
    # - rel_id: str (deterministic SHA1)
    # - relation_type: str (= "Requires")
    # - episode_ids: Optional[List[str]]
    # - created_at: Optional[datetime]
    # - valid_at: Optional[datetime]
    # - expired_at: Optional[datetime]
```

---

## Example 4: Numeric Constraints

### **Current V1: Customer**
```python
class Customer(BaseModel):
    """A business customer or client entity."""
    contract_value: Optional[float] = Field(None, description="Annual contract value")
    # No constraint - can be -1000000 💀
```

### **Recommended V2: Customer**
```python
class Customer(NodeProv):
    """A business customer or client entity."""
    contract_value: Optional[float] = Field(None, ge=0)  # ✅ Must be non-negative
```

---

## Example 5: Complete Comparison Table

| Field | V1 Type | V1 Problem | V2 Type | V2 Benefit |
|-------|---------|------------|---------|-----------|
| `status` | `Optional[str]` | Any string accepted | `Optional[OutcomeStatus]` | Only valid enum values |
| `priority` | `Optional[str]` | Any string accepted | `Optional[Priority]` | Only valid enum values |
| `due_date` | `Optional[str]` | "banana" accepted | `Optional[datetime]` | Proper date validation |
| `approved_at` | `Optional[str]` | "2024-13-99" accepted | `Optional[datetime]` | ISO 8601 validation |
| `confidence_score` | `Optional[float]` | Can be -5 or 100 | `Optional[float] = Field(ge=0, le=1)` | Enforced 0-1 range |
| `contract_value` | `Optional[float]` | Can be negative | `Optional[float] = Field(ge=0)` | Non-negative enforced |
| `for_customer` | `Optional[str]` | String reference | **REMOVED** → Edge | Graph relationship |
| `owner` | `Optional[str]` | String reference | **REMOVED** → Edge | Graph relationship |
| **(no provenance)** | N/A | No tracking | `node_id`, `episode_ids`, `created_at` | Full lineage |

---

## What Validation Catches in V2 (That V1 Misses)

### **V1 Accepts Invalid Data:**
```python
# V1 - All of these are "valid" 💀
outcome = BusinessOutcome(
    status="banana",           # ❌ Not a valid status
    priority="super ultra",    # ❌ Not a valid priority
    due_date="next Tuesday",   # ❌ Not ISO 8601
    confidence_score=150.0,    # ❌ Not 0-1
    unknown_field="surprise"   # ❌ Extra field accepted
)
```

### **V2 Rejects Invalid Data:**
```python
# V2 - All of these raise ValidationError ✅
try:
    outcome = BusinessOutcome(
        status="banana",  # ValidationError: not a valid OutcomeStatus
    )
except ValidationError as e:
    print(e)

try:
    outcome = BusinessOutcome(
        confidence=150.0,  # ValidationError: must be <= 1
    )
except ValidationError as e:
    print(e)

try:
    outcome = BusinessOutcome(
        unknown_field="surprise",  # ValidationError: extra fields forbidden
    )
except ValidationError as e:
    print(e)
```

---

## Migration Path: V1 → V2

### **Step 1: Define Enums and Slots in LinkML**
```yaml
# schemas/overlays/business_overlay.yaml
enums:
  OutcomeStatus:
    permissible_values:
      proposed: {}
      in_progress: {}
      completed: {}
      blocked: {}

slots:
  status: { range: OutcomeStatus }
  due_date: { range: datetime }
  confidence: { range: float, minimum_value: 0, maximum_value: 1 }
```

### **Step 2: Generate V2 Models**
```bash
linkml generate pydantic schemas/overlays/business_overlay.yaml > generated/pydantic/business_models.py
```

### **Step 3: Update Graphiti Integration**
```python
# Old V1
from entities_Pydantiv_V1 import BUSINESS_ENTITY_TYPES, BUSINESS_EDGE_TYPES

# New V2
from generated.pydantic.business_models import (
    BusinessOutcome, BusinessDecision, ...
)
from business_glue import BUSINESS_ENTITY_TYPES, BUSINESS_EDGE_TYPES
```

---

## Bottom Line

**Your Current State:**
- ✅ V2 **foundation** complete (NodeProv/EdgeProv, ID utils)
- ✅ V2 **pattern validated** on Invoice example
- ❌ V2 **NOT applied** to Business entities yet

**The Gap:**
Business entities still use V1 pattern with:
- String enums (not type-safe)
- String dates (not validated)
- No numeric constraints
- No provenance tracking
- Deprecated back-references

**Next Step:**
Create `business_overlay.yaml` and generate V2 Business models before Graphiti integration.
