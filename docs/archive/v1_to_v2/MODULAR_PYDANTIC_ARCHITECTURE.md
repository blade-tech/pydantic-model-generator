# Modular Pydantic Model Architecture

## Executive Summary

This document outlines best practices for creating modular Pydantic model structures based on:
1. Analysis of existing `graphmodels/` implementation
2. Research on Pydantic/FastAPI project organization patterns
3. LinkML schema modularization strategies
4. Domain-Driven Design (DDD) principles

---

## 1. Current Architecture Analysis

### Existing Structure (`graphmodels/`)

```
graphmodels/
├── __init__.py                    # Package root
├── core/                          # Shared infrastructure
│   ├── __init__.py               # Core exports
│   ├── provenance.py             # NodeProv, EdgeProv mixins
│   ├── ids.py                    # ID generation utilities
│   ├── registries.py             # Global model registries
│   └── plugin_loader.py          # Domain discovery/loading
└── domains/                       # Domain plugins
    ├── __init__.py
    ├── business/                  # Business workflow domain
    │   └── __init__.py           # ENTITIES, EDGES exports
    ├── aaoifi/                    # Islamic finance standards domain
    │   └── __init__.py
    └── murabaha_audit/            # Audit domain
        └── __init__.py
```

### ✅ Strengths of Current Design

1. **Clear Separation of Concerns**
   - `core/`: Reusable infrastructure (provenance, IDs, registries)
   - `domains/`: Business logic organized by domain

2. **Plugin Architecture**
   - Automatic domain discovery via `plugin_loader.py`
   - Loose coupling between domains
   - Easy to add new domains without modifying core

3. **Global Registry Pattern**
   - Central `_ENTITY_REGISTRY` and `_EDGE_REGISTRY`
   - Runtime model lookup by entity/edge type string
   - Prevents type conflicts across domains

4. **Standardized Provenance**
   - `NodeProv` and `EdgeProv` mixins provide consistent metadata
   - Temporal tracking (`valid_at`, `invalid_at`, `expired_at`)
   - Episode-based provenance for citation

---

## 2. Recommended Architecture Patterns

### 2.1 Three-Layer Domain Organization

Based on Domain-Driven Design and FastAPI best practices:

```
graphmodels/
├── core/                          # Layer 1: Infrastructure
│   ├── base.py                   # Base models, ConfigDict
│   ├── provenance.py             # Provenance mixins
│   ├── types.py                  # Custom types (Email, E164Phone, Confidence01)
│   ├── ids.py                    # ID generation
│   ├── registries.py             # Global registries
│   └── plugin_loader.py          # Plugin system
│
└── domains/                       # Layer 2: Domain Logic
    ├── [domain_name]/
    │   ├── __init__.py           # Domain plugin entry point
    │   ├── models.py             # Pydantic models (generated or hand-written)
    │   ├── schemas.py            # LinkML YAML schemas (source of truth)
    │   ├── enums.py              # Domain-specific enums
    │   ├── types.py              # Domain-specific custom types
    │   ├── validators.py         # Custom Pydantic validators
    │   └── glue.py               # ENTITIES/EDGES registries
    │
    └── shared/                    # Layer 3: Cross-Domain Shared Models
        ├── geography.py          # Address, Country, etc.
        ├── financial.py          # Money, Currency, etc.
        ├── temporal.py           # DateRange, Period, etc.
        └── identity.py           # Person, Organization, etc.
```

### 2.2 File Naming Conventions

| File | Purpose | Contents |
|------|---------|----------|
| `models.py` | Pydantic models | Entity and edge classes |
| `schemas.py` | LinkML schemas | YAML source (if using LinkML) |
| `enums.py` | Enumerations | Python Enum classes for categorical data |
| `types.py` | Custom types | NewType, annotated types, custom validators |
| `validators.py` | Field validators | `@field_validator`, `@model_validator` |
| `glue.py` | Registries | `ENTITIES`, `EDGES` dictionaries |
| `__init__.py` | Public API | Exports for domain plugin |

---

## 3. LinkML Schema Modularization

### 3.1 Schema Organization

**Recommended Directory Structure:**

```
schemas/
├── core/
│   ├── provenance.yaml           # ProvenanceFields, EdgeProvenanceFields mixins
│   ├── types.yaml                # Custom types (Email, Confidence01, etc.)
│   └── base.yaml                 # Base classes, ConfigDict settings
│
├── shared/                        # Cross-domain schemas
│   ├── geography.yaml
│   ├── financial.yaml
│   └── temporal.yaml
│
└── domains/
    ├── business/
    │   ├── business_v2.yaml      # Main schema
    │   ├── entities.yaml         # Entity definitions
    │   └── edges.yaml            # Edge/relationship definitions
    │
    └── aaoifi/
        ├── aaoifi_v1.yaml
        ├── documents.yaml
        └── standards.yaml
```

