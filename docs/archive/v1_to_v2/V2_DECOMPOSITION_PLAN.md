# V2 Business Model Decomposition Plan

## Overview

This document provides a step-by-step plan for decomposing the existing monolithic `business_model_v2.yaml` into a modular structure following the architecture defined in `MODULAR_PYDANTIC_ARCHITECTURE.md`.

---

## Current State Analysis

### Existing V2 Schema (`business_model_v2.yaml`)

**Total Lines:** ~700+ lines
**Structure:**
- **Types (3)**: Email, E164Phone, Confidence01
- **Enums (8)**: OutcomeStatus, TaskStatus, DecisionStatus, Priority, Severity, VerificationStatus, HandoffState, CustomerSize, CustomerTier
- **Slots (~70)**: Provenance fields, entity fields, deprecated fields
- **Mixins (2)**: ProvenanceFields, EdgeProvenanceFields
- **Entity Classes (10)**: BusinessOutcome, BusinessDecision, BusinessTask, BusinessHandoff, BusinessClaim, BusinessContradiction, BusinessPrediction, Customer, Project, Actor
- **Edge Classes (10)**: Requires, Fulfills, BlockedBy, SupportedBy, Transfers, Threats, DerivedFrom, AssignedTo, ResponsibleFor, DependsOn

---

## Decomposition Strategy

### Phase 1: Identify Decomposition Boundaries

#### 1.1 Core Components (Reusable Across All Domains)

**Location:** `schemas/core/`

| Component | File | Content |
|-----------|------|---------|
| **Provenance Mixins** | `provenance.yaml` | ProvenanceFields, EdgeProvenanceFields |
| **Common Types** | `types.yaml` | Email, E164Phone, Confidence01 |
| **Common Enums** | `enums.yaml` | Priority, Severity (used across domains) |

**Rationale:**
- Provenance is universal (every entity/edge needs it)
- Email/Phone are universal contact types
- Priority/Severity are common business concepts

#### 1.2 Shared Components (Cross-Domain but Not Universal)

**Location:** `schemas/shared/`

| Component | File | Content |
|-----------|------|---------|
| **Temporal** | `temporal.yaml` | Date/time related slots (due_date, issued_at, approved_at, etc.) |
| **Identity** | `identity.yaml` | Actor, name, role, email, phone slots |
| **Financial** | `financial.yaml` | contract_value, budget, etc. (for future expansion) |

**Rationale:**
- Temporal fields are used across business, audit, compliance domains
- Actor/identity concepts span multiple domains
- Financial concepts are shared but not in core (domain-agnostic)

#### 1.3 Domain-Specific Components

**Location:** `schemas/domains/business/`

| Component | File | Content |
|-----------|------|---------|
| **Business Enums** | `enums.yaml` | OutcomeStatus, TaskStatus, DecisionStatus, HandoffState, VerificationStatus, CustomerSize, CustomerTier |
| **Business Entities** | `entities.yaml` | BusinessOutcome, BusinessDecision, BusinessTask, BusinessHandoff, BusinessClaim, BusinessContradiction, BusinessPrediction |
| **Business Domain Entities** | `domain_entities.yaml` | Customer, Project |
| **Business Edges** | `edges.yaml` | Requires, Fulfills, BlockedBy, SupportedBy, Transfers, Threats, DerivedFrom, AssignedTo, ResponsibleFor, DependsOn |
| **Main Schema** | `business_v2.yaml` | Imports + top-level config |

**Rationale:**
- Business workflow concepts (Outcome, Task, Decision) are domain-specific
- Customer/Project are business domain entities
- Relationships are specific to business workflow logic

---

## Phase 2: Create Modular Schema Structure

### Step 1: Create Directory Structure

```bash
mkdir -p schemas/core
mkdir -p schemas/shared
mkdir -p schemas/domains/business
```

### Step 2: Extract Core Schemas

#### 2.1 Create `schemas/core/provenance.yaml`

