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


linkml_meta = LinkMLMeta({'default_prefix': 'sukuk_shariah_compliance_audit',
     'description': 'Schema for auditing Sukuk transactions to ensure adherence to '
                    'Shariah principles and Islamic finance requirements',
     'id': 'https://example.org/schemas/sukuk-shariah-compliance-audit',
     'imports': ['../core/provenance'],
     'name': 'sukuk_shariah_compliance_audit',
     'prefixes': {'fabio': {'prefix_prefix': 'fabio',
                            'prefix_reference': 'http://purl.org/spar/fabio/'},
                  'fibo-fbc': {'prefix_prefix': 'fibo-fbc',
                               'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FBC/ProductsAndServices/FinancialProductsAndServices/'},
                  'fibo-fnd': {'prefix_prefix': 'fibo-fnd',
                               'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FND/Law/LegalCore/'},
                  'fibo-reg': {'prefix_prefix': 'fibo-reg',
                               'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FBC/FunctionalEntities/RegulatoryAgencies/'},
                  'fibo-sec': {'prefix_prefix': 'fibo-sec',
                               'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/SEC/Debt/Bonds/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'}},
     'source_file': 'D:\\projects\\Pydantic Model '
                    'Generator\\pydantic_library\\schemas\\overlays\\business_outcome_overlay.yaml'} )

class SukukStructureTypeEnum(str, Enum):
    """
    Types of Shariah-compliant Sukuk structures
    """
    IJARA = "IJARA"
    """
    Lease-based Sukuk
    """
    MUDARABA = "MUDARABA"
    """
    Profit-sharing partnership Sukuk
    """
    MUSHARAKA = "MUSHARAKA"
    """
    Joint venture partnership Sukuk
    """
    MURABAHA = "MURABAHA"
    """
    Cost-plus financing Sukuk
    """
    SALAM = "SALAM"
    """
    Forward sale Sukuk
    """
    ISTISNA = "ISTISNA"
    """
    Manufacturing contract Sukuk
    """
    WAKALA = "WAKALA"
    """
    Agency-based Sukuk
    """
    HYBRID = "HYBRID"
    """
    Combination of multiple structures
    """


class TransactionTypeEnum(str, Enum):
    """
    Types of Sukuk transactions
    """
    ISSUANCE = "ISSUANCE"
    """
    Initial issuance of Sukuk
    """
    PURCHASE = "PURCHASE"
    """
    Purchase of Sukuk
    """
    SALE = "SALE"
    """
    Sale of Sukuk
    """
    TRANSFER = "TRANSFER"
    """
    Transfer of Sukuk ownership
    """
    REDEMPTION = "REDEMPTION"
    """
    Redemption at maturity
    """
    COUPON_PAYMENT = "COUPON_PAYMENT"
    """
    Periodic profit distribution
    """
    RESTRUCTURING = "RESTRUCTURING"
    """
    Restructuring of Sukuk terms
    """


class AuditTypeEnum(str, Enum):
    """
    Types of Shariah compliance audits
    """
    INITIAL = "INITIAL"
    """
    Initial compliance audit
    """
    PERIODIC = "PERIODIC"
    """
    Regular periodic audit
    """
    SPECIAL = "SPECIAL"
    """
    Special investigation audit
    """
    FOLLOW_UP = "FOLLOW_UP"
    """
    Follow-up audit after violations
    """
    COMPREHENSIVE = "COMPREHENSIVE"
    """
    Comprehensive full-scope audit
    """
    TARGETED = "TARGETED"
    """
    Targeted audit of specific aspects
    """


class ComplianceStatusEnum(str, Enum):
    """
    Compliance status values
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
    Partially compliant with minor issues
    """
    PENDING_REVIEW = "PENDING_REVIEW"
    """
    Assessment pending further review
    """
    UNDER_REMEDIATION = "UNDER_REMEDIATION"
    """
    Non-compliance being remediated
    """


class RiskLevelEnum(str, Enum):
    """
    Risk level classifications
    """
    LOW = "LOW"
    """
    Low risk to Shariah compliance
    """
    MEDIUM = "MEDIUM"
    """
    Medium risk to Shariah compliance
    """
    HIGH = "HIGH"
    """
    High risk to Shariah compliance
    """
    CRITICAL = "CRITICAL"
    """
    Critical risk requiring immediate action
    """


