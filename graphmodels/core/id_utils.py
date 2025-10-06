"""Deterministic ID generation utilities for graph nodes and edges."""

import hashlib
from typing import List, Optional


def generate_text_hash(text: str) -> str:
    """Generate SHA1 hash of text content.

    Args:
        text: Text to hash

    Returns:
        SHA1 hash as hexadecimal string
    """
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def generate_node_id(
    entity_type: str,
    key_fields: dict,
    group_id: Optional[str] = None,
) -> str:
    """Generate deterministic node ID from entity type and key fields.

    Args:
        entity_type: The entity type (e.g., "Paragraph", "Allocation")
        key_fields: Dictionary of key fields that uniquely identify this node
        group_id: Optional group ID for namespace isolation

    Returns:
        Deterministic node ID string

    Example:
        >>> generate_node_id("Paragraph", {"doc_id": "SS-59", "ordinal": 45})
        'Paragraph:SS-59:45'
        >>> generate_node_id("Allocation", {"team": "Alpha", "project": "Daytona"}, "BRIEF-2024")
        'BRIEF-2024:Allocation:Alpha:Daytona'
    """
    # Sort key fields for deterministic ordering
    sorted_keys = sorted(key_fields.items())
    key_values = [str(v) for k, v in sorted_keys]

    if group_id:
        parts = [group_id, entity_type] + key_values
    else:
        parts = [entity_type] + key_values

    return ":".join(parts)


def generate_edge_id(
    edge_type: str,
    source_id: str,
    target_id: str,
    group_id: Optional[str] = None,
) -> str:
    """Generate deterministic edge ID from edge type and node IDs.

    Args:
        edge_type: The edge/relationship type (e.g., "BasedOn", "ConstrainedBy")
        source_id: Source node ID
        target_id: Target node ID
        group_id: Optional group ID for namespace isolation

    Returns:
        Deterministic edge ID string

    Example:
        >>> generate_edge_id("BasedOn", "Allocation:A1", "TeamCapacity:TC1")
        'BasedOn:Allocation:A1=>TeamCapacity:TC1'
    """
    if group_id:
        return f"{group_id}:{edge_type}:{source_id}=>{target_id}"
    else:
        return f"{edge_type}:{source_id}=>{target_id}"


def compute_support_ids(text: str, support_count: int = 1) -> List[str]:
    """Compute support IDs for evidence tracking.

    Args:
        text: The text content providing support
        support_count: Number of questions this text supports

    Returns:
        List of support IDs (currently just text hash)
    """
    text_hash = generate_text_hash(text)
    return [f"SUPPORT:{text_hash}"]
