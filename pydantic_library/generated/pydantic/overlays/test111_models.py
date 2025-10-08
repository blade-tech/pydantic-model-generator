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


linkml_meta = LinkMLMeta({'default_prefix': 'murabaha_shariah_compliance_audit',
     'description': 'LinkML schema for auditing and verifying Shariah compliance '
                    'in Murabaha transactions, including ownership verification, '
                    'profit disclosure, payment terms validation, and '
                    'comprehensive audit trail management following AAOIFI Shariah '
                    'Standards.',
     'id': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
     'imports': ['../core/provenance'],
     'name': 'murabaha_shariah_compliance_audit',
     'prefixes': {'fibo-fbc': {'prefix_prefix': 'fibo-fbc',
                               'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FBC/'},
                  'fibo-fnd': {'prefix_prefix': 'fibo-fnd',
                               'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FND/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'}},
     'source_file': 'D:\\projects\\Pydantic Model '
                    'Generator\\pydantic_library\\schemas\\overlays\\test111_overlay.yaml'} )

class CustomerTypeEnum(str, Enum):
    """
    Types of customers in Murabaha transactions
    """
    INDIVIDUAL = "INDIVIDUAL"
    """
    Individual retail customer
    """
    CORPORATE = "CORPORATE"
    """
    Corporate business entity
    """
    INSTITUTIONAL = "INSTITUTIONAL"
    """
    Institutional investor
    """
    SME = "SME"
    """
    Small and medium enterprise
    """
    GOVERNMENT = "GOVERNMENT"
    """
    Government entity
    """


class AssetTypeEnum(str, Enum):
    """
    Categories of assets financed through Murabaha
    """
    REAL_ESTATE = "REAL_ESTATE"
    """
    Property and real estate
    """
    VEHICLE = "VEHICLE"
    """
    Automobiles and vehicles
    """
    EQUIPMENT = "EQUIPMENT"
    """
    Machinery and equipment
    """
    COMMODITY = "COMMODITY"
    """
    Tradeable commodities
    """
    INVENTORY = "INVENTORY"
    """
    Business inventory
    """
    OTHER = "OTHER"
    """
    Other asset types
    """


class AuditTypeEnum(str, Enum):
    """
    Types of Shariah compliance audits
    """
    OWNERSHIP_VERIFICATION = "OWNERSHIP_VERIFICATION"
    """
    Verify bank owned asset before sale
    """
    PROFIT_DISCLOSURE = "PROFIT_DISCLOSURE"
    """
    Check profit markup transparency
    """
    PAYMENT_TERMS = "PAYMENT_TERMS"
    """
    Validate payment terms compliance
    """
    DOCUMENTATION = "DOCUMENTATION"
    """
    Review transaction documentation
    """
    COMPREHENSIVE = "COMPREHENSIVE"
    """
    Full transaction audit
    """
    PERIODIC_REVIEW = "PERIODIC_REVIEW"
    """
    Scheduled periodic review
    """


class AuditResultEnum(str, Enum):
    """
    Possible outcomes of audit activities
    """
    PASS = "PASS"
    """
    Audit passed successfully
    """
    FAIL = "FAIL"
    """
    Audit failed
    """
    CONDITIONAL_PASS = "CONDITIONAL_PASS"
    """
    Passed with conditions
    """
    PENDING = "PENDING"
    """
    Audit pending completion
    """
    REQUIRES_REVIEW = "REQUIRES_REVIEW"
    """
    Requires additional review
    """


class TransferTypeEnum(str, Enum):
    """
    Types of ownership transfers
    """
    SUPPLIER_TO_BANK = "SUPPLIER_TO_BANK"
    """
    Initial purchase by bank from supplier
    """
    BANK_TO_CUSTOMER = "BANK_TO_CUSTOMER"
    """
    Sale from bank to customer
    """
    INTERNAL_TRANSFER = "INTERNAL_TRANSFER"
    """
    Internal ownership change
    """
    RETURN = "RETURN"
    """
    Asset return transaction
    """


class VerificationStatusEnum(str, Enum):
    """
    Status of transfer verification
    """
    VERIFIED = "VERIFIED"
    """
    Transfer verified and confirmed
    """
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    """
    Awaiting verification
    """
    REJECTED = "REJECTED"
    """
    Verification rejected
    """
    UNDER_REVIEW = "UNDER_REVIEW"
    """
    Currently under review
    """


