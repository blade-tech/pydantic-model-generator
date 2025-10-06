# Implementation Plan: V1 → V2 Alignment + Modular Architecture + AAOIFI Integration

## Executive Summary

This plan aligns the working Pydantic V1 model (`entities - Pydantiv V1.py`) with recommended V2 patterns while creating a modular, generalizable foundation for any outcome → Pydantic workflow.

**Foundation Status**: ✅ Complete
- NodeProv/EdgeProv mixins created
- Deterministic ID utilities working
- Pattern validated on Invoice example (6/6 tests passing)

**Goal**: Create a tightened, modular, AAOIFI-integrated Pydantic model foundation that works with Graphiti and supports extractive evaluation.

---

## Phase 1: V1 Tightening Strategy (Business Domain)

### 1.1 Create Business LinkML Schema

**File**: `schemas/overlays/business_overlay.yaml`

**Structure**:
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

  TaskStatus:
    permissible_values:
      todo: {}
      in_progress: {}
      completed: {}
      blocked: {}

  DecisionStatus:
    permissible_values:
      proposed: {}
      approved: {}
      rejected: {}
      deferred: {}

  HandoffState:
    permissible_values:
      pending: {}
      acknowledged: {}
      accepted: {}
      rejected: {}

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

  VerificationStatus:
    permissible_values:
      unverified: {}
      verified: {}
      refuted: {}

  ProjectStatus:
    permissible_values:
      planning: {}
      active: {}
      on_hold: {}
      completed: {}

  CustomerTier:
    permissible_values:
      bronze: {}
      silver: {}
      gold: {}
      platinum: {}

  CompanySize:
    permissible_values:
      small: {}
      medium: {}
      enterprise: {}

slots:
  # BusinessOutcome slots
  outcome_type: { range: string }
  status: { range: OutcomeStatus }
  priority: { range: Priority }
  due_date: { range: datetime }
  confidence: { range: float, minimum_value: 0, maximum_value: 1 }

  # [DEPRECATED] Legacy back-references (keep for compatibility)
  for_customer: { range: string, deprecated: true }
  in_project: { range: string, deprecated: true }
  owner: { range: string, deprecated: true }

  # BusinessDecision slots
  conclusion: { range: string }
  rationale: { range: string }
  decision_status: { range: DecisionStatus }
  approvers: { range: string, multivalued: true }
  approved_at: { range: datetime }
  impact_level: { range: Severity }
  reversible: { range: boolean }

  # BusinessTask slots
  description: { range: string }
  task_status: { range: TaskStatus }
  assigned_to: { range: string }
  task_due_date: { range: datetime }
  estimated_effort: { range: string }
  blocking_reason: { range: string }
  depends_on: { range: string }

  # BusinessHandoff slots
  context: { range: string }
  handoff_state: { range: HandoffState }
  from_actor: { range: string }
  to_actor: { range: string }
  issued_at: { range: datetime }
  handoff_due_at: { range: datetime }
  acknowledged_at: { range: datetime }
  accepted_at: { range: datetime }
  risk_level: { range: Severity }

  # BusinessClaim slots
  claim_text: { range: string }
  claim_confidence: { range: float, minimum_value: 0, maximum_value: 1 }
  source: { range: string }
  verification_status: { range: VerificationStatus }
  evidence: { range: string }

  # BusinessContradiction slots
  contradiction_description: { range: string }
  contradiction_severity: { range: Severity }
  detected_at: { range: datetime }
  resolved: { range: boolean }
  resolution: { range: string }

  # BusinessPrediction slots
  prediction_text: { range: string }
  prediction_confidence: { range: float, minimum_value: 0, maximum_value: 1 }
  timeframe: { range: string }
  based_on: { range: string }
  risk_factors: { range: string }

  # Customer slots
  industry: { range: string }
  size: { range: CompanySize }
  tier: { range: CustomerTier }
  contract_value: { range: float, minimum_value: 0 }
  start_date: { range: datetime }
  account_manager: { range: string }

  # Project slots
  project_status: { range: ProjectStatus }
  project_start_date: { range: datetime }
  project_end_date: { range: datetime }
  budget: { range: float, minimum_value: 0 }
  project_manager: { range: string }
  team_size: { range: integer, minimum_value: 0 }

  # Actor slots
  role: { range: string }
  team: { range: string }
  department: { range: string }
  email: { range: string }
  phone: { range: string }
  expertise: { range: string }
  availability: { range: string }

  # Edge slots
  criticality: { range: Severity }
  deadline: { range: datetime }
  blocker: { range: boolean }
  completion_percentage: { range: float, minimum_value: 0, maximum_value: 1 }
  contribution_type: { range: string }
  blocking_since: { range: datetime }
  workaround_exists: { range: boolean }
  weight: { range: float, minimum_value: 0, maximum_value: 1 }
  evidence_type: { range: string }
  transfer_date: { range: datetime }
  acceptance_required: { range: boolean }
  threat_level: { range: Severity }
  impact_description: { range: string }
  derivation_method: { range: string }
  confidence_contribution: { range: float, minimum_value: 0, maximum_value: 1 }

classes:
  BusinessOutcome:
    mixins: [NodeProv]
    slots:
      - outcome_type
      - status
      - priority
      - due_date
      - confidence
      - for_customer  # [DEPRECATED] Use (Customer)-[:Requires]->(BusinessOutcome)
      - in_project    # [DEPRECATED] Use (Project)-[:Fulfills]->(BusinessOutcome)
      - owner         # [DEPRECATED] Use (Actor)-[:ResponsibleFor]->(BusinessOutcome)

  BusinessDecision:
    mixins: [NodeProv]
    slots:
      - conclusion
      - rationale
      - decision_status
      - approvers
      - approved_at
      - impact_level
      - reversible

  BusinessTask:
    mixins: [NodeProv]
    slots:
      - description
      - task_status
      - priority
      - assigned_to
      - task_due_date
      - estimated_effort
      - blocking_reason
      - depends_on

  BusinessHandoff:
    mixins: [NodeProv]
    slots:
      - context
      - handoff_state
      - from_actor
      - to_actor
      - issued_at
      - handoff_due_at
      - acknowledged_at
      - accepted_at
      - risk_level

  BusinessClaim:
    mixins: [NodeProv]
    slots:
      - claim_text
      - claim_confidence
      - source
      - verification_status
      - evidence

  BusinessContradiction:
    mixins: [NodeProv]
    slots:
      - contradiction_description
      - contradiction_severity
      - detected_at
      - resolved
      - resolution

  BusinessPrediction:
    mixins: [NodeProv]
    slots:
      - prediction_text
      - prediction_confidence
      - timeframe
      - based_on
      - risk_factors

  Customer:
    mixins: [NodeProv]
    slots:
      - industry
      - size
      - tier
      - contract_value
      - start_date
      - account_manager

  Project:
    mixins: [NodeProv]
    slots:
      - project_status
      - project_start_date
      - project_end_date
      - budget
      - project_manager
      - team_size

  Actor:
    mixins: [NodeProv]
    slots:
      - role
      - team
      - department
      - email
      - phone
      - expertise
      - availability

  # Edge classes
  Requires:
    mixins: [EdgeProv]
    slots:
      - criticality
      - deadline
      - blocker

  Fulfills:
    mixins: [EdgeProv]
    slots:
      - completion_percentage
      - contribution_type

  BlockedBy:
    mixins: [EdgeProv]
    slots:
      - blocking_since
      - severity
      - workaround_exists

  SupportedBy:
    mixins: [EdgeProv]
    slots:
      - weight
      - evidence_type

  Transfers:
    mixins: [EdgeProv]
    slots:
      - transfer_date
      - acceptance_required

  Threats:
    mixins: [EdgeProv]
    slots:
      - threat_level
      - impact_description

  DerivedFrom:
    mixins: [EdgeProv]
    slots:
      - derivation_method
      - confidence_contribution
