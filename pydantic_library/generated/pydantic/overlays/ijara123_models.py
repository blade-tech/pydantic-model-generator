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


linkml_meta = LinkMLMeta({'default_prefix': 'ijara_shariah_compliance_audit',
     'description': 'Schema for auditing Ijara (Islamic lease) transactions to '
                    'ensure compliance with Shariah principles, including asset '
                    'ownership, lease structure, and prohibited elements',
     'id': 'https://example.org/schemas/ijara-shariah-compliance-audit',
     'imports': ['../core/provenance'],
     'name': 'ijara_shariah_compliance_audit',
     'prefixes': {'doco': {'prefix_prefix': 'doco',
                           'prefix_reference': 'http://purl.org/spar/doco/'},
                  'fabio': {'prefix_prefix': 'fabio',
                            'prefix_reference': 'http://purl.org/spar/fabio/'},
                  'fibo': {'prefix_prefix': 'fibo',
                           'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/'},
                  'fibo-fbc': {'prefix_prefix': 'fibo-fbc',
                               'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FBC/ProductsAndServices/FinancialProductsAndServices/'},
                  'fibo-fnd': {'prefix_prefix': 'fibo-fnd',
                               'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FND/Law/Regulation/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'}},
     'source_file': 'D:\\projects\\Pydantic Model '
                    'Generator\\pydantic_library\\schemas\\overlays\\ijara123_overlay.yaml'} )

class OwnershipStatusEnum(str, Enum):
    """
    Status of asset ownership
    """
    VERIFIED = "VERIFIED"
    """
    Ownership has been verified
    """
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    """
    Ownership verification in progress
    """
    DISPUTED = "DISPUTED"
    """
    Ownership is disputed
    """
    UNVERIFIED = "UNVERIFIED"
    """
    Ownership has not been verified
    """


class PaymentFrequencyEnum(str, Enum):
    """
    Frequency of rental payments
    """
    MONTHLY = "MONTHLY"
    """
    Payments made monthly
    """
    QUARTERLY = "QUARTERLY"
    """
    Payments made quarterly
    """
    SEMI_ANNUALLY = "SEMI_ANNUALLY"
    """
    Payments made twice per year
    """
    ANNUALLY = "ANNUALLY"
    """
    Payments made annually
    """
    CUSTOM = "CUSTOM"
    """
    Custom payment schedule
    """


class TransactionStatusEnum(str, Enum):
    """
    Status of transaction
    """
    DRAFT = "DRAFT"
    """
    Transaction in draft state
    """
    PENDING_APPROVAL = "PENDING_APPROVAL"
    """
    Awaiting approval
    """
    ACTIVE = "ACTIVE"
    """
    Transaction is active
    """
    COMPLETED = "COMPLETED"
    """
    Transaction completed
    """
    CANCELLED = "CANCELLED"
    """
    Transaction cancelled
    """
    SUSPENDED = "SUSPENDED"
    """
    Transaction suspended
    """


class AuditTypeEnum(str, Enum):
    """
    Type of audit
    """
    INITIAL = "INITIAL"
    """
    Initial Shariah compliance audit
    """
    PERIODIC = "PERIODIC"
    """
    Regular periodic audit
    """
    SPECIAL = "SPECIAL"
    """
    Special purpose audit
    """
    FOLLOW_UP = "FOLLOW_UP"
    """
    Follow-up audit after remediation
    """
    COMPREHENSIVE = "COMPREHENSIVE"
    """
    Comprehensive full-scope audit
    """


class AuditStatusEnum(str, Enum):
    """
    Status of audit
    """
    PLANNED = "PLANNED"
    """
    Audit is planned
    """
    IN_PROGRESS = "IN_PROGRESS"
    """
    Audit in progress
    """
    UNDER_REVIEW = "UNDER_REVIEW"
    """
    Audit findings under review
    """
    COMPLETED = "COMPLETED"
    """
    Audit completed
    """
    CANCELLED = "CANCELLED"
    """
    Audit cancelled
    """


