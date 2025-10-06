"""Provenance field mixins for graph nodes and edges.

These mixins provide standardized provenance tracking for all entities and relationships
in the knowledge graph, enabling citation, validation, and temporal queries.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class NodeProv(BaseModel):
    """Base mixin for all graph nodes with provenance tracking.

    Attributes:
        node_id: Unique identifier for this node (deterministic SHA1 hash)
        entity_type: Business/logical entity type (e.g., "Invoice", "Budget")
        episode_ids: Source episodes that created/mentioned this node
        created_at: When this node was first created
        valid_at: When this data became valid/true
        invalid_at: When this data became invalid (None = still valid)
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        arbitrary_types_allowed=False,
    )

    node_id: str = Field(
        ...,
        description="Unique identifier for a node",
    )

    entity_type: str = Field(
        ...,
        description="Business/logical entity type",
    )

    episode_ids: Optional[List[str]] = Field(
        default=None,
        description="Source episodes that created/mentioned this node",
    )

    created_at: Optional[datetime] = Field(
        default=None,
        description="When this node was first created",
    )

    valid_at: Optional[datetime] = Field(
        default=None,
        description="When this data became valid/true",
    )

    invalid_at: Optional[datetime] = Field(
        default=None,
        description="When this data became invalid (None = still valid)",
    )


class EdgeProv(BaseModel):
    """Base mixin for all graph edges with provenance tracking.

    Attributes:
        edge_id: Unique identifier for this edge (deterministic SHA1 hash)
        relation_type: Relationship type (e.g., "WITHIN_BUDGET", "FROM_VENDOR")
        episode_ids: Source episodes that created/mentioned this relationship
        created_at: When this relationship was first created
        valid_at: When this relationship became valid/true
        invalid_at: When this relationship became invalid (None = still valid)
        expired_at: When this relationship expired (for time-bounded relationships)
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        arbitrary_types_allowed=False,
    )

    edge_id: str = Field(
        ...,
        description="Unique identifier for an edge",
    )

    relation_type: str = Field(
        ...,
        description="Relationship type",
    )

    episode_ids: Optional[List[str]] = Field(
        default=None,
        description="Source episodes that created/mentioned this relationship",
    )

    created_at: Optional[datetime] = Field(
        default=None,
        description="When this relationship was first created",
    )

    valid_at: Optional[datetime] = Field(
        default=None,
        description="When this relationship became valid/true",
    )

    invalid_at: Optional[datetime] = Field(
        default=None,
        description="When this relationship became invalid (None = still valid)",
    )

    expired_at: Optional[datetime] = Field(
        default=None,
        description="When this relationship expired",
    )