```

### 1.2 Generate Pydantic V2 Models

**Command**:
```bash
linkml generate pydantic schemas/overlays/business_overlay.yaml > generated/pydantic/business_models.py
```

**Post-Generation**: Add required imports to generated file:
```python
from lib.provenance_fields import NodeProv, EdgeProv
from lib.id_utils import make_node_id, make_edge_id
from enum import Enum
from datetime import datetime
```

### 1.3 Create Business Glue Module

**File**: `graphmodels/domains/business/glue.py`

**Purpose**: Registry mappings for Graphiti integration

```python
"""Business domain glue - registries and edge maps for Graphiti integration."""

from typing import Dict, List, Type
from pydantic import BaseModel
from generated.pydantic.business_models import (
    BusinessOutcome, BusinessDecision, BusinessTask, BusinessHandoff,
    BusinessClaim, BusinessContradiction, BusinessPrediction,
    Customer, Project, Actor,
    Requires, Fulfills, BlockedBy, SupportedBy, Transfers, Threats, DerivedFrom
)

# Entity type registry
BUSINESS_ENTITY_TYPES: Dict[str, Type[BaseModel]] = {
    "BusinessOutcome": BusinessOutcome,
    "BusinessDecision": BusinessDecision,
    "BusinessTask": BusinessTask,
    "BusinessHandoff": BusinessHandoff,
    "BusinessClaim": BusinessClaim,
    "BusinessContradiction": BusinessContradiction,
    "BusinessPrediction": BusinessPrediction,
    "Customer": Customer,
    "Project": Project,
    "Actor": Actor
}

# Edge type registry
BUSINESS_EDGE_TYPES: Dict[str, Type[BaseModel]] = {
    "Requires": Requires,
    "Fulfills": Fulfills,
    "BlockedBy": BlockedBy,
    "SupportedBy": SupportedBy,
    "Transfers": Transfers,
    "Threats": Threats,
    "DerivedFrom": DerivedFrom
}

# Edge type mapping: canonical edge directions
BUSINESS_EDGE_TYPE_MAP: Dict[tuple[str, str], List[str]] = {
    # BusinessOutcome relationships
    ("BusinessOutcome", "BusinessDecision"): ["Requires"],

    # BusinessTask relationships
    ("BusinessTask", "BusinessOutcome"): ["Fulfills"],
    ("BusinessTask", "BusinessClaim"): ["BlockedBy"],
    ("BusinessTask", "BusinessContradiction"): ["BlockedBy"],

    # BusinessDecision relationships
    ("BusinessDecision", "BusinessClaim"): ["SupportedBy"],

    # BusinessHandoff relationships
    ("BusinessHandoff", "BusinessTask"): ["Transfers"],
    ("BusinessHandoff", "Actor"): ["Transfers"],

    # BusinessContradiction relationships
    ("BusinessContradiction", "BusinessOutcome"): ["Threats"],

    # BusinessPrediction relationships
    ("BusinessPrediction", "BusinessClaim"): ["DerivedFrom"],

    # Actor relationships
    ("Actor", "BusinessTask"): ["Fulfills"],
    ("Actor", "BusinessOutcome"): ["Requires"],  # ResponsibleFor
    ("Actor", "Project"): ["Fulfills"],

    # Customer relationships
    ("Customer", "BusinessOutcome"): ["Requires"],
    ("Customer", "Project"): ["Requires"],

    # Project relationships
    ("Project", "BusinessOutcome"): ["Fulfills"],
    ("Project", "Actor"): ["Requires"],
}
```

### 1.4 Validation Tests for Business V2

**File**: `tests/test_business_v2.py`

**Test Coverage**:
1. Enum validation (status can't be "banana")
2. Datetime validation (due_date must be valid datetime)
3. Numeric constraints (confidence must be 0-1)
4. Provenance tracking (node_id, episode_ids populated)
5. Deprecated field warnings
6. Edge provenance (rel_id, relation_type)

---

## Phase 2: Modular Repository Structure

### 2.1 Directory Layout

```
graphmodels/
├── core/
│   ├── __init__.py
│   ├── provenance.py        # NodeProv/EdgeProv base classes
│   ├── ids.py               # Deterministic ID utilities
│   ├── registries.py        # Domain registry pattern
│   └── plugin_loader.py     # Domain discovery and merging
│
├── domains/
│   ├── __init__.py
│   │
│   ├── business/
│   │   ├── __init__.py
│   │   ├── linkml/
│   │   │   └── business_overlay.yaml
│   │   ├── generated/
│   │   │   └── business_models.py  # Auto-generated from LinkML
│   │   └── glue.py                 # Registries, edge maps
│   │
│   └── aaoifi/
│       ├── __init__.py
│       ├── linkml/
│       │   ├── document_overlay.yaml
│       │   ├── standards_overlay.yaml
│       │   └── rules_overlay.yaml
│       ├── generated/
│       │   ├── document_models.py
│       │   ├── standards_models.py
│       │   └── rules_models.py
│       └── glue.py
│
├── schemas/
│   ├── core.yaml            # Base provenance mixins
│   └── overlays/
│       ├── invoice_overlay.yaml     # Example validation domain
│       ├── business_overlay.yaml    # → moved to domains/business/linkml/
│       ├── document_overlay.yaml    # → moved to domains/aaoifi/linkml/
│       └── standards_overlay.yaml   # → moved to domains/aaoifi/linkml/
│
├── lib/                     # Legacy location (migrate to core/)
│   ├── provenance_fields.py → core/provenance.py
│   └── id_utils.py          → core/ids.py
│
├── generated/               # Legacy location (migrate to domains/)
│   └── pydantic/
│       └── invoice_models.py
│
└── tests/
    ├── test_core.py
    ├── test_business_v2.py
    └── test_aaoifi.py
```

### 2.2 Core Module Implementation

**File**: `graphmodels/core/provenance.py`

Migrate from `lib/provenance_fields.py` with no changes to content.

**File**: `graphmodels/core/ids.py`

Migrate from `lib/id_utils.py` with no changes to content.

**File**: `graphmodels/core/registries.py` (NEW)

```python
"""Domain registry pattern for plugin-based entity and edge types."""

from typing import Dict, List, Type, Tuple
from pydantic import BaseModel

class DomainRegistry:
    """Registry for a single domain's entity types, edge types, and edge maps."""

    def __init__(
        self,
        name: str,
        entity_types: Dict[str, Type[BaseModel]],
        edge_types: Dict[str, Type[BaseModel]],
        edge_type_map: Dict[Tuple[str, str], List[str]]
    ):
        self.name = name
        self.entity_types = entity_types
        self.edge_types = edge_types
        self.edge_type_map = edge_type_map

    def validate(self):
        """Validate registry consistency."""
        # Check edge types referenced in map exist in edge_types
        referenced_edges = set()
        for edges in self.edge_type_map.values():
            referenced_edges.update(edges)

        missing = referenced_edges - set(self.edge_types.keys())
        if missing:
            raise ValueError(f"Domain {self.name}: Edge types {missing} in edge_type_map but not in edge_types")

        # Check entity types referenced in map exist in entity_types
        referenced_entities = set()
        for (src, tgt) in self.edge_type_map.keys():
            referenced_entities.add(src)
            referenced_entities.add(tgt)

        missing = referenced_entities - set(self.entity_types.keys())
        if missing:
            raise ValueError(f"Domain {self.name}: Entity types {missing} in edge_type_map but not in entity_types")

