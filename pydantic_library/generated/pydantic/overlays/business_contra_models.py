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
     'description': 'Schema for surfacing and tracking business contradictions '
                    'from Neo4j to enable proper adjudication and resolution of '
                    'conflicting constraints, policies, and rules',
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
     'source_file': '..\\..\\pydantic_library\\schemas\\overlays\\business_contra_overlay.yaml'} )

class SeverityEnum(str, Enum):
    """
    Severity levels for contradictions
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
    informational = "informational"
    """
    Informational only
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
    documentation = "documentation"
    """
    Evidence from documentation
    """


class DecisionEnum(str, Enum):
    """
    Types of adjudication decisions
    """
    accept_constraint_a = "accept_constraint_a"
    """
    Accept first constraint, reject second
    """
    accept_constraint_b = "accept_constraint_b"
    """
    Accept second constraint, reject first
    """
    modify_both = "modify_both"
    """
    Modify both constraints to resolve conflict
    """
    escalate = "escalate"
    """
    Escalate to higher authority
    """
    defer = "defer"
    """
    Defer decision pending more information
    """
    create_exception = "create_exception"
    """
    Create an exception rule
    """
    no_action = "no_action"
    """
    No action required
    """


class ConflictTypeEnum(str, Enum):
    """
    Types of conflicts between constraints
    """
    logical_contradiction = "logical_contradiction"
    """
    Logical contradiction between rules
    """
    temporal_conflict = "temporal_conflict"
    """
    Conflict in timing or sequence
    """
    scope_overlap = "scope_overlap"
    """
    Overlapping scopes with different rules
    """
    priority_conflict = "priority_conflict"
    """
    Conflicting priority assignments
    """
    resource_contention = "resource_contention"
    """
    Conflict over resource allocation
    """
    policy_inconsistency = "policy_inconsistency"
    """
    Inconsistent policy statements
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
    A detected conflict between business constraints, policies, or rules that requires adjudication
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'skos:Concept',
         'from_schema': 'https://example.org/schemas/business-contradiction-adjudication',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'detected_at': {'name': 'detected_at', 'required': True},
                        'id': {'identifier': True, 'name': 'id', 'required': True},
                        'severity': {'name': 'severity', 'required': True},
                        'status': {'name': 'status', 'required': True}}})

    id: str = Field(default=..., description="""Unique identifier for the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Contradiction',
                       'BusinessConstraint',
                       'ContradictionEvidence',
                       'AdjudicationActivity',
                       'Adjudicator',
                       'AdjudicationDecision',
                       'ConflictRelationship']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Contradiction', 'BusinessConstraint', 'ContradictionEvidence']} })
    severity: SeverityEnum = Field(default=..., description="""Severity level of the contradiction""", json_schema_extra = { "linkml_meta": {'alias': 'severity', 'domain_of': ['Contradiction']} })
    status: str = Field(default=..., description="""Current status of the entity""", json_schema_extra = { "linkml_meta": {'alias': 'status', 'domain_of': ['Contradiction', 'AdjudicationActivity']} })
    detected_at: datetime  = Field(default=..., description="""Timestamp when the contradiction was detected""", json_schema_extra = { "linkml_meta": {'alias': 'detected_at', 'domain_of': ['Contradiction']} })
    conflicting_constraints: Optional[list[str]] = Field(default=None, description="""Business constraints involved in the contradiction""", json_schema_extra = { "linkml_meta": {'alias': 'conflicting_constraints',
         'domain_of': ['Contradiction'],
         'inverse': 'contradictions'} })
    supporting_evidence: Optional[list[str]] = Field(default=None, description="""Evidence supporting the contradiction""", json_schema_extra = { "linkml_meta": {'alias': 'supporting_evidence',
         'domain_of': ['Contradiction'],
         'inverse': 'supports_contradiction'} })
    adjudication_activities: Optional[list[str]] = Field(default=None, description="""Adjudication activities for this contradiction""", json_schema_extra = { "linkml_meta": {'alias': 'adjudication_activities',
         'domain_of': ['Contradiction', 'Adjudicator'],
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
         'slot_usage': {'id': {'identifier': True, 'name': 'id', 'required': True},
                        'name': {'name': 'name', 'required': True},
                        'type': {'name': 'type', 'required': True}}})

    id: str = Field(default=..., description="""Unique identifier for the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Contradiction',
                       'BusinessConstraint',
                       'ContradictionEvidence',
                       'AdjudicationActivity',
                       'Adjudicator',
                       'AdjudicationDecision',
                       'ConflictRelationship']} })
    name: str = Field(default=..., description="""Name of the business constraint""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['BusinessConstraint', 'Adjudicator']} })
    type: str = Field(default=..., description="""Type or category of the constraint""", json_schema_extra = { "linkml_meta": {'alias': 'type', 'domain_of': ['BusinessConstraint']} })
    rule: Optional[str] = Field(default=None, description="""The formal rule or policy statement""", json_schema_extra = { "linkml_meta": {'alias': 'rule', 'domain_of': ['BusinessConstraint']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Contradiction', 'BusinessConstraint', 'ContradictionEvidence']} })
    scope: Optional[str] = Field(default=None, description="""Scope of applicability for the constraint""", json_schema_extra = { "linkml_meta": {'alias': 'scope', 'domain_of': ['BusinessConstraint']} })
    priority: Optional[int] = Field(default=None, description="""Priority level of the constraint""", json_schema_extra = { "linkml_meta": {'alias': 'priority', 'domain_of': ['BusinessConstraint']} })
    effective_date: Optional[date] = Field(default=None, description="""Date when the constraint became effective""", json_schema_extra = { "linkml_meta": {'alias': 'effective_date', 'domain_of': ['BusinessConstraint']} })
    contradictions: Optional[list[str]] = Field(default=None, description="""Contradictions involving this constraint""", json_schema_extra = { "linkml_meta": {'alias': 'contradictions',
         'domain_of': ['BusinessConstraint'],
         'inverse': 'conflicting_constraints'} })
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
    Supporting evidence that demonstrates or documents a contradiction
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Entity',
         'from_schema': 'https://example.org/schemas/business-contradiction-adjudication',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'captured_at': {'name': 'captured_at', 'required': True},
                        'id': {'identifier': True, 'name': 'id', 'required': True},
                        'source': {'name': 'source', 'required': True}}})

    id: str = Field(default=..., description="""Unique identifier for the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Contradiction',
                       'BusinessConstraint',
                       'ContradictionEvidence',
                       'AdjudicationActivity',
                       'Adjudicator',
                       'AdjudicationDecision',
                       'ConflictRelationship']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Contradiction', 'BusinessConstraint', 'ContradictionEvidence']} })
    source: str = Field(default=..., description="""Source system or origin of the evidence""", json_schema_extra = { "linkml_meta": {'alias': 'source', 'domain_of': ['ContradictionEvidence']} })
    captured_at: datetime  = Field(default=..., description="""Timestamp when the evidence was captured""", json_schema_extra = { "linkml_meta": {'alias': 'captured_at', 'domain_of': ['ContradictionEvidence']} })
    confidence_score: Optional[float] = Field(default=None, description="""Confidence score for the evidence (0-1)""", ge=0.0, le=1.0, json_schema_extra = { "linkml_meta": {'alias': 'confidence_score', 'domain_of': ['ContradictionEvidence']} })
    evidence_type: Optional[EvidenceTypeEnum] = Field(default=None, description="""Type of evidence""", json_schema_extra = { "linkml_meta": {'alias': 'evidence_type', 'domain_of': ['ContradictionEvidence']} })
    supporting_data: Optional[str] = Field(default=None, description="""Additional supporting data or references""", json_schema_extra = { "linkml_meta": {'alias': 'supporting_data', 'domain_of': ['ContradictionEvidence']} })
    supports_contradiction: Optional[str] = Field(default=None, description="""The contradiction this evidence supports""", json_schema_extra = { "linkml_meta": {'alias': 'supports_contradiction',
         'domain_of': ['ContradictionEvidence'],
         'inverse': 'supporting_evidence'} })
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
    The process of reviewing and deciding on a contradiction
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Activity',
         'from_schema': 'https://example.org/schemas/business-contradiction-adjudication',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'id': {'identifier': True, 'name': 'id', 'required': True},
                        'started_at': {'name': 'started_at', 'required': True},
                        'status': {'name': 'status', 'required': True}}})

    id: str = Field(default=..., description="""Unique identifier for the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Contradiction',
                       'BusinessConstraint',
                       'ContradictionEvidence',
                       'AdjudicationActivity',
                       'Adjudicator',
                       'AdjudicationDecision',
                       'ConflictRelationship']} })
    status: str = Field(default=..., description="""Current status of the entity""", json_schema_extra = { "linkml_meta": {'alias': 'status', 'domain_of': ['Contradiction', 'AdjudicationActivity']} })
    started_at: datetime  = Field(default=..., description="""Timestamp when the activity started""", json_schema_extra = { "linkml_meta": {'alias': 'started_at', 'domain_of': ['AdjudicationActivity']} })
    completed_at: Optional[datetime ] = Field(default=None, description="""Timestamp when the activity was completed""", json_schema_extra = { "linkml_meta": {'alias': 'completed_at', 'domain_of': ['AdjudicationActivity']} })
    notes: Optional[str] = Field(default=None, description="""Additional notes or comments""", json_schema_extra = { "linkml_meta": {'alias': 'notes', 'domain_of': ['AdjudicationActivity']} })
    adjudicates_contradiction: Optional[str] = Field(default=None, description="""The contradiction being adjudicated""", json_schema_extra = { "linkml_meta": {'alias': 'adjudicates_contradiction',
         'domain_of': ['AdjudicationActivity'],
         'inverse': 'adjudication_activities'} })
    performed_by: Optional[str] = Field(default=None, description="""The adjudicator performing the activity""", json_schema_extra = { "linkml_meta": {'alias': 'performed_by',
         'domain_of': ['AdjudicationActivity'],
         'inverse': 'adjudication_activities'} })
    resulted_in_decision: Optional[str] = Field(default=None, description="""The decision resulting from this activity""", json_schema_extra = { "linkml_meta": {'alias': 'resulted_in_decision',
         'domain_of': ['AdjudicationActivity'],
         'inverse': 'resulted_from_activity'} })
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
    An agent (person or role) responsible for adjudicating contradictions
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Agent',
         'from_schema': 'https://example.org/schemas/business-contradiction-adjudication',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'id': {'identifier': True, 'name': 'id', 'required': True},
                        'name': {'name': 'name', 'required': True},
                        'role': {'name': 'role', 'required': True}}})

    id: str = Field(default=..., description="""Unique identifier for the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Contradiction',
                       'BusinessConstraint',
                       'ContradictionEvidence',
                       'AdjudicationActivity',
                       'Adjudicator',
                       'AdjudicationDecision',
                       'ConflictRelationship']} })
    name: str = Field(default=..., description="""Name of the business constraint""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['BusinessConstraint', 'Adjudicator']} })
    role: str = Field(default=..., description="""Role or title of the adjudicator""", json_schema_extra = { "linkml_meta": {'alias': 'role', 'domain_of': ['Adjudicator']} })
    department: Optional[str] = Field(default=None, description="""Department or organizational unit""", json_schema_extra = { "linkml_meta": {'alias': 'department', 'domain_of': ['Adjudicator']} })
    email: Optional[str] = Field(default=None, description="""Email address""", json_schema_extra = { "linkml_meta": {'alias': 'email', 'domain_of': ['Adjudicator']} })
    authority_level: Optional[int] = Field(default=None, description="""Level of decision-making authority""", json_schema_extra = { "linkml_meta": {'alias': 'authority_level', 'domain_of': ['Adjudicator']} })
    specialization: Optional[str] = Field(default=None, description="""Area of specialization or expertise""", json_schema_extra = { "linkml_meta": {'alias': 'specialization', 'domain_of': ['Adjudicator']} })
    adjudication_activities: Optional[list[str]] = Field(default=None, description="""Adjudication activities for this contradiction""", json_schema_extra = { "linkml_meta": {'alias': 'adjudication_activities',
         'domain_of': ['Contradiction', 'Adjudicator'],
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


class AdjudicationDecision(ProvenanceFields):
    """
    The outcome and rationale of an adjudication activity
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Entity',
         'from_schema': 'https://example.org/schemas/business-contradiction-adjudication',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'decided_at': {'name': 'decided_at', 'required': True},
                        'decision': {'name': 'decision', 'required': True},
                        'id': {'identifier': True, 'name': 'id', 'required': True},
                        'rationale': {'name': 'rationale', 'required': True}}})

    id: str = Field(default=..., description="""Unique identifier for the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Contradiction',
                       'BusinessConstraint',
                       'ContradictionEvidence',
                       'AdjudicationActivity',
                       'Adjudicator',
                       'AdjudicationDecision',
                       'ConflictRelationship']} })
    decision: DecisionEnum = Field(default=..., description="""The decision made regarding the contradiction""", json_schema_extra = { "linkml_meta": {'alias': 'decision', 'domain_of': ['AdjudicationDecision']} })
    rationale: str = Field(default=..., description="""Reasoning and justification for the decision""", json_schema_extra = { "linkml_meta": {'alias': 'rationale', 'domain_of': ['AdjudicationDecision']} })
    decided_at: datetime  = Field(default=..., description="""Timestamp when the decision was made""", json_schema_extra = { "linkml_meta": {'alias': 'decided_at', 'domain_of': ['AdjudicationDecision']} })
    resolution_action: Optional[str] = Field(default=None, description="""Action to be taken to resolve the contradiction""", json_schema_extra = { "linkml_meta": {'alias': 'resolution_action', 'domain_of': ['AdjudicationDecision']} })
    impact_assessment: Optional[str] = Field(default=None, description="""Assessment of the impact of the decision""", json_schema_extra = { "linkml_meta": {'alias': 'impact_assessment', 'domain_of': ['AdjudicationDecision']} })
    follow_up_required: Optional[bool] = Field(default=None, description="""Whether follow-up action is required""", json_schema_extra = { "linkml_meta": {'alias': 'follow_up_required', 'domain_of': ['AdjudicationDecision']} })
    resulted_from_activity: Optional[str] = Field(default=None, description="""The activity that produced this decision""", json_schema_extra = { "linkml_meta": {'alias': 'resulted_from_activity',
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
    A semantic relationship representing the conflict between business constraints
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'skos:semanticRelation',
         'from_schema': 'https://example.org/schemas/business-contradiction-adjudication',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'conflict_type': {'name': 'conflict_type', 'required': True},
                        'id': {'identifier': True, 'name': 'id', 'required': True}}})

    id: str = Field(default=..., description="""Unique identifier for the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Contradiction',
                       'BusinessConstraint',
                       'ContradictionEvidence',
                       'AdjudicationActivity',
                       'Adjudicator',
                       'AdjudicationDecision',
                       'ConflictRelationship']} })
    conflict_type: ConflictTypeEnum = Field(default=..., description="""Type of conflict between constraints""", json_schema_extra = { "linkml_meta": {'alias': 'conflict_type', 'domain_of': ['ConflictRelationship']} })
    conflict_description: Optional[str] = Field(default=None, description="""Description of how the constraints conflict""", json_schema_extra = { "linkml_meta": {'alias': 'conflict_description', 'domain_of': ['ConflictRelationship']} })
    severity_impact: Optional[str] = Field(default=None, description="""Impact severity of the conflict""", json_schema_extra = { "linkml_meta": {'alias': 'severity_impact', 'domain_of': ['ConflictRelationship']} })
    source_constraint: Optional[str] = Field(default=None, description="""Source constraint in the conflict relationship""", json_schema_extra = { "linkml_meta": {'alias': 'source_constraint', 'domain_of': ['ConflictRelationship']} })
    target_constraint: Optional[str] = Field(default=None, description="""Target constraint in the conflict relationship""", json_schema_extra = { "linkml_meta": {'alias': 'target_constraint', 'domain_of': ['ConflictRelationship']} })
    identified_in_contradiction: Optional[str] = Field(default=None, description="""The contradiction where this conflict was identified""", json_schema_extra = { "linkml_meta": {'alias': 'identified_in_contradiction', 'domain_of': ['ConflictRelationship']} })
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