class ComplianceStatusEnum(str, Enum):
    """
    Compliance status
    """
    COMPLIANT = "COMPLIANT"
    """
    Fully compliant with Shariah principles
    """
    NON_COMPLIANT = "NON_COMPLIANT"
    """
    Not compliant with Shariah principles
    """
    PARTIALLY_COMPLIANT = "PARTIALLY_COMPLIANT"
    """
    Partially compliant, some issues found
    """
    UNDER_REVIEW = "UNDER_REVIEW"
    """
    Compliance status under review
    """
    NOT_ASSESSED = "NOT_ASSESSED"
    """
    Not yet assessed
    """


class SeverityLevelEnum(str, Enum):
    """
    Severity level of non-compliance
    """
    CRITICAL = "CRITICAL"
    """
    Critical violation requiring immediate action
    """
    HIGH = "HIGH"
    """
    High severity requiring prompt action
    """
    MEDIUM = "MEDIUM"
    """
    Medium severity requiring attention
    """
    LOW = "LOW"
    """
    Low severity, minor issue
    """
    INFORMATIONAL = "INFORMATIONAL"
    """
    Informational only, no violation
    """


class ComplianceRatingEnum(str, Enum):
    """
    Overall compliance rating
    """
    EXCELLENT = "EXCELLENT"
    """
    Excellent compliance, no issues
    """
    GOOD = "GOOD"
    """
    Good compliance, minor issues only
    """
    SATISFACTORY = "SATISFACTORY"
    """
    Satisfactory compliance, some issues
    """
    NEEDS_IMPROVEMENT = "NEEDS_IMPROVEMENT"
    """
    Needs improvement, multiple issues
    """
    UNSATISFACTORY = "UNSATISFACTORY"
    """
    Unsatisfactory, major issues found
    """


class ApprovalStatusEnum(str, Enum):
    """
    Approval status
    """
    DRAFT = "DRAFT"
    """
    Report in draft state
    """
    PENDING_REVIEW = "PENDING_REVIEW"
    """
    Pending review
    """
    APPROVED = "APPROVED"
    """
    Report approved
    """
    REJECTED = "REJECTED"
    """
    Report rejected
    """
    REVISED = "REVISED"
    """
    Report revised
    """


class RuleCategoryEnum(str, Enum):
    """
    Category of Shariah compliance rule
    """
    ASSET_OWNERSHIP = "ASSET_OWNERSHIP"
    """
    Rules related to asset ownership
    """
    LEASE_STRUCTURE = "LEASE_STRUCTURE"
    """
    Rules related to lease structure
    """
    PROHIBITED_ELEMENTS = "PROHIBITED_ELEMENTS"
    """
    Rules about prohibited elements (riba, gharar, etc.)
    """
    RISK_SHARING = "RISK_SHARING"
    """
    Rules about risk sharing
    """
    DOCUMENTATION = "DOCUMENTATION"
    """
    Rules about documentation requirements
    """
    PAYMENT_TERMS = "PAYMENT_TERMS"
    """
    Rules about payment terms
    """
    TERMINATION = "TERMINATION"
    """
    Rules about contract termination
    """
    GENERAL = "GENERAL"
    """
    General compliance rules
    """


class SchoolOfThoughtEnum(str, Enum):
    """
    Islamic school of jurisprudence
    """
    HANAFI = "HANAFI"
    """
    Hanafi school of thought
    """
    MALIKI = "MALIKI"
    """
    Maliki school of thought
    """
    SHAFI = "SHAFI"
    """
    Shafi school of thought
    """
    HANBALI = "HANBALI"
    """
    Hanbali school of thought
    """
    JAFARI = "JAFARI"
    """
    Jafari school of thought
    """
    MULTIPLE = "MULTIPLE"
    """
    Multiple schools considered
    """
    NOT_SPECIFIED = "NOT_SPECIFIED"
    """
    School not specified
    """


