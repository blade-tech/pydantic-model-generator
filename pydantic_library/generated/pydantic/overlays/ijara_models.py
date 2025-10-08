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


linkml_meta = LinkMLMeta({'default_prefix': 'ijara_sukuk_transaction_audit',
     'description': 'Schema for tracking and verifying Ijara lease transactions '
                    'associated with Sukuk Islamic bond instruments, ensuring '
                    'compliance and traceability of financial activities',
     'id': 'https://example.org/schemas/ijara-sukuk-transaction-audit',
     'imports': ['../core/provenance'],
     'name': 'ijara_sukuk_transaction_audit',
     'prefixes': {'fibo-fbc-dae': {'prefix_prefix': 'fibo-fbc-dae',
                                   'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FBC/DebtAndEquities/Debt/'},
                  'fibo-fbc-pas': {'prefix_prefix': 'fibo-fbc-pas',
                                   'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FBC/ProductsAndServices/FinancialProductsAndServices/'},
                  'fibo-fnd': {'prefix_prefix': 'fibo-fnd',
                               'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FND/Law/LegalCore/'},
                  'fibo-sec': {'prefix_prefix': 'fibo-sec',
                               'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/SEC/Debt/Bonds/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'}},
     'source_file': 'D:\\projects\\Pydantic Model '
                    'Generator\\pydantic_library\\schemas\\overlays\\ijara_overlay.yaml'} )

class AuditTypeEnum(str, Enum):
    """
    Types of audits performed
    """
    COMPLIANCE = "COMPLIANCE"
    """
    Compliance audit
    """
    FINANCIAL = "FINANCIAL"
    """
    Financial audit
    """
    OPERATIONAL = "OPERATIONAL"
    """
    Operational audit
    """
    SHARIAH = "SHARIAH"
    """
    Shariah compliance audit
    """
    INTERNAL = "INTERNAL"
    """
    Internal audit
    """
    EXTERNAL = "EXTERNAL"
    """
    External audit
    """


class AuditStatusEnum(str, Enum):
    """
    Status values for audits
    """
    PLANNED = "PLANNED"
    """
    Audit is planned
    """
    IN_PROGRESS = "IN_PROGRESS"
    """
    Audit is in progress
    """
    COMPLETED = "COMPLETED"
    """
    Audit is completed
    """
    APPROVED = "APPROVED"
    """
    Audit is approved
    """
    CANCELLED = "CANCELLED"
    """
    Audit is cancelled
    """


class PaymentFrequencyEnum(str, Enum):
    """
    Frequency of payments
    """
    MONTHLY = "MONTHLY"
    """
    Monthly payments
    """
    QUARTERLY = "QUARTERLY"
    """
    Quarterly payments
    """
    SEMI_ANNUAL = "SEMI_ANNUAL"
    """
    Semi-annual payments
    """
    ANNUAL = "ANNUAL"
    """
    Annual payments
    """
    ONE_TIME = "ONE_TIME"
    """
    One-time payment
    """


class LeaseStatusEnum(str, Enum):
    """
    Status values for leases
    """
    ACTIVE = "ACTIVE"
    """
    Lease is active
    """
    PENDING = "PENDING"
    """
    Lease is pending
    """
    EXPIRED = "EXPIRED"
    """
    Lease has expired
    """
    TERMINATED = "TERMINATED"
    """
    Lease is terminated
    """
    RENEWED = "RENEWED"
    """
    Lease is renewed
    """


class TransactionTypeEnum(str, Enum):
    """
    Types of financial transactions
    """
    RENTAL_PAYMENT = "RENTAL_PAYMENT"
    """
    Rental payment transaction
    """
    PURCHASE = "PURCHASE"
    """
    Purchase transaction
    """
    TRANSFER = "TRANSFER"
    """
    Transfer transaction
    """
    REFUND = "REFUND"
    """
    Refund transaction
    """
    PROFIT_DISTRIBUTION = "PROFIT_DISTRIBUTION"
    """
    Profit distribution
    """
    PRINCIPAL_REPAYMENT = "PRINCIPAL_REPAYMENT"
    """
    Principal repayment
    """


class TransactionStatusEnum(str, Enum):
    """
    Status values for transactions
    """
    PENDING = "PENDING"
    """
    Transaction is pending
    """
    COMPLETED = "COMPLETED"
    """
    Transaction is completed
    """
    FAILED = "FAILED"
    """
    Transaction has failed
    """
    CANCELLED = "CANCELLED"
    """
    Transaction is cancelled
    """
    REVERSED = "REVERSED"
    """
    Transaction is reversed
    """


