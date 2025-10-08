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
     'description': 'LinkML schema for auditing Murabaha transactions to ensure '
                    'Shariah compliance.\n'
                    'Tracks ownership transfers, profit markup transparency, '
                    'payment terms, and maintains \n'
                    'comprehensive audit trails for Islamic finance compliance '
                    'verification.\n',
     'id': 'https://example.org/schemas/murabaha-shariah-compliance-audit',
     'imports': ['../core/provenance'],
     'name': 'murabaha_shariah_compliance_audit',
     'prefixes': {'doco': {'prefix_prefix': 'doco',
                           'prefix_reference': 'http://purl.org/spar/doco/'},
                  'fabio': {'prefix_prefix': 'fabio',
                            'prefix_reference': 'http://purl.org/spar/fabio/'},
                  'fibo-fbc-caa': {'prefix_prefix': 'fibo-fbc-caa',
                                   'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FBC/ProductsAndServices/ClientsAndAccounts/'},
                  'fibo-fbc-dae': {'prefix_prefix': 'fibo-fbc-dae',
                                   'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FBC/DebtAndEquities/CreditEvents/'},
                  'fibo-fbc-fse': {'prefix_prefix': 'fibo-fbc-fse',
                                   'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FBC/FunctionalEntities/FinancialServicesEntities/'},
                  'fibo-fbc-pas': {'prefix_prefix': 'fibo-fbc-pas',
                                   'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FBC/ProductsAndServices/FinancialProductsAndServices/'},
                  'fibo-fnd-pty': {'prefix_prefix': 'fibo-fnd-pty',
                                   'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FND/Parties/Roles/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'}},
     'source_file': 'D:\\projects\\Pydantic Model '
                    'Generator\\pydantic_library\\schemas\\overlays\\business_outcome456_overlay.yaml'} )

class ComplianceStatusEnum(str, Enum):
    """
    Possible Shariah compliance status values
    """
    COMPLIANT = "COMPLIANT"
    """
    Transaction is fully Shariah compliant
    """
    NON_COMPLIANT = "NON_COMPLIANT"
    """
    Transaction violates Shariah requirements
    """
    FAILED = "FAILED"
    """
    Transaction failed compliance checks
    """
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    """
    Transaction requires additional review
    """
    PENDING = "PENDING"
    """
    Compliance check is pending
    """
    APPROVED = "APPROVED"
    """
    Transaction approved by Shariah board
    """


class CustomerTypeEnum(str, Enum):
    """
    Types of customers in Islamic finance
    """
    INDIVIDUAL = "INDIVIDUAL"
    """
    Individual retail customer
    """
    CORPORATE = "CORPORATE"
    """
    Corporate or business customer
    """
    INSTITUTIONAL = "INSTITUTIONAL"
    """
    Institutional investor
    """
    GOVERNMENT = "GOVERNMENT"
    """
    Government entity
    """
    SME = "SME"
    """
    Small and medium enterprise
    """


class OwnershipTypeEnum(str, Enum):
    """
    Types of ownership transfer
    """
    FULL_OWNERSHIP = "FULL_OWNERSHIP"
    """
    Complete ownership transfer
    """
    BENEFICIAL_OWNERSHIP = "BENEFICIAL_OWNERSHIP"
    """
    Beneficial ownership only
    """
    LEGAL_OWNERSHIP = "LEGAL_OWNERSHIP"
    """
    Legal ownership only
    """
    CONSTRUCTIVE_OWNERSHIP = "CONSTRUCTIVE_OWNERSHIP"
    """
    Constructive possession
    """
    TEMPORARY_OWNERSHIP = "TEMPORARY_OWNERSHIP"
    """
    Temporary ownership for transaction
    """


class AuditResultEnum(str, Enum):
    """
    Possible audit results
    """
    PASSED = "PASSED"
    """
    Audit check passed
    """
    FAILED = "FAILED"
    """
    Audit check failed
    """
    NON_COMPLIANT = "NON_COMPLIANT"
    """
    Non-compliant with criteria
    """
    COMPLIANT = "COMPLIANT"
    """
    Compliant with criteria
    """
    CONDITIONAL = "CONDITIONAL"
    """
    Conditionally compliant
    """
    INCONCLUSIVE = "INCONCLUSIVE"
    """
    Results are inconclusive
    """