```yaml
id: https://example.org/core/provenance
name: core_provenance
description: Universal provenance tracking for all entities and edges

prefixes:
  linkml: https://w3id.org/linkml/
  core: https://example.org/core/

default_prefix: core
imports:
  - linkml:types

slots:
  # Node provenance
  node_id:
    range: string
    description: Stable citation id (deterministic)

  # Edge provenance
  rel_id:
    range: string
    description: Stable relationship id (deterministic)

  # Source system tracking
  prov_system:
    range: string
    description: Primary source system (e.g., slack, gdrive)

  prov_channel_ids:
    range: string
    multivalued: true
    description: Slack channel IDs, Teams channel IDs, etc.

  prov_thread_tss:
    range: string
    multivalued: true
    description: Thread timestamps from source system

  prov_tss:
    range: string
    multivalued: true
    description: Message timestamps

  prov_permalinks:
    range: string
    multivalued: true
    description: Permanent links to source messages/documents

  prov_file_ids:
    range: string
    multivalued: true
    description: Google Drive file IDs, Dropbox file IDs, etc.

  prov_rev_ids:
    range: string
    multivalued: true
    description: Revision IDs for versioned documents

  prov_text_sha1s:
    range: string
    multivalued: true
    description: SHA1 hashes of source text

  # Document provenance
  doco_types:
    range: string
    multivalued: true
    description: Document types (pdf, docx, etc.)

  doco_paths:
    range: string
    multivalued: true
    description: Document file paths

  page_nums:
    range: integer
    multivalued: true
    description: Page numbers in source documents

  # Evidence tracking
  support_count:
    range: integer
    description: Number of supporting episodes/sources

  # Derivation tracking (for edges)
  derived:
    range: boolean
    description: Whether derived vs directly extracted

  derivation_rule:
    range: string
    description: Rule or logic used for derivation

classes:
  ProvenanceFields:
    mixin: true
    description: Provenance mixin for all graph nodes
    slots:
      - node_id
      - prov_system
      - prov_channel_ids
      - prov_thread_tss
      - prov_tss
      - prov_permalinks
      - prov_file_ids
      - prov_rev_ids
      - prov_text_sha1s
      - doco_types
      - doco_paths
      - page_nums
      - support_count

  EdgeProvenanceFields:
    mixin: true
    description: Provenance mixin for all graph edges
    slots:
      - rel_id
      - prov_system
      - prov_channel_ids
      - prov_thread_tss
      - prov_tss
      - prov_permalinks
      - prov_file_ids
      - prov_rev_ids
      - prov_text_sha1s
      - doco_types
      - doco_paths
      - page_nums
      - derived
      - derivation_rule
      - support_count
```

#### 2.2 Create `schemas/core/types.yaml`

```yaml
id: https://example.org/core/types
name: core_types
description: Universal custom types for validation

prefixes:
  linkml: https://w3id.org/linkml/
  core: https://example.org/core/

default_prefix: core
imports:
  - linkml:types

types:
  Email:
    base: str
    uri: xsd:string
    pattern: '^[^@\s]+@[^@\s]+\.[^@\s]+$'
    description: Email address with regex validation

  E164Phone:
    base: str
    uri: xsd:string
    pattern: '^\+?[1-9]\d{7,15}$'
    description: E.164 international phone number format

  Confidence01:
    base: float
    uri: xsd:float
    minimum_value: 0
    maximum_value: 1
    description: Confidence score between 0 and 1
```

#### 2.3 Create `schemas/core/enums.yaml`

```yaml
id: https://example.org/core/enums
name: core_enums
description: Universal enumerations used across all domains

prefixes:
  linkml: https://w3id.org/linkml/
  core: https://example.org/core/

default_prefix: core

enums:
  Priority:
    description: Priority level (universal across domains)
    permissible_values:
      low: {description: "Low priority"}
      medium: {description: "Medium priority"}
      high: {description: "High priority"}
      critical: {description: "Critical priority"}

  Severity:
    description: Severity level (universal across domains)
    permissible_values:
      low: {description: "Low severity"}
      medium: {description: "Medium severity"}
      high: {description: "High severity"}
```

### Step 3: Extract Shared Schemas

#### 3.1 Create `schemas/shared/temporal.yaml`

```yaml
id: https://example.org/shared/temporal
name: shared_temporal
description: Temporal/time-related fields and types

prefixes:
  linkml: https://w3id.org/linkml/
  shared: https://example.org/shared/

default_prefix: shared
imports:
  - linkml:types

slots:
  due_date:
    range: datetime
    description: Deadline for completion

  issued_at:
    range: datetime
    description: When something was issued/created

  due_at:
    range: datetime
    description: When response/action is due

  acknowledged_at:
    range: datetime
    description: When acknowledged by recipient

  accepted_at:
    range: datetime
    description: When accepted by recipient

  approved_at:
    range: datetime
    description: When approved

  detected_at:
    range: datetime
    description: When detected/discovered
```