class SukukStructureEnum(str, Enum):
    """
    Structure types of Sukuk instruments
    """
    IJARA = "IJARA"
    """
    Ijara-based Sukuk
    """
    MUDARABA = "MUDARABA"
    """
    Mudaraba-based Sukuk
    """
    MUSHARAKA = "MUSHARAKA"
    """
    Musharaka-based Sukuk
    """
    MURABAHA = "MURABAHA"
    """
    Murabaha-based Sukuk
    """
    WAKALA = "WAKALA"
    """
    Wakala-based Sukuk
    """
    HYBRID = "HYBRID"
    """
    Hybrid structure Sukuk
    """


class SukukStatusEnum(str, Enum):
    """
    Status values for Sukuk instruments
    """
    ISSUED = "ISSUED"
    """
    Sukuk is issued
    """
    ACTIVE = "ACTIVE"
    """
    Sukuk is active
    """
    MATURED = "MATURED"
    """
    Sukuk has matured
    """
    REDEEMED = "REDEEMED"
    """
    Sukuk is redeemed
    """
    DEFAULTED = "DEFAULTED"
    """
    Sukuk is in default
    """
    CANCELLED = "CANCELLED"
    """
    Sukuk is cancelled
    """


class ComplianceStatusEnum(str, Enum):
    """
    Compliance status outcomes
    """
    COMPLIANT = "COMPLIANT"
    """
    Fully compliant
    """
    NON_COMPLIANT = "NON_COMPLIANT"
    """
    Non-compliant
    """
    PARTIALLY_COMPLIANT = "PARTIALLY_COMPLIANT"
    """
    Partially compliant
    """
    UNDER_REVIEW = "UNDER_REVIEW"
    """
    Under review
    """
    NOT_APPLICABLE = "NOT_APPLICABLE"
    """
    Not applicable
    """


class ProcessStatusEnum(str, Enum):
    """
    Status values for audit processes
    """
    DRAFT = "DRAFT"
    """
    Process is in draft
    """
    ACTIVE = "ACTIVE"
    """
    Process is active
    """
    SUSPENDED = "SUSPENDED"
    """
    Process is suspended
    """
    COMPLETED = "COMPLETED"
    """
    Process is completed
    """
    ARCHIVED = "ARCHIVED"
    """
    Process is archived
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


class Audit(ProvenanceFields):
    """
    Audit activity tracking verification actions for Ijara transactions
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Activity',
         'from_schema': 'https://example.org/schemas/ijara-sukuk-transaction-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Audit', 'Ijara', 'Transaction', 'Sukuk', 'AuditProcess']} })
    audit_id: str = Field(default=..., description="""Unique identifier for the audit""", json_schema_extra = { "linkml_meta": {'alias': 'audit_id', 'domain_of': ['Audit']} })
    audit_date: datetime  = Field(default=..., description="""Date when the audit was conducted""", json_schema_extra = { "linkml_meta": {'alias': 'audit_date', 'domain_of': ['Audit']} })
    completion_date: Optional[datetime ] = Field(default=None, description="""Date when the audit was completed""", json_schema_extra = { "linkml_meta": {'alias': 'completion_date', 'domain_of': ['Audit']} })
    audit_type: AuditTypeEnum = Field(default=..., description="""Type of audit performed""", json_schema_extra = { "linkml_meta": {'alias': 'audit_type', 'domain_of': ['Audit']} })
    auditor_name: str = Field(default=..., description="""Name of the auditor""", json_schema_extra = { "linkml_meta": {'alias': 'auditor_name', 'domain_of': ['Audit']} })
    auditor_organization: Optional[str] = Field(default=None, description="""Organization conducting the audit""", json_schema_extra = { "linkml_meta": {'alias': 'auditor_organization', 'domain_of': ['Audit']} })
    audit_scope: Optional[str] = Field(default=None, description="""Scope and boundaries of the audit""", json_schema_extra = { "linkml_meta": {'alias': 'audit_scope', 'domain_of': ['Audit']} })
    findings: Optional[str] = Field(default=None, description="""Key findings from the audit""", json_schema_extra = { "linkml_meta": {'alias': 'findings', 'domain_of': ['Audit']} })
    recommendations: Optional[str] = Field(default=None, description="""Recommendations based on audit findings""", json_schema_extra = { "linkml_meta": {'alias': 'recommendations', 'domain_of': ['Audit']} })
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


