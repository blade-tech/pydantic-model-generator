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
                    'Shariah principles and generate compliance reports',
     'id': 'https://example.org/schemas/sukuk-shariah-compliance-audit',
     'imports': ['../core/provenance'],
     'name': 'sukuk_shariah_compliance_audit',
     'prefixes': {'fabio': {'prefix_prefix': 'fabio',
                            'prefix_reference': 'http://purl.org/spar/fabio/'},
                  'fibo-fbc': {'prefix_prefix': 'fibo-fbc',
                               'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FBC/ProductsAndServices/FinancialProductsAndServices/'},
                  'fibo-law': {'prefix_prefix': 'fibo-law',
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
                    'Generator\\pydantic_library\\schemas\\overlays\\sukuk_overlay.yaml'} )

class SukukTypeEnum(str, Enum):
    """
    Types of Sukuk structures
    """
    IJARA = "IJARA"
    """
    Lease-based Sukuk
    """
    MUDARABA = "MUDARABA"
    """
    Partnership-based Sukuk
    """
    MUSHARAKA = "MUSHARAKA"
    """
    Joint venture Sukuk
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
    Purchase of existing Sukuk
    """
    SALE = "SALE"
    """
    Sale of Sukuk holdings
    """
    REDEMPTION = "REDEMPTION"
    """
    Redemption at maturity
    """
    COUPON_PAYMENT = "COUPON_PAYMENT"
    """
    Periodic profit distribution
    """
    TRANSFER = "TRANSFER"
    """
    Transfer of ownership
    """


class TransactionStatusEnum(str, Enum):
    """
    Status of a transaction
    """
    PENDING = "PENDING"
    """
    Transaction is pending
    """
    SETTLED = "SETTLED"
    """
    Transaction has settled
    """
    CANCELLED = "CANCELLED"
    """
    Transaction was cancelled
    """
    FAILED = "FAILED"
    """
    Transaction failed
    """
    UNDER_REVIEW = "UNDER_REVIEW"
    """
    Transaction under compliance review
    """


class AuditTypeEnum(str, Enum):
    """
    Types of audits
    """
    PERIODIC = "PERIODIC"
    """
    Regular scheduled audit
    """
    SPECIAL = "SPECIAL"
    """
    Special purpose audit
    """
    COMPLIANCE = "COMPLIANCE"
    """
    Compliance-focused audit
    """
    FORENSIC = "FORENSIC"
    """
    Detailed investigative audit
    """
    PRE_ISSUANCE = "PRE_ISSUANCE"
    """
    Audit before Sukuk issuance
    """


class ComplianceStatusEnum(str, Enum):
    """
    Compliance assessment results
    """
    COMPLIANT = "COMPLIANT"
    """
    Fully compliant with Shariah principles
    """
    NON_COMPLIANT = "NON_COMPLIANT"
    """
    Violates Shariah principles
    """
    PARTIALLY_COMPLIANT = "PARTIALLY_COMPLIANT"
    """
    Partially compliant with minor issues
    """
    UNDER_REVIEW = "UNDER_REVIEW"
    """
    Assessment in progress
    """
    REMEDIATED = "REMEDIATED"
    """
    Previously non-compliant, now remediated
    """


class SeverityLevelEnum(str, Enum):
    """
    Severity levels for compliance violations
    """
    CRITICAL = "CRITICAL"
    """
    Critical violation requiring immediate action
    """
    HIGH = "HIGH"
    """
    High severity violation
    """
    MEDIUM = "MEDIUM"
    """
    Medium severity violation
    """
    LOW = "LOW"
    """
    Low severity violation
    """
    INFORMATIONAL = "INFORMATIONAL"
    """
    Informational finding, not a violation
    """