class EvidenceTypeEnum(str, Enum):
    """
    Types of compliance evidence
    """
    CONTRACT = "CONTRACT"
    """
    Contract document
    """
    INVOICE = "INVOICE"
    """
    Invoice or receipt
    """
    OWNERSHIP_CERTIFICATE = "OWNERSHIP_CERTIFICATE"
    """
    Certificate of ownership
    """
    BANK_STATEMENT = "BANK_STATEMENT"
    """
    Bank statement
    """
    AUDIT_REPORT = "AUDIT_REPORT"
    """
    Audit report
    """
    SHARIAH_CERTIFICATE = "SHARIAH_CERTIFICATE"
    """
    Shariah compliance certificate
    """
    CORRESPONDENCE = "CORRESPONDENCE"
    """
    Email or letter correspondence
    """
    PHOTOGRAPH = "PHOTOGRAPH"
    """
    Photographic evidence
    """
    DIGITAL_RECORD = "DIGITAL_RECORD"
    """
    Digital transaction record
    """


class VerificationStatusEnum(str, Enum):
    """
    Status of evidence verification
    """
    VERIFIED = "VERIFIED"
    """
    Evidence has been verified
    """
    UNVERIFIED = "UNVERIFIED"
    """
    Evidence not yet verified
    """
    PENDING = "PENDING"
    """
    Verification pending
    """
    REJECTED = "REJECTED"
    """
    Evidence rejected
    """
    EXPIRED = "EXPIRED"
    """
    Evidence has expired
    """
    AUTHENTIC = "AUTHENTIC"
    """
    Evidence authenticated
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
    Islamic finance transaction where bank purchases asset and sells to customer 
    at cost plus profit markup. Represents complete transaction lifecycle.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc-dae:Transaction',
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
                       'ProfitMarkup']} })
    transaction_id: str = Field(default=..., description="""Unique identifier for Murabaha transaction""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_id', 'domain_of': ['MurabahaTransaction']} })
    transaction_date: date = Field(default=..., description="""Date when transaction was executed""", json_schema_extra = { "linkml_meta": {'alias': 'transaction_date', 'domain_of': ['MurabahaTransaction']} })
    cost_price: float = Field(default=..., description="""Original cost price paid by bank for asset""", json_schema_extra = { "linkml_meta": {'alias': 'cost_price', 'domain_of': ['MurabahaTransaction']} })
    selling_price: float = Field(default=..., description="""Final selling price to customer including markup""", json_schema_extra = { "linkml_meta": {'alias': 'selling_price', 'domain_of': ['MurabahaTransaction']} })
    compliance_status: ComplianceStatusEnum = Field(default=..., description="""Current Shariah compliance status of transaction""", json_schema_extra = { "linkml_meta": {'alias': 'compliance_status', 'domain_of': ['MurabahaTransaction']} })
    payment_terms: str = Field(default=..., description="""Terms and schedule for customer payment""", json_schema_extra = { "linkml_meta": {'alias': 'payment_terms', 'domain_of': ['MurabahaTransaction']} })
    involves_bank: str = Field(default=..., description="""Reference to bank participating in transaction""", json_schema_extra = { "linkml_meta": {'alias': 'involves_bank', 'domain_of': ['MurabahaTransaction']} })
    involves_customer: str = Field(default=..., description="""Reference to customer participating in transaction""", json_schema_extra = { "linkml_meta": {'alias': 'involves_customer', 'domain_of': ['MurabahaTransaction']} })
    concerns_asset: str = Field(default=..., description="""Reference to asset being traded""", json_schema_extra = { "linkml_meta": {'alias': 'concerns_asset', 'domain_of': ['MurabahaTransaction']} })
    has_profit_markup: Optional[str] = Field(default=None, description="""Reference to profit markup applied""", json_schema_extra = { "linkml_meta": {'alias': 'has_profit_markup', 'domain_of': ['MurabahaTransaction']} })
    has_ownership_transfers: Optional[list[str]] = Field(default=None, description="""List of ownership transfers in transaction""", json_schema_extra = { "linkml_meta": {'alias': 'has_ownership_transfers', 'domain_of': ['MurabahaTransaction']} })
    audited_by: Optional[list[str]] = Field(default=None, description="""List of audit activities for this transaction""", json_schema_extra = { "linkml_meta": {'alias': 'audited_by', 'domain_of': ['MurabahaTransaction']} })
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
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc-fse:Bank',
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
                       'ProfitMarkup']} })
    bank_id: str = Field(default=..., description="""Unique identifier for bank""", json_schema_extra = { "linkml_meta": {'alias': 'bank_id', 'domain_of': ['Bank']} })
    bank_name: str = Field(default=..., description="""Official name of bank""", json_schema_extra = { "linkml_meta": {'alias': 'bank_name', 'domain_of': ['Bank']} })
    shariah_board_certified: bool = Field(default=..., description="""Whether bank is certified by Shariah board""", json_schema_extra = { "linkml_meta": {'alias': 'shariah_board_certified', 'domain_of': ['Bank']} })
    participates_in_transaction: Optional[list[str]] = Field(default=None, description="""Reference to transaction entity is participating in""", json_schema_extra = { "linkml_meta": {'alias': 'participates_in_transaction', 'domain_of': ['Bank', 'Customer']} })
    owns_asset: Optional[list[str]] = Field(default=None, description="""Reference to asset owned by entity""", json_schema_extra = { "linkml_meta": {'alias': 'owns_asset', 'domain_of': ['Bank']} })
    transfers_ownership: Optional[list[str]] = Field(default=None, description="""Reference to ownership transfer performed""", json_schema_extra = { "linkml_meta": {'alias': 'transfers_ownership', 'domain_of': ['Bank']} })
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
    Party purchasing asset through Murabaha financing
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fnd-pty:Customer',
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
                       'ProfitMarkup']} })
    customer_id: str = Field(default=..., description="""Unique identifier for customer""", json_schema_extra = { "linkml_meta": {'alias': 'customer_id', 'domain_of': ['Customer']} })
    customer_name: str = Field(default=..., description="""Full name of customer""", json_schema_extra = { "linkml_meta": {'alias': 'customer_name', 'domain_of': ['Customer']} })
    customer_type: CustomerTypeEnum = Field(default=..., description="""Type of customer (individual, corporate, etc)""", json_schema_extra = { "linkml_meta": {'alias': 'customer_type', 'domain_of': ['Customer']} })
    participates_in_transaction: Optional[list[str]] = Field(default=None, description="""Reference to transaction entity is participating in""", json_schema_extra = { "linkml_meta": {'alias': 'participates_in_transaction', 'domain_of': ['Bank', 'Customer']} })
    receives_asset: Optional[list[str]] = Field(default=None, description="""Reference to asset received by customer""", json_schema_extra = { "linkml_meta": {'alias': 'receives_asset', 'domain_of': ['Customer']} })
    receives_ownership: Optional[list[str]] = Field(default=None, description="""Reference to ownership transfer received""", json_schema_extra = { "linkml_meta": {'alias': 'receives_ownership', 'domain_of': ['Customer']} })
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
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc-pas:Asset',
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
                       'ProfitMarkup']} })
    asset_id: str = Field(default=..., description="""Unique identifier for asset""", json_schema_extra = { "linkml_meta": {'alias': 'asset_id', 'domain_of': ['Asset']} })
    asset_type: str = Field(default=..., description="""Type or category of asset""", json_schema_extra = { "linkml_meta": {'alias': 'asset_type', 'domain_of': ['Asset']} })
    asset_description: str = Field(default=..., description="""Detailed description of asset""", json_schema_extra = { "linkml_meta": {'alias': 'asset_description', 'domain_of': ['Asset']} })
    valuation: float = Field(default=..., description="""Current valuation of asset""", json_schema_extra = { "linkml_meta": {'alias': 'valuation', 'domain_of': ['Asset']} })
    shariah_compliant: bool = Field(default=..., description="""Whether asset is Shariah compliant""", json_schema_extra = { "linkml_meta": {'alias': 'shariah_compliant', 'domain_of': ['Asset']} })
    subject_of_transaction: Optional[list[str]] = Field(default=None, description="""Reference to transaction involving this asset""", json_schema_extra = { "linkml_meta": {'alias': 'subject_of_transaction', 'domain_of': ['Asset']} })
    owned_by: Optional[str] = Field(default=None, description="""Reference to current owner of asset""", json_schema_extra = { "linkml_meta": {'alias': 'owned_by', 'domain_of': ['Asset']} })
    transferred_in: Optional[list[str]] = Field(default=None, description="""Reference to ownership transfer involving asset""", json_schema_extra = { "linkml_meta": {'alias': 'transferred_in', 'domain_of': ['Asset']} })
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
    Critical event representing transfer of asset ownership. Tracks temporal 
    sequence to verify bank ownership before customer sale.

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
                       'ProfitMarkup']} })
    transfer_id: str = Field(default=..., description="""Unique identifier for ownership transfer""", json_schema_extra = { "linkml_meta": {'alias': 'transfer_id', 'domain_of': ['OwnershipTransfer']} })
    transfer_date: date = Field(default=..., description="""Date of ownership transfer""", json_schema_extra = { "linkml_meta": {'alias': 'transfer_date', 'domain_of': ['OwnershipTransfer']} })
    transfer_timestamp: datetime  = Field(default=..., description="""Precise timestamp of ownership transfer""", json_schema_extra = { "linkml_meta": {'alias': 'transfer_timestamp', 'domain_of': ['OwnershipTransfer']} })
    from_party: str = Field(default=..., description="""Party transferring ownership""", json_schema_extra = { "linkml_meta": {'alias': 'from_party', 'domain_of': ['OwnershipTransfer']} })
    to_party: str = Field(default=..., description="""Party receiving ownership""", json_schema_extra = { "linkml_meta": {'alias': 'to_party', 'domain_of': ['OwnershipTransfer']} })
    ownership_type: OwnershipTypeEnum = Field(default=..., description="""Type of ownership being transferred""", json_schema_extra = { "linkml_meta": {'alias': 'ownership_type', 'domain_of': ['OwnershipTransfer']} })
    possession_transferred: bool = Field(default=..., description="""Whether physical possession was transferred""", json_schema_extra = { "linkml_meta": {'alias': 'possession_transferred', 'domain_of': ['OwnershipTransfer']} })
    part_of_transaction: Optional[str] = Field(default=None, description="""Reference to parent transaction""", json_schema_extra = { "linkml_meta": {'alias': 'part_of_transaction', 'domain_of': ['OwnershipTransfer']} })
    transfers_asset: Optional[str] = Field(default=None, description="""Reference to asset being transferred""", json_schema_extra = { "linkml_meta": {'alias': 'transfers_asset', 'domain_of': ['OwnershipTransfer']} })
    has_evidence: Optional[list[str]] = Field(default=None, description="""Reference to supporting evidence""", json_schema_extra = { "linkml_meta": {'alias': 'has_evidence', 'domain_of': ['OwnershipTransfer', 'ProfitMarkup']} })
    precedes: Optional[str] = Field(default=None, description="""Reference to subsequent ownership transfer""", json_schema_extra = { "linkml_meta": {'alias': 'precedes', 'domain_of': ['OwnershipTransfer']} })
    follows: Optional[str] = Field(default=None, description="""Reference to previous ownership transfer""", json_schema_extra = { "linkml_meta": {'alias': 'follows', 'domain_of': ['OwnershipTransfer']} })
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
                       'ProfitMarkup']} })
    audit_id: str = Field(default=..., description="""Unique identifier for audit activity""", json_schema_extra = { "linkml_meta": {'alias': 'audit_id', 'domain_of': ['AuditActivity']} })
    audit_date: date = Field(default=..., description="""Date when audit was performed""", json_schema_extra = { "linkml_meta": {'alias': 'audit_date', 'domain_of': ['AuditActivity']} })
    auditor_name: str = Field(default=..., description="""Name of auditor performing activity""", json_schema_extra = { "linkml_meta": {'alias': 'auditor_name', 'domain_of': ['AuditActivity']} })
    compliance_criterion: str = Field(default=..., description="""Specific Shariah compliance criterion being checked""", json_schema_extra = { "linkml_meta": {'alias': 'compliance_criterion', 'domain_of': ['AuditActivity']} })
    audit_result: AuditResultEnum = Field(default=..., description="""Result of audit check""", json_schema_extra = { "linkml_meta": {'alias': 'audit_result', 'domain_of': ['AuditActivity']} })
    findings: Optional[str] = Field(default=None, description="""Detailed findings from audit""", json_schema_extra = { "linkml_meta": {'alias': 'findings', 'domain_of': ['AuditActivity']} })
    audits_transaction: Optional[str] = Field(default=None, description="""Reference to transaction being audited""", json_schema_extra = { "linkml_meta": {'alias': 'audits_transaction', 'domain_of': ['AuditActivity']} })
    generates_evidence: Optional[list[str]] = Field(default=None, description="""Reference to evidence generated by audit""", json_schema_extra = { "linkml_meta": {'alias': 'generates_evidence', 'domain_of': ['AuditActivity']} })
    performed_by: Optional[str] = Field(default=None, description="""Reference to auditor who performed activity""", json_schema_extra = { "linkml_meta": {'alias': 'performed_by', 'domain_of': ['AuditActivity']} })
    validates_transfer: Optional[str] = Field(default=None, description="""Reference to ownership transfer being validated""", json_schema_extra = { "linkml_meta": {'alias': 'validates_transfer', 'domain_of': ['AuditActivity']} })
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
    Documentation and records supporting compliance verification
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
                       'ProfitMarkup']} })
    evidence_id: str = Field(default=..., description="""Unique identifier for evidence""", json_schema_extra = { "linkml_meta": {'alias': 'evidence_id', 'domain_of': ['ComplianceEvidence']} })
    evidence_type: EvidenceTypeEnum = Field(default=..., description="""Type of evidence document""", json_schema_extra = { "linkml_meta": {'alias': 'evidence_type', 'domain_of': ['ComplianceEvidence']} })
    evidence_date: date = Field(default=..., description="""Date evidence was created or collected""", json_schema_extra = { "linkml_meta": {'alias': 'evidence_date', 'domain_of': ['ComplianceEvidence']} })
    document_reference: str = Field(default=..., description="""Reference to physical or digital document""", json_schema_extra = { "linkml_meta": {'alias': 'document_reference', 'domain_of': ['ComplianceEvidence']} })
    verification_status: VerificationStatusEnum = Field(default=..., description="""Status of evidence verification""", json_schema_extra = { "linkml_meta": {'alias': 'verification_status', 'domain_of': ['ComplianceEvidence']} })
    supports_audit: Optional[str] = Field(default=None, description="""Reference to audit activity this evidence supports""", json_schema_extra = { "linkml_meta": {'alias': 'supports_audit', 'domain_of': ['ComplianceEvidence']} })
    relates_to_transaction: Optional[str] = Field(default=None, description="""Reference to related transaction""", json_schema_extra = { "linkml_meta": {'alias': 'relates_to_transaction', 'domain_of': ['ComplianceEvidence']} })
    documents_transfer: Optional[str] = Field(default=None, description="""Reference to ownership transfer documented""", json_schema_extra = { "linkml_meta": {'alias': 'documents_transfer', 'domain_of': ['ComplianceEvidence']} })
    generated_by: Optional[str] = Field(default=None, description="""Reference to activity that generated evidence""", json_schema_extra = { "linkml_meta": {'alias': 'generated_by', 'domain_of': ['ComplianceEvidence']} })
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