class Ijara(ProvenanceFields):
    """
    Islamic lease contract forming the underlying asset for Sukuk instruments
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc-dae:Lease',
         'from_schema': 'https://example.org/schemas/ijara-sukuk-transaction-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Audit', 'Ijara', 'Transaction', 'Sukuk', 'AuditProcess']} })
    lease_id: str = Field(default=..., description="""Unique identifier for the Ijara lease""", json_schema_extra = { "linkml_meta": {'alias': 'lease_id', 'domain_of': ['Ijara']} })
    lease_term: int = Field(default=..., description="""Duration of the lease in months""", json_schema_extra = { "linkml_meta": {'alias': 'lease_term', 'domain_of': ['Ijara']} })
    start_date: datetime  = Field(default=..., description="""Start date of the lease or process""", json_schema_extra = { "linkml_meta": {'alias': 'start_date', 'domain_of': ['Ijara', 'AuditProcess']} })
    end_date: Optional[datetime ] = Field(default=None, description="""End date of the lease or process""", json_schema_extra = { "linkml_meta": {'alias': 'end_date', 'domain_of': ['Ijara', 'AuditProcess']} })
    asset_description: str = Field(default=..., description="""Description of the leased asset""", json_schema_extra = { "linkml_meta": {'alias': 'asset_description', 'domain_of': ['Ijara']} })
    asset_value: float = Field(default=..., description="""Monetary value of the asset""", json_schema_extra = { "linkml_meta": {'alias': 'asset_value', 'domain_of': ['Ijara']} })
    rental_amount: float = Field(default=..., description="""Rental payment amount for the lease""", json_schema_extra = { "linkml_meta": {'alias': 'rental_amount', 'domain_of': ['Ijara']} })
    payment_frequency: PaymentFrequencyEnum = Field(default=..., description="""Frequency of rental payments""", json_schema_extra = { "linkml_meta": {'alias': 'payment_frequency', 'domain_of': ['Ijara']} })
    lessee_name: str = Field(default=..., description="""Name of the lessee""", json_schema_extra = { "linkml_meta": {'alias': 'lessee_name', 'domain_of': ['Ijara']} })
    lessor_name: str = Field(default=..., description="""Name of the lessor""", json_schema_extra = { "linkml_meta": {'alias': 'lessor_name', 'domain_of': ['Ijara']} })
    lease_status: LeaseStatusEnum = Field(default=..., description="""Current status of the lease""", json_schema_extra = { "linkml_meta": {'alias': 'lease_status', 'domain_of': ['Ijara']} })
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


class Transaction(ProvenanceFields):
    """
    Financial transaction involving Ijara payments or transfers
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc-pas:Transaction',
         'from_schema': 'https://example.org/schemas/ijara-sukuk-transaction-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Audit', 'Ijara', 'Transaction', 'Sukuk', 'AuditProcess']} })
    transaction_id: str = Field(default=..., description="""Unique identifier for the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_id', 'domain_of': ['Transaction']} })
    transaction_date: datetime  = Field(default=..., description="""Date when the transaction occurred""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_date', 'domain_of': ['Transaction']} })
    amount: float = Field(default=..., description="""Monetary amount of the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'amount', 'domain_of': ['Transaction']} })
    currency: str = Field(default=..., description="""Currency code for the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'currency', 'domain_of': ['Transaction', 'Sukuk']} })
    transaction_type: TransactionTypeEnum = Field(default=..., description="""Type of financial transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_type', 'domain_of': ['Transaction']} })
    payment_method: Optional[str] = Field(default=None, description="""Method used for payment""", json_schema_extra = { "linkml_meta": {'alias': 'payment_method', 'domain_of': ['Transaction']} })
    payer: str = Field(default=..., description="""Entity making the payment""", json_schema_extra = { "linkml_meta": {'alias': 'payer', 'domain_of': ['Transaction']} })
    payee: str = Field(default=..., description="""Entity receiving the payment""", json_schema_extra = { "linkml_meta": {'alias': 'payee', 'domain_of': ['Transaction']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'description', 'domain_of': ['Transaction']} })
    reference_number: Optional[str] = Field(default=None, description="""Reference number for the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'reference_number', 'domain_of': ['Transaction']} })
    transaction_status: TransactionStatusEnum = Field(default=..., description="""Current status of the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_status', 'domain_of': ['Transaction']} })
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


class Sukuk(ProvenanceFields):
    """
    Islamic bond instrument backed by Ijara lease assets
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-sec:Bond',
         'from_schema': 'https://example.org/schemas/ijara-sukuk-transaction-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Audit', 'Ijara', 'Transaction', 'Sukuk', 'AuditProcess']} })
    sukuk_id: str = Field(default=..., description="""Unique identifier for the Sukuk instrument""", json_schema_extra = { "linkml_meta": {'alias': 'sukuk_id', 'domain_of': ['Sukuk']} })
    issuance_date: datetime  = Field(default=..., description="""Date when the Sukuk was issued""", json_schema_extra = { "linkml_meta": {'alias': 'issuance_date', 'domain_of': ['Sukuk']} })
    maturity_date: datetime  = Field(default=..., description="""Maturity date of the Sukuk""", json_schema_extra = { "linkml_meta": {'alias': 'maturity_date', 'domain_of': ['Sukuk']} })
    face_value: float = Field(default=..., description="""Face value of individual Sukuk certificate""", json_schema_extra = { "linkml_meta": {'alias': 'face_value', 'domain_of': ['Sukuk']} })
    currency: str = Field(default=..., description="""Currency code for the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'currency', 'domain_of': ['Transaction', 'Sukuk']} })
    coupon_rate: Optional[float] = Field(default=None, description="""Profit rate for the Sukuk""", json_schema_extra = { "linkml_meta": {'alias': 'coupon_rate', 'domain_of': ['Sukuk']} })
    issuer_name: str = Field(default=..., description="""Name of the Sukuk issuer""", json_schema_extra = { "linkml_meta": {'alias': 'issuer_name', 'domain_of': ['Sukuk']} })
    trustee_name: Optional[str] = Field(default=None, description="""Name of the trustee managing the Sukuk""", json_schema_extra = { "linkml_meta": {'alias': 'trustee_name', 'domain_of': ['Sukuk']} })
    underlying_asset_type: str = Field(default=..., description="""Type of underlying asset backing the Sukuk""", json_schema_extra = { "linkml_meta": {'alias': 'underlying_asset_type', 'domain_of': ['Sukuk']} })
    total_issuance_amount: float = Field(default=..., description="""Total amount of Sukuk issuance""", json_schema_extra = { "linkml_meta": {'alias': 'total_issuance_amount', 'domain_of': ['Sukuk']} })
    sukuk_structure_type: SukukStructureEnum = Field(default=..., description="""Structure type of the Sukuk""", json_schema_extra = { "linkml_meta": {'alias': 'sukuk_structure_type', 'domain_of': ['Sukuk']} })
    sukuk_status: SukukStatusEnum = Field(default=..., description="""Current status of the Sukuk""", json_schema_extra = { "linkml_meta": {'alias': 'sukuk_status', 'domain_of': ['Sukuk']} })
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


class AuditProcess(ProvenanceFields):
    """
    Formal verification process for compliance and accuracy of Ijara transactions
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fnd:LegalProcess',
         'from_schema': 'https://example.org/schemas/ijara-sukuk-transaction-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Audit', 'Ijara', 'Transaction', 'Sukuk', 'AuditProcess']} })
    process_id: str = Field(default=..., description="""Unique identifier for the audit process""", json_schema_extra = { "linkml_meta": {'alias': 'process_id', 'domain_of': ['AuditProcess']} })
    process_name: str = Field(default=..., description="""Name of the audit process""", json_schema_extra = { "linkml_meta": {'alias': 'process_name', 'domain_of': ['AuditProcess']} })
    process_description: Optional[str] = Field(default=None, description="""Detailed description of the audit process""", json_schema_extra = { "linkml_meta": {'alias': 'process_description', 'domain_of': ['AuditProcess']} })
    compliance_status: ComplianceStatusEnum = Field(default=..., description="""Compliance status result from the audit process""", json_schema_extra = { "linkml_meta": {'alias': 'compliance_status', 'domain_of': ['AuditProcess']} })
    compliance_framework: Optional[str] = Field(default=None, description="""Regulatory or compliance framework applied""", json_schema_extra = { "linkml_meta": {'alias': 'compliance_framework', 'domain_of': ['AuditProcess']} })
    verification_methodology: Optional[str] = Field(default=None, description="""Methodology used for verification""", json_schema_extra = { "linkml_meta": {'alias': 'verification_methodology', 'domain_of': ['AuditProcess']} })
    process_owner: Optional[str] = Field(default=None, description="""Owner or responsible party for the process""", json_schema_extra = { "linkml_meta": {'alias': 'process_owner', 'domain_of': ['AuditProcess']} })
    start_date: datetime  = Field(default=..., description="""Start date of the lease or process""", json_schema_extra = { "linkml_meta": {'alias': 'start_date', 'domain_of': ['Ijara', 'AuditProcess']} })
    end_date: Optional[datetime ] = Field(default=None, description="""End date of the lease or process""", json_schema_extra = { "linkml_meta": {'alias': 'end_date', 'domain_of': ['Ijara', 'AuditProcess']} })
    process_version: Optional[str] = Field(default=None, description="""Version of the audit process""", json_schema_extra = { "linkml_meta": {'alias': 'process_version', 'domain_of': ['AuditProcess']} })
    process_status: ProcessStatusEnum = Field(default=..., description="""Current status of the audit process""", json_schema_extra = { "linkml_meta": {'alias': 'process_status', 'domain_of': ['AuditProcess']} })
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
Audit.model_rebuild()
Ijara.model_rebuild()
Transaction.model_rebuild()
Sukuk.model_rebuild()
AuditProcess.model_rebuild()