class EvidenceTypeEnum(str, Enum):
    """
    Types of audit evidence documents
    """
    PROFIT_DISCLOSURE = "PROFIT_DISCLOSURE"
    """
    Profit disclosure documentation
    """
    OWNERSHIP_CERTIFICATE = "OWNERSHIP_CERTIFICATE"
    """
    Ownership certificate or deed
    """
    PURCHASE_INVOICE = "PURCHASE_INVOICE"
    """
    Invoice from supplier to bank
    """
    SALE_AGREEMENT = "SALE_AGREEMENT"
    """
    Sale agreement bank to customer
    """
    PAYMENT_TERMS_VERIFICATION = "PAYMENT_TERMS_VERIFICATION"
    """
    Payment terms documentation
    """
    AUDIT_REPORT = "AUDIT_REPORT"
    """
    Formal audit report
    """
    SHARIAH_CERTIFICATE = "SHARIAH_CERTIFICATE"
    """
    Shariah compliance certificate
    """
    CORRESPONDENCE = "CORRESPONDENCE"
    """
    Related correspondence
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


class MurabahaTransaction(ProvenanceFields):
    """
    Islamic financing transaction where bank purchases asset and sells to customer at disclosed markup following Shariah principles
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc:ProductsAndServices/FinancialProductsAndServices/Transaction',
         'from_schema': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier for the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['MurabahaTransaction',
                       'Bank',
                       'Customer',
                       'Asset',
                       'AuditActivity',
                       'OwnershipTransfer',
                       'ComplianceStatus',
                       'AuditEvidence']} })
    transaction_id: str = Field(default=..., description="""Unique identifier for Murabaha transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_id', 'domain_of': ['MurabahaTransaction']} })
    transaction_date: datetime  = Field(default=..., description="""Date when Murabaha transaction was executed""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_date', 'domain_of': ['MurabahaTransaction']} })
    cost_price: float = Field(default=..., description="""Original cost price paid by bank to acquire asset""", json_schema_extra = { "linkml_meta": {'alias': 'cost_price', 'domain_of': ['MurabahaTransaction']} })
    profit_markup: float = Field(default=..., description="""Profit margin added by bank (must be disclosed to customer)""", json_schema_extra = { "linkml_meta": {'alias': 'profit_markup', 'domain_of': ['MurabahaTransaction']} })
    selling_price: float = Field(default=..., description="""Final selling price to customer (cost_price + profit_markup)""", json_schema_extra = { "linkml_meta": {'alias': 'selling_price', 'domain_of': ['MurabahaTransaction']} })
    payment_terms: str = Field(default=..., description="""Payment schedule and terms agreed with customer""", json_schema_extra = { "linkml_meta": {'alias': 'payment_terms', 'domain_of': ['MurabahaTransaction']} })
    shariah_compliant: bool = Field(default=..., description="""Boolean indicating if transaction meets Shariah requirements""", json_schema_extra = { "linkml_meta": {'alias': 'shariah_compliant', 'domain_of': ['MurabahaTransaction']} })
    participates_bank: str = Field(default=..., description="""Reference to bank participating in transaction""", json_schema_extra = { "linkml_meta": {'alias': 'participates_bank', 'domain_of': ['MurabahaTransaction']} })
    participates_customer: str = Field(default=..., description="""Reference to customer participating in transaction""", json_schema_extra = { "linkml_meta": {'alias': 'participates_customer', 'domain_of': ['MurabahaTransaction']} })
    subject_asset: str = Field(default=..., description="""Reference to asset being financed""", json_schema_extra = { "linkml_meta": {'alias': 'subject_asset', 'domain_of': ['MurabahaTransaction']} })
    compliance_status: str = Field(default=..., description="""Current compliance status of transaction""", json_schema_extra = { "linkml_meta": {'alias': 'compliance_status', 'domain_of': ['MurabahaTransaction']} })
    audit_activities: Optional[list[str]] = Field(default=None, description="""List of audit activities performed on transaction""", json_schema_extra = { "linkml_meta": {'alias': 'audit_activities', 'domain_of': ['MurabahaTransaction']} })
    audit_evidences: Optional[list[str]] = Field(default=None, description="""Documentary evidence supporting transaction compliance""", json_schema_extra = { "linkml_meta": {'alias': 'audit_evidences', 'domain_of': ['MurabahaTransaction']} })
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


class Bank(ProvenanceFields):
    """
    Financial institution acting as intermediary purchaser and seller in Murabaha transactions, certified by Shariah board
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc:FunctionalEntities/FinancialServicesEntities/FinancialInstitution',
         'from_schema': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier for the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['MurabahaTransaction',
                       'Bank',
                       'Customer',
                       'Asset',
                       'AuditActivity',
                       'OwnershipTransfer',
                       'ComplianceStatus',
                       'AuditEvidence']} })
    bank_id: str = Field(default=..., description="""Unique identifier for financial institution""", json_schema_extra = { "linkml_meta": {'alias': 'bank_id', 'domain_of': ['Bank']} })
    bank_name: str = Field(default=..., description="""Official name of financial institution""", json_schema_extra = { "linkml_meta": {'alias': 'bank_name', 'domain_of': ['Bank']} })
    shariah_board_certified: bool = Field(default=..., description="""Whether bank is certified by Shariah supervisory board""", json_schema_extra = { "linkml_meta": {'alias': 'shariah_board_certified', 'domain_of': ['Bank']} })
    certification_date: Optional[datetime ] = Field(default=None, description="""Date of Shariah board certification""", json_schema_extra = { "linkml_meta": {'alias': 'certification_date', 'domain_of': ['Bank']} })
    certification_authority: Optional[str] = Field(default=None, description="""Name of certifying Shariah authority""", json_schema_extra = { "linkml_meta": {'alias': 'certification_authority', 'domain_of': ['Bank']} })
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


class Customer(ProvenanceFields):
    """
    Party purchasing asset through Murabaha financing arrangement
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fnd:Parties/Roles/PartyInRole',
         'from_schema': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier for the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['MurabahaTransaction',
                       'Bank',
                       'Customer',
                       'Asset',
                       'AuditActivity',
                       'OwnershipTransfer',
                       'ComplianceStatus',
                       'AuditEvidence']} })
    customer_id: str = Field(default=..., description="""Unique identifier for customer""", json_schema_extra = { "linkml_meta": {'alias': 'customer_id', 'domain_of': ['Customer']} })
    customer_name: str = Field(default=..., description="""Full name of customer""", json_schema_extra = { "linkml_meta": {'alias': 'customer_name', 'domain_of': ['Customer']} })
    customer_type: CustomerTypeEnum = Field(default=..., description="""Type of customer (individual, corporate, institutional)""", json_schema_extra = { "linkml_meta": {'alias': 'customer_type', 'domain_of': ['Customer']} })
    contact_information: Optional[str] = Field(default=None, description="""Customer contact details""", json_schema_extra = { "linkml_meta": {'alias': 'contact_information', 'domain_of': ['Customer']} })
    registration_date: Optional[datetime ] = Field(default=None, description="""Date customer registered with institution""", json_schema_extra = { "linkml_meta": {'alias': 'registration_date', 'domain_of': ['Customer']} })
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