#### 3.2 Create `schemas/shared/identity.yaml`

```yaml
id: https://example.org/shared/identity
name: shared_identity
description: Identity/actor-related fields

prefixes:
  linkml: https://w3id.org/linkml/
  shared: https://example.org/shared/

default_prefix: shared
imports:
  - linkml:types
  - ../core/types

slots:
  name:
    range: string
    description: Full name

  role:
    range: string
    description: Job role or title

  team:
    range: string
    description: Team name

  department:
    range: string
    description: Department

  email:
    range: Email
    description: Email address

  phone:
    range: E164Phone
    description: Phone number (E.164 format)

  expertise:
    range: string
    description: Areas of expertise

  availability:
    range: string
    description: Current availability

classes:
  Actor:
    description: A team member or stakeholder
    mixins:
      - ProvenanceFields  # Will be imported from core
    slots:
      - name
      - role
      - team
      - department
      - email
      - phone
      - expertise
      - availability
```

### Step 4: Extract Domain-Specific Schemas

#### 4.1 Create `schemas/domains/business/enums.yaml`

```yaml
id: https://example.org/business/enums
name: business_enums
description: Business workflow enumerations

prefixes:
  linkml: https://w3id.org/linkml/
  biz: https://example.org/business/

default_prefix: biz

enums:
  OutcomeStatus:
    description: Status of a business outcome
    permissible_values:
      proposed: {description: "Outcome has been proposed"}
      in_progress: {description: "Work is in progress"}
      completed: {description: "Outcome completed"}
      blocked: {description: "Outcome is blocked"}

  TaskStatus:
    description: Status of a task
    permissible_values:
      todo: {description: "Task is todo"}
      in_progress: {description: "Task in progress"}
      completed: {description: "Task completed"}
      blocked: {description: "Task is blocked"}

  DecisionStatus:
    description: Status of a decision
    permissible_values:
      proposed: {description: "Decision proposed"}
      approved: {description: "Decision approved"}
      rejected: {description: "Decision rejected"}
      deferred: {description: "Decision deferred"}

  HandoffState:
    description: Handoff state
    permissible_values:
      pending: {description: "Handoff pending"}
      acknowledged: {description: "Acknowledged"}
      accepted: {description: "Accepted"}
      rejected: {description: "Rejected"}

  VerificationStatus:
    description: Verification status for claims
    permissible_values:
      unverified: {description: "Unverified"}
      verified: {description: "Verified"}
      refuted: {description: "Refuted"}

  CustomerSize:
    description: Customer company size
    permissible_values:
      small: {description: "Small company"}
      medium: {description: "Medium company"}
      enterprise: {description: "Enterprise"}

  CustomerTier:
    description: Customer service tier
    permissible_values:
      bronze: {description: "Bronze tier"}
      silver: {description: "Silver tier"}
      gold: {description: "Gold tier"}
```

#### 4.2 Create `schemas/domains/business/entities.yaml`