### 3.2 LinkML Schema Imports

**Example: `business_v2.yaml`**

```yaml
id: https://example.org/business_v2
name: business_v2

# Import shared schemas
imports:
  - ../../core/provenance       # Provenance mixins
  - ../../core/types            # Custom types
  - ../../shared/geography      # Address, Location
  - ../../shared/financial      # Money, Currency

prefixes:
  linkml: https://w3id.org/linkml/
  business: https://example.org/business_v2/

default_prefix: business

# Domain-specific enums
enums:
  OutcomeStatus:
    permissible_values:
      proposed: {}
      in_progress: {}
      completed: {}
      blocked: {}

# Domain-specific classes
classes:
  BusinessOutcome:
    mixins:
      - ProvenanceFields       # From core/provenance.yaml
    slots:
      - outcome_type
      - status
      - priority
      - due_date
      - confidence
```

### 3.3 Benefits of Modular LinkML Schemas

1. **Single Source of Truth**: One schema file per domain
2. **Reusable Components**: Shared mixins (provenance), types, enums
3. **Versioning**: Independent domain schema versions
4. **Namespace Isolation**: Prevent naming conflicts
5. **Incremental Generation**: Only regenerate changed domains

---

## 4. Domain Plugin Pattern

### 4.1 Plugin Structure

Each domain follows a standardized plugin pattern:

**`domains/business/__init__.py`**

```python
"""
Business Domain Plugin

Provides:
- Entity models: BusinessOutcome, BusinessTask, etc.
- Edge models: Requires, Fulfills, etc.
"""

from .models import (
    # Entities
    BusinessOutcome,
    BusinessTask,
    # Edges
    Requires,
    Fulfills,
)
from .glue import BUSINESS_ENTITIES, BUSINESS_EDGES

# Export for plugin loader
ENTITIES = BUSINESS_ENTITIES
EDGES = BUSINESS_EDGES

__all__ = [
    "BusinessOutcome",
    "BusinessTask",
    "Requires",
    "Fulfills",
    "ENTITIES",
    "EDGES",
]
```

**`domains/business/glue.py`**

```python
"""Business domain registries."""

from typing import Dict, Type
from pydantic import BaseModel
from .models import (
    BusinessOutcome,
    BusinessTask,
    Requires,
    Fulfills,
)

BUSINESS_ENTITIES: Dict[str, Type[BaseModel]] = {
    "BusinessOutcome": BusinessOutcome,
    "BusinessTask": BusinessTask,
}

BUSINESS_EDGES: Dict[str, Type[BaseModel]] = {
    "REQUIRES": Requires,
    "FULFILLS": Fulfills,
}
```

### 4.2 Plugin Discovery and Loading

The existing `plugin_loader.py` provides automatic domain discovery:

```python
from pathlib import Path
from graphmodels.core import load_all_domains

# Automatically discover and load all domains
domains_path = Path("graphmodels/domains")
loaded_domains = load_all_domains(domains_path)

print(f"Loaded domains: {', '.join(loaded_domains)}")
# Output: Loaded domains: business, aaoifi, murabaha_audit
```

**Benefits:**
- No manual registration required
- Add new domain → automatically discovered
- Failed domains don't break other domains
- Runtime introspection of available models

---

## 5. Best Practices

### 5.1 Model Organization

**✅ DO:**

1. **One Domain Per Directory**
   ```
   domains/business/
   domains/aaoifi/
   domains/customer_success/
   ```

2. **Separate Entities and Edges**
   ```python
   # models.py
   class BusinessOutcome(NodeProv):  # Entity
       ...

   class Requires(EdgeProv):         # Edge
       ...
   ```

3. **Use Mixins for Shared Behavior**
   ```python
   class NodeProv(BaseModel):
       node_id: str
       entity_type: str
       episode_ids: Optional[List[str]]

   class BusinessOutcome(NodeProv):  # Inherits provenance
       status: OutcomeStatus
   ```

4. **Register with Unique Keys**
   ```python
   ENTITIES = {
       "BusinessOutcome": BusinessOutcome,  # Key = entity_type
   }

   EDGES = {
       "REQUIRES": Requires,                # Key = relation_type
   }
   ```

**❌ DON'T:**

1. **Mix Domains in One File**
   ```python
   # BAD: All domains in models.py
   class BusinessOutcome(BaseModel): ...
   class Invoice(BaseModel): ...
   class AuditLog(BaseModel): ...
   ```

2. **Hardcode Domain Logic in Core**
   ```python
   # BAD: core/base.py should not know about domains
   from domains.business.models import BusinessOutcome
   ```

