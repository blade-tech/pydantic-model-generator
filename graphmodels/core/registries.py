"""
Central registries for domain models.

Provides:
1. Global entity and edge registries
2. Domain registration functions
3. Model lookup utilities
"""

from typing import Dict, Type, Optional
from pydantic import BaseModel


# Global registries
_ENTITY_REGISTRY: Dict[str, Type[BaseModel]] = {}
_EDGE_REGISTRY: Dict[str, Type[BaseModel]] = {}
_DOMAIN_REGISTRY: Dict[str, dict] = {}


def register_domain(
    domain_name: str,
    entities: Dict[str, Type[BaseModel]],
    edges: Dict[str, Type[BaseModel]],
) -> None:
    """
    Register a domain's models with the global registry.

    Args:
        domain_name: Name of the domain (e.g., 'business', 'aaoifi')
        entities: Dictionary mapping entity type strings to model classes
        edges: Dictionary mapping relation type strings to model classes

    Example:
        >>> from generated.pydantic.business_glue import BUSINESS_ENTITIES, BUSINESS_EDGES
        >>> register_domain('business', BUSINESS_ENTITIES, BUSINESS_EDGES)
    """
    # Register entities
    for entity_type, model_cls in entities.items():
        if entity_type in _ENTITY_REGISTRY:
            raise ValueError(
                f"Entity type '{entity_type}' already registered by domain "
                f"'{_get_domain_for_entity(entity_type)}'"
            )
        _ENTITY_REGISTRY[entity_type] = model_cls

    # Register edges
    for relation_type, model_cls in edges.items():
        if relation_type in _EDGE_REGISTRY:
            raise ValueError(
                f"Relation type '{relation_type}' already registered by domain "
                f"'{_get_domain_for_edge(relation_type)}'"
            )
        _EDGE_REGISTRY[relation_type] = model_cls

    # Register domain metadata
    _DOMAIN_REGISTRY[domain_name] = {
        "entities": list(entities.keys()),
        "edges": list(edges.keys()),
    }


def get_entity_model(entity_type: str) -> Optional[Type[BaseModel]]:
    """
    Get Pydantic model class for a given entity type.

    Args:
        entity_type: Entity type string (e.g., 'BusinessOutcome', 'Document')

    Returns:
        Pydantic model class or None if not found

    Example:
        >>> model_cls = get_entity_model('BusinessOutcome')
        >>> if model_cls:
        ...     instance = model_cls(node_id='123', entity_type='BusinessOutcome')
    """
    return _ENTITY_REGISTRY.get(entity_type)


def get_edge_model(relation_type: str) -> Optional[Type[BaseModel]]:
    """
    Get Pydantic model class for a given relationship type.

    Args:
        relation_type: Relationship type string (e.g., 'Requires', 'Cites')

    Returns:
        Pydantic model class or None if not found

    Example:
        >>> model_cls = get_edge_model('Requires')
        >>> if model_cls:
        ...     instance = model_cls(rel_id='rel-123', relation_type='Requires')
    """
    return _EDGE_REGISTRY.get(relation_type)


def list_entity_types() -> list[str]:
    """List all registered entity types across all domains."""
    return list(_ENTITY_REGISTRY.keys())


def list_edge_types() -> list[str]:
    """List all registered edge/relationship types across all domains."""
    return list(_EDGE_REGISTRY.keys())


def list_domains() -> list[str]:
    """List all registered domains."""
    return list(_DOMAIN_REGISTRY.keys())


def get_domain_info(domain_name: str) -> Optional[dict]:
    """
    Get metadata for a registered domain.

    Args:
        domain_name: Name of the domain

    Returns:
        Dict with 'entities' and 'edges' lists, or None if not found
    """
    return _DOMAIN_REGISTRY.get(domain_name)


def _get_domain_for_entity(entity_type: str) -> Optional[str]:
    """Find which domain registered a given entity type."""
    for domain_name, metadata in _DOMAIN_REGISTRY.items():
        if entity_type in metadata["entities"]:
            return domain_name
    return None


def _get_domain_for_edge(relation_type: str) -> Optional[str]:
    """Find which domain registered a given edge type."""
    for domain_name, metadata in _DOMAIN_REGISTRY.items():
        if relation_type in metadata["edges"]:
            return domain_name
    return None


__all__ = [
    "register_domain",
    "get_entity_model",
    "get_edge_model",
    "list_entity_types",
    "list_edge_types",
    "list_domains",
    "get_domain_info",
]