```yaml
id: https://example.org/business/entities
name: business_entities
description: Core business workflow entities

prefixes:
  linkml: https://w3id.org/linkml/
  biz: https://example.org/business/

default_prefix: biz
imports:
  - ../../core/provenance
  - ../../core/types
  - ../../core/enums
  - ../../shared/temporal
  - ./enums

slots:
  # Business-specific slots
  outcome_type:
    range: string
    description: Type of outcome (deliverable, milestone, goal)

  status:
    range: OutcomeStatus
    description: Outcome status (canonicalized from input)

  task_status:
    range: TaskStatus
    description: Task status (canonicalized from input)

  decision_status:
    range: DecisionStatus
    description: Decision status

  confidence:
    range: Confidence01
    description: Confidence in achieving outcome (0-1)
    aliases: ["confidence_score"]

  # Deprecated fields (V1 compatibility)
  for_customer:
    range: string
    deprecated: true
    description: "[DEPRECATED] use Customer->Outcome edge"

  in_project:
    range: string
    deprecated: true
    description: "[DEPRECATED] use Project->Outcome edge"

  owner:
    range: string
    deprecated: true
    description: "[DEPRECATED] use ResponsibleFor edge"

  assigned_to:
    range: string
    deprecated: true
    description: "[DEPRECATED] use AssignedTo edge"

  depends_on:
    range: string
    deprecated: true
    description: "[DEPRECATED] use DependsOn edge"

  # Decision-specific
  title:
    range: string

  conclusion:
    range: string

  rationale:
    range: string

  approvers:
    range: string
    multivalued: true

  approved_by:
    range: string
    deprecated: true
    description: "[DEPRECATED] use approvers list"

  impact_level:
    range: Severity

  reversible:
    range: boolean

  # Task-specific
  description:
    range: string

  estimated_effort_hours:
    range: float
    minimum_value: 0
    description: Estimated effort in hours
    aliases: ["estimated_effort"]

  blocking_reason:
    range: string

  # Claim-specific
  claim_text:
    range: string

  source:
    range: string

  verification_status:
    range: VerificationStatus

  evidence:
    range: string

  # Contradiction-specific
  severity:
    range: Severity

  resolved:
    range: boolean

  resolution:
    range: string

  # Prediction-specific
  prediction_text:
    range: string

  timeframe:
    range: string

  based_on:
    range: string

  risk_factors:
    range: string

classes:
  BusinessOutcome:
    description: A business deliverable or goal
    mixins:
      - ProvenanceFields
    slots:
      - outcome_type
      - status
      - priority        # From core/enums
      - due_date        # From shared/temporal
      - confidence
      - for_customer    # Deprecated
      - in_project      # Deprecated
      - owner           # Deprecated

  BusinessDecision:
    description: A crystallized choice or approval
    mixins:
      - ProvenanceFields
    slots:
      - title
      - conclusion
      - rationale
      - decision_status
      - approvers
      - approved_by     # Deprecated
      - approved_at     # From shared/temporal
      - impact_level
      - reversible

  BusinessTask:
    description: A unit of work
    mixins:
      - ProvenanceFields
    slots:
      - title
      - description
      - task_status
      - priority        # From core/enums
      - estimated_effort_hours
      - due_date        # From shared/temporal
      - blocking_reason
      - assigned_to     # Deprecated
      - depends_on      # Deprecated

  BusinessHandoff:
    description: A transition point where work moves between people
    mixins:
      - ProvenanceFields
    slots:
      - title
      - description
      - handoff_state
      - from_actor
      - to_actor
      - issued_at       # From shared/temporal
      - due_at          # From shared/temporal
      - acknowledged_at # From shared/temporal
      - accepted_at     # From shared/temporal
      - risk_level: Severity

  BusinessClaim:
    description: An assertion that may need verification
    mixins:
      - ProvenanceFields
    slots:
      - claim_text
      - confidence
      - source
      - verification_status
      - evidence

  BusinessContradiction:
    description: A conflict between claims or decisions
    mixins:
      - ProvenanceFields
    slots:
      - description
      - severity
      - detected_at     # From shared/temporal
      - resolved
      - resolution

  BusinessPrediction:
    description: Forward-looking intelligence based on data
    mixins:
      - ProvenanceFields
    slots:
      - prediction_text
      - confidence
      - timeframe
      - based_on
      - risk_factors
```

#### 4.3 Create `schemas/domains/business/domain_entities.yaml`

```yaml
id: https://example.org/business/domain_entities
name: business_domain_entities
description: Business domain-specific entities (Customer, Project)

prefixes:
  linkml: https://w3id.org/linkml/
  biz: https://example.org/business/

default_prefix: biz
imports:
  - ../../core/provenance
  - ../../shared/temporal
  - ./enums

slots:
  industry:
    range: string
    description: Customer's industry

  size:
    range: CustomerSize

  tier:
    range: CustomerTier

  contract_value:
    range: float
    minimum_value: 0
    description: Annual contract value

  start_date:
    range: datetime
    description: When customer relationship started

  account_manager:
    range: string

  # Project-specific
  project_status:
    range: string  # Could be enum: planning, active, on_hold, completed

  end_date:
    range: datetime

  budget:
    range: float
    minimum_value: 0

  project_manager:
    range: string

  team_size:
    range: integer
    minimum_value: 0

classes:
  Customer:
    description: A business customer or client entity
    mixins:
      - ProvenanceFields
    slots:
      - name          # From shared/identity
      - industry
      - size
      - tier
      - contract_value
      - start_date
      - account_manager

  Project:
    description: A business project entity
    mixins:
      - ProvenanceFields
    slots:
      - name          # From shared/identity
      - project_status
      - start_date    # From shared/temporal
      - end_date
      - budget
      - project_manager
      - team_size
```

