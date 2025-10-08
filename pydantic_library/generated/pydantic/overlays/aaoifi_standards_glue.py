"""AAOIFI standards overlay - Graphiti type registries with canonical ontology URIs.

This module provides type registries for Graphiti integration, enabling
the knowledge graph to validate and route AAOIFI standards entities and edges
using canonical ontology URIs from DoCO, FaBiO, PROV-O, FIBO, and SKOS.

Driven by: specs/aaoifi_standards_extraction.yaml

Canonical ontologies used:
- DoCO (Document Components Ontology): Document structure
- FaBiO (FRBR-aligned Bibliographic Ontology): Document types
- PROV-O (Provenance Ontology): Attribution and derivation
- FIBO (Financial Industry Business Ontology): Financial contracts
- SKOS (Simple Knowledge Organization System): Concepts and terminology
"""
from __future__ import annotations

from typing import Dict, List
from pydantic import BaseModel

# Import all entity and edge classes
from .aaoifi_standards_models import (
    Document,
    Section,
    Paragraph,
    Concept,
    ContractType,
    Rule,
    Agent,
    HasComponent,
    About,
    EvidenceOf,
    AttributedTo,
)

# ==================================================================
# CANONICAL ONTOLOGY URI MAPPINGS
# ==================================================================
# These URIs enable semantic interoperability and RDF export

AAOIFI_NODE_URI: Dict[str, str] = {
    "Document": "http://purl.org/spar/fabio/SpecificationDocument",  # FaBiO
    "Section": "http://purl.org/spar/doco/Section",  # DoCO
    "Paragraph": "http://purl.org/spar/doco/Paragraph",  # DoCO
    "Concept": "http://www.w3.org/2004/02/skos/core#Concept",  # SKOS
    "ContractType": "https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/Contract",  # FIBO
    "Rule": "https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/ContractualElement",  # FIBO
    "Agent": "http://www.w3.org/ns/prov#Agent",  # PROV-O
}

AAOIFI_EDGE_URI: Dict[str, str] = {
    "HasComponent": "http://purl.org/dc/terms/hasPart",  # Dublin Core
    "About": "http://purl.org/dc/terms/subject",  # Dublin Core
    "EvidenceOf": "http://www.w3.org/ns/prov#wasDerivedFrom",  # PROV-O
    "AttributedTo": "http://www.w3.org/ns/prov#wasAttributedTo",  # PROV-O
}

# ==================================================================
# GRAPHITI TYPE REGISTRIES
# ==================================================================

AAOIFI_ENTITY_TYPES: Dict[str, type[BaseModel]] = {
    "Document": Document,
    "Section": Section,
    "Paragraph": Paragraph,
    "Concept": Concept,
    "ContractType": ContractType,
    "Rule": Rule,
    "Agent": Agent,
}

AAOIFI_EDGE_TYPES: Dict[str, type[BaseModel]] = {
    "HasComponent": HasComponent,
    "About": About,
    "EvidenceOf": EvidenceOf,
    "AttributedTo": AttributedTo,
}

# ==================================================================
# CANONICAL EDGE TYPE MAPPINGS
# ==================================================================
# Maps (source_type, target_type) tuples to allowed edge types

AAOIFI_EDGE_TYPE_MAP: Dict[tuple, List[str]] = {
    # Structural hierarchy (Document → Section → Paragraph)
    ("Document", "Section"): ["HasComponent"],
    ("Section", "Paragraph"): ["HasComponent"],

    # Topical tagging (any structural node → Concept/ContractType)
    ("Document", "Concept"): ["About"],
    ("Document", "ContractType"): ["About"],
    ("Section", "Concept"): ["About"],
    ("Section", "ContractType"): ["About"],
    ("Paragraph", "Concept"): ["About"],
    ("Paragraph", "ContractType"): ["About"],

    # Rule provenance (Rule → Paragraph)
    ("Rule", "Paragraph"): ["EvidenceOf"],

    # Document attribution (Document → Agent)
    ("Document", "Agent"): ["AttributedTo"],
}

# ==================================================================
# VALIDATION HELPERS
# ==================================================================

def validate_edge_type(source_type: str, target_type: str, edge_type: str) -> bool:
    """Validate if an edge type is allowed between two entity types.

    Args:
        source_type: Source entity type name
        target_type: Target entity type name
        edge_type: Edge type name

    Returns:
        bool: True if edge type is valid for this entity pair
    """
    allowed_edges = AAOIFI_EDGE_TYPE_MAP.get((source_type, target_type), [])
    return edge_type in allowed_edges


def get_allowed_edges(source_type: str, target_type: str) -> List[str]:
    """Get allowed edge types between two entity types.

    Args:
        source_type: Source entity type name
        target_type: Target entity type name

    Returns:
        List of allowed edge type names (empty if no edges allowed)
    """
    return AAOIFI_EDGE_TYPE_MAP.get((source_type, target_type), [])


def get_entity_uri(entity_type: str) -> str | None:
    """Get canonical ontology URI for an entity type.

    Args:
        entity_type: Entity type name

    Returns:
        Canonical URI string, or None if not found
    """
    return AAOIFI_NODE_URI.get(entity_type)


def get_edge_uri(edge_type: str) -> str | None:
    """Get canonical ontology URI for an edge type.

    Args:
        edge_type: Edge type name

    Returns:
        Canonical URI string, or None if not found
    """
    return AAOIFI_EDGE_URI.get(edge_type)


# ==================================================================
# OUTCOME SPEC METADATA
# ==================================================================

OUTCOME_SPEC_ID = "https://example.org/specs/aaoifi-standards-extraction"
OUTCOME_SPEC_NAME = "aaoifi_standards_extraction"

OUTCOME_QUESTIONS = [
    "What AAOIFI standard documents exist and who issued them?",
    "What is the structural hierarchy of a standard document?",
    "What topical concepts are covered in each section or paragraph?",
    "What normative rules exist and where are they sourced from?",
    "What contract types are defined and what rules apply to them?",
]

# Validation query names from OutcomeSpec
VALIDATION_QUERIES = [
    "test_document_retrieval",
    "test_document_structure",
    "test_topical_tagging",
    "test_rule_provenance",
    "test_contract_type_rules",
]

# ==================================================================
# ONTOLOGY METADATA
# ==================================================================

ONTOLOGY_PREFIXES = {
    "doco": "http://purl.org/spar/doco/",
    "fabio": "http://purl.org/spar/fabio/",
    "prov": "http://www.w3.org/ns/prov#",
    "fibo": "https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "dcterms": "http://purl.org/dc/terms/",
    "foaf": "http://xmlns.com/foaf/0.1/",
}

ONTOLOGY_DOCUMENTATION = {
    "DoCO": "http://www.sparontologies.net/ontologies/doco",
    "FaBiO": "http://www.sparontologies.net/ontologies/fabio",
    "PROV-O": "https://www.w3.org/TR/prov-o/",
    "FIBO": "https://spec.edmcouncil.org/fibo/",
    "SKOS": "https://www.w3.org/TR/skos-reference/",
}