3. **Duplicate Provenance Fields**
   ```python
   # BAD: Each model defines node_id
   class BusinessOutcome(BaseModel):
       node_id: str  # ❌ Duplicate

   class Invoice(BaseModel):
       node_id: str  # ❌ Duplicate

   # GOOD: Use mixin
   class BusinessOutcome(NodeProv):
       pass  # ✅ Inherits node_id
   ```

### 5.2 Configuration Standards

**Base ConfigDict (core/base.py):**

```python
from pydantic import BaseModel, ConfigDict

class GraphModel(BaseModel):
    """Base model for all graph entities and edges."""

    model_config = ConfigDict(
        extra="ignore",                  # Allow unknown fields (graph flexibility)
        validate_assignment=True,        # Validate on field assignment
        str_strip_whitespace=True,       # Strip whitespace from strings
        populate_by_name=True,           # Allow field aliases
        arbitrary_types_allowed=True,    # Allow custom types
        use_enum_values=True,            # Use enum values in serialization
    )
```

**Domain-Specific Config Override:**

```python
class StrictBusinessModel(BaseModel):
    """Business models with strict validation."""

    model_config = ConfigDict(
        extra="forbid",                  # Reject unknown fields
        validate_assignment=True,
        str_strip_whitespace=True,
    )
```

### 5.3 Type Safety and Validation

**Custom Types (core/types.py):**

```python
from typing import Annotated
from pydantic import Field, field_validator
import re

# Email with pattern validation
Email = Annotated[
    str,
    Field(pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
]

# E.164 phone format
E164Phone = Annotated[
    str,
    Field(pattern=r'^\+[1-9]\d{1,14}$')
]

# Confidence score (0-1 range)
Confidence01 = Annotated[
    float,
    Field(ge=0.0, le=1.0)
]
```

**Field Validators (domains/business/validators.py):**

```python
from pydantic import field_validator, model_validator

class BusinessOutcome(NodeProv):
    status: OutcomeStatus
    priority: Priority

    @field_validator('status', mode='before')
    @classmethod
    def canonicalize_status(cls, v):
        """Canonicalize status input ('In Progress' → 'in_progress')."""
        if isinstance(v, str):
            return v.lower().replace(' ', '_').replace('-', '_')
        return v

    @model_validator(mode='after')
    def validate_blocked_outcome(self):
        """Blocked outcomes must have blocking_reason."""
        if self.status == OutcomeStatus.blocked and not self.blocking_reason:
            raise ValueError("Blocked outcomes require blocking_reason")
        return self
```

### 5.4 Registry Pattern

**Global Registry (core/registries.py):**

```python
_ENTITY_REGISTRY: Dict[str, Type[BaseModel]] = {}
_EDGE_REGISTRY: Dict[str, Type[BaseModel]] = {}

def register_domain(domain_name: str, entities: dict, edges: dict):
    """Register domain models globally."""
    for entity_type, model_cls in entities.items():
        if entity_type in _ENTITY_REGISTRY:
            raise ValueError(f"Duplicate entity type: {entity_type}")
        _ENTITY_REGISTRY[entity_type] = model_cls

    for relation_type, model_cls in edges.items():
        if relation_type in _EDGE_REGISTRY:
            raise ValueError(f"Duplicate relation type: {relation_type}")
        _EDGE_REGISTRY[relation_type] = model_cls
```

**Runtime Model Lookup:**

```python
from graphmodels.core import get_entity_model

# Get model class by entity type string
model_cls = get_entity_model("BusinessOutcome")
if model_cls:
    instance = model_cls(
        node_id="outcome-123",
        entity_type="BusinessOutcome",
        status="in_progress"
    )
```

---

## 6. Migration Strategy

### 6.1 Current State → Recommended State

**Phase 1: Organize Schemas**
```bash
# Create modular LinkML schemas
mkdir -p schemas/{core,shared,domains}

# Move existing schemas
mv schemas/business_model_v2.yaml schemas/domains/business/
mv schemas/aaoifi_schema.yaml schemas/domains/aaoifi/

# Extract common patterns to core
# - Create schemas/core/provenance.yaml
# - Create schemas/core/types.yaml
```

**Phase 2: Update Imports**
```yaml
# schemas/domains/business/business_v2.yaml
imports:
  - ../../core/provenance
  - ../../core/types
```

**Phase 3: Regenerate Models**
```bash
cd schemas/domains/business
gen-pydantic business_v2.yaml \
  --template-dir ../../../v1_to_v2_migration/templates \
  > ../../../generated/pydantic/business_models.py
```

**Phase 4: Update Glue Files**
```python
# generated/pydantic/business_glue.py
from generated.pydantic.business_models import (
    BusinessOutcome,
    BusinessTask,
    # ... all models
)

BUSINESS_ENTITIES = {
    "BusinessOutcome": BusinessOutcome,
    "BusinessTask": BusinessTask,
}
```

### 6.2 Adding a New Domain

**Step 1: Create Domain Directory**
```bash
mkdir -p graphmodels/domains/new_domain
touch graphmodels/domains/new_domain/__init__.py
```