class EventTypeEnum(str, Enum):
    """
    Type of audit trail event
    """
    TRANSACTION_CREATED = "TRANSACTION_CREATED"
    """
    Transaction was created
    """
    TRANSACTION_MODIFIED = "TRANSACTION_MODIFIED"
    """
    Transaction was modified
    """
    AUDIT_INITIATED = "AUDIT_INITIATED"
    """
    Audit was initiated
    """
    ASSESSMENT_PERFORMED = "ASSESSMENT_PERFORMED"
    """
    Compliance assessment performed
    """
    REPORT_GENERATED = "REPORT_GENERATED"
    """
    Audit report generated
    """
    APPROVAL_GRANTED = "APPROVAL_GRANTED"
    """
    Approval was granted
    """
    APPROVAL_REJECTED = "APPROVAL_REJECTED"
    """
    Approval was rejected
    """
    STATUS_CHANGED = "STATUS_CHANGED"
    """
    Status was changed
    """
    DOCUMENT_UPLOADED = "DOCUMENT_UPLOADED"
    """
    Document was uploaded
    """
    COMMENT_ADDED = "COMMENT_ADDED"
    """
    Comment was added
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


class IjaraTransaction(ProvenanceFields):
    """
    Islamic lease transaction where lessor retains ownership of asset while lessee has right to use
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc:FinancialInstrument',
         'from_schema': 'https://example.org/schemas/ijara-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['IjaraTransaction',
                       'Audit',
                       'ComplianceAssessment',
                       'AuditReport',
                       'ComplianceRule',
                       'ShariahCompliance',
                       'AuditTrail']} })
    transaction_id: str = Field(default=..., description="""Unique identifier for the Ijara transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_id',
         'domain_of': ['IjaraTransaction', 'ComplianceAssessment', 'AuditTrail']} })
    lessor: str = Field(default=..., description="""Party who owns the asset and leases it""", json_schema_extra = { "linkml_meta": {'alias': 'lessor', 'domain_of': ['IjaraTransaction']} })
    lessee: str = Field(default=..., description="""Party who leases the asset""", json_schema_extra = { "linkml_meta": {'alias': 'lessee', 'domain_of': ['IjaraTransaction']} })
    asset_description: str = Field(default=..., description="""Detailed description of the leased asset""", json_schema_extra = { "linkml_meta": {'alias': 'asset_description', 'domain_of': ['IjaraTransaction']} })
    asset_ownership_status: OwnershipStatusEnum = Field(default=..., description="""Confirmation of lessor's ownership of the asset""", json_schema_extra = { "linkml_meta": {'alias': 'asset_ownership_status', 'domain_of': ['IjaraTransaction']} })
    lease_amount: float = Field(default=..., description="""Total value of the lease agreement""", json_schema_extra = { "linkml_meta": {'alias': 'lease_amount', 'domain_of': ['IjaraTransaction']} })
    lease_term: int = Field(default=..., description="""Duration of the lease in months""", json_schema_extra = { "linkml_meta": {'alias': 'lease_term', 'domain_of': ['IjaraTransaction']} })
    lease_start_date: date = Field(default=..., description="""Date when lease period begins""", json_schema_extra = { "linkml_meta": {'alias': 'lease_start_date', 'domain_of': ['IjaraTransaction']} })
    lease_end_date: date = Field(default=..., description="""Date when lease period ends""", json_schema_extra = { "linkml_meta": {'alias': 'lease_end_date', 'domain_of': ['IjaraTransaction']} })
    rental_payment_frequency: PaymentFrequencyEnum = Field(default=..., description="""Frequency of rental payments""", json_schema_extra = { "linkml_meta": {'alias': 'rental_payment_frequency', 'domain_of': ['IjaraTransaction']} })
    purchase_option: Optional[bool] = Field(default=None, description="""Whether lessee has option to purchase asset at end of lease""", json_schema_extra = { "linkml_meta": {'alias': 'purchase_option', 'domain_of': ['IjaraTransaction']} })
    transaction_date: date = Field(default=..., description="""Date when transaction was executed""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_date', 'domain_of': ['IjaraTransaction']} })
    transaction_status: TransactionStatusEnum = Field(default=..., description="""Current status of the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_status', 'domain_of': ['IjaraTransaction']} })
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


class Audit(ProvenanceFields):
    """
    Systematic examination of Ijara transaction for Shariah compliance
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Activity',
         'from_schema': 'https://example.org/schemas/ijara-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['IjaraTransaction',
                       'Audit',
                       'ComplianceAssessment',
                       'AuditReport',
                       'ComplianceRule',
                       'ShariahCompliance',
                       'AuditTrail']} })
    audit_id: str = Field(default=..., description="""Unique identifier for the audit""", json_schema_extra = { "linkml_meta": {'alias': 'audit_id', 'domain_of': ['Audit', 'AuditReport']} })
    auditor_name: str = Field(default=..., description="""Name of the person or entity conducting the audit""", json_schema_extra = { "linkml_meta": {'alias': 'auditor_name', 'domain_of': ['Audit']} })
    auditor_certification: Optional[str] = Field(default=None, description="""Professional certification of the auditor""", json_schema_extra = { "linkml_meta": {'alias': 'auditor_certification', 'domain_of': ['Audit']} })
    audit_type: AuditTypeEnum = Field(default=..., description="""Type of audit being conducted""", json_schema_extra = { "linkml_meta": {'alias': 'audit_type', 'domain_of': ['Audit']} })
    audit_scope: str = Field(default=..., description="""Scope and boundaries of the audit""", json_schema_extra = { "linkml_meta": {'alias': 'audit_scope', 'domain_of': ['Audit']} })
    audit_date: date = Field(default=..., description="""Primary date of the audit""", json_schema_extra = { "linkml_meta": {'alias': 'audit_date', 'domain_of': ['Audit']} })
    audit_start_date: date = Field(default=..., description="""Date when audit commenced""", json_schema_extra = { "linkml_meta": {'alias': 'audit_start_date', 'domain_of': ['Audit']} })
    audit_completion_date: Optional[date] = Field(default=None, description="""Date when audit was completed""", json_schema_extra = { "linkml_meta": {'alias': 'audit_completion_date', 'domain_of': ['Audit']} })
    audit_methodology: Optional[str] = Field(default=None, description="""Methodology and approach used for the audit""", json_schema_extra = { "linkml_meta": {'alias': 'audit_methodology', 'domain_of': ['Audit']} })
    audit_status: AuditStatusEnum = Field(default=..., description="""Current status of the audit""", json_schema_extra = { "linkml_meta": {'alias': 'audit_status', 'domain_of': ['Audit']} })
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


class ComplianceAssessment(ProvenanceFields):
    """
    Evaluation of transaction against specific Shariah compliance rules
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Activity',
         'from_schema': 'https://example.org/schemas/ijara-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['IjaraTransaction',
                       'Audit',
                       'ComplianceAssessment',
                       'AuditReport',
                       'ComplianceRule',
                       'ShariahCompliance',
                       'AuditTrail']} })
    assessment_id: str = Field(default=..., description="""Unique identifier for the compliance assessment""", json_schema_extra = { "linkml_meta": {'alias': 'assessment_id', 'domain_of': ['ComplianceAssessment']} })
    rule_id: str = Field(default=..., description="""Identifier of the compliance rule being evaluated""", json_schema_extra = { "linkml_meta": {'alias': 'rule_id', 'domain_of': ['ComplianceAssessment', 'ComplianceRule']} })
    transaction_id: str = Field(default=..., description="""Unique identifier for the Ijara transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_id',
         'domain_of': ['IjaraTransaction', 'ComplianceAssessment', 'AuditTrail']} })
    is_compliant: bool = Field(default=..., description="""Boolean indicating if rule was satisfied""", json_schema_extra = { "linkml_meta": {'alias': 'is_compliant', 'domain_of': ['ComplianceAssessment']} })
    compliance_status: ComplianceStatusEnum = Field(default=..., description="""Overall compliance status""", json_schema_extra = { "linkml_meta": {'alias': 'compliance_status', 'domain_of': ['ComplianceAssessment']} })
    assessment_date: date = Field(default=..., description="""Date when assessment was performed""", json_schema_extra = { "linkml_meta": {'alias': 'assessment_date', 'domain_of': ['ComplianceAssessment']} })
    assessor_name: str = Field(default=..., description="""Name of person who performed the assessment""", json_schema_extra = { "linkml_meta": {'alias': 'assessor_name', 'domain_of': ['ComplianceAssessment']} })
    violation_details: Optional[str] = Field(default=None, description="""Details of any violations found""", json_schema_extra = { "linkml_meta": {'alias': 'violation_details', 'domain_of': ['ComplianceAssessment']} })
    severity_level: Optional[SeverityLevelEnum] = Field(default=None, description="""Severity of any non-compliance found""", json_schema_extra = { "linkml_meta": {'alias': 'severity_level', 'domain_of': ['ComplianceAssessment']} })
    remediation_required: Optional[bool] = Field(default=None, description="""Whether remediation action is required""", json_schema_extra = { "linkml_meta": {'alias': 'remediation_required', 'domain_of': ['ComplianceAssessment']} })
    remediation_steps: Optional[str] = Field(default=None, description="""Steps required to remediate non-compliance""", json_schema_extra = { "linkml_meta": {'alias': 'remediation_steps', 'domain_of': ['ComplianceAssessment']} })
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


class AuditReport(ProvenanceFields):
    """
    Formal document presenting audit findings and recommendations
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fabio:Report',
         'from_schema': 'https://example.org/schemas/ijara-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['IjaraTransaction',
                       'Audit',
                       'ComplianceAssessment',
                       'AuditReport',
                       'ComplianceRule',
                       'ShariahCompliance',
                       'AuditTrail']} })
    report_id: str = Field(default=..., description="""Unique identifier for the audit report""", json_schema_extra = { "linkml_meta": {'alias': 'report_id', 'domain_of': ['AuditReport']} })
    audit_id: str = Field(default=..., description="""Unique identifier for the audit""", json_schema_extra = { "linkml_meta": {'alias': 'audit_id', 'domain_of': ['Audit', 'AuditReport']} })
    report_title: str = Field(default=..., description="""Title of the audit report""", json_schema_extra = { "linkml_meta": {'alias': 'report_title', 'domain_of': ['AuditReport']} })
    issued_date: date = Field(default=..., description="""Date when report was issued""", json_schema_extra = { "linkml_meta": {'alias': 'issued_date', 'domain_of': ['AuditReport']} })
    report_period_start: date = Field(default=..., description="""Start date of period covered by report""", json_schema_extra = { "linkml_meta": {'alias': 'report_period_start', 'domain_of': ['AuditReport']} })
    report_period_end: date = Field(default=..., description="""End date of period covered by report""", json_schema_extra = { "linkml_meta": {'alias': 'report_period_end', 'domain_of': ['AuditReport']} })
    executive_summary: Optional[str] = Field(default=None, description="""High-level summary of audit findings""", json_schema_extra = { "linkml_meta": {'alias': 'executive_summary', 'domain_of': ['AuditReport']} })
    findings_summary: str = Field(default=..., description="""Summary of detailed findings""", json_schema_extra = { "linkml_meta": {'alias': 'findings_summary', 'domain_of': ['AuditReport']} })
    overall_compliance_rating: ComplianceRatingEnum = Field(default=..., description="""Overall rating of compliance""", json_schema_extra = { "linkml_meta": {'alias': 'overall_compliance_rating', 'domain_of': ['AuditReport']} })
    recommendations: Optional[str] = Field(default=None, description="""Recommendations for improvement""", json_schema_extra = { "linkml_meta": {'alias': 'recommendations', 'domain_of': ['AuditReport']} })
    auditor_signature: Optional[str] = Field(default=None, description="""Digital or physical signature of auditor""", json_schema_extra = { "linkml_meta": {'alias': 'auditor_signature', 'domain_of': ['AuditReport']} })
    approval_status: ApprovalStatusEnum = Field(default=..., description="""Approval status of the report""", json_schema_extra = { "linkml_meta": {'alias': 'approval_status', 'domain_of': ['AuditReport']} })
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