#### 4.4 Create `schemas/domains/business/edges.yaml`

```yaml
id: https://example.org/business/edges
name: business_edges
description: Business workflow relationships

prefixes:
  linkml: https://w3id.org/linkml/
  biz: https://example.org/business/

default_prefix: biz
imports:
  - ../../core/provenance
  - ../../core/enums
  - ../../shared/temporal

slots:
  # Edge-specific slots
  criticality:
    range: Severity

  deadline:
    range: datetime

  blocker:
    range: boolean

  completion_percentage:
    range: float
    minimum_value: 0
    maximum_value: 1

  contribution_type:
    range: string

  blocking_since:
    range: datetime

  workaround_exists:
    range: boolean

  weight:
    range: float
    minimum_value: 0
    maximum_value: 1

  evidence_type:
    range: string

  transfer_date:
    range: datetime

  acceptance_required:
    range: boolean

  threat_level:
    range: Severity

  impact_description:
    range: string

  derivation_method:
    range: string

  confidence_contribution:
    range: float
    minimum_value: 0
    maximum_value: 1

classes:
  Requires:
    description: An outcome requires a decision or resource
    annotations:
      rel_type: REQUIRES
    mixins:
      - EdgeProvenanceFields
    slots:
      - criticality
      - deadline
      - blocker

  Fulfills:
    description: A task fulfills an outcome
    annotations:
      rel_type: FULFILLS
    mixins:
      - EdgeProvenanceFields
    slots:
      - completion_percentage
      - contribution_type

  BlockedBy:
    description: A task is blocked by a claim or risk
    annotations:
      rel_type: BLOCKED_BY
    mixins:
      - EdgeProvenanceFields
    slots:
      - blocking_since
      - severity: Severity
      - workaround_exists

  SupportedBy:
    description: A decision is supported by claims/evidence
    annotations:
      rel_type: SUPPORTED_BY
    mixins:
      - EdgeProvenanceFields
    slots:
      - weight
      - evidence_type

  Transfers:
    description: A handoff transfers a task
    annotations:
      rel_type: TRANSFERS
    mixins:
      - EdgeProvenanceFields
    slots:
      - transfer_date
      - acceptance_required

  Threats:
    description: A contradiction threatens an outcome
    annotations:
      rel_type: THREATS
    mixins:
      - EdgeProvenanceFields
    slots:
      - threat_level
      - impact_description

  DerivedFrom:
    description: A prediction is derived from claims
    annotations:
      rel_type: DERIVED_FROM
    mixins:
      - EdgeProvenanceFields
    slots:
      - derivation_method
      - confidence_contribution

  AssignedTo:
    description: A task is assigned to an actor
    annotations:
      rel_type: ASSIGNED_TO
    mixins:
      - EdgeProvenanceFields
    slots:
      - assigned_at: datetime

  ResponsibleFor:
    description: An actor is responsible for an outcome
    annotations:
      rel_type: RESPONSIBLE_FOR
    mixins:
      - EdgeProvenanceFields

  DependsOn:
    description: A task depends on another task/outcome
    annotations:
      rel_type: DEPENDS_ON
    mixins:
      - EdgeProvenanceFields
    slots:
      - dependency_type: string
```

#### 4.5 Create `schemas/domains/business/business_v2.yaml` (Main Schema)

```yaml
id: https://example.org/business_model_v2
name: business_model_v2
description: |
  Business workflow domain schema (V2) - modular structure

prefixes:
  linkml: https://w3id.org/linkml/
  biz: https://example.org/business/

default_prefix: biz

# Import all modular schemas
imports:
  - ../../core/provenance
  - ../../core/types
  - ../../core/enums
  - ../../shared/temporal
  - ../../shared/identity
  - ./enums
  - ./entities
  - ./domain_entities
  - ./edges

default_range: string
```

---

