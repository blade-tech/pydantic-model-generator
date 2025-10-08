from __future__ import annotations 

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal 
from enum import Enum 
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)


metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'bca',
     'description': 'Schema for surfacing and tracking business contradictions to '
                    'enable proper adjudication and resolution of conflicting '
                    'constraints, policies, and rules',
     'id': 'https://example.org/schemas/business-contradiction-adjudication',
     'imports': ['../core/provenance'],
     'name': 'business_contradiction_adjudication',
     'prefixes': {'bca': {'prefix_prefix': 'bca',
                          'prefix_reference': 'https://example.org/schemas/business-contradiction-adjudication/'},
                  'doco': {'prefix_prefix': 'doco',
                           'prefix_reference': 'http://purl.org/spar/doco/'},
                  'fabio': {'prefix_prefix': 'fabio',
                            'prefix_reference': 'http://purl.org/spar/fabio/'},
                  'fibo': {'prefix_prefix': 'fibo',
                           'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'}},
     'source_file': '..\\..\\pydantic_library\\schemas\\overlays\\business-contradiction-adjudication_overlay.yaml'} )

class SeverityEnum(str, Enum):
    """
    Severity levels for contradictions and conflicts
    """
    critical = "critical"
    """
    Critical severity requiring immediate attention
    """
    high = "high"
    """
    High severity requiring prompt attention
    """
    medium = "medium"
    """
    Medium severity
    """
    low = "low"
    """
    Low severity
    """
    info = "info"
    """
    Informational only
    """


class StatusEnum(str, Enum):
    """
    Status values for contradictions and activities
    """
    detected = "detected"
    """
    Contradiction detected but not yet assigned
    """
    assigned = "assigned"
    """
    Assigned for adjudication
    """
    in_progress = "in_progress"
    """
    Adjudication in progress
    """
    completed = "completed"
    """
    Adjudication completed
    """
    resolved = "resolved"
    """
    Contradiction resolved
    """
    closed = "closed"
    """
    Closed without resolution
    """


class ConstraintTypeEnum(str, Enum):
    """
    Types of business constraints
    """
    policy = "policy"
    """
    Business policy
    """
    rule = "rule"
    """
    Business rule
    """
    regulation = "regulation"
    """
    Regulatory requirement
    """
    guideline = "guideline"
    """
    Guideline or best practice
    """
    standard = "standard"
    """
    Standard or specification
    """
    requirement = "requirement"
    """
    Business requirement
    """


class EvidenceTypeEnum(str, Enum):
    """
    Types of contradiction evidence
    """
    system_log = "system_log"
    """
    Evidence from system logs
    """
    data_analysis = "data_analysis"
    """
    Evidence from data analysis
    """
    user_report = "user_report"
    """
    Evidence from user reports
    """
    automated_detection = "automated_detection"
    """
    Evidence from automated detection
    """
    manual_review = "manual_review"
    """
    Evidence from manual review
    """
    external_source = "external_source"
    """
    Evidence from external sources
    """


class DecisionEnum(str, Enum):
    """
    Types of adjudication decisions
    """
    accept_constraint_a = "accept_constraint_a"
    """
    Accept first constraint, modify or remove second
    """
    accept_constraint_b = "accept_constraint_b"
    """
    Accept second constraint, modify or remove first
    """
    modify_both = "modify_both"
    """
    Modify both constraints to resolve conflict
    """
    create_exception = "create_exception"
    """
    Create exception rule to handle both
    """
    escalate = "escalate"
    """
    Escalate to higher authority
    """
    defer = "defer"
    """
    Defer decision pending additional information
    """
    merge = "merge"
    """
    Merge constraints into single unified constraint
    """


class ApprovalStatusEnum(str, Enum):
    """
    Approval status for decisions
    """
    draft = "draft"
    """
    Decision in draft form
    """
    pending_approval = "pending_approval"
    """
    Awaiting approval
    """
    approved = "approved"
    """
    Decision approved
    """
    rejected = "rejected"
    """
    Decision rejected
    """
    implemented = "implemented"
    """
    Decision implemented
    """


class ConflictTypeEnum(str, Enum):
    """
    Types of conflicts between constraints
    """
    logical_contradiction = "logical_contradiction"
    """
    Logical contradiction between rules
    """
    priority_conflict = "priority_conflict"
    """
    Conflict in priorities
    """
    scope_overlap = "scope_overlap"
    """
    Overlapping scopes with different requirements
    """
    temporal_conflict = "temporal_conflict"
    """
    Conflicting time-based requirements
    """
    resource_conflict = "resource_conflict"
    """
    Conflicting resource allocation
    """
    authority_conflict = "authority_conflict"
    """
    Conflicting authority or ownership
    """



