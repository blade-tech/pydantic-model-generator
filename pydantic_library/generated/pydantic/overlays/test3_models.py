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


linkml_meta = LinkMLMeta({'default_prefix': 'murabaha',
     'description': 'Audit framework for Murabaha (Islamic cost-plus financing) '
                    'transactions ensuring \n'
                    'Shariah compliance through verification of asset ownership, '
                    'profit transparency, \n'
                    'payment terms adherence, and comprehensive audit trail '
                    'maintenance.\n',
     'id': 'https://spec.edmcouncil.org/outcomes/murabaha-shariah-compliance-audit',
     'imports': ['../core/provenance'],
     'name': 'murabaha_shariah_compliance_audit',
     'prefixes': {'fibo-fbc-fse': {'prefix_prefix': 'fibo-fbc-fse',
                                   'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FBC/FunctionalEntities/FinancialServicesEntities/'},
                  'fibo-fbc-pas': {'prefix_prefix': 'fibo-fbc-pas',
                                   'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FBC/ProductsAndServices/FinancialProductsAndServices/'},
                  'fibo-fnd-pty': {'prefix_prefix': 'fibo-fnd-pty',
                                   'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FND/Parties/Roles/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'murabaha': {'prefix_prefix': 'murabaha',
                               'prefix_reference': 'https://spec.edmcouncil.org/outcomes/murabaha-shariah-compliance-audit/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'}},
     'source_file': '..\\..\\pydantic_library\\schemas\\overlays\\test3_overlay.yaml'} )

class ComplianceStatusEnum(str, Enum):
    """
    Enumeration of possible compliance status values
    """
    COMPLIANT = "COMPLIANT"
    """
    Transaction meets all Shariah compliance requirements
    """
    NON_COMPLIANT = "NON_COMPLIANT"
    """
    Transaction fails Shariah compliance requirements
    """
    APPROVED = "APPROVED"
    """
    Transaction approved by Shariah board
    """
    REJECTED = "REJECTED"
    """
    Transaction rejected by Shariah board
    """
    REQUIRES_REVIEW = "REQUIRES_REVIEW"
    """
    Transaction requires additional review
    """
    PENDING = "PENDING"
    """
    Compliance assessment pending
    """
    REMEDIATED = "REMEDIATED"
    """
    Previously non-compliant transaction has been corrected
    """


class EvidenceTypeEnum(str, Enum):
    """
    Types of audit evidence
    """
    PROFIT_DISCLOSURE = "PROFIT_DISCLOSURE"
    """
    Evidence of profit markup disclosure to customer
    """
    OWNERSHIP_PROOF = "OWNERSHIP_PROOF"
    """
    Proof of asset ownership by bank
    """
    PAYMENT_TERMS_REVIEW = "PAYMENT_TERMS_REVIEW"
    """
    Review of payment terms for Shariah compliance
    """
    ASSET_VALUATION = "ASSET_VALUATION"
    """
    Independent asset valuation documentation
    """
    CUSTOMER_ACKNOWLEDGMENT = "CUSTOMER_ACKNOWLEDGMENT"
    """
    Customer acknowledgment of terms
    """
    SHARIAH_BOARD_APPROVAL = "SHARIAH_BOARD_APPROVAL"
    """
    Shariah supervisory board approval
    """
    TRANSFER_DOCUMENTATION = "TRANSFER_DOCUMENTATION"
    """
    Documentation of ownership transfer
    """


class TransferTypeEnum(str, Enum):
    """
    Types of ownership transfers
    """
    PURCHASE = "PURCHASE"
    """
    Bank purchasing asset from original seller
    """
    SALE = "SALE"
    """
    Bank selling asset to customer
    """
    INITIAL_ACQUISITION = "INITIAL_ACQUISITION"
    """
    Initial acquisition by original seller
    """
    RETURN = "RETURN"
    """
    Asset returned due to defect or non-compliance
    """


