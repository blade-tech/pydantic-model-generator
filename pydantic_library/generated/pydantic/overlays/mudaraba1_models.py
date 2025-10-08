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


linkml_meta = LinkMLMeta({'default_prefix': 'mudarabah_wakalah_hybrid_shariah_audit',
     'description': 'Comprehensive audit specification for hybrid Islamic finance '
                    'contracts combining Mudarabah (profit-sharing) and Wakalah '
                    '(agency) structures, ensuring Shariah compliance and proper '
                    'documentation of contract terms, parties, and audit findings.',
     'id': 'https://example.org/schemas/mudarabah-wakalah-hybrid-shariah-audit',
     'imports': ['../core/provenance'],
     'name': 'mudarabah_wakalah_hybrid_shariah_audit',
     'prefixes': {'doco': {'prefix_prefix': 'doco',
                           'prefix_reference': 'http://purl.org/spar/doco/'},
                  'fabio': {'prefix_prefix': 'fabio',
                            'prefix_reference': 'http://purl.org/spar/fabio/'},
                  'fibo-fbc': {'prefix_prefix': 'fibo-fbc',
                               'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FBC/ProductsAndServices/FinancialProductsAndServices/'},
                  'fibo-fnd': {'prefix_prefix': 'fibo-fnd',
                               'prefix_reference': 'https://spec.edmcouncil.org/fibo/ontology/FND/Law/LegalCore/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'}},
     'source_file': '..\\..\\pydantic_library\\schemas\\overlays\\mudaraba1_overlay.yaml'} )

class ContractStatusEnum(str, Enum):
    """
    Enumeration of possible contract statuses
    """
    ACTIVE = "ACTIVE"
    """
    Contract is currently active
    """
    EXPIRED = "EXPIRED"
    """
    Contract has reached maturity
    """
    TERMINATED = "TERMINATED"
    """
    Contract was terminated early
    """
    PENDING = "PENDING"
    """
    Contract is pending approval
    """
    SUSPENDED = "SUSPENDED"
    """
    Contract is temporarily suspended
    """


class AuditOpinionEnum(str, Enum):
    """
    Enumeration of possible audit opinions
    """
    COMPLIANT = "COMPLIANT"
    """
    Fully compliant with Shariah requirements
    """
    NON_COMPLIANT = "NON_COMPLIANT"
    """
    Not compliant with Shariah requirements
    """
    QUALIFIED_OPINION = "QUALIFIED_OPINION"
    """
    Compliant with some reservations
    """
    ADVERSE_OPINION = "ADVERSE_OPINION"
    """
    Significant non-compliance issues
    """
    DISCLAIMER = "DISCLAIMER"
    """
    Unable to form an opinion
    """