## Phase 3: Generate Modular Pydantic Models

### Step 1: Test Schema Validity

```bash
# Validate each schema independently
linkml-validate schemas/core/provenance.yaml
linkml-validate schemas/core/types.yaml
linkml-validate schemas/core/enums.yaml
linkml-validate schemas/shared/temporal.yaml
linkml-validate schemas/shared/identity.yaml
linkml-validate schemas/domains/business/enums.yaml
linkml-validate schemas/domains/business/entities.yaml
linkml-validate schemas/domains/business/domain_entities.yaml
linkml-validate schemas/domains/business/edges.yaml

# Validate main schema (with all imports)
linkml-validate schemas/domains/business/business_v2.yaml
```

### Step 2: Generate Pydantic Models

```bash
# Generate business domain models
gen-pydantic schemas/domains/business/business_v2.yaml \
  --template-dir v1_to_v2_migration/templates \
  > generated/pydantic/business_models_modular.py
```

### Step 3: Create Glue File

```python
# generated/pydantic/business_glue_modular.py
"""
Business domain registries (modular version).
"""

from typing import Dict, Type
from pydantic import BaseModel
from generated.pydantic.business_models_modular import (
    # Entities
    BusinessOutcome,
    BusinessDecision,
    BusinessTask,
    BusinessHandoff,
    BusinessClaim,
    BusinessContradiction,
    BusinessPrediction,
    Customer,
    Project,
    Actor,

    # Edges
    Requires,
    Fulfills,
    BlockedBy,
    SupportedBy,
    Transfers,
    Threats,
    DerivedFrom,
    AssignedTo,
    ResponsibleFor,
    DependsOn,
)

BUSINESS_ENTITIES: Dict[str, Type[BaseModel]] = {
    "BusinessOutcome": BusinessOutcome,
    "BusinessDecision": BusinessDecision,
    "BusinessTask": BusinessTask,
    "BusinessHandoff": BusinessHandoff,
    "BusinessClaim": BusinessClaim,
    "BusinessContradiction": BusinessContradiction,
    "BusinessPrediction": BusinessPrediction,
    "Customer": Customer,
    "Project": Project,
    "Actor": Actor,
}

BUSINESS_EDGES: Dict[str, Type[BaseModel]] = {
    "REQUIRES": Requires,
    "FULFILLS": Fulfills,
    "BLOCKED_BY": BlockedBy,
    "SUPPORTED_BY": SupportedBy,
    "TRANSFERS": Transfers,
    "THREATS": Threats,
    "DERIVED_FROM": DerivedFrom,
    "ASSIGNED_TO": AssignedTo,
    "RESPONSIBLE_FOR": ResponsibleFor,
    "DEPENDS_ON": DependsOn,
}
```

### Step 4: Update Domain Plugin

```python
# graphmodels/domains/business/__init__.py
"""
Business Domain Plugin (modular version)
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from generated.pydantic.business_glue_modular import (
    BUSINESS_ENTITIES,
    BUSINESS_EDGES,
)

ENTITIES = BUSINESS_ENTITIES
EDGES = BUSINESS_EDGES

__all__ = ["ENTITIES", "EDGES"]
```

---

## Phase 4: Validation and Testing

### Step 1: Run Existing Tests

```bash
# Run existing V2 validation tests
cd v1_to_v2_migration
python scripts/validate_v2.py

# Run pytest tests
python -m pytest tests/test_v1_v2_compatibility.py -v
```

### Step 2: Compare Monolithic vs Modular

```python
# test_modular_equivalence.py
"""
Test that modular schemas generate equivalent models to monolithic schema.
"""

def test_modular_entities_match_monolithic():
    from generated.pydantic.entities_v2 import BusinessOutcome as MonolithicOutcome
    from generated.pydantic.business_models_modular import BusinessOutcome as ModularOutcome

    # Compare field names
    monolithic_fields = set(MonolithicOutcome.model_fields.keys())
    modular_fields = set(ModularOutcome.model_fields.keys())

    assert monolithic_fields == modular_fields

def test_modular_edges_match_monolithic():
    from generated.pydantic.entities_v2 import Requires as MonolithicRequires
    from generated.pydantic.business_models_modular import Requires as ModularRequires

    # Check REL_TYPE constant
    assert MonolithicRequires.REL_TYPE == ModularRequires.REL_TYPE == "REQUIRES"
```