class ComplianceRatingEnum(str, Enum):
    """
    Overall compliance ratings
    """
    EXCELLENT = "EXCELLENT"
    """
    Excellent compliance with no issues
    """
    SATISFACTORY = "SATISFACTORY"
    """
    Satisfactory compliance with minor issues
    """
    NEEDS_IMPROVEMENT = "NEEDS_IMPROVEMENT"
    """
    Compliance needs improvement
    """
    UNSATISFACTORY = "UNSATISFACTORY"
    """
    Unsatisfactory compliance
    """
    FAILED = "FAILED"
    """
    Failed to meet compliance requirements
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


class Sukuk(ProvenanceFields):
    """
    Islamic financial certificate representing ownership interest in an asset or pool of assets
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-sec:Bond',
         'from_schema': 'https://example.org/schemas/sukuk-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Sukuk',
                       'Transaction',
                       'Audit',
                       'ShariahComplianceFramework',
                       'ComplianceAssessment',
                       'AuditReport']} })
    identifier: str = Field(default=..., description="""Sukuk instrument identifier""", json_schema_extra = { "linkml_meta": {'alias': 'identifier', 'domain_of': ['Sukuk']} })
    sukuk_name: str = Field(default=..., description="""Name of the Sukuk instrument""", json_schema_extra = { "linkml_meta": {'alias': 'sukuk_name', 'domain_of': ['Sukuk']} })
    structure_type: SukukStructureTypeEnum = Field(default=..., description="""Type of Shariah-compliant structure""", json_schema_extra = { "linkml_meta": {'alias': 'structure_type', 'domain_of': ['Sukuk']} })
    issuance_date: datetime  = Field(default=..., description="""Date when the Sukuk was issued""", json_schema_extra = { "linkml_meta": {'alias': 'issuance_date', 'domain_of': ['Sukuk']} })
    maturity_date: Optional[datetime ] = Field(default=None, description="""Date when the Sukuk matures""", json_schema_extra = { "linkml_meta": {'alias': 'maturity_date', 'domain_of': ['Sukuk']} })
    face_value: float = Field(default=..., description="""Face value of the Sukuk""", json_schema_extra = { "linkml_meta": {'alias': 'face_value', 'domain_of': ['Sukuk']} })
    underlying_asset: str = Field(default=..., description="""Asset backing the Sukuk""", json_schema_extra = { "linkml_meta": {'alias': 'underlying_asset', 'domain_of': ['Sukuk']} })
    issuer_name: str = Field(default=..., description="""Name of the Sukuk issuer""", json_schema_extra = { "linkml_meta": {'alias': 'issuer_name', 'domain_of': ['Sukuk']} })
    shariah_board_approval: bool = Field(default=..., description="""Approval status from Shariah board""", json_schema_extra = { "linkml_meta": {'alias': 'shariah_board_approval', 'domain_of': ['Sukuk']} })
    has_transactions: Optional[list[str]] = Field(default=None, description="""Transactions associated with this Sukuk""", json_schema_extra = { "linkml_meta": {'alias': 'has_transactions', 'domain_of': ['Sukuk']} })
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
    Financial activity involving the exchange or transfer of Sukuk instruments
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc:Transaction',
         'from_schema': 'https://example.org/schemas/sukuk-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Sukuk',
                       'Transaction',
                       'Audit',
                       'ShariahComplianceFramework',
                       'ComplianceAssessment',
                       'AuditReport']} })
    transaction_id: str = Field(default=..., description="""Unique identifier for the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_id', 'domain_of': ['Transaction']} })
    transaction_date: datetime  = Field(default=..., description="""Date when the transaction occurred""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_date', 'domain_of': ['Transaction']} })
    transaction_type: TransactionTypeEnum = Field(default=..., description="""Type of transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_type', 'domain_of': ['Transaction']} })
    amount: float = Field(default=..., description="""Transaction amount""", json_schema_extra = { "linkml_meta": {'alias': 'amount', 'domain_of': ['Transaction']} })
    currency: str = Field(default=..., description="""Currency code for the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'currency', 'domain_of': ['Transaction']} })
    counterparty: Optional[str] = Field(default=None, description="""Other party in the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'counterparty', 'domain_of': ['Transaction']} })
    settlement_date: Optional[datetime ] = Field(default=None, description="""Date when the transaction settles""", json_schema_extra = { "linkml_meta": {'alias': 'settlement_date', 'domain_of': ['Transaction']} })
    sukuk_reference: str = Field(default=..., description="""Reference to the Sukuk instrument""", json_schema_extra = { "linkml_meta": {'alias': 'sukuk_reference', 'domain_of': ['Transaction']} })
    governed_by_framework: Optional[list[str]] = Field(default=None, description="""Shariah compliance framework governing this transaction""", json_schema_extra = { "linkml_meta": {'alias': 'governed_by_framework', 'domain_of': ['Transaction']} })
    assessed_by_assessment: Optional[list[str]] = Field(default=None, description="""Compliance assessments for this transaction""", json_schema_extra = { "linkml_meta": {'alias': 'assessed_by_assessment', 'domain_of': ['Transaction']} })
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
    Systematic examination process to verify Shariah compliance of Sukuk transactions
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Activity',
         'from_schema': 'https://example.org/schemas/sukuk-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Sukuk',
                       'Transaction',
                       'Audit',
                       'ShariahComplianceFramework',
                       'ComplianceAssessment',
                       'AuditReport']} })
    audit_id: str = Field(default=..., description="""Unique identifier for the audit""", json_schema_extra = { "linkml_meta": {'alias': 'audit_id', 'domain_of': ['Audit']} })
    audit_date: datetime  = Field(default=..., description="""Date when the audit was conducted""", json_schema_extra = { "linkml_meta": {'alias': 'audit_date', 'domain_of': ['Audit']} })
    audit_type: AuditTypeEnum = Field(default=..., description="""Type of audit performed""", json_schema_extra = { "linkml_meta": {'alias': 'audit_type', 'domain_of': ['Audit']} })
    auditor_name: str = Field(default=..., description="""Name of the auditor""", json_schema_extra = { "linkml_meta": {'alias': 'auditor_name', 'domain_of': ['Audit']} })
    auditor_organization: Optional[str] = Field(default=None, description="""Organization conducting the audit""", json_schema_extra = { "linkml_meta": {'alias': 'auditor_organization', 'domain_of': ['Audit']} })
    audit_scope: Optional[str] = Field(default=None, description="""Scope of the audit""", json_schema_extra = { "linkml_meta": {'alias': 'audit_scope', 'domain_of': ['Audit']} })
    audit_methodology: Optional[str] = Field(default=None, description="""Methodology used for the audit""", json_schema_extra = { "linkml_meta": {'alias': 'audit_methodology', 'domain_of': ['Audit']} })
    evaluates_assessment: list[str] = Field(default=..., description="""Compliance assessments evaluated by this audit""", json_schema_extra = { "linkml_meta": {'alias': 'evaluates_assessment', 'domain_of': ['Audit']} })
    produces_report: str = Field(default=..., description="""Audit report produced by this audit""", json_schema_extra = { "linkml_meta": {'alias': 'produces_report', 'domain_of': ['Audit']} })
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


class ShariahComplianceFramework(ProvenanceFields):
    """
    Set of Islamic legal principles and rules governing permissible financial activities
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fnd:Law',
         'from_schema': 'https://example.org/schemas/sukuk-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Sukuk',
                       'Transaction',
                       'Audit',
                       'ShariahComplianceFramework',
                       'ComplianceAssessment',
                       'AuditReport']} })
    framework_name: str = Field(default=..., description="""Name of the Shariah compliance framework""", json_schema_extra = { "linkml_meta": {'alias': 'framework_name', 'domain_of': ['ShariahComplianceFramework']} })
    framework_version: Optional[str] = Field(default=None, description="""Version of the framework""", json_schema_extra = { "linkml_meta": {'alias': 'framework_version', 'domain_of': ['ShariahComplianceFramework']} })
    issuing_authority: str = Field(default=..., description="""Authority that issued the framework""", json_schema_extra = { "linkml_meta": {'alias': 'issuing_authority', 'domain_of': ['ShariahComplianceFramework']} })
    publication_date: Optional[datetime ] = Field(default=None, description="""Date when the framework was published""", json_schema_extra = { "linkml_meta": {'alias': 'publication_date', 'domain_of': ['ShariahComplianceFramework']} })
    effective_date: Optional[datetime ] = Field(default=None, description="""Date when the framework became effective""", json_schema_extra = { "linkml_meta": {'alias': 'effective_date', 'domain_of': ['ShariahComplianceFramework']} })
    jurisdiction: Optional[str] = Field(default=None, description="""Geographic or organizational jurisdiction""", json_schema_extra = { "linkml_meta": {'alias': 'jurisdiction', 'domain_of': ['ShariahComplianceFramework']} })
    key_principles: Optional[list[str]] = Field(default=None, description="""Key Shariah principles in the framework""", json_schema_extra = { "linkml_meta": {'alias': 'key_principles', 'domain_of': ['ShariahComplianceFramework']} })
    prohibited_activities: Optional[list[str]] = Field(default=None, description="""Activities prohibited under this framework""", json_schema_extra = { "linkml_meta": {'alias': 'prohibited_activities', 'domain_of': ['ShariahComplianceFramework']} })
    documentation_url: Optional[str] = Field(default=None, description="""URL to framework documentation""", json_schema_extra = { "linkml_meta": {'alias': 'documentation_url', 'domain_of': ['ShariahComplianceFramework']} })
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
    Evaluation of transaction adherence to Shariah compliance requirements
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-reg:RegulatoryCompliance',
         'from_schema': 'https://example.org/schemas/sukuk-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Sukuk',
                       'Transaction',
                       'Audit',
                       'ShariahComplianceFramework',
                       'ComplianceAssessment',
                       'AuditReport']} })
    assessment_id: str = Field(default=..., description="""Unique identifier for the assessment""", json_schema_extra = { "linkml_meta": {'alias': 'assessment_id', 'domain_of': ['ComplianceAssessment']} })
    assessment_date: datetime  = Field(default=..., description="""Date when the assessment was performed""", json_schema_extra = { "linkml_meta": {'alias': 'assessment_date', 'domain_of': ['ComplianceAssessment']} })
    assessor_name: str = Field(default=..., description="""Name of the person performing the assessment""", json_schema_extra = { "linkml_meta": {'alias': 'assessor_name', 'domain_of': ['ComplianceAssessment']} })
    assessor_credentials: Optional[str] = Field(default=None, description="""Credentials of the assessor""", json_schema_extra = { "linkml_meta": {'alias': 'assessor_credentials', 'domain_of': ['ComplianceAssessment']} })
    compliance_status: ComplianceStatusEnum = Field(default=..., description="""Compliance status result""", json_schema_extra = { "linkml_meta": {'alias': 'compliance_status', 'domain_of': ['ComplianceAssessment']} })
    violations_found: Optional[int] = Field(default=None, description="""Number of violations found""", json_schema_extra = { "linkml_meta": {'alias': 'violations_found', 'domain_of': ['ComplianceAssessment']} })
    violation_details: Optional[list[str]] = Field(default=None, description="""Details of violations found""", json_schema_extra = { "linkml_meta": {'alias': 'violation_details', 'domain_of': ['ComplianceAssessment']} })
    risk_level: Optional[RiskLevelEnum] = Field(default=None, description="""Risk level assessment""", json_schema_extra = { "linkml_meta": {'alias': 'risk_level', 'domain_of': ['ComplianceAssessment']} })
    remediation_required: Optional[bool] = Field(default=None, description="""Whether remediation is required""", json_schema_extra = { "linkml_meta": {'alias': 'remediation_required', 'domain_of': ['ComplianceAssessment']} })
    transaction_reference: str = Field(default=..., description="""Reference to the transaction assessed""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_reference', 'domain_of': ['ComplianceAssessment']} })
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
    Formal document detailing audit findings, compliance status, and recommendations
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fabio:Report',
         'from_schema': 'https://example.org/schemas/sukuk-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Sukuk',
                       'Transaction',
                       'Audit',
                       'ShariahComplianceFramework',
                       'ComplianceAssessment',
                       'AuditReport']} })
    report_id: str = Field(default=..., description="""Unique identifier for the report""", json_schema_extra = { "linkml_meta": {'alias': 'report_id', 'domain_of': ['AuditReport']} })
    report_date: datetime  = Field(default=..., description="""Date when the report was generated""", json_schema_extra = { "linkml_meta": {'alias': 'report_date', 'domain_of': ['AuditReport']} })
    report_title: str = Field(default=..., description="""Title of the audit report""", json_schema_extra = { "linkml_meta": {'alias': 'report_title', 'domain_of': ['AuditReport']} })
    executive_summary: Optional[str] = Field(default=None, description="""Executive summary of the report""", json_schema_extra = { "linkml_meta": {'alias': 'executive_summary', 'domain_of': ['AuditReport']} })
    conclusion: str = Field(default=..., description="""Overall conclusion of the audit""", json_schema_extra = { "linkml_meta": {'alias': 'conclusion', 'domain_of': ['AuditReport']} })
    overall_compliance_rating: ComplianceRatingEnum = Field(default=..., description="""Overall compliance rating""", json_schema_extra = { "linkml_meta": {'alias': 'overall_compliance_rating', 'domain_of': ['AuditReport']} })
    findings_summary: Optional[str] = Field(default=None, description="""Summary of audit findings""", json_schema_extra = { "linkml_meta": {'alias': 'findings_summary', 'domain_of': ['AuditReport']} })
    recommendations: Optional[list[str]] = Field(default=None, description="""Recommendations from the audit""", json_schema_extra = { "linkml_meta": {'alias': 'recommendations', 'domain_of': ['AuditReport']} })
    audit_reference: str = Field(default=..., description="""Reference to the audit that produced this report""", json_schema_extra = { "linkml_meta": {'alias': 'audit_reference', 'domain_of': ['AuditReport']} })
    next_review_date: Optional[datetime ] = Field(default=None, description="""Date for next review""", json_schema_extra = { "linkml_meta": {'alias': 'next_review_date', 'domain_of': ['AuditReport']} })
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
Sukuk.model_rebuild()
Transaction.model_rebuild()
Audit.model_rebuild()
ShariahComplianceFramework.model_rebuild()
ComplianceAssessment.model_rebuild()
AuditReport.model_rebuild()