class ProvenanceFields(ConfiguredBaseModel):
    """
    Provenance mixin for nodes
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Entity',
         'from_schema': 'https://example.org/core/provenance',
         'mixin': True})

    node_id: Optional[str] = Field(default=None, description="""Stable citation id (deterministic)""", json_schema_extra = { "linkml_meta": {'alias': 'node_id',
         'domain_of': ['ProvenanceFields'],
         'slot_uri': 'prov:identifier'} })
    prov_system: Optional[str] = Field(default=None, description="""Primary source system (e.g., slack, gdrive, aaoifi_db)""", json_schema_extra = { "linkml_meta": {'alias': 'prov_system',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields'],
         'slot_uri': 'prov:wasAttributedTo'} })
    prov_channel_ids: Optional[list[str]] = Field(default=None, description="""Slack channel IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_channel_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_thread_tss: Optional[list[str]] = Field(default=None, description="""Slack thread timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_thread_tss',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_tss: Optional[list[str]] = Field(default=None, description="""Slack message timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_tss', 'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_permalinks: Optional[list[str]] = Field(default=None, description="""Slack permalinks""", json_schema_extra = { "linkml_meta": {'alias': 'prov_permalinks',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_file_ids: Optional[list[str]] = Field(default=None, description="""Document/file identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'prov_file_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_rev_ids: Optional[list[str]] = Field(default=None, description="""Document revision IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_rev_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_text_sha1s: Optional[list[str]] = Field(default=None, description="""SHA1 hashes of source text""", json_schema_extra = { "linkml_meta": {'alias': 'prov_text_sha1s',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_types: Optional[list[str]] = Field(default=None, description="""Document component types (section, paragraph, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'doco_types',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_paths: Optional[list[str]] = Field(default=None, description="""Document structural paths""", json_schema_extra = { "linkml_meta": {'alias': 'doco_paths',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    page_nums: Optional[list[int]] = Field(default=None, description="""Page numbers""", json_schema_extra = { "linkml_meta": {'alias': 'page_nums',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    support_count: Optional[int] = Field(default=None, description="""Number of supporting evidences""", ge=0, json_schema_extra = { "linkml_meta": {'alias': 'support_count',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })


class EdgeProvenanceFields(ConfiguredBaseModel):
    """
    Provenance mixin for edges
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Entity',
         'from_schema': 'https://example.org/core/provenance',
         'mixin': True})

    rel_id: Optional[str] = Field(default=None, description="""Stable relationship id (deterministic)""", json_schema_extra = { "linkml_meta": {'alias': 'rel_id',
         'domain_of': ['EdgeProvenanceFields'],
         'slot_uri': 'prov:identifier'} })
    prov_system: Optional[str] = Field(default=None, description="""Primary source system (e.g., slack, gdrive, aaoifi_db)""", json_schema_extra = { "linkml_meta": {'alias': 'prov_system',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields'],
         'slot_uri': 'prov:wasAttributedTo'} })
    prov_channel_ids: Optional[list[str]] = Field(default=None, description="""Slack channel IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_channel_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_thread_tss: Optional[list[str]] = Field(default=None, description="""Slack thread timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_thread_tss',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_tss: Optional[list[str]] = Field(default=None, description="""Slack message timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_tss', 'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_permalinks: Optional[list[str]] = Field(default=None, description="""Slack permalinks""", json_schema_extra = { "linkml_meta": {'alias': 'prov_permalinks',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_file_ids: Optional[list[str]] = Field(default=None, description="""Document/file identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'prov_file_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_rev_ids: Optional[list[str]] = Field(default=None, description="""Document revision IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_rev_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_text_sha1s: Optional[list[str]] = Field(default=None, description="""SHA1 hashes of source text""", json_schema_extra = { "linkml_meta": {'alias': 'prov_text_sha1s',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_types: Optional[list[str]] = Field(default=None, description="""Document component types (section, paragraph, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'doco_types',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_paths: Optional[list[str]] = Field(default=None, description="""Document structural paths""", json_schema_extra = { "linkml_meta": {'alias': 'doco_paths',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    page_nums: Optional[list[int]] = Field(default=None, description="""Page numbers""", json_schema_extra = { "linkml_meta": {'alias': 'page_nums',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    derived: Optional[bool] = Field(default=None, description="""Whether derived vs directly extracted""", json_schema_extra = { "linkml_meta": {'alias': 'derived', 'domain_of': ['EdgeProvenanceFields']} })
    derivation_rule: Optional[str] = Field(default=None, description="""Rule or method used for derivation""", json_schema_extra = { "linkml_meta": {'alias': 'derivation_rule', 'domain_of': ['EdgeProvenanceFields']} })
    support_count: Optional[int] = Field(default=None, description="""Number of supporting evidences""", ge=0, json_schema_extra = { "linkml_meta": {'alias': 'support_count',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })


class Contradiction(ProvenanceFields):
    """
    A business contradiction representing conflicting constraints, policies, or rules within the system
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'skos:Concept',
         'from_schema': 'https://example.org/schemas/business-contradiction-adjudication',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'contradiction_id': {'identifier': True,
                                             'name': 'contradiction_id',
                                             'required': True},
                        'detected_at': {'name': 'detected_at', 'required': True},
                        'severity': {'name': 'severity', 'required': True},
                        'status': {'name': 'status', 'required': True}}})

    contradiction_id: str = Field(default=..., description="""Unique identifier for the contradiction""", json_schema_extra = { "linkml_meta": {'alias': 'contradiction_id', 'domain_of': ['Contradiction']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Contradiction', 'ContradictionEvidence']} })
    severity: SeverityEnum = Field(default=..., description="""Severity level of the contradiction""", json_schema_extra = { "linkml_meta": {'alias': 'severity', 'domain_of': ['Contradiction']} })
    detected_at: datetime  = Field(default=..., description="""Timestamp when the contradiction was detected""", json_schema_extra = { "linkml_meta": {'alias': 'detected_at', 'domain_of': ['Contradiction']} })
    status: StatusEnum = Field(default=..., description="""Current status of the contradiction or activity""", json_schema_extra = { "linkml_meta": {'alias': 'status', 'domain_of': ['Contradiction', 'AdjudicationActivity']} })
    resolution_notes: Optional[str] = Field(default=None, description="""Notes about the resolution of the contradiction""", json_schema_extra = { "linkml_meta": {'alias': 'resolution_notes', 'domain_of': ['Contradiction']} })
    has_conflict_with: Optional[list[str]] = Field(default=None, description="""Business constraints that this contradiction involves""", json_schema_extra = { "linkml_meta": {'alias': 'has_conflict_with',
         'domain_of': ['Contradiction'],
         'slot_uri': 'bca:HAS_CONFLICT'} })
    supported_by_evidence: Optional[list[str]] = Field(default=None, description="""Evidence supporting this contradiction""", json_schema_extra = { "linkml_meta": {'alias': 'supported_by_evidence',
         'domain_of': ['Contradiction'],
         'slot_uri': 'bca:SUPPORTED_BY'} })
    adjudicated_by_activity: Optional[list[str]] = Field(default=None, description="""Adjudication activities addressing this contradiction""", json_schema_extra = { "linkml_meta": {'alias': 'adjudicated_by_activity',
         'domain_of': ['Contradiction'],
         'inverse': 'adjudicates_contradiction'} })
    node_id: Optional[str] = Field(default=None, description="""Stable citation id (deterministic)""", json_schema_extra = { "linkml_meta": {'alias': 'node_id',
         'domain_of': ['ProvenanceFields'],
         'slot_uri': 'prov:identifier'} })
    prov_system: Optional[str] = Field(default=None, description="""Primary source system (e.g., slack, gdrive, aaoifi_db)""", json_schema_extra = { "linkml_meta": {'alias': 'prov_system',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields'],
         'slot_uri': 'prov:wasAttributedTo'} })
    prov_channel_ids: Optional[list[str]] = Field(default=None, description="""Slack channel IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_channel_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_thread_tss: Optional[list[str]] = Field(default=None, description="""Slack thread timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_thread_tss',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_tss: Optional[list[str]] = Field(default=None, description="""Slack message timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_tss', 'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_permalinks: Optional[list[str]] = Field(default=None, description="""Slack permalinks""", json_schema_extra = { "linkml_meta": {'alias': 'prov_permalinks',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_file_ids: Optional[list[str]] = Field(default=None, description="""Document/file identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'prov_file_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_rev_ids: Optional[list[str]] = Field(default=None, description="""Document revision IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_rev_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_text_sha1s: Optional[list[str]] = Field(default=None, description="""SHA1 hashes of source text""", json_schema_extra = { "linkml_meta": {'alias': 'prov_text_sha1s',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_types: Optional[list[str]] = Field(default=None, description="""Document component types (section, paragraph, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'doco_types',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_paths: Optional[list[str]] = Field(default=None, description="""Document structural paths""", json_schema_extra = { "linkml_meta": {'alias': 'doco_paths',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    page_nums: Optional[list[int]] = Field(default=None, description="""Page numbers""", json_schema_extra = { "linkml_meta": {'alias': 'page_nums',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    support_count: Optional[int] = Field(default=None, description="""Number of supporting evidences""", ge=0, json_schema_extra = { "linkml_meta": {'alias': 'support_count',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })


class BusinessConstraint(ProvenanceFields):
    """
    A business rule, policy, or constraint that may conflict with other constraints
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Entity',
         'from_schema': 'https://example.org/schemas/business-contradiction-adjudication',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'constraint_id': {'identifier': True,
                                          'name': 'constraint_id',
                                          'required': True},
                        'constraint_type': {'name': 'constraint_type',
                                            'required': True},
                        'name': {'name': 'name', 'required': True}}})

    constraint_id: str = Field(default=..., description="""Unique identifier for the business constraint""", json_schema_extra = { "linkml_meta": {'alias': 'constraint_id', 'domain_of': ['BusinessConstraint']} })
    name: str = Field(default=..., description="""Name of the entity""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['BusinessConstraint', 'Adjudicator']} })
    constraint_type: ConstraintTypeEnum = Field(default=..., description="""Type or category of the business constraint""", json_schema_extra = { "linkml_meta": {'alias': 'constraint_type', 'domain_of': ['BusinessConstraint']} })
    rule: Optional[str] = Field(default=None, description="""The formal rule or policy statement""", json_schema_extra = { "linkml_meta": {'alias': 'rule', 'domain_of': ['BusinessConstraint']} })
    scope: Optional[str] = Field(default=None, description="""Scope of applicability for the constraint""", json_schema_extra = { "linkml_meta": {'alias': 'scope', 'domain_of': ['BusinessConstraint']} })
    priority: Optional[int] = Field(default=None, description="""Priority level of the constraint or activity""", json_schema_extra = { "linkml_meta": {'alias': 'priority',
         'domain_of': ['BusinessConstraint', 'AdjudicationActivity']} })
    owner: Optional[str] = Field(default=None, description="""Owner or responsible party for the constraint""", json_schema_extra = { "linkml_meta": {'alias': 'owner', 'domain_of': ['BusinessConstraint']} })
    effective_date: Optional[date] = Field(default=None, description="""Date when the constraint becomes effective""", json_schema_extra = { "linkml_meta": {'alias': 'effective_date', 'domain_of': ['BusinessConstraint']} })
    expiration_date: Optional[date] = Field(default=None, description="""Date when the constraint expires""", json_schema_extra = { "linkml_meta": {'alias': 'expiration_date', 'domain_of': ['BusinessConstraint']} })
    conflicts_with: Optional[list[str]] = Field(default=None, description="""Other constraints that conflict with this constraint""", json_schema_extra = { "linkml_meta": {'alias': 'conflicts_with', 'domain_of': ['BusinessConstraint']} })
    node_id: Optional[str] = Field(default=None, description="""Stable citation id (deterministic)""", json_schema_extra = { "linkml_meta": {'alias': 'node_id',
         'domain_of': ['ProvenanceFields'],
         'slot_uri': 'prov:identifier'} })
    prov_system: Optional[str] = Field(default=None, description="""Primary source system (e.g., slack, gdrive, aaoifi_db)""", json_schema_extra = { "linkml_meta": {'alias': 'prov_system',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields'],
         'slot_uri': 'prov:wasAttributedTo'} })
    prov_channel_ids: Optional[list[str]] = Field(default=None, description="""Slack channel IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_channel_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_thread_tss: Optional[list[str]] = Field(default=None, description="""Slack thread timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_thread_tss',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_tss: Optional[list[str]] = Field(default=None, description="""Slack message timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_tss', 'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_permalinks: Optional[list[str]] = Field(default=None, description="""Slack permalinks""", json_schema_extra = { "linkml_meta": {'alias': 'prov_permalinks',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_file_ids: Optional[list[str]] = Field(default=None, description="""Document/file identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'prov_file_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_rev_ids: Optional[list[str]] = Field(default=None, description="""Document revision IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_rev_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_text_sha1s: Optional[list[str]] = Field(default=None, description="""SHA1 hashes of source text""", json_schema_extra = { "linkml_meta": {'alias': 'prov_text_sha1s',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_types: Optional[list[str]] = Field(default=None, description="""Document component types (section, paragraph, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'doco_types',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_paths: Optional[list[str]] = Field(default=None, description="""Document structural paths""", json_schema_extra = { "linkml_meta": {'alias': 'doco_paths',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    page_nums: Optional[list[int]] = Field(default=None, description="""Page numbers""", json_schema_extra = { "linkml_meta": {'alias': 'page_nums',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    support_count: Optional[int] = Field(default=None, description="""Number of supporting evidences""", ge=0, json_schema_extra = { "linkml_meta": {'alias': 'support_count',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })


class ContradictionEvidence(ProvenanceFields):
    """
    Evidence supporting the identification of a contradiction, including source data and provenance
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Entity',
         'from_schema': 'https://example.org/schemas/business-contradiction-adjudication',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'captured_at': {'name': 'captured_at', 'required': True},
                        'evidence_id': {'identifier': True,
                                        'name': 'evidence_id',
                                        'required': True},
                        'source': {'name': 'source', 'required': True}}})

    evidence_id: str = Field(default=..., description="""Unique identifier for the evidence""", json_schema_extra = { "linkml_meta": {'alias': 'evidence_id', 'domain_of': ['ContradictionEvidence']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Contradiction', 'ContradictionEvidence']} })
    source: str = Field(default=..., description="""Source system or origin of the evidence""", json_schema_extra = { "linkml_meta": {'alias': 'source', 'domain_of': ['ContradictionEvidence']} })
    captured_at: datetime  = Field(default=..., description="""Timestamp when the evidence was captured""", json_schema_extra = { "linkml_meta": {'alias': 'captured_at', 'domain_of': ['ContradictionEvidence']} })
    confidence_score: Optional[float] = Field(default=None, description="""Confidence score for the evidence""", ge=0.0, le=1.0, json_schema_extra = { "linkml_meta": {'alias': 'confidence_score', 'domain_of': ['ContradictionEvidence']} })
    evidence_type: Optional[EvidenceTypeEnum] = Field(default=None, description="""Type of evidence""", json_schema_extra = { "linkml_meta": {'alias': 'evidence_type', 'domain_of': ['ContradictionEvidence']} })
    raw_data: Optional[str] = Field(default=None, description="""Raw data supporting the evidence""", json_schema_extra = { "linkml_meta": {'alias': 'raw_data', 'domain_of': ['ContradictionEvidence']} })
    supports_contradiction: Optional[str] = Field(default=None, description="""Contradiction that this evidence supports""", json_schema_extra = { "linkml_meta": {'alias': 'supports_contradiction',
         'domain_of': ['ContradictionEvidence'],
         'inverse': 'supported_by_evidence'} })
    node_id: Optional[str] = Field(default=None, description="""Stable citation id (deterministic)""", json_schema_extra = { "linkml_meta": {'alias': 'node_id',
         'domain_of': ['ProvenanceFields'],
         'slot_uri': 'prov:identifier'} })
    prov_system: Optional[str] = Field(default=None, description="""Primary source system (e.g., slack, gdrive, aaoifi_db)""", json_schema_extra = { "linkml_meta": {'alias': 'prov_system',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields'],
         'slot_uri': 'prov:wasAttributedTo'} })
    prov_channel_ids: Optional[list[str]] = Field(default=None, description="""Slack channel IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_channel_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_thread_tss: Optional[list[str]] = Field(default=None, description="""Slack thread timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_thread_tss',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_tss: Optional[list[str]] = Field(default=None, description="""Slack message timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_tss', 'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_permalinks: Optional[list[str]] = Field(default=None, description="""Slack permalinks""", json_schema_extra = { "linkml_meta": {'alias': 'prov_permalinks',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_file_ids: Optional[list[str]] = Field(default=None, description="""Document/file identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'prov_file_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_rev_ids: Optional[list[str]] = Field(default=None, description="""Document revision IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_rev_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_text_sha1s: Optional[list[str]] = Field(default=None, description="""SHA1 hashes of source text""", json_schema_extra = { "linkml_meta": {'alias': 'prov_text_sha1s',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_types: Optional[list[str]] = Field(default=None, description="""Document component types (section, paragraph, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'doco_types',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_paths: Optional[list[str]] = Field(default=None, description="""Document structural paths""", json_schema_extra = { "linkml_meta": {'alias': 'doco_paths',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    page_nums: Optional[list[int]] = Field(default=None, description="""Page numbers""", json_schema_extra = { "linkml_meta": {'alias': 'page_nums',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    support_count: Optional[int] = Field(default=None, description="""Number of supporting evidences""", ge=0, json_schema_extra = { "linkml_meta": {'alias': 'support_count',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })


class AdjudicationActivity(ProvenanceFields):
    """
    The process of adjudicating a contradiction to reach a resolution decision
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Activity',
         'from_schema': 'https://example.org/schemas/business-contradiction-adjudication',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'activity_id': {'identifier': True,
                                        'name': 'activity_id',
                                        'required': True},
                        'started_at': {'name': 'started_at', 'required': True},
                        'status': {'name': 'status', 'required': True}}})

    activity_id: str = Field(default=..., description="""Unique identifier for the adjudication activity""", json_schema_extra = { "linkml_meta": {'alias': 'activity_id', 'domain_of': ['AdjudicationActivity']} })
    status: StatusEnum = Field(default=..., description="""Current status of the contradiction or activity""", json_schema_extra = { "linkml_meta": {'alias': 'status', 'domain_of': ['Contradiction', 'AdjudicationActivity']} })
    started_at: datetime  = Field(default=..., description="""Timestamp when the activity started""", json_schema_extra = { "linkml_meta": {'alias': 'started_at', 'domain_of': ['AdjudicationActivity']} })
    completed_at: Optional[datetime ] = Field(default=None, description="""Timestamp when the activity completed""", json_schema_extra = { "linkml_meta": {'alias': 'completed_at', 'domain_of': ['AdjudicationActivity']} })
    priority: Optional[int] = Field(default=None, description="""Priority level of the constraint or activity""", json_schema_extra = { "linkml_meta": {'alias': 'priority',
         'domain_of': ['BusinessConstraint', 'AdjudicationActivity']} })
    notes: Optional[str] = Field(default=None, description="""Additional notes or comments""", json_schema_extra = { "linkml_meta": {'alias': 'notes', 'domain_of': ['AdjudicationActivity']} })
    adjudicates_contradiction: Optional[str] = Field(default=None, description="""Contradiction being adjudicated""", json_schema_extra = { "linkml_meta": {'alias': 'adjudicates_contradiction',
         'domain_of': ['AdjudicationActivity'],
         'slot_uri': 'bca:ADJUDICATES'} })
    performed_by_adjudicator: Optional[str] = Field(default=None, description="""Adjudicator performing this activity""", json_schema_extra = { "linkml_meta": {'alias': 'performed_by_adjudicator',
         'domain_of': ['AdjudicationActivity'],
         'slot_uri': 'prov:wasAssociatedWith'} })
    resulted_in_decision: Optional[str] = Field(default=None, description="""Decision resulting from this activity""", json_schema_extra = { "linkml_meta": {'alias': 'resulted_in_decision',
         'domain_of': ['AdjudicationActivity'],
         'slot_uri': 'bca:RESULTED_IN'} })
    node_id: Optional[str] = Field(default=None, description="""Stable citation id (deterministic)""", json_schema_extra = { "linkml_meta": {'alias': 'node_id',
         'domain_of': ['ProvenanceFields'],
         'slot_uri': 'prov:identifier'} })
    prov_system: Optional[str] = Field(default=None, description="""Primary source system (e.g., slack, gdrive, aaoifi_db)""", json_schema_extra = { "linkml_meta": {'alias': 'prov_system',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields'],
         'slot_uri': 'prov:wasAttributedTo'} })
    prov_channel_ids: Optional[list[str]] = Field(default=None, description="""Slack channel IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_channel_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_thread_tss: Optional[list[str]] = Field(default=None, description="""Slack thread timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_thread_tss',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_tss: Optional[list[str]] = Field(default=None, description="""Slack message timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_tss', 'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_permalinks: Optional[list[str]] = Field(default=None, description="""Slack permalinks""", json_schema_extra = { "linkml_meta": {'alias': 'prov_permalinks',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_file_ids: Optional[list[str]] = Field(default=None, description="""Document/file identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'prov_file_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_rev_ids: Optional[list[str]] = Field(default=None, description="""Document revision IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_rev_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_text_sha1s: Optional[list[str]] = Field(default=None, description="""SHA1 hashes of source text""", json_schema_extra = { "linkml_meta": {'alias': 'prov_text_sha1s',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_types: Optional[list[str]] = Field(default=None, description="""Document component types (section, paragraph, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'doco_types',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_paths: Optional[list[str]] = Field(default=None, description="""Document structural paths""", json_schema_extra = { "linkml_meta": {'alias': 'doco_paths',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    page_nums: Optional[list[int]] = Field(default=None, description="""Page numbers""", json_schema_extra = { "linkml_meta": {'alias': 'page_nums',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    support_count: Optional[int] = Field(default=None, description="""Number of supporting evidences""", ge=0, json_schema_extra = { "linkml_meta": {'alias': 'support_count',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })


class Adjudicator(ProvenanceFields):
    """
    An agent (person or system) responsible for adjudicating contradictions and making resolution decisions
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Agent',
         'from_schema': 'https://example.org/schemas/business-contradiction-adjudication',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'adjudicator_id': {'identifier': True,
                                           'name': 'adjudicator_id',
                                           'required': True},
                        'name': {'name': 'name', 'required': True},
                        'role': {'name': 'role', 'required': True}}})

    adjudicator_id: str = Field(default=..., description="""Unique identifier for the adjudicator""", json_schema_extra = { "linkml_meta": {'alias': 'adjudicator_id', 'domain_of': ['Adjudicator']} })
    name: str = Field(default=..., description="""Name of the entity""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['BusinessConstraint', 'Adjudicator']} })
    role: str = Field(default=..., description="""Role or title of the adjudicator""", json_schema_extra = { "linkml_meta": {'alias': 'role', 'domain_of': ['Adjudicator']} })
    department: Optional[str] = Field(default=None, description="""Department or organizational unit""", json_schema_extra = { "linkml_meta": {'alias': 'department', 'domain_of': ['Adjudicator']} })
    expertise_areas: Optional[list[str]] = Field(default=None, description="""Areas of expertise for the adjudicator""", json_schema_extra = { "linkml_meta": {'alias': 'expertise_areas', 'domain_of': ['Adjudicator']} })
    contact_info: Optional[str] = Field(default=None, description="""Contact information""", json_schema_extra = { "linkml_meta": {'alias': 'contact_info', 'domain_of': ['Adjudicator']} })
    authorization_level: Optional[int] = Field(default=None, description="""Authorization level for decision-making""", json_schema_extra = { "linkml_meta": {'alias': 'authorization_level', 'domain_of': ['Adjudicator']} })
    performs_adjudication: Optional[list[str]] = Field(default=None, description="""Adjudication activities performed by this adjudicator""", json_schema_extra = { "linkml_meta": {'alias': 'performs_adjudication',
         'domain_of': ['Adjudicator'],
         'inverse': 'performed_by_adjudicator'} })
    node_id: Optional[str] = Field(default=None, description="""Stable citation id (deterministic)""", json_schema_extra = { "linkml_meta": {'alias': 'node_id',
         'domain_of': ['ProvenanceFields'],
         'slot_uri': 'prov:identifier'} })
    prov_system: Optional[str] = Field(default=None, description="""Primary source system (e.g., slack, gdrive, aaoifi_db)""", json_schema_extra = { "linkml_meta": {'alias': 'prov_system',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields'],
         'slot_uri': 'prov:wasAttributedTo'} })
    prov_channel_ids: Optional[list[str]] = Field(default=None, description="""Slack channel IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_channel_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_thread_tss: Optional[list[str]] = Field(default=None, description="""Slack thread timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_thread_tss',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_tss: Optional[list[str]] = Field(default=None, description="""Slack message timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_tss', 'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_permalinks: Optional[list[str]] = Field(default=None, description="""Slack permalinks""", json_schema_extra = { "linkml_meta": {'alias': 'prov_permalinks',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_file_ids: Optional[list[str]] = Field(default=None, description="""Document/file identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'prov_file_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_rev_ids: Optional[list[str]] = Field(default=None, description="""Document revision IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_rev_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_text_sha1s: Optional[list[str]] = Field(default=None, description="""SHA1 hashes of source text""", json_schema_extra = { "linkml_meta": {'alias': 'prov_text_sha1s',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_types: Optional[list[str]] = Field(default=None, description="""Document component types (section, paragraph, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'doco_types',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_paths: Optional[list[str]] = Field(default=None, description="""Document structural paths""", json_schema_extra = { "linkml_meta": {'alias': 'doco_paths',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    page_nums: Optional[list[int]] = Field(default=None, description="""Page numbers""", json_schema_extra = { "linkml_meta": {'alias': 'page_nums',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    support_count: Optional[int] = Field(default=None, description="""Number of supporting evidences""", ge=0, json_schema_extra = { "linkml_meta": {'alias': 'support_count',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })


class AdjudicationDecision(ProvenanceFields):
    """
    The outcome of an adjudication activity, documenting the decision and rationale for resolving a contradiction
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Entity',
         'from_schema': 'https://example.org/schemas/business-contradiction-adjudication',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'decided_at': {'name': 'decided_at', 'required': True},
                        'decision': {'name': 'decision', 'required': True},
                        'decision_id': {'identifier': True,
                                        'name': 'decision_id',
                                        'required': True},
                        'rationale': {'name': 'rationale', 'required': True}}})

    decision_id: str = Field(default=..., description="""Unique identifier for the decision""", json_schema_extra = { "linkml_meta": {'alias': 'decision_id', 'domain_of': ['AdjudicationDecision']} })
    decision: DecisionEnum = Field(default=..., description="""The decision made during adjudication""", json_schema_extra = { "linkml_meta": {'alias': 'decision', 'domain_of': ['AdjudicationDecision']} })
    rationale: str = Field(default=..., description="""Rationale or justification for the decision""", json_schema_extra = { "linkml_meta": {'alias': 'rationale', 'domain_of': ['AdjudicationDecision']} })
    decided_at: datetime  = Field(default=..., description="""Timestamp when the decision was made""", json_schema_extra = { "linkml_meta": {'alias': 'decided_at', 'domain_of': ['AdjudicationDecision']} })
    implementation_plan: Optional[str] = Field(default=None, description="""Plan for implementing the decision""", json_schema_extra = { "linkml_meta": {'alias': 'implementation_plan', 'domain_of': ['AdjudicationDecision']} })
    affected_constraints: Optional[list[str]] = Field(default=None, description="""List of constraints affected by the decision""", json_schema_extra = { "linkml_meta": {'alias': 'affected_constraints', 'domain_of': ['AdjudicationDecision']} })
    approval_status: Optional[ApprovalStatusEnum] = Field(default=None, description="""Approval status of the decision""", json_schema_extra = { "linkml_meta": {'alias': 'approval_status', 'domain_of': ['AdjudicationDecision']} })
    result_of_activity: Optional[str] = Field(default=None, description="""Activity that produced this decision""", json_schema_extra = { "linkml_meta": {'alias': 'result_of_activity',
         'domain_of': ['AdjudicationDecision'],
         'inverse': 'resulted_in_decision'} })
    node_id: Optional[str] = Field(default=None, description="""Stable citation id (deterministic)""", json_schema_extra = { "linkml_meta": {'alias': 'node_id',
         'domain_of': ['ProvenanceFields'],
         'slot_uri': 'prov:identifier'} })
    prov_system: Optional[str] = Field(default=None, description="""Primary source system (e.g., slack, gdrive, aaoifi_db)""", json_schema_extra = { "linkml_meta": {'alias': 'prov_system',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields'],
         'slot_uri': 'prov:wasAttributedTo'} })
    prov_channel_ids: Optional[list[str]] = Field(default=None, description="""Slack channel IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_channel_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_thread_tss: Optional[list[str]] = Field(default=None, description="""Slack thread timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_thread_tss',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_tss: Optional[list[str]] = Field(default=None, description="""Slack message timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_tss', 'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_permalinks: Optional[list[str]] = Field(default=None, description="""Slack permalinks""", json_schema_extra = { "linkml_meta": {'alias': 'prov_permalinks',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_file_ids: Optional[list[str]] = Field(default=None, description="""Document/file identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'prov_file_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_rev_ids: Optional[list[str]] = Field(default=None, description="""Document revision IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_rev_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_text_sha1s: Optional[list[str]] = Field(default=None, description="""SHA1 hashes of source text""", json_schema_extra = { "linkml_meta": {'alias': 'prov_text_sha1s',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_types: Optional[list[str]] = Field(default=None, description="""Document component types (section, paragraph, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'doco_types',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_paths: Optional[list[str]] = Field(default=None, description="""Document structural paths""", json_schema_extra = { "linkml_meta": {'alias': 'doco_paths',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    page_nums: Optional[list[int]] = Field(default=None, description="""Page numbers""", json_schema_extra = { "linkml_meta": {'alias': 'page_nums',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    support_count: Optional[int] = Field(default=None, description="""Number of supporting evidences""", ge=0, json_schema_extra = { "linkml_meta": {'alias': 'support_count',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })


class ConflictRelationship(ProvenanceFields):
    """
    A semantic relationship representing the nature and details of a conflict between business constraints
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'skos:semanticRelation',
         'from_schema': 'https://example.org/schemas/business-contradiction-adjudication',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'conflict_type': {'name': 'conflict_type', 'required': True},
                        'relationship_id': {'identifier': True,
                                            'name': 'relationship_id',
                                            'required': True},
                        'source_constraint': {'name': 'source_constraint',
                                              'required': True},
                        'target_constraint': {'name': 'target_constraint',
                                              'required': True}}})

    relationship_id: str = Field(default=..., description="""Unique identifier for the conflict relationship""", json_schema_extra = { "linkml_meta": {'alias': 'relationship_id', 'domain_of': ['ConflictRelationship']} })
    conflict_type: ConflictTypeEnum = Field(default=..., description="""Type of conflict between constraints""", json_schema_extra = { "linkml_meta": {'alias': 'conflict_type', 'domain_of': ['ConflictRelationship']} })
    conflict_description: Optional[str] = Field(default=None, description="""Description of the conflict""", json_schema_extra = { "linkml_meta": {'alias': 'conflict_description', 'domain_of': ['ConflictRelationship']} })
    severity_level: Optional[SeverityEnum] = Field(default=None, description="""Severity level of the conflict""", json_schema_extra = { "linkml_meta": {'alias': 'severity_level', 'domain_of': ['ConflictRelationship']} })
    detected_date: Optional[date] = Field(default=None, description="""Date when the conflict was detected""", json_schema_extra = { "linkml_meta": {'alias': 'detected_date', 'domain_of': ['ConflictRelationship']} })
    source_constraint: str = Field(default=..., description="""Source constraint in the conflict relationship""", json_schema_extra = { "linkml_meta": {'alias': 'source_constraint', 'domain_of': ['ConflictRelationship']} })
    target_constraint: str = Field(default=..., description="""Target constraint in the conflict relationship""", json_schema_extra = { "linkml_meta": {'alias': 'target_constraint', 'domain_of': ['ConflictRelationship']} })
    associated_contradiction: Optional[str] = Field(default=None, description="""Contradiction associated with this conflict relationship""", json_schema_extra = { "linkml_meta": {'alias': 'associated_contradiction', 'domain_of': ['ConflictRelationship']} })
    node_id: Optional[str] = Field(default=None, description="""Stable citation id (deterministic)""", json_schema_extra = { "linkml_meta": {'alias': 'node_id',
         'domain_of': ['ProvenanceFields'],
         'slot_uri': 'prov:identifier'} })
    prov_system: Optional[str] = Field(default=None, description="""Primary source system (e.g., slack, gdrive, aaoifi_db)""", json_schema_extra = { "linkml_meta": {'alias': 'prov_system',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields'],
         'slot_uri': 'prov:wasAttributedTo'} })
    prov_channel_ids: Optional[list[str]] = Field(default=None, description="""Slack channel IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_channel_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_thread_tss: Optional[list[str]] = Field(default=None, description="""Slack thread timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_thread_tss',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_tss: Optional[list[str]] = Field(default=None, description="""Slack message timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_tss', 'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_permalinks: Optional[list[str]] = Field(default=None, description="""Slack permalinks""", json_schema_extra = { "linkml_meta": {'alias': 'prov_permalinks',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_file_ids: Optional[list[str]] = Field(default=None, description="""Document/file identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'prov_file_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_rev_ids: Optional[list[str]] = Field(default=None, description="""Document revision IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_rev_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_text_sha1s: Optional[list[str]] = Field(default=None, description="""SHA1 hashes of source text""", json_schema_extra = { "linkml_meta": {'alias': 'prov_text_sha1s',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_types: Optional[list[str]] = Field(default=None, description="""Document component types (section, paragraph, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'doco_types',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_paths: Optional[list[str]] = Field(default=None, description="""Document structural paths""", json_schema_extra = { "linkml_meta": {'alias': 'doco_paths',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    page_nums: Optional[list[int]] = Field(default=None, description="""Page numbers""", json_schema_extra = { "linkml_meta": {'alias': 'page_nums',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    support_count: Optional[int] = Field(default=None, description="""Number of supporting evidences""", ge=0, json_schema_extra = { "linkml_meta": {'alias': 'support_count',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
ProvenanceFields.model_rebuild()
EdgeProvenanceFields.model_rebuild()
Contradiction.model_rebuild()
BusinessConstraint.model_rebuild()
ContradictionEvidence.model_rebuild()
AdjudicationActivity.model_rebuild()
Adjudicator.model_rebuild()
AdjudicationDecision.model_rebuild()
ConflictRelationship.model_rebuild()