class Asset(ProvenanceFields):
    """
    Physical or financial asset being financed through Murabaha transaction
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc:ProductsAndServices/FinancialProductsAndServices/Asset',
         'from_schema': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier for the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['MurabahaTransaction',
                       'Bank',
                       'Customer',
                       'Asset',
                       'AuditActivity',
                       'OwnershipTransfer',
                       'ComplianceStatus',
                       'AuditEvidence']} })
    asset_id: str = Field(default=..., description="""Unique identifier for asset""", json_schema_extra = { "linkml_meta": {'alias': 'asset_id', 'domain_of': ['Asset']} })
    asset_description: str = Field(default=..., description="""Detailed description of asset""", json_schema_extra = { "linkml_meta": {'alias': 'asset_description', 'domain_of': ['Asset']} })
    asset_type: AssetTypeEnum = Field(default=..., description="""Category or type of asset""", json_schema_extra = { "linkml_meta": {'alias': 'asset_type', 'domain_of': ['Asset']} })
    asset_value: float = Field(default=..., description="""Current market value of asset""", json_schema_extra = { "linkml_meta": {'alias': 'asset_value', 'domain_of': ['Asset']} })
    acquisition_date: Optional[datetime ] = Field(default=None, description="""Date asset was acquired""", json_schema_extra = { "linkml_meta": {'alias': 'acquisition_date', 'domain_of': ['Asset']} })
    ownership_transfers: Optional[list[str]] = Field(default=None, description="""History of ownership transfers for asset""", json_schema_extra = { "linkml_meta": {'alias': 'ownership_transfers', 'domain_of': ['Asset']} })
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


class AuditActivity(ProvenanceFields):
    """
    Compliance audit check performed on Murabaha transaction to verify Shariah adherence and regulatory compliance
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Activity',
         'from_schema': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier for the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['MurabahaTransaction',
                       'Bank',
                       'Customer',
                       'Asset',
                       'AuditActivity',
                       'OwnershipTransfer',
                       'ComplianceStatus',
                       'AuditEvidence']} })
    audit_id: str = Field(default=..., description="""Unique identifier for audit activity""", json_schema_extra = { "linkml_meta": {'alias': 'audit_id', 'domain_of': ['AuditActivity']} })
    audit_type: AuditTypeEnum = Field(default=..., description="""Type of audit performed""", json_schema_extra = { "linkml_meta": {'alias': 'audit_type', 'domain_of': ['AuditActivity']} })
    audit_date: datetime  = Field(default=..., description="""Date audit was conducted""", json_schema_extra = { "linkml_meta": {'alias': 'audit_date', 'domain_of': ['AuditActivity']} })
    auditor_name: str = Field(default=..., description="""Name of auditor who performed the audit""", json_schema_extra = { "linkml_meta": {'alias': 'auditor_name', 'domain_of': ['AuditActivity']} })
    audit_result: AuditResultEnum = Field(default=..., description="""Outcome of audit activity""", json_schema_extra = { "linkml_meta": {'alias': 'audit_result', 'domain_of': ['AuditActivity']} })
    audit_scope: Optional[str] = Field(default=None, description="""Scope and boundaries of audit""", json_schema_extra = { "linkml_meta": {'alias': 'audit_scope', 'domain_of': ['AuditActivity']} })
    findings: Optional[str] = Field(default=None, description="""Key findings from audit""", json_schema_extra = { "linkml_meta": {'alias': 'findings', 'domain_of': ['AuditActivity']} })
    recommendations: Optional[str] = Field(default=None, description="""Auditor recommendations for improvement""", json_schema_extra = { "linkml_meta": {'alias': 'recommendations', 'domain_of': ['AuditActivity']} })
    generated_evidences: Optional[list[str]] = Field(default=None, description="""Evidence documents generated by audit""", json_schema_extra = { "linkml_meta": {'alias': 'generated_evidences', 'domain_of': ['AuditActivity']} })
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


