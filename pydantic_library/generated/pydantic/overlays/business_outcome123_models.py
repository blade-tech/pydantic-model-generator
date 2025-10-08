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
     'description': 'Structured data model for auditing Murabaha transactions to '
                    'ensure Shariah compliance.\n'
                    'Tracks ownership transfer, profit disclosure, payment terms, '
                    'and maintains comprehensive\n'
                    'audit trails for Islamic finance compliance verification.\n',
     'id': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
     'imports': ['../core/provenance'],
     'name': 'murabaha_shariah_compliance_audit',
     'prefixes': {'doco': {'prefix_prefix': 'doco',
                           'prefix_reference': 'http://purl.org/spar/doco/'},
                  'fabio': {'prefix_prefix': 'fabio',
                            'prefix_reference': 'http://purl.org/spar/fabio/'},
                  'fibo-acc': {'prefix_prefix': 'fibo-acc',
                               'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FND/Accounting/AccountingEquity/'},
                  'fibo-debt': {'prefix_prefix': 'fibo-debt',
                                'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FBC/DebtAndEquities/Debt/'},
                  'fibo-fse': {'prefix_prefix': 'fibo-fse',
                               'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FBC/FunctionalEntities/FinancialServicesEntities/'},
                  'fibo-own': {'prefix_prefix': 'fibo-own',
                               'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FND/OwnershipAndControl/Ownership/'},
                  'fibo-parties': {'prefix_prefix': 'fibo-parties',
                                   'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FND/Parties/Roles/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'}},
     'source_file': 'D:\\projects\\Pydantic Model '
                    'Generator\\pydantic_library\\schemas\\overlays\\business_outcome123_overlay.yaml'} )

class ComplianceStatusEnum(str, Enum):
    """
    Possible Shariah compliance statuses
    """
    compliant = "compliant"
    """
    Transaction meets all Shariah requirements
    """
    non_compliant = "non_compliant"
    """
    Transaction violates Shariah principles
    """
    pending_review = "pending_review"
    """
    Compliance review in progress
    """
    conditional = "conditional"
    """
    Compliant with conditions
    """
    failed = "failed"
    """
    Failed compliance checks
    """
    rejected = "rejected"
    """
    Rejected by Shariah board
    """


class CustomerTypeEnum(str, Enum):
    """
    Types of customers
    """
    individual = "individual"
    """
    Individual retail customer
    """
    corporate = "corporate"
    """
    Corporate entity
    """
    institutional = "institutional"
    """
    Institutional investor
    """
    government = "government"
    """
    Government entity
    """
    sme = "sme"
    """
    Small and medium enterprise
    """


class AssetTypeEnum(str, Enum):
    """
    Types of assets in Murabaha transactions
    """
    real_estate = "real_estate"
    """
    Real property
    """
    vehicle = "vehicle"
    """
    Automobiles and transport
    """
    equipment = "equipment"
    """
    Machinery and equipment
    """
    commodity = "commodity"
    """
    Tradable commodities
    """
    inventory = "inventory"
    """
    Business inventory
    """
    financial_instrument = "financial_instrument"
    """
    Financial securities
    """


class TransferTypeEnum(str, Enum):
    """
    Types of ownership transfers
    """
    acquisition = "acquisition"
    """
    Bank acquiring asset
    """
    sale = "sale"
    """
    Bank selling to customer
    """
    return = "return"
    """
    Asset returned to bank
    """
    collateral = "collateral"
    """
    Transfer for collateral purposes
    """


class ActivityTypeEnum(str, Enum):
    """
    Types of audit activities
    """
    ownership_verification = "ownership_verification"
    """
    Verify bank ownership before sale
    """
    profit_disclosure_check = "profit_disclosure_check"
    """
    Check profit transparency
    """
    payment_terms_review = "payment_terms_review"
    """
    Review payment terms compliance
    """
    documentation_review = "documentation_review"
    """
    Review supporting documents
    """
    final_assessment = "final_assessment"
    """
    Final compliance assessment
    """


class ResultStatusEnum(str, Enum):
    """
    Results of audit checks
    """
    passed = "passed"
    """
    Check passed successfully
    """
    failed = "failed"
    """
    Check failed
    """
    warning = "warning"
    """
    Check passed with warnings
    """
    not_applicable = "not_applicable"
    """
    Check not applicable
    """
    requires_followup = "requires_followup"
    """
    Requires additional review
    """