**Step 2: Create LinkML Schema**
```yaml
# schemas/domains/new_domain/schema.yaml
id: https://example.org/new_domain
name: new_domain

imports:
  - ../../core/provenance
  - ../../core/types

classes:
  MyEntity:
    mixins:
      - ProvenanceFields
    slots:
      - my_field
```

**Step 3: Generate Pydantic Models**
```bash
gen-pydantic schemas/domains/new_domain/schema.yaml \
  --template-dir v1_to_v2_migration/templates \
  > generated/pydantic/new_domain_models.py
```

**Step 4: Create Glue File**
```python
# generated/pydantic/new_domain_glue.py
from generated.pydantic.new_domain_models import MyEntity

NEW_DOMAIN_ENTITIES = {
    "MyEntity": MyEntity,
}

NEW_DOMAIN_EDGES = {}
```

**Step 5: Create Plugin Entry Point**
```python
# graphmodels/domains/new_domain/__init__.py
from generated.pydantic.new_domain_glue import (
    NEW_DOMAIN_ENTITIES,
    NEW_DOMAIN_EDGES,
)

ENTITIES = NEW_DOMAIN_ENTITIES
EDGES = NEW_DOMAIN_EDGES

__all__ = ["ENTITIES", "EDGES"]
```

**Step 6: Auto-Discovery**
```python
# Automatically loaded by plugin_loader.py
from graphmodels.core import load_all_domains
from pathlib import Path

domains = load_all_domains(Path("graphmodels/domains"))
# Output: ['business', 'aaoifi', 'murabaha_audit', 'new_domain']
```

---

## 7. Testing Strategy

### 7.1 Unit Tests per Domain

```
tests/
├── core/
│   ├── test_provenance.py
│   ├── test_ids.py
│   └── test_registries.py
│
└── domains/
    ├── business/
    │   ├── test_business_entities.py
    │   ├── test_business_edges.py
    │   └── test_business_validators.py
    │
    └── aaoifi/
        ├── test_aaoifi_entities.py
        └── test_aaoifi_edges.py
```

### 7.2 Integration Tests

```python
# tests/test_plugin_system.py
def test_domain_discovery():
    """Test automatic domain discovery."""
    domains = discover_domains(Path("graphmodels/domains"))
    assert "business" in domains
    assert "aaoifi" in domains

def test_domain_registration():
    """Test domain models are registered correctly."""
    load_all_domains(Path("graphmodels/domains"))

    # Check entities registered
    assert get_entity_model("BusinessOutcome") is not None

    # Check edges registered
    assert get_edge_model("REQUIRES") is not None

def test_no_type_conflicts():
    """Test no duplicate entity/edge types across domains."""
    load_all_domains(Path("graphmodels/domains"))

    entity_types = list_entity_types()
    assert len(entity_types) == len(set(entity_types))  # No duplicates
```

---

## 8. Summary of Recommendations

### ✅ Strengths to Keep

1. **Plugin Architecture**: Automatic domain discovery
2. **Provenance Mixins**: Standardized temporal tracking
3. **Global Registries**: Runtime model lookup
4. **Clear Core/Domain Separation**: Infrastructure vs business logic

### 🔄 Improvements to Consider

1. **Modular LinkML Schemas**: Import core schemas, reduce duplication
2. **Standardized File Layout**: `models.py`, `enums.py`, `validators.py`, `glue.py`
3. **Shared Models**: Create `domains/shared/` for cross-domain types
4. **Type Safety**: Use `Annotated` types, custom validators
5. **Testing Structure**: Mirror domain structure in `tests/`

### 📋 Action Items

1. ✅ Create `schemas/core/` for shared LinkML schemas
2. ✅ Extract common types to `core/types.py`
3. ✅ Standardize domain plugin structure (`__init__.py`, `glue.py`)
4. ✅ Add custom validators for enum canonicalization
5. ✅ Document domain plugin creation process
6. ✅ Add integration tests for plugin system

---

## 9. References

### Internal Documentation
- `graphmodels/core/registries.py` - Global registry pattern
- `graphmodels/core/plugin_loader.py` - Plugin discovery system
- `v1_to_v2_migration/FIXES_APPLIED.md` - LinkML template customization

### External Resources
- [LinkML Schema Imports](https://linkml.io/linkml/schemas/imports.html)
- [FastAPI Project Structure](https://github.com/zhanymkanov/fastapi-best-practices)
- [Domain-Driven Design with Python](https://www.cosmicpython.com/book/chapter_01_domain_model.html)
- [Pydantic Best Practices](https://docs.pydantic.dev/latest/concepts/models/)

---

**Document Version:** 1.0
**Last Updated:** 2025-10-06
**Author:** Claude Code
**Status:** ✅ Ready for Review