class OwnershipTransfer(ProvenanceFields):
    """
    Event recording change of asset ownership between supplier, bank, and customer in Murabaha transaction chain
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Activity',
         'from_schema': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier for the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['MurabahaTransaction',
                       'Bank',
                       'Customer',
                       'Asset',
                       'AuditActivity',
                       'OwnershipTransfer',
                       'ComplianceStatus',
                       'AuditEvidence']} })
    transfer_id: str = Field(default=..., description="""Unique identifier for ownership transfer""", json_schema_extra = { "linkml_meta": {'alias': 'transfer_id', 'domain_of': ['OwnershipTransfer']} })
    transfer_date: datetime  = Field(default=..., description="""Date ownership was transferred""", json_schema_extra = { "linkml_meta": {'alias': 'transfer_date', 'domain_of': ['OwnershipTransfer']} })
    from_party: str = Field(default=..., description="""Party transferring ownership (seller)""", json_schema_extra = { "linkml_meta": {'alias': 'from_party', 'domain_of': ['OwnershipTransfer']} })
    to_party: str = Field(default=..., description="""Party receiving ownership (buyer)""", json_schema_extra = { "linkml_meta": {'alias': 'to_party', 'domain_of': ['OwnershipTransfer']} })
    transfer_evidence: str = Field(default=..., description="""Documentary evidence of ownership transfer""", json_schema_extra = { "linkml_meta": {'alias': 'transfer_evidence', 'domain_of': ['OwnershipTransfer']} })
    transfer_type: Optional[TransferTypeEnum] = Field(default=None, description="""Type of ownership transfer""", json_schema_extra = { "linkml_meta": {'alias': 'transfer_type', 'domain_of': ['OwnershipTransfer']} })
    legal_documentation: Optional[str] = Field(default=None, description="""Legal documents supporting transfer""", json_schema_extra = { "linkml_meta": {'alias': 'legal_documentation', 'domain_of': ['OwnershipTransfer']} })
    verification_status: Optional[VerificationStatusEnum] = Field(default=None, description="""Status of transfer verification""", json_schema_extra = { "linkml_meta": {'alias': 'verification_status', 'domain_of': ['OwnershipTransfer']} })
    transferred_asset: Optional[str] = Field(default=None, description="""Asset being transferred""", json_schema_extra = { "linkml_meta": {'alias': 'transferred_asset', 'domain_of': ['OwnershipTransfer']} })
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


class ComplianceStatus(ProvenanceFields):
    """
    Classification of Shariah compliance state for Murabaha transaction with reasons for non-compliance if applicable
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'skos:Concept',
         'from_schema': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier for the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['MurabahaTransaction',
                       'Bank',
                       'Customer',
                       'Asset',
                       'AuditActivity',
                       'OwnershipTransfer',
                       'ComplianceStatus',
                       'AuditEvidence']} })
    status_code: str = Field(default=..., description="""Code representing compliance status""", json_schema_extra = { "linkml_meta": {'alias': 'status_code', 'domain_of': ['ComplianceStatus']} })
    status_label: str = Field(default=..., description="""Human-readable label for status""", json_schema_extra = { "linkml_meta": {'alias': 'status_label', 'domain_of': ['ComplianceStatus']} })
    status_description: str = Field(default=..., description="""Detailed description of compliance status""", json_schema_extra = { "linkml_meta": {'alias': 'status_description', 'domain_of': ['ComplianceStatus']} })
    non_compliance_reasons: Optional[list[str]] = Field(default=None, description="""Reasons for non-compliance if applicable""", json_schema_extra = { "linkml_meta": {'alias': 'non_compliance_reasons', 'domain_of': ['ComplianceStatus']} })
    determination_date: Optional[datetime ] = Field(default=None, description="""Date compliance status was determined""", json_schema_extra = { "linkml_meta": {'alias': 'determination_date', 'domain_of': ['ComplianceStatus']} })
    determined_by: Optional[str] = Field(default=None, description="""Person or system that determined status""", json_schema_extra = { "linkml_meta": {'alias': 'determined_by', 'domain_of': ['ComplianceStatus']} })
    review_date: Optional[datetime ] = Field(default=None, description="""Date for next compliance review""", json_schema_extra = { "linkml_meta": {'alias': 'review_date', 'domain_of': ['ComplianceStatus']} })
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