class ComplianceRule(ProvenanceFields):
    """
    Specific Shariah principle or requirement that must be satisfied
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fnd:Regulation',
         'from_schema': 'https://example.org/schemas/ijara-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['IjaraTransaction',
                       'Audit',
                       'ComplianceAssessment',
                       'AuditReport',
                       'ComplianceRule',
                       'ShariahCompliance',
                       'AuditTrail']} })
    rule_id: str = Field(default=..., description="""Identifier of the compliance rule being evaluated""", json_schema_extra = { "linkml_meta": {'alias': 'rule_id', 'domain_of': ['ComplianceAssessment', 'ComplianceRule']} })
    rule_name: str = Field(default=..., description="""Name of the compliance rule""", json_schema_extra = { "linkml_meta": {'alias': 'rule_name', 'domain_of': ['ComplianceRule']} })
    rule_description: str = Field(default=..., description="""Detailed description of the rule requirements""", json_schema_extra = { "linkml_meta": {'alias': 'rule_description', 'domain_of': ['ComplianceRule']} })
    category: RuleCategoryEnum = Field(default=..., description="""Category of the compliance rule""", json_schema_extra = { "linkml_meta": {'alias': 'category', 'domain_of': ['ComplianceRule']} })
    rule_source: str = Field(default=..., description="""Source of the rule (Quran, Hadith, scholarly consensus, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'rule_source', 'domain_of': ['ComplianceRule']} })
    rule_reference: Optional[str] = Field(default=None, description="""Specific reference citation for the rule""", json_schema_extra = { "linkml_meta": {'alias': 'rule_reference', 'domain_of': ['ComplianceRule']} })
    applicability_criteria: Optional[str] = Field(default=None, description="""Criteria determining when rule applies""", json_schema_extra = { "linkml_meta": {'alias': 'applicability_criteria', 'domain_of': ['ComplianceRule']} })
    severity: SeverityLevelEnum = Field(default=..., description="""Severity level of rule violation""", json_schema_extra = { "linkml_meta": {'alias': 'severity', 'domain_of': ['ComplianceRule']} })
    is_mandatory: bool = Field(default=..., description="""Whether rule is mandatory or recommended""", json_schema_extra = { "linkml_meta": {'alias': 'is_mandatory', 'domain_of': ['ComplianceRule']} })
    effective_date: date = Field(default=..., description="""Date when rule becomes effective""", json_schema_extra = { "linkml_meta": {'alias': 'effective_date',
         'domain_of': ['ComplianceRule', 'ShariahCompliance']} })
    version: Optional[str] = Field(default=None, description="""Version number of the rule or framework""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['ComplianceRule', 'ShariahCompliance']} })
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


class ShariahCompliance(ProvenanceFields):
    """
    Framework of Islamic principles governing financial transactions
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'skos:Concept',
         'from_schema': 'https://example.org/schemas/ijara-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['IjaraTransaction',
                       'Audit',
                       'ComplianceAssessment',
                       'AuditReport',
                       'ComplianceRule',
                       'ShariahCompliance',
                       'AuditTrail']} })
    framework_id: str = Field(default=..., description="""Unique identifier for the Shariah compliance framework""", json_schema_extra = { "linkml_meta": {'alias': 'framework_id', 'domain_of': ['ShariahCompliance']} })
    framework_name: str = Field(default=..., description="""Name of the compliance framework""", json_schema_extra = { "linkml_meta": {'alias': 'framework_name', 'domain_of': ['ShariahCompliance']} })
    framework_description: str = Field(default=..., description="""Description of the framework and its purpose""", json_schema_extra = { "linkml_meta": {'alias': 'framework_description', 'domain_of': ['ShariahCompliance']} })
    version: Optional[str] = Field(default=None, description="""Version number of the rule or framework""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['ComplianceRule', 'ShariahCompliance']} })
    issuing_authority: str = Field(default=..., description="""Authority that issued the framework""", json_schema_extra = { "linkml_meta": {'alias': 'issuing_authority', 'domain_of': ['ShariahCompliance']} })
    effective_date: date = Field(default=..., description="""Date when rule becomes effective""", json_schema_extra = { "linkml_meta": {'alias': 'effective_date',
         'domain_of': ['ComplianceRule', 'ShariahCompliance']} })
    last_updated: Optional[date] = Field(default=None, description="""Date when framework was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'last_updated', 'domain_of': ['ShariahCompliance']} })
    geographical_scope: Optional[str] = Field(default=None, description="""Geographical area where framework applies""", json_schema_extra = { "linkml_meta": {'alias': 'geographical_scope', 'domain_of': ['ShariahCompliance']} })
    school_of_thought: Optional[SchoolOfThoughtEnum] = Field(default=None, description="""Islamic school of jurisprudence (madhab) followed""", json_schema_extra = { "linkml_meta": {'alias': 'school_of_thought', 'domain_of': ['ShariahCompliance']} })
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