class RuleCategoryEnum(str, Enum):
    """
    Categories of compliance rules
    """
    RIBA_PROHIBITION = "RIBA_PROHIBITION"
    """
    Rules prohibiting interest (riba)
    """
    GHARAR_PROHIBITION = "GHARAR_PROHIBITION"
    """
    Rules prohibiting excessive uncertainty
    """
    ASSET_BACKING = "ASSET_BACKING"
    """
    Rules requiring asset backing
    """
    PROFIT_SHARING = "PROFIT_SHARING"
    """
    Rules governing profit distribution
    """
    DOCUMENTATION = "DOCUMENTATION"
    """
    Documentation requirements
    """
    GOVERNANCE = "GOVERNANCE"
    """
    Governance and oversight rules
    """
    PROHIBITED_ACTIVITIES = "PROHIBITED_ACTIVITIES"
    """
    Rules on prohibited business activities
    """
    STRUCTURAL = "STRUCTURAL"
    """
    Structural requirements for Sukuk
    """


class EnforcementLevelEnum(str, Enum):
    """
    Enforcement levels for compliance rules
    """
    MANDATORY = "MANDATORY"
    """
    Mandatory compliance required
    """
    RECOMMENDED = "RECOMMENDED"
    """
    Recommended best practice
    """
    OPTIONAL = "OPTIONAL"
    """
    Optional guidance
    """
    CONDITIONAL = "CONDITIONAL"
    """
    Required under specific conditions
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
    Islamic financial certificate representing ownership in an underlying asset
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-sec:Bond',
         'from_schema': 'https://example.org/schemas/sukuk-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Sukuk',
                       'Transaction',
                       'Audit',
                       'ComplianceAssessment',
                       'ShariahComplianceFramework',
                       'AuditReport',
                       'ComplianceRule']} })
    identifier: str = Field(default=..., description="""Business identifier for the Sukuk instrument""", json_schema_extra = { "linkml_meta": {'alias': 'identifier', 'domain_of': ['Sukuk']} })
    sukuk_type: SukukTypeEnum = Field(default=..., description="""Type of Sukuk structure""", json_schema_extra = { "linkml_meta": {'alias': 'sukuk_type', 'domain_of': ['Sukuk']} })
    issuance_date: date = Field(default=..., description="""Date when the Sukuk was issued""", json_schema_extra = { "linkml_meta": {'alias': 'issuance_date', 'domain_of': ['Sukuk']} })
    maturity_date: date = Field(default=..., description="""Date when the Sukuk matures""", json_schema_extra = { "linkml_meta": {'alias': 'maturity_date', 'domain_of': ['Sukuk']} })
    face_value: float = Field(default=..., description="""Nominal value of the Sukuk""", json_schema_extra = { "linkml_meta": {'alias': 'face_value', 'domain_of': ['Sukuk']} })
    underlying_asset: str = Field(default=..., description="""Asset backing the Sukuk""", json_schema_extra = { "linkml_meta": {'alias': 'underlying_asset', 'domain_of': ['Sukuk']} })
    issuer_name: str = Field(default=..., description="""Name of the entity issuing the Sukuk""", json_schema_extra = { "linkml_meta": {'alias': 'issuer_name', 'domain_of': ['Sukuk']} })
    shariah_board_approval: bool = Field(default=..., description="""Approval status from Shariah board""", json_schema_extra = { "linkml_meta": {'alias': 'shariah_board_approval', 'domain_of': ['Sukuk']} })
    structure_type: Optional[str] = Field(default=None, description="""Structural classification of the Sukuk""", json_schema_extra = { "linkml_meta": {'alias': 'structure_type', 'domain_of': ['Sukuk']} })
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
    Financial activity involving the issuance, trading, or settlement of Sukuk
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc:FinancialTransaction',
         'from_schema': 'https://example.org/schemas/sukuk-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Sukuk',
                       'Transaction',
                       'Audit',
                       'ComplianceAssessment',
                       'ShariahComplianceFramework',
                       'AuditReport',
                       'ComplianceRule']} })
    transaction_id: str = Field(default=..., description="""Unique identifier for the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_id',
         'domain_of': ['Transaction', 'ComplianceAssessment']} })
    transaction_date: datetime  = Field(default=..., description="""Date when the transaction occurred""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_date', 'domain_of': ['Transaction']} })
    transaction_type: TransactionTypeEnum = Field(default=..., description="""Type of transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_type', 'domain_of': ['Transaction']} })
    sukuk_identifier: str = Field(default=..., description="""Reference to the Sukuk involved in the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'sukuk_identifier', 'domain_of': ['Transaction']} })
    counterparty: str = Field(default=..., description="""Other party involved in the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'counterparty', 'domain_of': ['Transaction']} })
    transaction_amount: float = Field(default=..., description="""Monetary amount of the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_amount', 'domain_of': ['Transaction']} })
    settlement_date: date = Field(default=..., description="""Date when the transaction settles""", json_schema_extra = { "linkml_meta": {'alias': 'settlement_date', 'domain_of': ['Transaction']} })
    transaction_status: TransactionStatusEnum = Field(default=..., description="""Current status of the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_status', 'domain_of': ['Transaction']} })
    currency: str = Field(default=..., description="""Currency of the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'currency', 'domain_of': ['Transaction']} })
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
    Systematic examination of Sukuk transactions for Shariah compliance
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Activity',
         'from_schema': 'https://example.org/schemas/sukuk-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Sukuk',
                       'Transaction',
                       'Audit',
                       'ComplianceAssessment',
                       'ShariahComplianceFramework',
                       'AuditReport',
                       'ComplianceRule']} })
    audit_id: str = Field(default=..., description="""Unique identifier for the audit""", json_schema_extra = { "linkml_meta": {'alias': 'audit_id', 'domain_of': ['Audit', 'AuditReport']} })
    audit_period: str = Field(default=..., description="""Time period covered by the audit""", json_schema_extra = { "linkml_meta": {'alias': 'audit_period', 'domain_of': ['Audit']} })
    audit_start_date: date = Field(default=..., description="""Start date of the audit period""", json_schema_extra = { "linkml_meta": {'alias': 'audit_start_date', 'domain_of': ['Audit']} })
    audit_end_date: date = Field(default=..., description="""End date of the audit period""", json_schema_extra = { "linkml_meta": {'alias': 'audit_end_date', 'domain_of': ['Audit']} })
    auditor_name: str = Field(default=..., description="""Name of the lead auditor""", json_schema_extra = { "linkml_meta": {'alias': 'auditor_name', 'domain_of': ['Audit']} })
    auditor_organization: str = Field(default=..., description="""Organization conducting the audit""", json_schema_extra = { "linkml_meta": {'alias': 'auditor_organization', 'domain_of': ['Audit']} })
    audit_scope: str = Field(default=..., description="""Scope and boundaries of the audit""", json_schema_extra = { "linkml_meta": {'alias': 'audit_scope', 'domain_of': ['Audit']} })
    audit_type: AuditTypeEnum = Field(default=..., description="""Type of audit being conducted""", json_schema_extra = { "linkml_meta": {'alias': 'audit_type', 'domain_of': ['Audit']} })
    shariah_board_members: Optional[list[str]] = Field(default=None, description="""List of Shariah board members involved""", json_schema_extra = { "linkml_meta": {'alias': 'shariah_board_members', 'domain_of': ['Audit']} })
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
    Evaluation activity determining conformance to Shariah principles
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Activity',
         'from_schema': 'https://example.org/schemas/sukuk-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Sukuk',
                       'Transaction',
                       'Audit',
                       'ComplianceAssessment',
                       'ShariahComplianceFramework',
                       'AuditReport',
                       'ComplianceRule']} })
    assessment_id: str = Field(default=..., description="""Unique identifier for the compliance assessment""", json_schema_extra = { "linkml_meta": {'alias': 'assessment_id', 'domain_of': ['ComplianceAssessment']} })
    assessment_date: datetime  = Field(default=..., description="""Date when the assessment was performed""", json_schema_extra = { "linkml_meta": {'alias': 'assessment_date', 'domain_of': ['ComplianceAssessment']} })
    compliance_status: ComplianceStatusEnum = Field(default=..., description="""Result of the compliance assessment""", json_schema_extra = { "linkml_meta": {'alias': 'compliance_status', 'domain_of': ['ComplianceAssessment']} })
    transaction_id: str = Field(default=..., description="""Unique identifier for the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_id',
         'domain_of': ['Transaction', 'ComplianceAssessment']} })
    assessor_name: str = Field(default=..., description="""Name of the person performing the assessment""", json_schema_extra = { "linkml_meta": {'alias': 'assessor_name', 'domain_of': ['ComplianceAssessment']} })
    violation_details: Optional[str] = Field(default=None, description="""Details of any compliance violations found""", json_schema_extra = { "linkml_meta": {'alias': 'violation_details', 'domain_of': ['ComplianceAssessment']} })
    severity_level: Optional[SeverityLevelEnum] = Field(default=None, description="""Severity of the compliance issue""", json_schema_extra = { "linkml_meta": {'alias': 'severity_level', 'domain_of': ['ComplianceAssessment']} })
    remediation_required: bool = Field(default=..., description="""Whether remediation action is required""", json_schema_extra = { "linkml_meta": {'alias': 'remediation_required', 'domain_of': ['ComplianceAssessment']} })
    remediation_deadline: Optional[date] = Field(default=None, description="""Deadline for completing remediation""", json_schema_extra = { "linkml_meta": {'alias': 'remediation_deadline', 'domain_of': ['ComplianceAssessment']} })
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
    Regulatory framework defining Islamic finance principles and requirements
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'skos:Concept',
         'from_schema': 'https://example.org/schemas/sukuk-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Sukuk',
                       'Transaction',
                       'Audit',
                       'ComplianceAssessment',
                       'ShariahComplianceFramework',
                       'AuditReport',
                       'ComplianceRule']} })
    framework_name: str = Field(default=..., description="""Name of the Shariah compliance framework""", json_schema_extra = { "linkml_meta": {'alias': 'framework_name', 'domain_of': ['ShariahComplianceFramework']} })
    framework_version: str = Field(default=..., description="""Version number of the framework""", json_schema_extra = { "linkml_meta": {'alias': 'framework_version', 'domain_of': ['ShariahComplianceFramework']} })
    issuing_authority: str = Field(default=..., description="""Authority that issued the framework""", json_schema_extra = { "linkml_meta": {'alias': 'issuing_authority', 'domain_of': ['ShariahComplianceFramework']} })
    effective_date: date = Field(default=..., description="""Date when the framework becomes effective""", json_schema_extra = { "linkml_meta": {'alias': 'effective_date', 'domain_of': ['ShariahComplianceFramework']} })
    jurisdiction: str = Field(default=..., description="""Geographic or legal jurisdiction of the framework""", json_schema_extra = { "linkml_meta": {'alias': 'jurisdiction', 'domain_of': ['ShariahComplianceFramework']} })
    framework_scope: str = Field(default=..., description="""Scope of application for the framework""", json_schema_extra = { "linkml_meta": {'alias': 'framework_scope', 'domain_of': ['ShariahComplianceFramework']} })
    update_frequency: Optional[str] = Field(default=None, description="""How often the framework is updated""", json_schema_extra = { "linkml_meta": {'alias': 'update_frequency', 'domain_of': ['ShariahComplianceFramework']} })
    reference_document: Optional[str] = Field(default=None, description="""Reference to the official framework document""", json_schema_extra = { "linkml_meta": {'alias': 'reference_document', 'domain_of': ['ShariahComplianceFramework']} })
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
    Document containing findings, assessments, and recommendations from audit
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fabio:Report',
         'from_schema': 'https://example.org/schemas/sukuk-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Sukuk',
                       'Transaction',
                       'Audit',
                       'ComplianceAssessment',
                       'ShariahComplianceFramework',
                       'AuditReport',
                       'ComplianceRule']} })
    report_id: str = Field(default=..., description="""Unique identifier for the audit report""", json_schema_extra = { "linkml_meta": {'alias': 'report_id', 'domain_of': ['AuditReport']} })
    report_date: date = Field(default=..., description="""Date when the report was generated""", json_schema_extra = { "linkml_meta": {'alias': 'report_date', 'domain_of': ['AuditReport']} })
    audit_id: str = Field(default=..., description="""Unique identifier for the audit""", json_schema_extra = { "linkml_meta": {'alias': 'audit_id', 'domain_of': ['Audit', 'AuditReport']} })
    overall_compliance: ComplianceStatusEnum = Field(default=..., description="""Overall compliance rating from the audit""", json_schema_extra = { "linkml_meta": {'alias': 'overall_compliance', 'domain_of': ['AuditReport']} })
    total_transactions_reviewed: int = Field(default=..., description="""Total number of transactions reviewed in the audit""", json_schema_extra = { "linkml_meta": {'alias': 'total_transactions_reviewed', 'domain_of': ['AuditReport']} })
    compliant_transactions_count: int = Field(default=..., description="""Number of transactions found to be compliant""", json_schema_extra = { "linkml_meta": {'alias': 'compliant_transactions_count', 'domain_of': ['AuditReport']} })
    non_compliant_transactions_count: int = Field(default=..., description="""Number of transactions found to be non-compliant""", json_schema_extra = { "linkml_meta": {'alias': 'non_compliant_transactions_count', 'domain_of': ['AuditReport']} })
    report_summary: str = Field(default=..., description="""Executive summary of the audit findings""", json_schema_extra = { "linkml_meta": {'alias': 'report_summary', 'domain_of': ['AuditReport']} })
    recommendations: Optional[list[str]] = Field(default=None, description="""Recommendations for improving compliance""", json_schema_extra = { "linkml_meta": {'alias': 'recommendations', 'domain_of': ['AuditReport']} })
    next_audit_date: Optional[date] = Field(default=None, description="""Scheduled date for the next audit""", json_schema_extra = { "linkml_meta": {'alias': 'next_audit_date', 'domain_of': ['AuditReport']} })
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
    Specific constraint or requirement derived from Shariah principles
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-law:Law',
         'from_schema': 'https://example.org/schemas/sukuk-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Sukuk',
                       'Transaction',
                       'Audit',
                       'ComplianceAssessment',
                       'ShariahComplianceFramework',
                       'AuditReport',
                       'ComplianceRule']} })
    rule_id: str = Field(default=..., description="""Unique identifier for the compliance rule""", json_schema_extra = { "linkml_meta": {'alias': 'rule_id', 'domain_of': ['ComplianceRule']} })
    rule_name: str = Field(default=..., description="""Name of the compliance rule""", json_schema_extra = { "linkml_meta": {'alias': 'rule_name', 'domain_of': ['ComplianceRule']} })
    rule_description: str = Field(default=..., description="""Detailed description of the compliance rule""", json_schema_extra = { "linkml_meta": {'alias': 'rule_description', 'domain_of': ['ComplianceRule']} })
    category: RuleCategoryEnum = Field(default=..., description="""Category classification of the rule""", json_schema_extra = { "linkml_meta": {'alias': 'category', 'domain_of': ['ComplianceRule']} })
    framework_reference: str = Field(default=..., description="""Reference to the framework defining this rule""", json_schema_extra = { "linkml_meta": {'alias': 'framework_reference', 'domain_of': ['ComplianceRule']} })
    applicable_sukuk_types: list[SukukTypeEnum] = Field(default=..., description="""Types of Sukuk to which this rule applies""", json_schema_extra = { "linkml_meta": {'alias': 'applicable_sukuk_types', 'domain_of': ['ComplianceRule']} })
    enforcement_level: EnforcementLevelEnum = Field(default=..., description="""Level of enforcement for the rule""", json_schema_extra = { "linkml_meta": {'alias': 'enforcement_level', 'domain_of': ['ComplianceRule']} })
    penalty_description: Optional[str] = Field(default=None, description="""Description of penalties for rule violation""", json_schema_extra = { "linkml_meta": {'alias': 'penalty_description', 'domain_of': ['ComplianceRule']} })
    rule_source: str = Field(default=..., description="""Source authority for the rule""", json_schema_extra = { "linkml_meta": {'alias': 'rule_source', 'domain_of': ['ComplianceRule']} })
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
ComplianceAssessment.model_rebuild()
ShariahComplianceFramework.model_rebuild()
AuditReport.model_rebuild()
ComplianceRule.model_rebuild()

