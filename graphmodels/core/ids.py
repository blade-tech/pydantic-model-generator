"""Deterministic ID generation utilities for stable, reproducible node and edge identifiers.

These utilities ensure that identical content always produces the same ID, enabling:
- Stable citations across pipeline runs
- Deduplication of identical entities
- Reproducible graph structures
- Content-addressable storage
"""

import hashlib
import base64
import re
import unicodedata
from typing import Optional


def normalize_text(text: str) -> str:
    """Normalize text for stable hashing.

    Applies:
    - NFKD Unicode normalization
    - ASCII conversion (removing accents)
    - Lowercase conversion
    - Whitespace normalization
    - Removal of non-alphanumeric characters (except space, underscore, colon, slash, period, hyphen, hash)

    Args:
        text: Text to normalize

    Returns:
        Normalized text suitable for stable hashing
    """
    if not text:
        return ""

    # Unicode normalization and ASCII conversion
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    # Lowercase and whitespace normalization
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)

    # Keep only safe characters
    text = re.sub(r"[^a-z0-9 _:/.\-#]", "", text)

    return text


def sha1_hash_base64(text: str) -> str:
    """Generate URL-safe base64-encoded SHA1 hash.

    Args:
        text: Text to hash

    Returns:
        URL-safe base64 string without padding
    """
    digest = hashlib.sha1(text.encode("utf-8")).digest()
    b64 = base64.urlsafe_b64encode(digest).decode("ascii")
    return b64.rstrip("=")  # Remove padding


def sha1_hash_hex(text: str) -> str:
    """Generate hexadecimal SHA1 hash.

    Args:
        text: Text to hash

    Returns:
        40-character hex string
    """
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def make_node_id(
    entity_type: str,
    label: str,
    anchor: Optional[str] = None,
    use_hex: bool = False
) -> str:
    """Generate deterministic node ID from entity type, label, and optional anchor.

    The ID is stable across runs for identical inputs, enabling deduplication
    and stable citations.

    Args:
        entity_type: Type of entity (e.g., "Invoice", "Budget", "Paragraph")
        label: Primary label/name for the entity
        anchor: Optional additional discriminator (e.g., department, timestamp)
        use_hex: If True, use hex encoding instead of base64

    Returns:
        Stable node ID in format: node:{type}:{hash}

    Examples:
        >>> make_node_id("Invoice", "INV-001", "engineering")
        'node:invoice:X9k2...'
        >>> make_node_id("Budget", "Q1-2024", None)
        'node:budget:7Hj3...'
    """
    # Normalize components
    norm_type = normalize_text(entity_type)
    norm_label = normalize_text(label)
    norm_anchor = normalize_text(anchor) if anchor else ""

    # Create composite key
    composite = f"{norm_type}|{norm_label}|{norm_anchor}"

    # Generate hash
    if use_hex:
        hash_value = sha1_hash_hex(composite)
    else:
        hash_value = sha1_hash_base64(composite)

    return f"node:{norm_type}:{hash_value}"


def make_edge_id(
    relation_type: str,
    source_id: str,
    target_id: str,
    use_hex: bool = False
) -> str:
    """Generate deterministic edge ID from relation type and node IDs.

    The ID is stable across runs for identical relationships, enabling
    deduplication and stable edge citations.

    Args:
        relation_type: Type of relationship (e.g., "WITHIN_BUDGET", "FROM_VENDOR")
        source_id: Source node ID
        target_id: Target node ID
        use_hex: If True, use hex encoding instead of base64

    Returns:
        Stable edge ID in format: rel:{type}:{hash}

    Examples:
        >>> make_edge_id("WITHIN_BUDGET", "node:invoice:abc", "node:budget:xyz")
        'rel:within_budget:K2m9...'
        >>> make_edge_id("FROM_VENDOR", "node:invoice:abc", "node:vendor:def")
        'rel:from_vendor:P7x4...'
    """
    # Normalize relation type
    norm_type = normalize_text(relation_type)

    # Create composite key (source and target IDs are already normalized)
    composite = f"{norm_type}|{source_id}|{target_id}"

    # Generate hash
    if use_hex:
        hash_value = sha1_hash_hex(composite)
    else:
        hash_value = sha1_hash_base64(composite)

    return f"rel:{norm_type}:{hash_value}"


def make_content_hash(content: str, use_hex: bool = True) -> str:
    """Generate content hash for text comparison and deduplication.

    Args:
        content: Text content to hash
        use_hex: If True, use hex encoding (default for content hashes)

    Returns:
        SHA1 hash of content

    Examples:
        >>> make_content_hash("Invoice approved")
        '3f8a...'
    """
    if use_hex:
        return sha1_hash_hex(content)
    else:
        return sha1_hash_base64(content)