class AuditStageEnum(str, Enum):
    """
    Stages in the audit process
    """
    INITIATED = "INITIATED"
    """
    Audit trail initiated
    """
    EVIDENCE_COLLECTION = "EVIDENCE_COLLECTION"
    """
    Collecting audit evidence
    """
    OWNERSHIP_VERIFICATION = "OWNERSHIP_VERIFICATION"
    """
    Verifying ownership chain
    """
    PRICING_REVIEW = "PRICING_REVIEW"
    """
    Reviewing profit disclosure and pricing
    """
    TERMS_ANALYSIS = "TERMS_ANALYSIS"
    """
    Analyzing payment terms for compliance
    """
    FINAL_ASSESSMENT = "FINAL_ASSESSMENT"
    """
    Final compliance assessment
    """
    COMPLETED = "COMPLETED"
    """
    Audit completed
    """
    REMEDIATION = "REMEDIATION"
    """
    Addressing non-compliance issues
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
    Islamic financing transaction where bank purchases asset and sells to customer 
    at cost plus disclosed profit markup with deferred payment terms.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc-pas:Transaction',
         'from_schema': 'https://spec.edmcouncil.org/outcomes/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'cost_price': {'name': 'cost_price', 'required': True},
                        'payment_terms': {'name': 'payment_terms', 'required': True},
                        'profit_markup': {'name': 'profit_markup', 'required': True},
                        'selling_price': {'name': 'selling_price', 'required': True},
                        'transaction_date': {'name': 'transaction_date',
                                             'required': True},
                        'transaction_id': {'identifier': True,
                                           'name': 'transaction_id',
                                           'required': True}}})

    transaction_id: str = Field(default=..., description="""Unique identifier for the Murabaha transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_id',
         'domain_of': ['MurabahaTransaction'],
         'slot_uri': 'fibo-fbc-pas:hasTransactionIdentifier'} })
    transaction_date: datetime  = Field(default=..., description="""Date when the transaction was executed""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_date',
         'domain_of': ['MurabahaTransaction'],
         'slot_uri': 'fibo-fbc-pas:hasTransactionDate'} })
    cost_price: Decimal = Field(default=..., description="""Original cost price of the asset to the bank""", json_schema_extra = { "linkml_meta": {'alias': 'cost_price',
         'domain_of': ['MurabahaTransaction'],
         'slot_uri': 'murabaha:hasCostPrice'} })
    profit_markup: Decimal = Field(default=..., description="""Profit markup amount added to cost price""", json_schema_extra = { "linkml_meta": {'alias': 'profit_markup',
         'domain_of': ['MurabahaTransaction'],
         'slot_uri': 'murabaha:hasProfitMarkup'} })
    selling_price: Decimal = Field(default=..., description="""Total selling price (cost + profit markup)""", json_schema_extra = { "linkml_meta": {'alias': 'selling_price',
         'domain_of': ['MurabahaTransaction'],
         'slot_uri': 'murabaha:hasSellingPrice'} })
    payment_terms: str = Field(default=..., description="""Terms and conditions for payment including schedule""", json_schema_extra = { "linkml_meta": {'alias': 'payment_terms',
         'domain_of': ['MurabahaTransaction'],
         'slot_uri': 'murabaha:hasPaymentTerms'} })
    involves_bank: Optional[str] = Field(default=None, description="""Bank participating in the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'involves_bank',
         'domain_of': ['MurabahaTransaction'],
         'slot_uri': 'murabaha:involvesBank'} })
    involves_customer: Optional[str] = Field(default=None, description="""Customer participating in the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'involves_customer',
         'domain_of': ['MurabahaTransaction'],
         'slot_uri': 'murabaha:involvesCustomer'} })
    involves_asset: Optional[str] = Field(default=None, description="""Asset being transacted""", json_schema_extra = { "linkml_meta": {'alias': 'involves_asset',
         'domain_of': ['MurabahaTransaction'],
         'slot_uri': 'murabaha:involvesAsset'} })
    has_audit_trail: Optional[str] = Field(default=None, description="""Audit trail tracking this transaction""", json_schema_extra = { "linkml_meta": {'alias': 'has_audit_trail',
         'domain_of': ['MurabahaTransaction'],
         'slot_uri': 'murabaha:hasAuditTrail'} })
    has_compliance_status: Optional[str] = Field(default=None, description="""Compliance status of the transaction""", json_schema_extra = { "linkml_meta": {'alias': 'has_compliance_status',
         'domain_of': ['MurabahaTransaction'],
         'slot_uri': 'murabaha:hasComplianceStatus'} })
    has_evidence: Optional[list[str]] = Field(default=None, description="""Evidence supporting transaction compliance""", json_schema_extra = { "linkml_meta": {'alias': 'has_evidence',
         'domain_of': ['MurabahaTransaction'],
         'slot_uri': 'murabaha:hasEvidence'} })
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
    Financial institution acting as intermediary purchaser and seller in Murabaha

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc-fse:FinancialInstitution',
         'from_schema': 'https://spec.edmcouncil.org/outcomes/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'institution_id': {'identifier': True,
                                           'name': 'institution_id',
                                           'required': True},
                        'institution_name': {'name': 'institution_name',
                                             'required': True},
                        'shariah_board_certified': {'name': 'shariah_board_certified',
                                                    'required': True}}})

    institution_id: str = Field(default=..., description="""Unique identifier for the financial institution""", json_schema_extra = { "linkml_meta": {'alias': 'institution_id',
         'domain_of': ['Bank'],
         'slot_uri': 'fibo-fbc-fse:hasInstitutionIdentifier'} })
    institution_name: str = Field(default=..., description="""Legal name of the financial institution""", json_schema_extra = { "linkml_meta": {'alias': 'institution_name',
         'domain_of': ['Bank'],
         'slot_uri': 'fibo-fbc-fse:hasInstitutionName'} })
    shariah_board_certified: bool = Field(default=..., description="""Whether institution is certified by Shariah supervisory board""", json_schema_extra = { "linkml_meta": {'alias': 'shariah_board_certified',
         'domain_of': ['Bank'],
         'slot_uri': 'murabaha:hasShariahBoardCertification'} })
    participates_in_transaction: Optional[list[str]] = Field(default=None, description="""Transaction the bank participates in""", json_schema_extra = { "linkml_meta": {'alias': 'participates_in_transaction',
         'domain_of': ['Bank', 'Customer'],
         'inverse': 'involves_bank',
         'slot_uri': 'murabaha:participatesInTransaction'} })
    owns_asset: Optional[list[str]] = Field(default=None, description="""Asset owned by the bank""", json_schema_extra = { "linkml_meta": {'alias': 'owns_asset', 'domain_of': ['Bank'], 'slot_uri': 'murabaha:ownsAsset'} })
    transfers_ownership: Optional[list[str]] = Field(default=None, description="""Ownership transfers executed by the bank""", json_schema_extra = { "linkml_meta": {'alias': 'transfers_ownership',
         'domain_of': ['Bank'],
         'slot_uri': 'murabaha:transfersOwnership'} })
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
    Party purchasing asset from bank under Murabaha arrangement

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fnd-pty:PartyInRole',
         'from_schema': 'https://spec.edmcouncil.org/outcomes/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'customer_id': {'identifier': True,
                                        'name': 'customer_id',
                                        'required': True},
                        'customer_name': {'name': 'customer_name', 'required': True},
                        'disclosure_acknowledged': {'name': 'disclosure_acknowledged',
                                                    'required': True}}})

    customer_id: str = Field(default=..., description="""Unique identifier for the customer""", json_schema_extra = { "linkml_meta": {'alias': 'customer_id',
         'domain_of': ['Customer'],
         'slot_uri': 'fibo-fnd-pty:hasPartyIdentifier'} })
    customer_name: str = Field(default=..., description="""Name of the customer party""", json_schema_extra = { "linkml_meta": {'alias': 'customer_name',
         'domain_of': ['Customer'],
         'slot_uri': 'fibo-fnd-pty:hasPartyName'} })
    disclosure_acknowledged: bool = Field(default=..., description="""Whether customer acknowledged profit disclosure""", json_schema_extra = { "linkml_meta": {'alias': 'disclosure_acknowledged',
         'domain_of': ['Customer'],
         'slot_uri': 'murabaha:hasDisclosureAcknowledgment'} })
    participates_in_transaction: Optional[list[str]] = Field(default=None, description="""Transaction the bank participates in""", json_schema_extra = { "linkml_meta": {'alias': 'participates_in_transaction',
         'domain_of': ['Bank', 'Customer'],
         'inverse': 'involves_bank',
         'slot_uri': 'murabaha:participatesInTransaction'} })
    receives_ownership: Optional[list[str]] = Field(default=None, description="""Ownership transfers received by customer""", json_schema_extra = { "linkml_meta": {'alias': 'receives_ownership',
         'domain_of': ['Customer'],
         'slot_uri': 'murabaha:receivesOwnership'} })
    makes_payment: Optional[list[str]] = Field(default=None, description="""Payments made by customer""", json_schema_extra = { "linkml_meta": {'alias': 'makes_payment',
         'domain_of': ['Customer'],
         'slot_uri': 'murabaha:makesPayment'} })
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
    Physical or financial asset being traded in Murabaha transaction

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc-pas:FinancialAsset',
         'from_schema': 'https://spec.edmcouncil.org/outcomes/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'asset_description': {'name': 'asset_description',
                                              'required': True},
                        'asset_id': {'identifier': True,
                                     'name': 'asset_id',
                                     'required': True},
                        'asset_type': {'name': 'asset_type', 'required': True},
                        'shariah_compliant': {'name': 'shariah_compliant',
                                              'required': True}}})

    asset_id: str = Field(default=..., description="""Unique identifier for the asset""", json_schema_extra = { "linkml_meta": {'alias': 'asset_id',
         'domain_of': ['Asset'],
         'slot_uri': 'fibo-fbc-pas:hasAssetIdentifier'} })
    asset_description: str = Field(default=..., description="""Detailed description of the asset""", json_schema_extra = { "linkml_meta": {'alias': 'asset_description',
         'domain_of': ['Asset'],
         'slot_uri': 'fibo-fbc-pas:hasAssetDescription'} })
    asset_type: str = Field(default=..., description="""Classification type of the asset""", json_schema_extra = { "linkml_meta": {'alias': 'asset_type',
         'domain_of': ['Asset'],
         'slot_uri': 'fibo-fbc-pas:hasAssetType'} })
    shariah_compliant: bool = Field(default=..., description="""Whether asset meets Shariah compliance requirements""", json_schema_extra = { "linkml_meta": {'alias': 'shariah_compliant',
         'domain_of': ['Asset'],
         'slot_uri': 'murabaha:isShariahCompliant'} })
    subject_of_transaction: Optional[list[str]] = Field(default=None, description="""Transaction where asset is the subject""", json_schema_extra = { "linkml_meta": {'alias': 'subject_of_transaction',
         'domain_of': ['Asset'],
         'inverse': 'involves_asset',
         'slot_uri': 'murabaha:subjectOfTransaction'} })
    owned_by: Optional[str] = Field(default=None, description="""Current owner of the asset""", json_schema_extra = { "linkml_meta": {'alias': 'owned_by', 'domain_of': ['Asset'], 'slot_uri': 'murabaha:ownedBy'} })
    transferred_in: Optional[list[str]] = Field(default=None, description="""Ownership transfers involving this asset""", json_schema_extra = { "linkml_meta": {'alias': 'transferred_in',
         'domain_of': ['Asset'],
         'slot_uri': 'murabaha:transferredIn'} })
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
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Activity',
         'from_schema': 'https://spec.edmcouncil.org/outcomes/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'from_party': {'name': 'from_party', 'required': True},
                        'to_party': {'name': 'to_party', 'required': True},
                        'transfer_id': {'identifier': True,
                                        'name': 'transfer_id',
                                        'required': True},
                        'transfer_timestamp': {'name': 'transfer_timestamp',
                                               'required': True},
                        'transfer_type': {'name': 'transfer_type', 'required': True}}})

    transfer_id: str = Field(default=..., description="""Unique identifier for the ownership transfer""", json_schema_extra = { "linkml_meta": {'alias': 'transfer_id',
         'domain_of': ['OwnershipTransfer'],
         'slot_uri': 'prov:identifier'} })
    transfer_timestamp: datetime  = Field(default=..., description="""Timestamp when ownership transfer occurred""", json_schema_extra = { "linkml_meta": {'alias': 'transfer_timestamp',
         'domain_of': ['OwnershipTransfer'],
         'slot_uri': 'prov:atTime'} })
    from_party: str = Field(default=..., description="""Party transferring ownership""", json_schema_extra = { "linkml_meta": {'alias': 'from_party',
         'domain_of': ['OwnershipTransfer'],
         'slot_uri': 'murabaha:hasTransferFromParty'} })
    to_party: str = Field(default=..., description="""Party receiving ownership""", json_schema_extra = { "linkml_meta": {'alias': 'to_party',
         'domain_of': ['OwnershipTransfer'],
         'slot_uri': 'murabaha:hasTransferToParty'} })
    transfer_type: str = Field(default=..., description="""Type of ownership transfer (purchase, sale, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'transfer_type',
         'domain_of': ['OwnershipTransfer'],
         'slot_uri': 'murabaha:hasTransferType'} })
    transfers_asset: Optional[str] = Field(default=None, description="""Asset being transferred""", json_schema_extra = { "linkml_meta": {'alias': 'transfers_asset',
         'domain_of': ['OwnershipTransfer'],
         'inverse': 'transferred_in',
         'slot_uri': 'murabaha:transfersAsset'} })
    part_of_transaction: Optional[str] = Field(default=None, description="""Transaction this transfer is part of""", json_schema_extra = { "linkml_meta": {'alias': 'part_of_transaction',
         'domain_of': ['OwnershipTransfer'],
         'slot_uri': 'murabaha:partOfTransaction'} })
    evidenced_by: Optional[list[str]] = Field(default=None, description="""Evidence supporting this transfer""", json_schema_extra = { "linkml_meta": {'alias': 'evidenced_by',
         'domain_of': ['OwnershipTransfer'],
         'slot_uri': 'prov:wasGeneratedBy'} })
    precedes_transfer: Optional[list[str]] = Field(default=None, description="""Transfer that follows this one in sequence""", json_schema_extra = { "linkml_meta": {'alias': 'precedes_transfer',
         'domain_of': ['OwnershipTransfer'],
         'slot_uri': 'prov:wasDerivedFrom'} })
    follows_transfer: Optional[list[str]] = Field(default=None, description="""Transfer that precedes this one in sequence""", json_schema_extra = { "linkml_meta": {'alias': 'follows_transfer',
         'domain_of': ['OwnershipTransfer'],
         'slot_uri': 'prov:wasRevisionOf'} })
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
    Documentation proving compliance with Shariah requirements

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Entity',
         'from_schema': 'https://spec.edmcouncil.org/outcomes/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'collection_timestamp': {'name': 'collection_timestamp',
                                                 'required': True},
                        'document_reference': {'name': 'document_reference',
                                               'required': True},
                        'evidence_id': {'identifier': True,
                                        'name': 'evidence_id',
                                        'required': True},
                        'evidence_type': {'name': 'evidence_type', 'required': True},
                        'verified_by': {'name': 'verified_by', 'required': True}}})

    evidence_id: str = Field(default=..., description="""Unique identifier for the audit evidence""", json_schema_extra = { "linkml_meta": {'alias': 'evidence_id',
         'domain_of': ['AuditEvidence'],
         'slot_uri': 'prov:identifier'} })
    evidence_type: str = Field(default=..., description="""Type of evidence (disclosure, ownership proof, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'evidence_type',
         'domain_of': ['AuditEvidence'],
         'slot_uri': 'murabaha:hasEvidenceType'} })
    document_reference: str = Field(default=..., description="""Reference to supporting documentation""", json_schema_extra = { "linkml_meta": {'alias': 'document_reference',
         'domain_of': ['AuditEvidence'],
         'slot_uri': 'murabaha:hasDocumentReference'} })
    collection_timestamp: datetime  = Field(default=..., description="""When the evidence was collected""", json_schema_extra = { "linkml_meta": {'alias': 'collection_timestamp',
         'domain_of': ['AuditEvidence'],
         'slot_uri': 'prov:generatedAtTime'} })
    verified_by: str = Field(default=..., description="""Person or system that verified the evidence""", json_schema_extra = { "linkml_meta": {'alias': 'verified_by',
         'domain_of': ['AuditEvidence'],
         'slot_uri': 'prov:wasAttributedTo'} })
    supports_compliance_check: Optional[list[str]] = Field(default=None, description="""Compliance status this evidence supports""", json_schema_extra = { "linkml_meta": {'alias': 'supports_compliance_check',
         'domain_of': ['AuditEvidence'],
         'slot_uri': 'murabaha:supportsComplianceCheck'} })
    relates_to_transaction: Optional[str] = Field(default=None, description="""Transaction this evidence relates to""", json_schema_extra = { "linkml_meta": {'alias': 'relates_to_transaction',
         'domain_of': ['AuditEvidence'],
         'inverse': 'has_evidence',
         'slot_uri': 'murabaha:relatesToTransaction'} })
    validates_ownership_transfer: Optional[list[str]] = Field(default=None, description="""Ownership transfer this evidence validates""", json_schema_extra = { "linkml_meta": {'alias': 'validates_ownership_transfer',
         'domain_of': ['AuditEvidence'],
         'inverse': 'evidenced_by',
         'slot_uri': 'murabaha:validatesOwnershipTransfer'} })
    included_in_audit_trail: Optional[str] = Field(default=None, description="""Audit trail containing this evidence""", json_schema_extra = { "linkml_meta": {'alias': 'included_in_audit_trail',
         'domain_of': ['AuditEvidence'],
         'slot_uri': 'murabaha:includedInAuditTrail'} })
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
    Classification of transaction compliance state

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'skos:Concept',
         'from_schema': 'https://spec.edmcouncil.org/outcomes/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'assessed_by': {'name': 'assessed_by', 'required': True},
                        'assessed_date': {'name': 'assessed_date', 'required': True},
                        'status_id': {'identifier': True,
                                      'name': 'status_id',
                                      'required': True},
                        'status_reason': {'name': 'status_reason', 'required': True},
                        'status_value': {'name': 'status_value', 'required': True}}})

    status_id: str = Field(default=..., description="""Unique identifier for the compliance status""", json_schema_extra = { "linkml_meta": {'alias': 'status_id',
         'domain_of': ['ComplianceStatus'],
         'slot_uri': 'skos:notation'} })
    status_value: ComplianceStatusEnum = Field(default=..., description="""Compliance status value (COMPLIANT, NON_COMPLIANT, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'status_value',
         'domain_of': ['ComplianceStatus'],
         'slot_uri': 'skos:prefLabel'} })
    status_reason: str = Field(default=..., description="""Reason or explanation for the compliance status""", json_schema_extra = { "linkml_meta": {'alias': 'status_reason',
         'domain_of': ['ComplianceStatus'],
         'slot_uri': 'skos:definition'} })
    assessed_date: datetime  = Field(default=..., description="""Date when compliance was assessed""", json_schema_extra = { "linkml_meta": {'alias': 'assessed_date',
         'domain_of': ['ComplianceStatus'],
         'slot_uri': 'murabaha:hasAssessmentDate'} })
    assessed_by: str = Field(default=..., description="""Auditor who assessed compliance""", json_schema_extra = { "linkml_meta": {'alias': 'assessed_by',
         'domain_of': ['ComplianceStatus'],
         'slot_uri': 'prov:wasAttributedTo'} })
    assigned_to_transaction: Optional[str] = Field(default=None, description="""Transaction assigned this status""", json_schema_extra = { "linkml_meta": {'alias': 'assigned_to_transaction',
         'domain_of': ['ComplianceStatus'],
         'inverse': 'has_compliance_status',
         'slot_uri': 'murabaha:assignedToTransaction'} })
    based_on_evidence: Optional[list[str]] = Field(default=None, description="""Evidence supporting this compliance status""", json_schema_extra = { "linkml_meta": {'alias': 'based_on_evidence',
         'domain_of': ['ComplianceStatus'],
         'inverse': 'supports_compliance_check',
         'slot_uri': 'murabaha:basedOnEvidence'} })
    recorded_in_audit_trail: Optional[str] = Field(default=None, description="""Audit trail recording this status""", json_schema_extra = { "linkml_meta": {'alias': 'recorded_in_audit_trail',
         'domain_of': ['ComplianceStatus'],
         'slot_uri': 'murabaha:recordedInAuditTrail'} })
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
    Comprehensive provenance record of all compliance checks and evidence

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Bundle',
         'from_schema': 'https://spec.edmcouncil.org/outcomes/murabaha-shariah-compliance-audit',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'audit_stage': {'name': 'audit_stage', 'required': True},
                        'created_timestamp': {'name': 'created_timestamp',
                                              'required': True},
                        'last_updated': {'name': 'last_updated', 'required': True},
                        'trail_id': {'identifier': True,
                                     'name': 'trail_id',
                                     'required': True}}})

    trail_id: str = Field(default=..., description="""Unique identifier for the audit trail""", json_schema_extra = { "linkml_meta": {'alias': 'trail_id',
         'domain_of': ['AuditTrail'],
         'slot_uri': 'prov:identifier'} })
    created_timestamp: datetime  = Field(default=..., description="""When the audit trail was created""", json_schema_extra = { "linkml_meta": {'alias': 'created_timestamp',
         'domain_of': ['AuditTrail'],
         'slot_uri': 'prov:generatedAtTime'} })
    last_updated: datetime  = Field(default=..., description="""When the audit trail was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'last_updated',
         'domain_of': ['AuditTrail'],
         'slot_uri': 'murabaha:lastUpdated'} })
    audit_stage: str = Field(default=..., description="""Current stage of the audit process""", json_schema_extra = { "linkml_meta": {'alias': 'audit_stage',
         'domain_of': ['AuditTrail'],
         'slot_uri': 'murabaha:hasAuditStage'} })
    tracks_transaction: Optional[str] = Field(default=None, description="""Transaction being tracked by this audit trail""", json_schema_extra = { "linkml_meta": {'alias': 'tracks_transaction',
         'domain_of': ['AuditTrail'],
         'inverse': 'has_audit_trail',
         'slot_uri': 'murabaha:tracksTransaction'} })
    contains_evidence: Optional[list[str]] = Field(default=None, description="""Evidence contained in this audit trail""", json_schema_extra = { "linkml_meta": {'alias': 'contains_evidence',
         'domain_of': ['AuditTrail'],
         'inverse': 'included_in_audit_trail',
         'slot_uri': 'murabaha:containsEvidence'} })
    records_compliance_status: Optional[list[str]] = Field(default=None, description="""Compliance statuses recorded in this trail""", json_schema_extra = { "linkml_meta": {'alias': 'records_compliance_status',
         'domain_of': ['AuditTrail'],
         'inverse': 'recorded_in_audit_trail',
         'slot_uri': 'murabaha:recordsComplianceStatus'} })
    documents_ownership_transfers: Optional[list[str]] = Field(default=None, description="""Ownership transfers documented in this trail""", json_schema_extra = { "linkml_meta": {'alias': 'documents_ownership_transfers',
         'domain_of': ['AuditTrail'],
         'slot_uri': 'murabaha:documentsOwnershipTransfers'} })
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
AuditEvidence.model_rebuild()
ComplianceStatus.model_rebuild()
AuditTrail.model_rebuild()