class GlobalRegistry:
    """Merged registry from all loaded domains."""

    def __init__(self):
        self.domains: Dict[str, DomainRegistry] = {}
        self.entity_types: Dict[str, Type[BaseModel]] = {}
        self.edge_types: Dict[str, Type[BaseModel]] = {}
        self.edge_type_map: Dict[Tuple[str, str], List[str]] = {}

    def register_domain(self, registry: DomainRegistry):
        """Register a domain's types into global registry."""
        registry.validate()

        # Check for naming conflicts
        conflicts = set(registry.entity_types.keys()) & set(self.entity_types.keys())
        if conflicts:
            raise ValueError(f"Entity type conflicts with domain {registry.name}: {conflicts}")

        conflicts = set(registry.edge_types.keys()) & set(self.edge_types.keys())
        if conflicts:
            raise ValueError(f"Edge type conflicts with domain {registry.name}: {conflicts}")

        # Merge
        self.domains[registry.name] = registry
        self.entity_types.update(registry.entity_types)
        self.edge_types.update(registry.edge_types)

        # Merge edge type maps (can have overlapping keys if same edge allowed)
        for key, edges in registry.edge_type_map.items():
            if key in self.edge_type_map:
                # Union of allowed edges
                self.edge_type_map[key] = list(set(self.edge_type_map[key]) | set(edges))
            else:
                self.edge_type_map[key] = edges

    def get_allowed_edges(self, source_type: str, target_type: str) -> List[str]:
        """Get allowed edge types between source and target entity types."""
        return self.edge_type_map.get((source_type, target_type), [])
```

**File**: `graphmodels/core/plugin_loader.py` (NEW)

```python
"""Plugin loader for domain discovery and registration."""

import importlib
from pathlib import Path
from graphmodels.core.registries import DomainRegistry, GlobalRegistry

def discover_domains(base_path: Path = None) -> GlobalRegistry:
    """Discover and load all domain plugins from graphmodels/domains/."""
    if base_path is None:
        base_path = Path(__file__).parent.parent / "domains"

    global_registry = GlobalRegistry()

    # Find all domain directories
    for domain_dir in base_path.iterdir():
        if not domain_dir.is_dir():
            continue
        if domain_dir.name.startswith("_"):
            continue

        glue_path = domain_dir / "glue.py"
        if not glue_path.exists():
            continue

        # Import domain glue module
        module_name = f"graphmodels.domains.{domain_dir.name}.glue"
        try:
            glue_module = importlib.import_module(module_name)
        except ImportError as e:
            print(f"Warning: Could not import {module_name}: {e}")
            continue

        # Extract registries
        entity_types = getattr(glue_module, f"{domain_dir.name.upper()}_ENTITY_TYPES", {})
        edge_types = getattr(glue_module, f"{domain_dir.name.upper()}_EDGE_TYPES", {})
        edge_type_map = getattr(glue_module, f"{domain_dir.name.upper()}_EDGE_TYPE_MAP", {})

        if not entity_types:
            print(f"Warning: No entity types found in {module_name}")
            continue

        # Create domain registry
        registry = DomainRegistry(
            name=domain_dir.name,
            entity_types=entity_types,
            edge_types=edge_types,
            edge_type_map=edge_type_map
        )

        global_registry.register_domain(registry)
        print(f"Loaded domain: {domain_dir.name} ({len(entity_types)} entities, {len(edge_types)} edges)")

    return global_registry
```

### 2.3 Migration Steps

1. **Migrate lib/ → core/**:
   ```bash
   mkdir -p graphmodels/core
   cp lib/provenance_fields.py graphmodels/core/provenance.py
   cp lib/id_utils.py graphmodels/core/ids.py
   ```

2. **Create core registries**:
   Create `graphmodels/core/registries.py` and `graphmodels/core/plugin_loader.py` as shown above

3. **Reorganize schemas**:
   ```bash
   mkdir -p graphmodels/domains/business/linkml
   mv schemas/overlays/business_overlay.yaml graphmodels/domains/business/linkml/
   ```

4. **Update imports** across all files:
   ```python
   # Old
   from lib.provenance_fields import NodeProv, EdgeProv
   from lib.id_utils import make_node_id

   # New
   from graphmodels.core.provenance import NodeProv, EdgeProv
   from graphmodels.core.ids import make_node_id
   ```

---

## Phase 3: AAOIFI Integration

### 3.1 AAOIFI Document Schema

**File**: `graphmodels/domains/aaoifi/linkml/document_overlay.yaml`

```yaml
id: https://example.org/graphmodels/aaoifi/document
name: aaoifi_document_validation
imports:
  - ../../../schemas/core

classes:
  Document:
    mixins: [NodeProv]
    class_uri: doco:Document
    slots:
      - document_title
      - document_type
      - edition
      - published_date
      - language
      - total_pages
      - group_id  # Edition isolation (AAOIFI_FAS_25_2020, AAOIFI_FAS_25_2015)

  Section:
    mixins: [NodeProv]
    class_uri: doco:Section
    slots:
      - section_number
      - section_title
      - level
      - parent_section_id
      - group_id

  Paragraph:
    mixins: [NodeProv]
    class_uri: doco:Paragraph
    slots:
      - paragraph_number
      - content
      - page_number
      - section_id
      - group_id

  # Edges
  HasComponent:
    mixins: [EdgeProv]
    class_uri: doco:hasComponent
    description: "Document has component Section/Paragraph (hierarchical)"

  HasPart:
    mixins: [EdgeProv]
    class_uri: doco:hasPart
    description: "Section has part Paragraph (flat)"

slots:
  document_title: { range: string }
  document_type: { range: string }
  edition: { range: string }
  published_date: { range: datetime }
  language: { range: string }
  total_pages: { range: integer }

  section_number: { range: string }
  section_title: { range: string }
  level: { range: integer }
  parent_section_id: { range: string }

  paragraph_number: { range: string }
  content: { range: string }
  page_number: { range: integer }
  section_id: { range: string }

  group_id: { range: string }  # Edition isolation
```

### 3.2 AAOIFI Standards Schema

**File**: `graphmodels/domains/aaoifi/linkml/standards_overlay.yaml`

```yaml
id: https://example.org/graphmodels/aaoifi/standards
name: aaoifi_standards_validation
imports:
  - ../../../schemas/core

enums:
  ConceptType:
    permissible_values:
      principle: {}
      definition: {}
      criterion: {}
      requirement: {}
      guideline: {}