class ReportStatusEnum(str, Enum):
    """
    Enumeration of possible report statuses
    """
    DRAFT = "DRAFT"
    """
    Report is in draft status
    """
    FINAL = "FINAL"
    """
    Report is finalized
    """
    UNDER_REVIEW = "UNDER_REVIEW"
    """
    Report is under review
    """
    PUBLISHED = "PUBLISHED"
    """
    Report has been published
    """
    ARCHIVED = "ARCHIVED"
    """
    Report has been archived
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
    Audit activity examining Shariah contract compliance
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Activity',
         'from_schema': 'https://example.org/schemas/mudarabah-wakalah-hybrid-shariah-audit',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'audit_date': {'name': 'audit_date', 'required': True},
                        'audit_id': {'identifier': True,
                                     'name': 'audit_id',
                                     'required': True},
                        'audit_scope': {'name': 'audit_scope', 'required': True},
                        'auditor_name': {'name': 'auditor_name', 'required': True}}})

    audit_id: str = Field(default=..., description="""Unique identifier for the audit activity""", json_schema_extra = { "linkml_meta": {'alias': 'audit_id', 'domain_of': ['Audit']} })
    audit_date: date = Field(default=..., description="""Date when the audit was conducted""", json_schema_extra = { "linkml_meta": {'alias': 'audit_date', 'domain_of': ['Audit']} })
    auditor_name: str = Field(default=..., description="""Name of the auditor or audit firm""", json_schema_extra = { "linkml_meta": {'alias': 'auditor_name', 'domain_of': ['Audit']} })
    audit_scope: str = Field(default=..., description="""Scope and coverage of the audit activity""", json_schema_extra = { "linkml_meta": {'alias': 'audit_scope', 'domain_of': ['Audit']} })
    audits_contract: Optional[list[str]] = Field(default=None, description="""Links audit to the contract being audited""", json_schema_extra = { "linkml_meta": {'alias': 'audits_contract', 'domain_of': ['Audit']} })
    produces_report: Optional[list[str]] = Field(default=None, description="""Links audit to the report it produces""", json_schema_extra = { "linkml_meta": {'alias': 'produces_report', 'domain_of': ['Audit']} })
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


class MudarabahContract(ProvenanceFields):
    """
    Profit-sharing partnership contract where one party provides capital and the other provides expertise
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc:Contract',
         'from_schema': 'https://example.org/schemas/mudarabah-wakalah-hybrid-shariah-audit',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'capital_amount': {'name': 'capital_amount', 'required': True},
                        'contract_id': {'identifier': True,
                                        'name': 'contract_id',
                                        'required': True},
                        'mudarib': {'name': 'mudarib', 'required': True},
                        'profit_sharing_ratio': {'name': 'profit_sharing_ratio',
                                                 'required': True},
                        'rabb_ul_maal': {'name': 'rabb_ul_maal', 'required': True}}})

    contract_id: str = Field(default=..., description="""Unique identifier for the contract""", json_schema_extra = { "linkml_meta": {'alias': 'contract_id',
         'domain_of': ['MudarabahContract', 'WakalahContract', 'HybridShariahContract']} })
    rabb_ul_maal: str = Field(default=..., description="""Capital provider in the Mudarabah contract""", json_schema_extra = { "linkml_meta": {'alias': 'rabb_ul_maal', 'domain_of': ['MudarabahContract']} })
    mudarib: str = Field(default=..., description="""Fund manager/entrepreneur in the Mudarabah contract""", json_schema_extra = { "linkml_meta": {'alias': 'mudarib', 'domain_of': ['MudarabahContract']} })
    capital_amount: float = Field(default=..., description="""Amount of capital provided by Rabb-ul-Maal""", json_schema_extra = { "linkml_meta": {'alias': 'capital_amount', 'domain_of': ['MudarabahContract']} })
    profit_sharing_ratio: str = Field(default=..., description="""Ratio for sharing profits between parties (e.g., 60:40)""", json_schema_extra = { "linkml_meta": {'alias': 'profit_sharing_ratio', 'domain_of': ['MudarabahContract']} })
    contract_date: Optional[date] = Field(default=None, description="""Date of contract execution""", json_schema_extra = { "linkml_meta": {'alias': 'contract_date',
         'domain_of': ['MudarabahContract', 'WakalahContract']} })
    contract_status: Optional[ContractStatusEnum] = Field(default=None, description="""Current status of the contract""", json_schema_extra = { "linkml_meta": {'alias': 'contract_status',
         'domain_of': ['MudarabahContract', 'WakalahContract', 'HybridShariahContract']} })
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