class EvidenceTypeEnum(str, Enum):
    """
    Types of compliance evidence
    """
    ownership_deed = "ownership_deed"
    """
    Proof of ownership document
    """
    purchase_invoice = "purchase_invoice"
    """
    Invoice for asset purchase
    """
    sale_agreement = "sale_agreement"
    """
    Sale agreement with customer
    """
    profit_disclosure = "profit_disclosure"
    """
    Profit disclosure statement
    """
    pricing_agreement = "pricing_agreement"
    """
    Pricing terms document
    """
    payment_schedule = "payment_schedule"
    """
    Payment schedule document
    """
    shariah_certificate = "shariah_certificate"
    """
    Shariah board certification
    """
    audit_report = "audit_report"
    """
    Audit report document
    """


class VerificationStatusEnum(str, Enum):
    """
    Verification status of evidence
    """
    verified = "verified"
    """
    Evidence verified and accepted
    """
    unverified = "unverified"
    """
    Evidence not yet verified
    """
    rejected = "rejected"
    """
    Evidence rejected
    """
    pending = "pending"
    """
    Verification pending
    """
    expired = "expired"
    """
    Evidence expired
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
    Islamic finance transaction where bank purchases asset and resells to customer
    at cost plus disclosed profit markup with deferred payment terms.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-debt:DebtInstrument',
         'from_schema': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['MurabahaTransaction',
                       'Bank',
                       'Customer',
                       'Asset',
                       'OwnershipTransfer',
                       'AuditActivity',
                       'ComplianceEvidence',
                       'AuditTrail']} })
    transaction_id: str = Field(default=..., description="""Unique identifier for Murabaha transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_id', 'domain_of': ['MurabahaTransaction']} })
    transaction_date: datetime  = Field(default=..., description="""Date when transaction was executed""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_date', 'domain_of': ['MurabahaTransaction']} })
    cost_price: float = Field(default=..., description="""Original cost price paid by bank for asset""", json_schema_extra = { "linkml_meta": {'alias': 'cost_price', 'domain_of': ['MurabahaTransaction']} })
    profit_markup: float = Field(default=..., description="""Profit amount added to cost price""", json_schema_extra = { "linkml_meta": {'alias': 'profit_markup', 'domain_of': ['MurabahaTransaction']} })
    selling_price: float = Field(default=..., description="""Total price charged to customer (cost + profit)""", json_schema_extra = { "linkml_meta": {'alias': 'selling_price', 'domain_of': ['MurabahaTransaction']} })
    payment_terms: str = Field(default=..., description="""Terms and schedule for customer payment""", json_schema_extra = { "linkml_meta": {'alias': 'payment_terms', 'domain_of': ['MurabahaTransaction']} })
    compliance_status: ComplianceStatusEnum = Field(default=..., description="""Overall Shariah compliance status of transaction""", json_schema_extra = { "linkml_meta": {'alias': 'compliance_status', 'domain_of': ['MurabahaTransaction']} })
    involves_bank: str = Field(default=..., description="""Reference to bank entity in transaction""", json_schema_extra = { "linkml_meta": {'alias': 'involves_bank', 'domain_of': ['MurabahaTransaction']} })
    involves_customer: str = Field(default=..., description="""Reference to customer entity in transaction""", json_schema_extra = { "linkml_meta": {'alias': 'involves_customer', 'domain_of': ['MurabahaTransaction']} })
    involves_asset: str = Field(default=..., description="""Reference to asset entity in transaction""", json_schema_extra = { "linkml_meta": {'alias': 'involves_asset', 'domain_of': ['MurabahaTransaction']} })
    has_audit_trail: Optional[str] = Field(default=None, description="""Reference to audit trail for transaction""", json_schema_extra = { "linkml_meta": {'alias': 'has_audit_trail', 'domain_of': ['MurabahaTransaction']} })
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
    Financial institution acting as seller in Murabaha transaction
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fse:Bank',
         'from_schema': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['MurabahaTransaction',
                       'Bank',
                       'Customer',
                       'Asset',
                       'OwnershipTransfer',
                       'AuditActivity',
                       'ComplianceEvidence',
                       'AuditTrail']} })
    bank_id: str = Field(default=..., description="""Unique identifier for bank""", json_schema_extra = { "linkml_meta": {'alias': 'bank_id', 'domain_of': ['Bank']} })
    bank_name: str = Field(default=..., description="""Official name of financial institution""", json_schema_extra = { "linkml_meta": {'alias': 'bank_name', 'domain_of': ['Bank']} })
    shariah_board_certified: bool = Field(default=..., description="""Whether bank has Shariah board certification""", json_schema_extra = { "linkml_meta": {'alias': 'shariah_board_certified', 'domain_of': ['Bank']} })
    sells_in_transaction: Optional[list[str]] = Field(default=None, description="""Transactions where bank is seller""", json_schema_extra = { "linkml_meta": {'alias': 'sells_in_transaction', 'domain_of': ['Bank']} })
    owns_asset: Optional[list[str]] = Field(default=None, description="""Assets owned by bank""", json_schema_extra = { "linkml_meta": {'alias': 'owns_asset', 'domain_of': ['Bank']} })
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
    Party purchasing asset from bank under Murabaha terms
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-parties:Customer',
         'from_schema': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['MurabahaTransaction',
                       'Bank',
                       'Customer',
                       'Asset',
                       'OwnershipTransfer',
                       'AuditActivity',
                       'ComplianceEvidence',
                       'AuditTrail']} })
    customer_id: str = Field(default=..., description="""Unique identifier for customer""", json_schema_extra = { "linkml_meta": {'alias': 'customer_id', 'domain_of': ['Customer']} })
    customer_name: str = Field(default=..., description="""Full name of customer""", json_schema_extra = { "linkml_meta": {'alias': 'customer_name', 'domain_of': ['Customer']} })
    customer_type: CustomerTypeEnum = Field(default=..., description="""Type of customer (individual, corporate, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'customer_type', 'domain_of': ['Customer']} })
    purchases_in_transaction: Optional[list[str]] = Field(default=None, description="""Transactions where customer is purchaser""", json_schema_extra = { "linkml_meta": {'alias': 'purchases_in_transaction', 'domain_of': ['Customer']} })
    receives_asset: Optional[list[str]] = Field(default=None, description="""Assets received by customer""", json_schema_extra = { "linkml_meta": {'alias': 'receives_asset', 'domain_of': ['Customer']} })
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
    Physical or financial asset being sold in Murabaha transaction
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-acc:Asset',
         'from_schema': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['MurabahaTransaction',
                       'Bank',
                       'Customer',
                       'Asset',
                       'OwnershipTransfer',
                       'AuditActivity',
                       'ComplianceEvidence',
                       'AuditTrail']} })
    asset_id: str = Field(default=..., description="""Unique identifier for asset""", json_schema_extra = { "linkml_meta": {'alias': 'asset_id', 'domain_of': ['Asset']} })
    asset_type: AssetTypeEnum = Field(default=..., description="""Category or type of asset""", json_schema_extra = { "linkml_meta": {'alias': 'asset_type', 'domain_of': ['Asset']} })
    asset_description: str = Field(default=..., description="""Detailed description of asset""", json_schema_extra = { "linkml_meta": {'alias': 'asset_description', 'domain_of': ['Asset']} })
    valuation: float = Field(default=..., description="""Current valuation of asset""", json_schema_extra = { "linkml_meta": {'alias': 'valuation', 'domain_of': ['Asset']} })
    subject_of_transaction: Optional[list[str]] = Field(default=None, description="""Transactions involving this asset""", json_schema_extra = { "linkml_meta": {'alias': 'subject_of_transaction', 'domain_of': ['Asset']} })
    has_ownership_transfer: Optional[list[str]] = Field(default=None, description="""Ownership transfers for this asset""", json_schema_extra = { "linkml_meta": {'alias': 'has_ownership_transfer', 'domain_of': ['Asset']} })
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
    Event recording transfer of asset ownership between parties
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-own:OwnershipPartyInRole',
         'from_schema': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['MurabahaTransaction',
                       'Bank',
                       'Customer',
                       'Asset',
                       'OwnershipTransfer',
                       'AuditActivity',
                       'ComplianceEvidence',
                       'AuditTrail']} })
    transfer_id: str = Field(default=..., description="""Unique identifier for ownership transfer""", json_schema_extra = { "linkml_meta": {'alias': 'transfer_id', 'domain_of': ['OwnershipTransfer']} })
    transfer_date: datetime  = Field(default=..., description="""Date ownership transfer occurred""", json_schema_extra = { "linkml_meta": {'alias': 'transfer_date', 'domain_of': ['OwnershipTransfer']} })
    transfer_type: TransferTypeEnum = Field(default=..., description="""Type of ownership transfer""", json_schema_extra = { "linkml_meta": {'alias': 'transfer_type', 'domain_of': ['OwnershipTransfer']} })
    from_party: str = Field(default=..., description="""Party transferring ownership""", json_schema_extra = { "linkml_meta": {'alias': 'from_party', 'domain_of': ['OwnershipTransfer']} })
    to_party: str = Field(default=..., description="""Party receiving ownership""", json_schema_extra = { "linkml_meta": {'alias': 'to_party', 'domain_of': ['OwnershipTransfer']} })
    evidence_document: str = Field(default=..., description="""Reference to supporting documentation""", json_schema_extra = { "linkml_meta": {'alias': 'evidence_document', 'domain_of': ['OwnershipTransfer']} })
    transfers_asset: str = Field(default=..., description="""Asset being transferred""", json_schema_extra = { "linkml_meta": {'alias': 'transfers_asset', 'domain_of': ['OwnershipTransfer']} })
    part_of_transaction: Optional[str] = Field(default=None, description="""Transaction this transfer is part of""", json_schema_extra = { "linkml_meta": {'alias': 'part_of_transaction', 'domain_of': ['OwnershipTransfer']} })
    verified_by_audit: Optional[str] = Field(default=None, description="""Audit activity that verified this transfer""", json_schema_extra = { "linkml_meta": {'alias': 'verified_by_audit', 'domain_of': ['OwnershipTransfer']} })
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
    Compliance verification activity performed by auditor
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Activity',
         'from_schema': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['MurabahaTransaction',
                       'Bank',
                       'Customer',
                       'Asset',
                       'OwnershipTransfer',
                       'AuditActivity',
                       'ComplianceEvidence',
                       'AuditTrail']} })
    activity_id: str = Field(default=..., description="""Unique identifier for audit activity""", json_schema_extra = { "linkml_meta": {'alias': 'activity_id', 'domain_of': ['AuditActivity']} })
    activity_type: ActivityTypeEnum = Field(default=..., description="""Type of audit activity performed""", json_schema_extra = { "linkml_meta": {'alias': 'activity_type', 'domain_of': ['AuditActivity']} })
    auditor_name: str = Field(default=..., description="""Name of auditor performing activity""", json_schema_extra = { "linkml_meta": {'alias': 'auditor_name', 'domain_of': ['AuditActivity']} })
    audit_date: datetime  = Field(default=..., description="""Date audit activity was performed""", json_schema_extra = { "linkml_meta": {'alias': 'audit_date', 'domain_of': ['AuditActivity']} })
    check_performed: str = Field(default=..., description="""Description of compliance check performed""", json_schema_extra = { "linkml_meta": {'alias': 'check_performed', 'domain_of': ['AuditActivity']} })
    result_status: ResultStatusEnum = Field(default=..., description="""Result of audit check""", json_schema_extra = { "linkml_meta": {'alias': 'result_status', 'domain_of': ['AuditActivity']} })
    audits_transaction: str = Field(default=..., description="""Transaction being audited""", json_schema_extra = { "linkml_meta": {'alias': 'audits_transaction', 'domain_of': ['AuditActivity']} })
    generates_evidence: Optional[list[str]] = Field(default=None, description="""Evidence generated by this activity""", json_schema_extra = { "linkml_meta": {'alias': 'generates_evidence', 'domain_of': ['AuditActivity']} })
    part_of_audit_trail: Optional[str] = Field(default=None, description="""Audit trail this activity belongs to""", json_schema_extra = { "linkml_meta": {'alias': 'part_of_audit_trail', 'domain_of': ['AuditActivity']} })
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