class ProfitMarkup(ProvenanceFields):
    """
    Transparent profit component added to cost price
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc-caa:PricingComponent',
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
                       'ProfitMarkup']} })
    markup_id: str = Field(default=..., description="""Unique identifier for profit markup""", json_schema_extra = { "linkml_meta": {'alias': 'markup_id', 'domain_of': ['ProfitMarkup']} })
    markup_amount: float = Field(default=..., description="""Absolute amount of profit markup""", json_schema_extra = { "linkml_meta": {'alias': 'markup_amount', 'domain_of': ['ProfitMarkup']} })
    markup_percentage: float = Field(default=..., description="""Percentage of profit markup""", json_schema_extra = { "linkml_meta": {'alias': 'markup_percentage', 'domain_of': ['ProfitMarkup']} })
    disclosed_to_customer: bool = Field(default=..., description="""Whether markup was disclosed to customer""", json_schema_extra = { "linkml_meta": {'alias': 'disclosed_to_customer', 'domain_of': ['ProfitMarkup']} })
    disclosure_date: Optional[date] = Field(default=None, description="""Date when markup was disclosed""", json_schema_extra = { "linkml_meta": {'alias': 'disclosure_date', 'domain_of': ['ProfitMarkup']} })
    calculation_method: str = Field(default=..., description="""Method used to calculate markup""", json_schema_extra = { "linkml_meta": {'alias': 'calculation_method', 'domain_of': ['ProfitMarkup']} })
    component_of_transaction: Optional[str] = Field(default=None, description="""Reference to parent transaction""", json_schema_extra = { "linkml_meta": {'alias': 'component_of_transaction', 'domain_of': ['ProfitMarkup']} })
    has_evidence: Optional[list[str]] = Field(default=None, description="""Reference to supporting evidence""", json_schema_extra = { "linkml_meta": {'alias': 'has_evidence', 'domain_of': ['OwnershipTransfer', 'ProfitMarkup']} })
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
ProfitMarkup.model_rebuild()