### Step 3: Integration Test

```python
# test_plugin_loading.py
from pathlib import Path
from graphmodels.core import load_all_domains, get_entity_model

def test_modular_business_domain_loads():
    domains_path = Path("graphmodels/domains")
    loaded = load_all_domains(domains_path)

    assert "business" in loaded

    # Test entity lookup
    outcome_cls = get_entity_model("BusinessOutcome")
    assert outcome_cls is not None

    # Test instantiation
    outcome = outcome_cls(
        node_id="test-123",
        outcome_type="deliverable",
        status="in_progress"
    )
    assert outcome.node_id == "test-123"
```

---

## Phase 5: Benefits Realized

### ✅ Modularity Benefits

1. **Reusable Core Components**
   - `ProvenanceFields` mixin used by all domains
   - `Email`, `Phone`, `Confidence01` types shared
   - `Priority`, `Severity` enums standardized

2. **Independent Domain Evolution**
   - Business domain can evolve without affecting AAOIFI domain
   - Add new business enums without modifying core

3. **Clear Dependencies**
   ```
   business_v2.yaml
   ├── imports: core/provenance      (reusable)
   ├── imports: core/types           (reusable)
   ├── imports: shared/temporal      (cross-domain)
   └── imports: business/enums       (domain-specific)
   ```

4. **Easier Testing**
   - Test core schemas independently
   - Test business domain in isolation
   - Mock shared components

5. **Better Documentation**
   - Each schema file is self-contained
   - Clear purpose: `provenance.yaml`, `temporal.yaml`, `entities.yaml`
   - Easier onboarding for new developers

---

## Migration Checklist

### Pre-Migration
- [ ] Backup existing `business_model_v2.yaml`
- [ ] Backup existing `entities_v2.py`
- [ ] Document current test coverage

### Schema Decomposition
- [ ] Create directory structure (`schemas/core`, `schemas/shared`, `schemas/domains/business`)
- [ ] Extract `schemas/core/provenance.yaml`
- [ ] Extract `schemas/core/types.yaml`
- [ ] Extract `schemas/core/enums.yaml`
- [ ] Extract `schemas/shared/temporal.yaml`
- [ ] Extract `schemas/shared/identity.yaml`
- [ ] Extract `schemas/domains/business/enums.yaml`
- [ ] Extract `schemas/domains/business/entities.yaml`
- [ ] Extract `schemas/domains/business/domain_entities.yaml`
- [ ] Extract `schemas/domains/business/edges.yaml`
- [ ] Create `schemas/domains/business/business_v2.yaml` (main)

### Validation
- [ ] Validate each core schema independently
- [ ] Validate each shared schema independently
- [ ] Validate each business schema independently
- [ ] Validate main `business_v2.yaml` with all imports

### Generation
- [ ] Generate Pydantic models from modular schema
- [ ] Create modular glue file
- [ ] Update domain plugin `__init__.py`

### Testing
- [ ] Run existing validation tests
- [ ] Run pytest compatibility tests
- [ ] Create equivalence tests (monolithic vs modular)
- [ ] Test plugin loading
- [ ] Test model instantiation

### Cleanup
- [ ] Archive monolithic `business_model_v2.yaml`
- [ ] Update documentation
- [ ] Update README with new structure

---

## Rollback Plan

If issues arise, rollback is straightforward:

```bash
# Restore original schema
cp business_model_v2.yaml.backup business_model_v2.yaml

# Regenerate from monolithic
gen-pydantic business_model_v2.yaml \
  --template-dir v1_to_v2_migration/templates \
  > generated/pydantic/entities_v2.py

# Restore original plugin
cp graphmodels/domains/business/__init__.py.backup \
   graphmodels/domains/business/__init__.py
```

---

## Next Steps After Decomposition

1. **Add New Domains**: Follow same pattern for AAOIFI, audit, etc.
2. **Extract More Shared Components**: Create `schemas/shared/financial.yaml`, `schemas/shared/geography.yaml`
3. **Custom Templates**: Add field validators, canonicalization
4. **Documentation**: Generate schema docs with `gen-doc`

---

**Document Version:** 1.0
**Last Updated:** 2025-10-06
**Status:** ✅ Ready for Implementation