class ComplianceEvidence(ProvenanceFields):
    """
    Documentation and proof supporting compliance verification
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Entity',
         'from_schema': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['MurabahaTransaction',
                       'Bank',
                       'Customer',
                       'Asset',
                       'OwnershipTransfer',
                       'AuditActivity',
                       'ComplianceEvidence',
                       'AuditTrail']} })
    evidence_id: str = Field(default=..., description="""Unique identifier for compliance evidence""", json_schema_extra = { "linkml_meta": {'alias': 'evidence_id', 'domain_of': ['ComplianceEvidence']} })
    evidence_type: EvidenceTypeEnum = Field(default=..., description="""Type of compliance evidence""", json_schema_extra = { "linkml_meta": {'alias': 'evidence_type', 'domain_of': ['ComplianceEvidence']} })
    document_reference: str = Field(default=..., description="""Reference to source document""", json_schema_extra = { "linkml_meta": {'alias': 'document_reference', 'domain_of': ['ComplianceEvidence']} })
    verification_status: VerificationStatusEnum = Field(default=..., description="""Verification status of evidence""", json_schema_extra = { "linkml_meta": {'alias': 'verification_status', 'domain_of': ['ComplianceEvidence']} })
    timestamp: datetime  = Field(default=..., description="""Timestamp when evidence was collected""", json_schema_extra = { "linkml_meta": {'alias': 'timestamp', 'domain_of': ['ComplianceEvidence']} })
    supports_transaction: Optional[str] = Field(default=None, description="""Transaction this evidence supports""", json_schema_extra = { "linkml_meta": {'alias': 'supports_transaction', 'domain_of': ['ComplianceEvidence']} })
    generated_by_activity: Optional[str] = Field(default=None, description="""Audit activity that generated evidence""", json_schema_extra = { "linkml_meta": {'alias': 'generated_by_activity', 'domain_of': ['ComplianceEvidence']} })
    included_in_trail: Optional[str] = Field(default=None, description="""Audit trail containing this evidence""", json_schema_extra = { "linkml_meta": {'alias': 'included_in_trail', 'domain_of': ['ComplianceEvidence']} })
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
    Complete collection of audit activities and evidence for a transaction
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Bundle',
         'from_schema': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields']})

    id: str = Field(default=..., description="""Unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['MurabahaTransaction',
                       'Bank',
                       'Customer',
                       'Asset',
                       'OwnershipTransfer',
                       'AuditActivity',
                       'ComplianceEvidence',
                       'AuditTrail']} })
    trail_id: str = Field(default=..., description="""Unique identifier for audit trail""", json_schema_extra = { "linkml_meta": {'alias': 'trail_id', 'domain_of': ['AuditTrail']} })
    transaction_reference: str = Field(default=..., description="""Reference to transaction being audited""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_reference', 'domain_of': ['AuditTrail']} })
    created_date: datetime  = Field(default=..., description="""Date audit trail was created""", json_schema_extra = { "linkml_meta": {'alias': 'created_date', 'domain_of': ['AuditTrail']} })
    final_compliance_status: ComplianceStatusEnum = Field(default=..., description="""Final compliance determination""", json_schema_extra = { "linkml_meta": {'alias': 'final_compliance_status', 'domain_of': ['AuditTrail']} })
    auditor_signature: str = Field(default=..., description="""Digital signature of auditor""", json_schema_extra = { "linkml_meta": {'alias': 'auditor_signature', 'domain_of': ['AuditTrail']} })
    documents_transaction: str = Field(default=..., description="""Transaction documented by this trail""", json_schema_extra = { "linkml_meta": {'alias': 'documents_transaction', 'domain_of': ['AuditTrail']} })
    contains_activities: Optional[list[str]] = Field(default=None, description="""Audit activities in this trail""", json_schema_extra = { "linkml_meta": {'alias': 'contains_activities', 'domain_of': ['AuditTrail']} })
    contains_evidence: Optional[list[str]] = Field(default=None, description="""Evidence items in this trail""", json_schema_extra = { "linkml_meta": {'alias': 'contains_evidence', 'domain_of': ['AuditTrail']} })
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
OwnershipTransfer.model_rebuild()
AuditActivity.model_rebuild()
ComplianceEvidence.model_rebuild()
AuditTrail.model_rebuild()

