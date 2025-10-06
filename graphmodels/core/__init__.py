"""Core utilities for graph modeling."""

from graphmodels.core.provenance import NodeProv, EdgeProv
from graphmodels.core.ids import (
    make_node_id,
    make_edge_id,
    make_content_hash,
    normalize_text,
)
from graphmodels.core.registries import (
    register_domain,
    get_entity_model,
    get_edge_model,
    list_entity_types,
    list_edge_types,
    list_domains,
    get_domain_info,
)
from graphmodels.core.plugin_loader import (
    discover_domains,
    load_domain,
    load_all_domains,
)

__all__ = [
    # Provenance
    "NodeProv",
    "EdgeProv",

    # IDs
    "make_node_id",
    "make_edge_id",
    "make_content_hash",
    "normalize_text",

    # Registries
    "register_domain",
    "get_entity_model",
    "get_edge_model",
    "list_entity_types",
    "list_edge_types",
    "list_domains",
    "get_domain_info",

    # Plugin Loader
    "discover_domains",
    "load_domain",
    "load_all_domains",
]