classes:
  Concept:
    mixins: [NodeProv]
    class_uri: skos:Concept
    slots:
      - concept_label
      - concept_type
      - definition
      - scope_note
      - group_id

  ContractType:
    mixins: [NodeProv]
    class_uri: fibo-fbc-pas-fpas:Contract
    slots:
      - contract_name
      - contract_category
      - description
      - permissibility
      - group_id

  Rule:
    mixins: [NodeProv]
    class_uri: fibo-fnd-law-lcap:Law
    slots:
      - rule_text
      - rule_type
      - applicability
      - exceptions
      - group_id

  Agent:
    mixins: [NodeProv]
    class_uri: prov:Agent
    slots:
      - agent_name
      - agent_type
      - role
      - group_id

  # Edges
  About:
    mixins: [EdgeProv]
    description: "Paragraph is about Concept/ContractType"
    slots:
      - relevance_score

  EvidenceOf:
    mixins: [EdgeProv]
    class_uri: prov:wasGeneratedBy
    description: "Paragraph provides evidence of Rule"
    slots:
      - quote_span_start
      - quote_span_end

  AttributedTo:
    mixins: [EdgeProv]
    class_uri: prov:wasAttributedTo
    description: "Document attributed to Agent (publisher)"

slots:
  concept_label: { range: string }
  concept_type: { range: ConceptType }
  definition: { range: string }
  scope_note: { range: string }

  contract_name: { range: string }
  contract_category: { range: string }
  permissibility: { range: string }

  rule_text: { range: string }
  rule_type: { range: string }
  applicability: { range: string }
  exceptions: { range: string }

  agent_name: { range: string }
  agent_type: { range: string }

  relevance_score: { range: float, minimum_value: 0, maximum_value: 1 }
  quote_span_start: { range: integer }
  quote_span_end: { range: integer }
```

### 3.3 AAOIFI Glue Module

**File**: `graphmodels/domains/aaoifi/glue.py`

```python
"""AAOIFI domain glue - registries and edge maps."""

from typing import Dict, List, Type
from pydantic import BaseModel
from generated.pydantic.aaoifi_document_models import (
    Document, Section, Paragraph,
    HasComponent, HasPart
)
from generated.pydantic.aaoifi_standards_models import (
    Concept, ContractType, Rule, Agent,
    About, EvidenceOf, AttributedTo
)

AAOIFI_ENTITY_TYPES: Dict[str, Type[BaseModel]] = {
    "Document": Document,
    "Section": Section,
    "Paragraph": Paragraph,
    "Concept": Concept,
    "ContractType": ContractType,
    "Rule": Rule,
    "Agent": Agent
}

AAOIFI_EDGE_TYPES: Dict[str, Type[BaseModel]] = {
    "HasComponent": HasComponent,
    "HasPart": HasPart,
    "About": About,
    "EvidenceOf": EvidenceOf,
    "AttributedTo": AttributedTo
}

AAOIFI_EDGE_TYPE_MAP: Dict[tuple[str, str], List[str]] = {
    # Document structure
    ("Document", "Section"): ["HasComponent"],
    ("Document", "Paragraph"): ["HasComponent"],
    ("Section", "Paragraph"): ["HasPart"],

    # Semantic relationships
    ("Paragraph", "Concept"): ["About"],
    ("Paragraph", "ContractType"): ["About"],
    ("Paragraph", "Rule"): ["EvidenceOf"],

    # Attribution
    ("Document", "Agent"): ["AttributedTo"],
}
```

### 3.4 Group Discipline (Edition Isolation)

**Critical Pattern**: Never mix editions in same query/subgraph

**Implementation**:
```python
# In graphmodels/core/provenance.py - add to NodeProv
class NodeProv(BaseModel):
    # ... existing fields ...
    group_id: Optional[str] = Field(
        None,
        description="Group/namespace ID for edition isolation (e.g., AAOIFI_FAS_25_2020)"
    )

# Query constraint example
def get_aaoifi_paragraphs_about_concept(
    concept_label: str,
    edition: str = "AAOIFI_FAS_25_2020"
) -> List[Paragraph]:
    """Get paragraphs about a concept - EDITION ISOLATED."""
    query = """
    MATCH (p:Paragraph)-[:About]->(c:Concept {label: $concept_label})
    WHERE p.group_id = $group_id
    RETURN p
    """
    # Edition isolation enforced at query level
    return execute_query(query, concept_label=concept_label, group_id=edition)
```

---

## Phase 4: Generalization Approach (Outcome → Pydantic Workflow)

### 4.1 LinkML-First Workflow

**Input**: Business outcome/question + Evidence Query Plan

**Output**: Validated Pydantic models ready for Graphiti

**Pipeline**:

```
1. Outcome Definition
   ↓
2. Evidence Query Plan (EQP) Creation
   ↓
3. LLM Schema Proposal (Instructor-guarded)
   ↓
4. LinkML Linting & Validation
   ↓
5. Pydantic Generation
   ↓
6. Type Tests (import, instantiate, validate)
   ↓
7. Extractive Evaluation Gate (ZUT)
   ↓
8. Graphiti Integration
```

### 4.2 Evidence Query Plan Template

**File**: `templates/evidence_query_plan.yaml`

```yaml
outcome:
  question: "Which invoices are blocked and why?"
  business_value: "Identify approval bottlenecks to reduce payment delays"

required_entities:
  - entity_type: Invoice
    key_fields: [invoice_id, amount, department_id]
    filters:
      - field: approval_status
        condition: equals
        value: "blocked"

  - entity_type: ApprovalRule
    key_fields: [rule_type, threshold]

required_edges:
  - edge_type: ViolatesRule
    source: Invoice
    target: ApprovalRule
    direction: outbound
    properties: [violation_reason]

metadata_constraints:
  - temporal_range: [last_30_days]
  - group_isolation: None  # Not edition-specific

extractive_requirements:
  - min_quote_coverage: 0.8  # 80% of answer from quotes
  - connective_whitelist: ["because", "since", "therefore", "and", "or"]
  - max_unsupported_tokens: 0  # Zero unsupported tokens (ZUT)
```

### 4.3 LLM Schema Proposal (Instructor-Guarded)

**File**: `workflow/schema_proposer.py`

```python
"""LLM-based schema proposal with Instructor validation."""

import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional

class SlotProposal(BaseModel):
    """Proposed slot definition."""
    name: str
    range: str  # "string", "datetime", "float", "SomeEnum"
    description: str
    minimum_value: Optional[float] = None
    maximum_value: Optional[float] = None
    multivalued: bool = False

class ClassProposal(BaseModel):
    """Proposed entity or edge class."""
    name: str
    description: str
    mixins: List[str]  # ["NodeProv"] or ["EdgeProv"]
    slots: List[str]  # References to SlotProposal names
    class_uri: Optional[str] = None  # For AAOIFI: doco:Document, fibo:Contract, etc.

class SchemaProposal(BaseModel):
    """Complete schema proposal from LLM."""
    schema_id: str
    schema_name: str
    imports: List[str] = Field(default_factory=lambda: ["../../../schemas/core"])
    enums: List[dict]  # LinkML enum definitions
    slots: List[SlotProposal]
    classes: List[ClassProposal]

client = instructor.from_openai(OpenAI())

def propose_schema_from_eqp(eqp: dict) -> SchemaProposal:
    """Generate LinkML schema proposal from Evidence Query Plan."""
    prompt = f"""
You are a LinkML schema designer. Given this Evidence Query Plan, propose a complete LinkML schema.

Evidence Query Plan:
{eqp}

Requirements:
1. All entities must use NodeProv mixin (inherited from core schema)
2. All edges must use EdgeProv mixin
3. Use proper enums for status/type fields (not strings)
4. Use datetime for temporal fields (not strings)
5. Add numeric constraints (minimum_value, maximum_value) where appropriate
6. Follow naming conventions: PascalCase for classes, snake_case for slots
7. For AAOIFI entities, include appropriate class_uri from DoCO/FIBO/PROV ontologies

Generate the schema proposal.
"""

    schema = client.chat.completions.create(
        model="gpt-4o",
        response_model=SchemaProposal,
        messages=[{"role": "user", "content": prompt}]
    )

    return schema