class AuditTrail(ProvenanceFields):
    """
    Chronological record of all activities and changes related to transaction audit
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Entity',
         'from_schema': 'https://example.org/schemas/ijara-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['IjaraTransaction',
                       'Audit',
                       'ComplianceAssessment',
                       'AuditReport',
                       'ComplianceRule',
                       'ShariahCompliance',
                       'AuditTrail']} })
    trail_id: str = Field(default=..., description="""Unique identifier for the audit trail entry""", json_schema_extra = { "linkml_meta": {'alias': 'trail_id', 'domain_of': ['AuditTrail']} })
    transaction_id: str = Field(default=..., description="""Unique identifier for the Ijara transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_id',
         'domain_of': ['IjaraTransaction', 'ComplianceAssessment', 'AuditTrail']} })
    event_type: EventTypeEnum = Field(default=..., description="""Type of event being recorded""", json_schema_extra = { "linkml_meta": {'alias': 'event_type', 'domain_of': ['AuditTrail']} })
    event_description: str = Field(default=..., description="""Description of the event""", json_schema_extra = { "linkml_meta": {'alias': 'event_description', 'domain_of': ['AuditTrail']} })
    event_timestamp: datetime  = Field(default=..., description="""Timestamp when event occurred""", json_schema_extra = { "linkml_meta": {'alias': 'event_timestamp', 'domain_of': ['AuditTrail']} })
    performed_by: str = Field(default=..., description="""User or system that performed the action""", json_schema_extra = { "linkml_meta": {'alias': 'performed_by', 'domain_of': ['AuditTrail']} })
    previous_value: Optional[str] = Field(default=None, description="""Value before the change""", json_schema_extra = { "linkml_meta": {'alias': 'previous_value', 'domain_of': ['AuditTrail']} })
    new_value: Optional[str] = Field(default=None, description="""Value after the change""", json_schema_extra = { "linkml_meta": {'alias': 'new_value', 'domain_of': ['AuditTrail']} })
    ip_address: Optional[str] = Field(default=None, description="""IP address from which action was performed""", json_schema_extra = { "linkml_meta": {'alias': 'ip_address', 'domain_of': ['AuditTrail']} })
    system_reference: Optional[str] = Field(default=None, description="""Reference to system or application""", json_schema_extra = { "linkml_meta": {'alias': 'system_reference', 'domain_of': ['AuditTrail']} })
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
IjaraTransaction.model_rebuild()
Audit.model_rebuild()
ComplianceAssessment.model_rebuild()
AuditReport.model_rebuild()
ComplianceRule.model_rebuild()
ShariahCompliance.model_rebuild()
AuditTrail.model_rebuild()