class WakalahContract(ProvenanceFields):
    """
    Agency contract where a principal appoints an agent to perform specific tasks
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc:Contract',
         'from_schema': 'https://example.org/schemas/mudarabah-wakalah-hybrid-shariah-audit',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'agency_fee': {'name': 'agency_fee', 'required': True},
                        'contract_id': {'identifier': True,
                                        'name': 'contract_id',
                                        'required': True},
                        'principal': {'name': 'principal', 'required': True},
                        'scope_of_authority': {'name': 'scope_of_authority',
                                               'required': True},
                        'wakil': {'name': 'wakil', 'required': True}}})

    contract_id: str = Field(default=..., description="""Unique identifier for the contract""", json_schema_extra = { "linkml_meta": {'alias': 'contract_id',
         'domain_of': ['MudarabahContract', 'WakalahContract', 'HybridShariahContract']} })
    principal: str = Field(default=..., description="""Principal party appointing the agent""", json_schema_extra = { "linkml_meta": {'alias': 'principal', 'domain_of': ['WakalahContract']} })
    wakil: str = Field(default=..., description="""Agent appointed to perform tasks on behalf of principal""", json_schema_extra = { "linkml_meta": {'alias': 'wakil', 'domain_of': ['WakalahContract']} })
    agency_fee: float = Field(default=..., description="""Fee paid to the agent for services""", json_schema_extra = { "linkml_meta": {'alias': 'agency_fee', 'domain_of': ['WakalahContract']} })
    scope_of_authority: str = Field(default=..., description="""Defined scope of authority granted to the agent""", json_schema_extra = { "linkml_meta": {'alias': 'scope_of_authority', 'domain_of': ['WakalahContract']} })
    contract_date: Optional[date] = Field(default=None, description="""Date of contract execution""", json_schema_extra = { "linkml_meta": {'alias': 'contract_date',
         'domain_of': ['MudarabahContract', 'WakalahContract']} })
    contract_status: Optional[ContractStatusEnum] = Field(default=None, description="""Current status of the contract""", json_schema_extra = { "linkml_meta": {'alias': 'contract_status',
         'domain_of': ['MudarabahContract', 'WakalahContract', 'HybridShariahContract']} })
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


class HybridShariahContract(ProvenanceFields):
    """
    Composite financial instrument combining Mudarabah and Wakalah structures
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fbc:FinancialInstrument',
         'from_schema': 'https://example.org/schemas/mudarabah-wakalah-hybrid-shariah-audit',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'contract_id': {'identifier': True,
                                        'name': 'contract_id',
                                        'required': True},
                        'contract_name': {'name': 'contract_name', 'required': True},
                        'inception_date': {'name': 'inception_date', 'required': True},
                        'maturity_date': {'name': 'maturity_date', 'required': True},
                        'total_value': {'name': 'total_value', 'required': True}}})

    contract_id: str = Field(default=..., description="""Unique identifier for the contract""", json_schema_extra = { "linkml_meta": {'alias': 'contract_id',
         'domain_of': ['MudarabahContract', 'WakalahContract', 'HybridShariahContract']} })
    contract_name: str = Field(default=..., description="""Name or title of the contract""", json_schema_extra = { "linkml_meta": {'alias': 'contract_name', 'domain_of': ['HybridShariahContract']} })
    inception_date: date = Field(default=..., description="""Date when the contract becomes effective""", json_schema_extra = { "linkml_meta": {'alias': 'inception_date', 'domain_of': ['HybridShariahContract']} })
    maturity_date: date = Field(default=..., description="""Date when the contract expires or matures""", json_schema_extra = { "linkml_meta": {'alias': 'maturity_date', 'domain_of': ['HybridShariahContract']} })
    total_value: float = Field(default=..., description="""Total monetary value of the contract""", json_schema_extra = { "linkml_meta": {'alias': 'total_value', 'domain_of': ['HybridShariahContract']} })
    contract_status: Optional[ContractStatusEnum] = Field(default=None, description="""Current status of the contract""", json_schema_extra = { "linkml_meta": {'alias': 'contract_status',
         'domain_of': ['MudarabahContract', 'WakalahContract', 'HybridShariahContract']} })
    comprises_mudarabah: Optional[list[str]] = Field(default=None, description="""Links hybrid contract to its Mudarabah component""", json_schema_extra = { "linkml_meta": {'alias': 'comprises_mudarabah', 'domain_of': ['HybridShariahContract']} })
    comprises_wakalah: Optional[list[str]] = Field(default=None, description="""Links hybrid contract to its Wakalah component""", json_schema_extra = { "linkml_meta": {'alias': 'comprises_wakalah', 'domain_of': ['HybridShariahContract']} })
    must_comply_with_framework: Optional[list[str]] = Field(default=None, description="""Links contract to compliance framework it must adhere to""", json_schema_extra = { "linkml_meta": {'alias': 'must_comply_with_framework', 'domain_of': ['HybridShariahContract']} })
    has_terms: Optional[list[str]] = Field(default=None, description="""Links contract to its terms and conditions""", json_schema_extra = { "linkml_meta": {'alias': 'has_terms', 'domain_of': ['HybridShariahContract']} })
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
    Regulatory framework defining Shariah compliance requirements for Islamic finance
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fibo-fnd:RegulatoryScheme',
         'from_schema': 'https://example.org/schemas/mudarabah-wakalah-hybrid-shariah-audit',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'compliance_standards': {'name': 'compliance_standards',
                                                 'required': True},
                        'framework_id': {'identifier': True,
                                         'name': 'framework_id',
                                         'required': True},
                        'framework_name': {'name': 'framework_name', 'required': True},
                        'governing_body': {'name': 'governing_body', 'required': True}}})

    framework_id: str = Field(default=..., description="""Unique identifier for the compliance framework""", json_schema_extra = { "linkml_meta": {'alias': 'framework_id', 'domain_of': ['ShariahComplianceFramework']} })
    framework_name: str = Field(default=..., description="""Name of the Shariah compliance framework""", json_schema_extra = { "linkml_meta": {'alias': 'framework_name', 'domain_of': ['ShariahComplianceFramework']} })
    governing_body: str = Field(default=..., description="""Organization or body governing the framework""", json_schema_extra = { "linkml_meta": {'alias': 'governing_body', 'domain_of': ['ShariahComplianceFramework']} })
    compliance_standards: list[str] = Field(default=..., description="""List of compliance standards and requirements""", json_schema_extra = { "linkml_meta": {'alias': 'compliance_standards', 'domain_of': ['ShariahComplianceFramework']} })
    effective_date: Optional[date] = Field(default=None, description="""Date when the framework becomes effective""", json_schema_extra = { "linkml_meta": {'alias': 'effective_date', 'domain_of': ['ShariahComplianceFramework']} })
    version: Optional[str] = Field(default=None, description="""Version number of the framework""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['ShariahComplianceFramework']} })
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
    Document containing audit findings and recommendations
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fabio:Report',
         'from_schema': 'https://example.org/schemas/mudarabah-wakalah-hybrid-shariah-audit',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'audit_opinion': {'name': 'audit_opinion', 'required': True},
                        'findings': {'name': 'findings', 'required': True},
                        'report_date': {'name': 'report_date', 'required': True},
                        'report_id': {'identifier': True,
                                      'name': 'report_id',
                                      'required': True}}})

    report_id: str = Field(default=..., description="""Unique identifier for the audit report""", json_schema_extra = { "linkml_meta": {'alias': 'report_id', 'domain_of': ['AuditReport']} })
    report_date: date = Field(default=..., description="""Date when the report was issued""", json_schema_extra = { "linkml_meta": {'alias': 'report_date', 'domain_of': ['AuditReport']} })
    audit_opinion: AuditOpinionEnum = Field(default=..., description="""Auditor's opinion on compliance status""", json_schema_extra = { "linkml_meta": {'alias': 'audit_opinion', 'domain_of': ['AuditReport']} })
    findings: list[str] = Field(default=..., description="""Detailed audit findings""", json_schema_extra = { "linkml_meta": {'alias': 'findings', 'domain_of': ['AuditReport']} })
    recommendations: Optional[list[str]] = Field(default=None, description="""Recommendations for addressing findings""", json_schema_extra = { "linkml_meta": {'alias': 'recommendations', 'domain_of': ['AuditReport']} })
    report_status: Optional[ReportStatusEnum] = Field(default=None, description="""Current status of the report""", json_schema_extra = { "linkml_meta": {'alias': 'report_status', 'domain_of': ['AuditReport']} })
    references_framework: Optional[list[str]] = Field(default=None, description="""Links audit report to referenced compliance framework""", json_schema_extra = { "linkml_meta": {'alias': 'references_framework', 'domain_of': ['AuditReport']} })
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


class ContractTerms(ProvenanceFields):
    """
    Structured vocabulary of terms and conditions in Shariah contracts
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'skos:ConceptScheme',
         'from_schema': 'https://example.org/schemas/mudarabah-wakalah-hybrid-shariah-audit',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'term_category': {'name': 'term_category', 'required': True},
                        'term_id': {'identifier': True,
                                    'name': 'term_id',
                                    'required': True},
                        'term_name': {'name': 'term_name', 'required': True},
                        'term_value': {'name': 'term_value', 'required': True}}})

    term_id: str = Field(default=..., description="""Unique identifier for the contract term""", json_schema_extra = { "linkml_meta": {'alias': 'term_id', 'domain_of': ['ContractTerms']} })
    term_name: str = Field(default=..., description="""Name of the contract term""", json_schema_extra = { "linkml_meta": {'alias': 'term_name', 'domain_of': ['ContractTerms']} })
    term_value: str = Field(default=..., description="""Value or content of the term""", json_schema_extra = { "linkml_meta": {'alias': 'term_value', 'domain_of': ['ContractTerms']} })
    term_category: str = Field(default=..., description="""Category classification of the term""", json_schema_extra = { "linkml_meta": {'alias': 'term_category', 'domain_of': ['ContractTerms']} })
    term_description: Optional[str] = Field(default=None, description="""Detailed description of the term""", json_schema_extra = { "linkml_meta": {'alias': 'term_description', 'domain_of': ['ContractTerms']} })
    is_mandatory: Optional[bool] = Field(default=None, description="""Whether the term is mandatory for compliance""", json_schema_extra = { "linkml_meta": {'alias': 'is_mandatory', 'domain_of': ['ContractTerms']} })
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
MudarabahContract.model_rebuild()
WakalahContract.model_rebuild()
HybridShariahContract.model_rebuild()
ShariahComplianceFramework.model_rebuild()
AuditReport.model_rebuild()
ContractTerms.model_rebuild()