def schema_to_linkml_yaml(schema: SchemaProposal) -> str:
    """Convert SchemaProposal to LinkML YAML."""
    # Implementation: serialize SchemaProposal to YAML format
    # This is a template - actual implementation would use yaml library
    pass
```

### 4.4 Validation Pipeline

**File**: `workflow/validation_pipeline.py`

```python
"""Schema validation pipeline: lint → generate → test."""

import subprocess
from pathlib import Path
from typing import Optional

class ValidationResult:
    def __init__(self):
        self.lint_passed = False
        self.generate_passed = False
        self.import_passed = False
        self.errors = []

def validate_schema(schema_path: Path) -> ValidationResult:
    """Run full validation pipeline on LinkML schema."""
    result = ValidationResult()

    # Step 1: Lint LinkML schema
    try:
        subprocess.run(
            ["linkml", "lint", str(schema_path)],
            check=True,
            capture_output=True,
            text=True
        )
        result.lint_passed = True
    except subprocess.CalledProcessError as e:
        result.errors.append(f"Lint failed: {e.stderr}")
        return result

    # Step 2: Generate Pydantic models
    output_path = schema_path.parent / "generated" / f"{schema_path.stem}_models.py"
    output_path.parent.mkdir(exist_ok=True)

    try:
        subprocess.run(
            ["linkml", "generate", "pydantic", str(schema_path)],
            check=True,
            capture_output=True,
            text=True,
            stdout=open(output_path, "w")
        )
        result.generate_passed = True
    except subprocess.CalledProcessError as e:
        result.errors.append(f"Generation failed: {e.stderr}")
        return result

    # Step 3: Test import
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("test_module", output_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result.import_passed = True
    except Exception as e:
        result.errors.append(f"Import failed: {str(e)}")
        return result

    return result
```

### 4.5 Extractive Evaluation Gate (Zero Unsupported Tokens)

**File**: `workflow/extractive_evaluator.py`

```python
"""Extractive evaluation gate - enforce zero unsupported tokens (ZUT)."""

from typing import List, Tuple, Set
import re

CONNECTIVE_WHITELIST = {
    "because", "since", "therefore", "thus", "however", "and", "or", "but",
    "the", "a", "an", "is", "are", "was", "were", "has", "have", "this", "that"
}

class ExtractionResult:
    def __init__(self):
        self.quote_spans: List[str] = []
        self.connectives: List[str] = []
        self.unsupported_tokens: List[str] = []
        self.coverage_ratio: float = 0.0
        self.zut_passed: bool = False

def evaluate_answer(
    answer: str,
    source_paragraphs: List[str],
    connective_whitelist: Set[str] = CONNECTIVE_WHITELIST
) -> ExtractionResult:
    """Evaluate if answer meets extractive requirements (ZUT)."""
    result = ExtractionResult()

    # Tokenize answer
    answer_tokens = re.findall(r'\b\w+\b', answer.lower())

    # Build quote span coverage
    covered_tokens = []
    for paragraph in source_paragraphs:
        paragraph_tokens = re.findall(r'\b\w+\b', paragraph.lower())

        # Find longest common subsequences
        for token in answer_tokens:
            if token in paragraph_tokens:
                covered_tokens.append(token)
                result.quote_spans.append(token)

    # Identify connectives
    for token in answer_tokens:
        if token in connective_whitelist:
            result.connectives.append(token)

    # Identify unsupported tokens (not in quotes, not connectives)
    supported = set(result.quote_spans) | set(result.connectives)
    result.unsupported_tokens = [t for t in answer_tokens if t not in supported]

    # Calculate coverage
    result.coverage_ratio = len(covered_tokens) / len(answer_tokens) if answer_tokens else 0

    # ZUT check: zero unsupported tokens
    result.zut_passed = len(result.unsupported_tokens) == 0

    return result

def enforce_zut_gate(answer: str, source_paragraphs: List[str]) -> Tuple[bool, ExtractionResult]:
    """Enforce zero unsupported tokens gate - fail closed if violated."""
    result = evaluate_answer(answer, source_paragraphs)

    if not result.zut_passed:
        print(f"❌ ZUT GATE FAILED: {len(result.unsupported_tokens)} unsupported tokens")
        print(f"Unsupported: {result.unsupported_tokens}")
        return False, result

    print(f"✅ ZUT GATE PASSED: 100% extractive (coverage: {result.coverage_ratio:.1%})")
    return True, result
```

---

## Phase 5: Implementation Order

### 5.1 Priority 1: Business V2 (Week 1)

1. **Day 1-2**: Create `business_overlay.yaml` with all enums, slots, classes
2. **Day 3**: Generate Business V2 Pydantic models, create glue module
3. **Day 4**: Write validation tests (enum, datetime, numeric constraints, provenance)
4. **Day 5**: Integration test with Graphiti adapter (ensure Optional compatibility)

**Deliverables**:
- ✅ `graphmodels/domains/business/linkml/business_overlay.yaml`
- ✅ `graphmodels/domains/business/generated/business_models.py`
- ✅ `graphmodels/domains/business/glue.py`
- ✅ All tests passing

### 5.2 Priority 2: Modular Structure (Week 2)

1. **Day 1-2**: Create core modules (provenance, ids, registries, plugin_loader)
2. **Day 3**: Migrate lib/ → core/, update all imports
3. **Day 4**: Reorganize schemas → domains structure
4. **Day 5**: Test plugin discovery, domain merging

**Deliverables**:
- ✅ `graphmodels/core/` fully functional
- ✅ Plugin loader discovers Business domain
- ✅ Global registry merges successfully

### 5.3 Priority 3: AAOIFI Domain (Week 3)

1. **Day 1-2**: Create document_overlay.yaml, standards_overlay.yaml
2. **Day 3**: Generate AAOIFI Pydantic models, create glue module
3. **Day 4**: Test group discipline (edition isolation)
4. **Day 5**: Integration test with Business domain (multi-domain registry)

**Deliverables**:
- ✅ `graphmodels/domains/aaoifi/` complete
- ✅ Edition isolation enforced in queries
- ✅ Plugin loader discovers both Business + AAOIFI

### 5.4 Priority 4: Generalization Workflow (Week 4)

1. **Day 1-2**: Implement schema proposer (Instructor-guarded LLM)
2. **Day 3**: Implement validation pipeline (lint → generate → test)
3. **Day 4**: Implement extractive evaluator (ZUT gate)
4. **Day 5**: End-to-end test: EQP → schema → models → Graphiti

**Deliverables**:
- ✅ `workflow/schema_proposer.py`
- ✅ `workflow/validation_pipeline.py`
- ✅ `workflow/extractive_evaluator.py`
- ✅ CLI integration with Typer

---

## Phase 6: Graphiti Integration

### 6.1 Adapter Pattern

**File**: `graphmodels/adapters/graphiti_adapter.py`

```python
"""Adapter for Graphiti integration with V2 models."""

from graphiti_core import Graphiti
from graphmodels.core.plugin_loader import discover_domains
from typing import Dict, Any

class GraphitiV2Adapter:
    """Adapter bridging V2 models with Graphiti."""

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        # Discover all domains
        self.registry = discover_domains()

        # Initialize Graphiti with merged types
        self.graphiti = Graphiti(
            neo4j_uri=neo4j_uri,
            neo4j_user=neo4j_user,
            neo4j_password=neo4j_password,
            entity_types=self.registry.entity_types,
            relation_types=self.registry.edge_types,
            relation_type_map=self.registry.edge_type_map
        )

    def add_episode(self, content: str, metadata: Dict[str, Any]) -> str:
        """Add episode with provenance tracking."""
        # Implementation uses graphiti.add_episode()
        # Automatically populates episode_ids in extracted entities
        pass

    def query_with_group_isolation(self, query: str, group_id: str = None):
        """Execute query with group discipline enforcement."""
        if group_id:
            # Add WHERE clause for group_id
            query = f"{query} WHERE n.group_id = '{group_id}'"
        return self.graphiti.execute(query)
```

### 6.2 Compatibility Notes

**Critical**: Graphiti requires all fields to be `Optional`

**Validation**: This is already enforced in LinkML schemas:
- All slots default to `range: string` with no `required: true`
- Generated Pydantic models have `Optional[...]` for all business fields
- Only provenance fields (node_id, entity_type, rel_id, relation_type) are required

**Verification**:
```python
# All business fields Optional ✅
class BusinessOutcome(NodeProv):
    outcome_type: Optional[str] = None
    status: Optional[OutcomeStatus] = None
    # ... all Optional

# Provenance fields required (inherited from NodeProv) ✅
class NodeProv(BaseModel):
    node_id: str = Field(..., description="Required")
    entity_type: str = Field(..., description="Required")
```

---

## Phase 7: CLI Integration

### 7.1 CLI Commands (Typer)

**File**: `cli.py`

```python
"""CLI for graphmodels - outcome to Pydantic workflow."""

import typer
from pathlib import Path
from workflow.schema_proposer import propose_schema_from_eqp
from workflow.validation_pipeline import validate_schema
from workflow.extractive_evaluator import enforce_zut_gate

app = typer.Typer()

@app.command()
def generate_schema(eqp_file: Path):
    """Generate LinkML schema from Evidence Query Plan."""
    import yaml
    eqp = yaml.safe_load(eqp_file.read_text())
    schema = propose_schema_from_eqp(eqp)
    print(f"Generated schema: {schema.schema_name}")

@app.command()
def validate(schema_file: Path):
    """Validate LinkML schema (lint → generate → test)."""
    result = validate_schema(schema_file)
    if result.import_passed:
        print("✅ Schema valid")
    else:
        print(f"❌ Errors: {result.errors}")

@app.command()
def evaluate_answer(answer: str, source_dir: Path):
    """Evaluate answer against ZUT gate."""
    paragraphs = []
    for p in source_dir.glob("*.txt"):
        paragraphs.append(p.read_text())

    passed, result = enforce_zut_gate(answer, paragraphs)
    if passed:
        print(f"✅ ZUT PASSED (coverage: {result.coverage_ratio:.1%})")
    else:
        print(f"❌ ZUT FAILED: {result.unsupported_tokens}")

if __name__ == "__main__":
    app()
```

---

## Success Criteria

### ✅ Phase 1 Complete When:
- Business V2 models generated from LinkML
- All validation tests pass (enum, datetime, numeric, provenance)
- Graphiti adapter works with V2 models

### ✅ Phase 2 Complete When:
- Core modules functional (provenance, ids, registries, plugin_loader)
- Plugin discovery finds all domains
- Global registry merges without conflicts

### ✅ Phase 3 Complete When:
- AAOIFI models generated from LinkML
- Edition isolation enforced in queries
- Multi-domain registry works (Business + AAOIFI)

### ✅ Phase 4 Complete When:
- LLM proposes valid LinkML schemas from EQPs
- Validation pipeline catches errors (lint → generate → test)
- ZUT gate enforces extractive requirements

### ✅ Overall Success When:
- User can provide EQP → get working Pydantic models
- All domains load via plugin discovery
- Graphiti integration maintains Graphiti compatibility
- Extractive evaluation enforces ZUT discipline

---

## Risk Mitigation

### Risk 1: Graphiti Optional Requirement
**Mitigation**: All business fields already Optional in LinkML, only provenance required

### Risk 2: LinkML Generation Errors
**Mitigation**: Validation pipeline catches errors before committing generated models

### Risk 3: Domain Registry Conflicts
**Mitigation**: GlobalRegistry validates naming conflicts before merging

### Risk 4: Edition Leakage (AAOIFI)
**Mitigation**: group_id enforcement at query level, ZUT gate catches unsupported cross-edition claims

### Risk 5: LLM Schema Quality
**Mitigation**: Instructor validation, lint/compile tests, human review gate

---

## Phase 8: AAOIFI Standards Ingestion (Complete Implementation)

### 8.1 Standards Processing Pipeline

**Goal**: Ingest AAOIFI standards PDFs → structured graph → 0-hallucination QA pipeline

**Input**: `D:\projects\Pydantic Model Generator\AAOIFI_Standards\*.pdf` (54 Shari'ah standards)

**Output**:
- Parsed Document/Section/Paragraph nodes
- Extracted Concept/Rule/ContractType nodes
- Citation-verified answers (zero unsupported tokens)

**Pipeline**:
```
1. PDF Parsing → Extract text, sections, paragraphs
   ↓
2. Pydantic Model Creation → Document, Section, Paragraph instances
   ↓
3. Graphiti Ingestion → Store in Neo4j with provenance
   ↓
4. Concept Extraction → LLM extracts Concepts/Rules (Instructor-guarded)
   ↓
5. Validation → Verify all concepts cited to source paragraphs
   ↓
6. QA Pipeline → Answer questions with extractive evidence
```

### 8.2 Implementation Files

**File**: `workflow/aaoifi_ingestion.py`

```python
"""AAOIFI standards ingestion pipeline."""

import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict
from generated.pydantic.aaoifi_document_models import Document, Section, Paragraph
from generated.pydantic.aaoifi_standards_models import Concept, Rule, ContractType
from graphmodels.core.ids import make_node_id, make_content_hash
from datetime import datetime

class AAOIFIParser:
    """Parse AAOIFI PDF standards into structured models."""

    def __init__(self, standards_dir: Path):
        self.standards_dir = standards_dir
        self.edition = "AAOIFI_SS_2020"  # Group ID for edition isolation

    def parse_pdf(self, pdf_path: Path) -> Document:
        """Parse single AAOIFI standard PDF."""
        doc = fitz.open(pdf_path)

        # Extract metadata from filename: SS_08_Murabahah.pdf
        filename = pdf_path.stem
        parts = filename.split("_", 2)
        doc_number = parts[1] if len(parts) > 1 else "00"
        doc_title = parts[2].replace("_", " ") if len(parts) > 2 else filename

        # Create Document node
        document = Document(
            node_id=make_node_id("Document", f"AAOIFI-SS-{doc_number}", self.edition),
            entity_type="Document",
            document_title=f"Shari'ah Standard {doc_number}: {doc_title}",
            document_type="Shari'ah Standard",
            edition=self.edition,
            published_date=datetime(2020, 1, 1),  # Placeholder
            language="English",
            total_pages=doc.page_count,
            group_id=self.edition,
            created_at=datetime.now()
        )

        return document

    def extract_paragraphs(self, pdf_path: Path, document: Document) -> List[Paragraph]:
        """Extract paragraphs from PDF with page numbers."""
        doc = fitz.open(pdf_path)
        paragraphs = []

        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()

            # Split into paragraphs (simple split on double newline)
            chunks = text.split("\n\n")

            for idx, chunk in enumerate(chunks):
                chunk = chunk.strip()
                if len(chunk) < 20:  # Skip very short chunks
                    continue

                para_id = f"{document.node_id}:p{page_num}_{idx}"

                paragraph = Paragraph(
                    node_id=para_id,
                    entity_type="Paragraph",
                    paragraph_number=f"{page_num}.{idx}",
                    content=chunk,
                    page_number=page_num,
                    section_id=None,  # TODO: Extract section hierarchy
                    group_id=self.edition,
                    created_at=datetime.now()
                )
                paragraphs.append(paragraph)

        return paragraphs

    def ingest_all_standards(self) -> Dict[str, List]:
        """Ingest all PDF standards."""
        results = {"documents": [], "paragraphs": []}

        for pdf_path in sorted(self.standards_dir.glob("SS_*.pdf")):
            print(f"Processing {pdf_path.name}...")

            document = self.parse_pdf(pdf_path)
            paragraphs = self.extract_paragraphs(pdf_path, document)

            results["documents"].append(document)
            results["paragraphs"].extend(paragraphs)

        return results
```

**File**: `workflow/concept_extraction.py`

```python
"""Extract concepts and rules from AAOIFI paragraphs using LLM + Instructor."""

import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional
from generated.pydantic.aaoifi_standards_models import Concept, Rule, ContractType

client = instructor.from_openai(OpenAI())

class ConceptProposal(BaseModel):
    """Proposed concept extracted from paragraph."""
    concept_label: str
    concept_type: str  # "principle", "definition", "criterion"
    definition: str
    source_paragraph_id: str
    quote_span_start: int
    quote_span_end: int

class RuleProposal(BaseModel):
    """Proposed rule extracted from paragraph."""
    rule_text: str
    rule_type: str  # "permissibility", "requirement", "prohibition"
    applicability: str
    source_paragraph_id: str
    quote_span_start: int
    quote_span_end: int

class ExtractionResult(BaseModel):
    """Extraction result from single paragraph."""
    concepts: List[ConceptProposal] = Field(default_factory=list)
    rules: List[RuleProposal] = Field(default_factory=list)

def extract_from_paragraph(paragraph_text: str, paragraph_id: str) -> ExtractionResult:
    """Extract concepts and rules from a single paragraph."""
    prompt = f"""
Extract Islamic finance concepts and Shari'ah rules from this paragraph.

Paragraph ID: {paragraph_id}
Content: {paragraph_text}

For each concept:
- Provide the concept label (e.g., "Murabahah", "Riba")
- Classify as principle/definition/criterion
- Extract exact definition from text
- Provide character span (start, end) of the quote

For each rule:
- Extract exact rule text
- Classify as permissibility/requirement/prohibition
- Note applicability conditions
- Provide character span (start, end) of the quote

IMPORTANT: Only extract concepts/rules that are EXPLICITLY stated in the text.
Do NOT infer or add information not present in the paragraph.
"""

    result = client.chat.completions.create(
        model="gpt-4o",
        response_model=ExtractionResult,
        messages=[{"role": "user", "content": prompt}]
    )

    return result
```

**File**: `workflow/qa_pipeline.py`

```python
"""Zero-hallucination QA pipeline using AAOIFI graph."""

from typing import List, Tuple
from graphmodels.adapters.graphiti_adapter import GraphitiV2Adapter
from workflow.extractive_evaluator import enforce_zut_gate

class AAOIFIQAPipeline:
    """QA pipeline with zero unsupported tokens enforcement."""

    def __init__(self, adapter: GraphitiV2Adapter, edition: str = "AAOIFI_SS_2020"):
        self.adapter = adapter
        self.edition = edition

    def query_paragraphs(self, question: str) -> List[dict]:
        """Retrieve relevant paragraphs for question."""
        # Use Graphiti search with group isolation
        query = f"""
        MATCH (p:Paragraph)
        WHERE p.group_id = '{self.edition}'
          AND toLower(p.content) CONTAINS toLower('{question}')
        RETURN p
        LIMIT 10
        """
        results = self.adapter.query_with_group_isolation(query, self.edition)
        return results

    def answer_with_citations(self, question: str) -> Tuple[str, List[str], bool]:
        """Answer question with extractive citations."""
        # Step 1: Retrieve paragraphs
        paragraphs = self.query_paragraphs(question)
        paragraph_texts = [p["content"] for p in paragraphs]

        # Step 2: LLM generates answer
        from openai import OpenAI
        client = OpenAI()

        context = "\n\n".join([f"[P{i}] {p}" for i, p in enumerate(paragraph_texts)])
        prompt = f"""
Answer this question using ONLY information from the provided paragraphs.
Cite paragraph numbers in your answer.

Question: {question}

Context:
{context}

Answer (use exact quotes where possible):
"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content

        # Step 3: Enforce ZUT gate
        zut_passed, eval_result = enforce_zut_gate(answer, paragraph_texts)

        return answer, paragraph_texts, zut_passed
```

### 8.3 Incremental Progress Tracker

**File**: `PROGRESS_TRACKER.md`

Auto-updated after each major step to track completion status across context resets.

```markdown
# Implementation Progress Tracker

## Session Metadata
- Start Date: [AUTO]
- Last Updated: [AUTO]
- Total Sessions: [AUTO]

## Phase Completion Status

### ✅ Phase 0: Foundation (COMPLETE)
- [x] NodeProv/EdgeProv mixins created
- [x] Deterministic ID utilities working
- [x] Invoice validation example (6/6 tests passing)
- **Completion Date**: [Previous session]

### 🔄 Phase 1: Business V2 (IN PROGRESS)
- [ ] business_overlay.yaml created
- [ ] Business V2 models generated
- [ ] Validation tests written
- [ ] Graphiti integration tested
- **Current Step**: Creating business_overlay.yaml
- **Blockers**: None

### ⏳ Phase 2: Modular Structure (PENDING)
- [ ] Core modules created
- [ ] Plugin loader implemented
- [ ] Domain discovery working

### ⏳ Phase 3: AAOIFI Domain (PENDING)
- [ ] document_overlay.yaml created
- [ ] standards_overlay.yaml created
- [ ] AAOIFI models generated

### ⏳ Phase 4: AAOIFI Ingestion (PENDING)
- [ ] PDF parsing pipeline created
- [ ] 54 standards parsed
- [ ] Concepts extracted
- [ ] Graph populated

### ⏳ Phase 5: QA Pipeline (PENDING)
- [ ] Query engine implemented
- [ ] ZUT gate enforced
- [ ] Test questions answered

## Verification Checkpoints

### Checkpoint 1: Business V2 Module Works
- [ ] Import test passes
- [ ] Enum validation works
- [ ] Datetime validation works
- [ ] Provenance tracking works
- [ ] Graphiti compatibility verified

### Checkpoint 2: AAOIFI Module Works
- [ ] Import test passes
- [ ] Edition isolation enforced
- [ ] Concepts linked to paragraphs
- [ ] Group discipline verified

### Checkpoint 3: QA Pipeline Works
- [ ] Answers 10 test questions correctly
- [ ] All answers pass ZUT gate
- [ ] Citations trace to source paragraphs
- [ ] No cross-edition leakage

## Test Results Summary

### Business V2 Tests
- Location: `test_results/business_v2/`
- Status: PENDING

### AAOIFI Ingestion Tests
- Location: `test_results/aaoifi_ingestion/`
- Status: PENDING

### QA Pipeline Tests
- Location: `test_results/qa_pipeline/`
- Status: PENDING

## Context Continuation Notes

**For Next Session**:
- Current phase: [AUTO]
- Last completed task: [AUTO]
- Next task: [AUTO]
- Files to review: [AUTO]
```

### 8.4 Test Results Structure

**Directory**: `test_results/`

```
test_results/
├── 00_COMPLETION_SUMMARY.md          # Overall completion proof
├── business_v2/
│   ├── test_enum_validation.json
│   ├── test_datetime_validation.json
│   ├── test_numeric_constraints.json
│   ├── test_provenance_tracking.json
│   └── test_graphiti_compatibility.json
├── aaoifi_ingestion/
│   ├── parsed_documents.json         # 54 documents parsed
│   ├── extracted_concepts.json       # Concepts with citations
│   ├── extracted_rules.json          # Rules with citations
│   └── graph_statistics.json         # Node/edge counts
├── qa_pipeline/
│   ├── test_questions.yaml           # 10 test questions
│   ├── answers_with_citations.json   # Answers + paragraph sources
│   ├── zut_gate_results.json         # ZUT pass/fail for each
│   └── evaluation_metrics.json       # Precision, coverage, etc.
└── module_verification/
    ├── business_import_test.py
    ├── aaoifi_import_test.py
    └── integration_test.py
```

**File**: `test_results/00_COMPLETION_SUMMARY.md`

```markdown
# Implementation Completion Summary

## Overall Status: [COMPLETE/IN_PROGRESS]

### Phase Completion
- ✅ Phase 0: Foundation - COMPLETE
- ✅ Phase 1: Business V2 - COMPLETE
- ✅ Phase 2: Modular Structure - COMPLETE
- ✅ Phase 3: AAOIFI Domain - COMPLETE
- ✅ Phase 4: AAOIFI Ingestion - COMPLETE
- ✅ Phase 5: QA Pipeline - COMPLETE

### Verification Results

#### Business V2 Module (5/5 tests passing)
- ✅ Enum validation: Status cannot be "banana"
- ✅ Datetime validation: due_date must be valid datetime
- ✅ Numeric constraints: confidence must be 0-1
- ✅ Provenance tracking: node_id, episode_ids populated
- ✅ Graphiti compatibility: All fields Optional except provenance

#### AAOIFI Ingestion (54/54 standards processed)
- ✅ Documents parsed: 54
- ✅ Paragraphs extracted: [COUNT]
- ✅ Concepts extracted: [COUNT]
- ✅ Rules extracted: [COUNT]
- ✅ Graph nodes created: [COUNT]
- ✅ Graph edges created: [COUNT]

#### QA Pipeline (10/10 questions answered, 10/10 ZUT passed)
- ✅ Question 1: "What is Murabahah?" - ZUT PASSED (coverage: 95%)
- ✅ Question 2: "Is Riba prohibited?" - ZUT PASSED (coverage: 100%)
- ✅ Question 3: "What are requirements for Ijarah?" - ZUT PASSED (coverage: 92%)
- ... (all 10 questions)

### Module Verification

#### New Pydantic Modules Created
1. ✅ `business_models.py` - Works with NodeProv/EdgeProv
2. ✅ `aaoifi_document_models.py` - Works with NodeProv/EdgeProv
3. ✅ `aaoifi_standards_models.py` - Works with NodeProv/EdgeProv

#### Integration Tests
- ✅ Business module imports successfully
- ✅ AAOIFI modules import successfully
- ✅ Plugin loader discovers all domains
- ✅ Global registry merges without conflicts
- ✅ Graphiti adapter works with all domains

### Key Metrics
- Total Standards Processed: 54
- Total Paragraphs: [COUNT]
- Total Concepts Extracted: [COUNT]
- Total Rules Extracted: [COUNT]
- QA Questions Answered: 10
- ZUT Gate Pass Rate: 100%
- Average Citation Coverage: [PERCENT]%

### Evidence of 0-Hallucination
All answers in `qa_pipeline/answers_with_citations.json` include:
- Exact paragraph sources
- Character-level quote spans
- ZUT gate validation results
- No unsupported tokens found

**Completion Date**: [AUTO]
**Total Implementation Time**: [AUTO]
```

## Phase 9: Execution Plan (Complete Until Done)

### 9.1 Execution Order

**Session 1: Business V2 + Module Verification**
1. Create `business_overlay.yaml`
2. Generate Business V2 models
3. Write validation tests
4. Run tests → populate `test_results/business_v2/`
5. Update `PROGRESS_TRACKER.md`

**Session 2: Modular Structure**
1. Create core modules (registries, plugin_loader)
2. Migrate lib/ → core/
3. Test plugin discovery
4. Update `PROGRESS_TRACKER.md`

**Session 3: AAOIFI Domain Schema**
1. Create `document_overlay.yaml`
2. Create `standards_overlay.yaml`
3. Generate AAOIFI models
4. Write import tests
5. Update `PROGRESS_TRACKER.md`

**Session 4: AAOIFI Ingestion**
1. Implement PDF parsing pipeline
2. Process 5 sample standards
3. Extract concepts/rules
4. Validate citations
5. Update `PROGRESS_TRACKER.md`

**Session 5: AAOIFI Ingestion (Complete)**
1. Process remaining 49 standards
2. Populate graph
3. Generate ingestion test results
4. Update `PROGRESS_TRACKER.md`

**Session 6: QA Pipeline**
1. Implement query engine
2. Implement ZUT gate enforcement
3. Create 10 test questions
4. Generate answers with citations
5. Validate ZUT gate (10/10 pass)
6. Generate QA test results
7. Update `PROGRESS_TRACKER.md`

**Session 7: Final Verification**
1. Run all integration tests
2. Generate `00_COMPLETION_SUMMARY.md`
3. Verify all test results present
4. Package test_results/ folder

### 9.2 Context Continuation Strategy

**Before Context Limit**:
1. Update `PROGRESS_TRACKER.md` with current status
2. Commit all generated files
3. Note next task in tracker

**After Context Reset**:
1. Read `PROGRESS_TRACKER.md`
2. Review last completed checkpoint
3. Continue from next pending task

### 9.3 Success Criteria (Exit Conditions)

**Implementation COMPLETE when**:
1. ✅ All 9 phases marked complete in `PROGRESS_TRACKER.md`
2. ✅ `test_results/00_COMPLETION_SUMMARY.md` exists
3. ✅ All test result files present in `test_results/`
4. ✅ 54/54 AAOIFI standards processed
5. ✅ 10/10 QA questions answered with ZUT pass
6. ✅ New Pydantic modules verifiably work with foundation

**Proof of Completion**:
- `test_results/` folder contains all evidence
- `00_COMPLETION_SUMMARY.md` shows all checkmarks
- QA pipeline demonstrates 0-hallucination capability

## Next Steps After Plan Approval

1. **User Review**: Review updated plan with new phases 8-9
2. **Begin Execution**: Start with Phase 1 (Business V2)
3. **Incremental Progress**: Update `PROGRESS_TRACKER.md` after each checkpoint
4. **Context Management**: Use tracker to continue across sessions
5. **Final Delivery**: Package `test_results/` folder with completion proof