class AuditEvidence(ProvenanceFields):
    """
    Documentary evidence supporting compliance verification and audit findings for Murabaha transactions
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Entity',
         'from_schema': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier for the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['MurabahaTransaction',
                       'Bank',
                       'Customer',
                       'Asset',
                       'AuditActivity',
                       'OwnershipTransfer',
                       'ComplianceStatus',
                       'AuditEvidence']} })
    evidence_id: str = Field(default=..., description="""Unique identifier for audit evidence""", json_schema_extra = { "linkml_meta": {'alias': 'evidence_id', 'domain_of': ['AuditEvidence']} })
    evidence_type: EvidenceTypeEnum = Field(default=..., description="""Type of evidence document""", json_schema_extra = { "linkml_meta": {'alias': 'evidence_type', 'domain_of': ['AuditEvidence']} })
    evidence_date: datetime  = Field(default=..., description="""Date evidence was created or collected""", json_schema_extra = { "linkml_meta": {'alias': 'evidence_date', 'domain_of': ['AuditEvidence']} })
    document_reference: str = Field(default=..., description="""Reference number or location of document""", json_schema_extra = { "linkml_meta": {'alias': 'document_reference', 'domain_of': ['AuditEvidence']} })
    verified_by: str = Field(default=..., description="""Person who verified the evidence""", json_schema_extra = { "linkml_meta": {'alias': 'verified_by', 'domain_of': ['AuditEvidence']} })
    verification_date: Optional[datetime ] = Field(default=None, description="""Date evidence was verified""", json_schema_extra = { "linkml_meta": {'alias': 'verification_date', 'domain_of': ['AuditEvidence']} })
    evidence_description: Optional[str] = Field(default=None, description="""Description of evidence content""", json_schema_extra = { "linkml_meta": {'alias': 'evidence_description', 'domain_of': ['AuditEvidence']} })
    storage_location: Optional[str] = Field(default=None, description="""Physical or digital storage location""", json_schema_extra = { "linkml_meta": {'alias': 'storage_location', 'domain_of': ['AuditEvidence']} })
    retention_period: Optional[str] = Field(default=None, description="""Period evidence must be retained""", json_schema_extra = { "linkml_meta": {'alias': 'retention_period', 'domain_of': ['AuditEvidence']} })
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
MurabahaTransaction.model_rebuild()
Bank.model_rebuild()
Customer.model_rebuild()
Asset.model_rebuild()
AuditActivity.model_rebuild()
OwnershipTransfer.model_rebuild()
ComplianceStatus.model_rebuild()
AuditEvidence.model_rebuild()

