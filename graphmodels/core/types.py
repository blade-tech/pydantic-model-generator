"""Type protocols for graph access and operations."""

from typing import Protocol, List, Dict, Any, Optional


class GraphAccessor(Protocol):
    """Protocol for graph database access.

    Defines the interface that graph adapters (Graphiti, Neo4j, mock) must implement.
    """

    async def add_node(
        self,
        node_id: str,
        entity_type: str,
        properties: Dict[str, Any],
        group_id: Optional[str] = None,
    ) -> None:
        """Add a node to the graph.

        Args:
            node_id: Unique node identifier
            entity_type: Type of entity (used for metadata stamping)
            properties: Node properties
            group_id: Optional group/namespace identifier
        """
        ...

    async def add_edge(
        self,
        rel_id: str,
        edge_type: str,
        source_id: str,
        target_id: str,
        properties: Dict[str, Any],
        group_id: Optional[str] = None,
    ) -> None:
        """Add an edge to the graph.

        Args:
            rel_id: Unique relationship identifier
            edge_type: Type of relationship
            source_id: Source node ID
            target_id: Target node ID
            properties: Edge properties
            group_id: Optional group/namespace identifier
        """
        ...

    async def search(
        self,
        query: str,
        k: int = 8,
        filters: Optional[Dict[str, Any]] = None,
        group_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Search the graph with hybrid retrieval.

        Args:
            query: Search query text
            k: Number of results to return
            filters: Optional metadata filters
            group_id: Optional group/namespace filter

        Returns:
            List of matching nodes with scores
        """
        ...

    async def get_node(
        self,
        node_id: str,
        group_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Retrieve a specific node by ID.

        Args:
            node_id: Node identifier
            group_id: Optional group/namespace filter

        Returns:
            Node properties or None if not found
        """
        ...
