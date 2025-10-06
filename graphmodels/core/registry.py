"""Type registries for managing entity and edge types."""

from typing import Dict, Set, Type, Optional, List
from collections import defaultdict
from .base import ModelBase


class EntityTypeRegistry:
    """Registry for tracking entity types and their Pydantic models.

    This enables:
    1. Dynamic model loading from generated code
    2. Metadata stamping for Graphiti (entity_type field)
    3. Type validation during ingestion
    """

    def __init__(self):
        self._types: Dict[str, Type[ModelBase]] = {}
        self._canonical_uris: Dict[str, str] = {}

    def register(
        self,
        entity_type: str,
        model_class: Type[ModelBase],
        canonical_uri: Optional[str] = None,
    ) -> None:
        """Register an entity type with its Pydantic model.

        Args:
            entity_type: Entity type name (e.g., "Paragraph", "Allocation")
            model_class: Pydantic model class
            canonical_uri: Optional canonical URI (e.g., "http://purl.org/spar/doco/Paragraph")
        """
        self._types[entity_type] = model_class
        if canonical_uri:
            self._canonical_uris[entity_type] = canonical_uri

    def get_model(self, entity_type: str) -> Optional[Type[ModelBase]]:
        """Get the Pydantic model for an entity type.

        Args:
            entity_type: Entity type name

        Returns:
            Pydantic model class or None if not registered
        """
        return self._types.get(entity_type)

    def get_uri(self, entity_type: str) -> Optional[str]:
        """Get the canonical URI for an entity type.

        Args:
            entity_type: Entity type name

        Returns:
            Canonical URI or None if not set
        """
        return self._canonical_uris.get(entity_type)

    def list_types(self) -> List[str]:
        """List all registered entity types.

        Returns:
            List of entity type names
        """
        return sorted(self._types.keys())

    def clear(self) -> None:
        """Clear all registered types."""
        self._types.clear()
        self._canonical_uris.clear()


class EdgeTypeRegistry:
    """Registry for tracking edge types and their valid node type combinations.

    This enables:
    1. Validation of edge creation (valid source/target types)
    2. Metadata stamping for edges
    3. Edge type mapping for Graphiti
    """

    def __init__(self):
        # edge_type -> list of (source_type, target_type) tuples
        self._valid_combinations: Dict[str, List[tuple[str, str]]] = defaultdict(list)
        self._canonical_uris: Dict[str, str] = {}

    def register(
        self,
        edge_type: str,
        source_type: str,
        target_type: str,
        canonical_uri: Optional[str] = None,
    ) -> None:
        """Register an edge type with valid source/target combination.

        Args:
            edge_type: Edge type name (e.g., "BasedOn", "IsPartOf")
            source_type: Valid source entity type
            target_type: Valid target entity type
            canonical_uri: Optional canonical URI (e.g., "http://purl.org/dc/terms/isPartOf")
        """
        self._valid_combinations[edge_type].append((source_type, target_type))
        if canonical_uri:
            self._canonical_uris[edge_type] = canonical_uri

    def is_valid(self, edge_type: str, source_type: str, target_type: str) -> bool:
        """Check if an edge type is valid for given source/target types.

        Args:
            edge_type: Edge type name
            source_type: Source entity type
            target_type: Target entity type

        Returns:
            True if combination is valid, False otherwise
        """
        if edge_type not in self._valid_combinations:
            return False
        return (source_type, target_type) in self._valid_combinations[edge_type]

    def get_uri(self, edge_type: str) -> Optional[str]:
        """Get the canonical URI for an edge type.

        Args:
            edge_type: Edge type name

        Returns:
            Canonical URI or None if not set
        """
        return self._canonical_uris.get(edge_type)

    def list_types(self) -> List[str]:
        """List all registered edge types.

        Returns:
            List of edge type names
        """
        return sorted(self._valid_combinations.keys())

    def get_valid_targets(self, edge_type: str, source_type: str) -> Set[str]:
        """Get valid target types for a given edge type and source type.

        Args:
            edge_type: Edge type name
            source_type: Source entity type

        Returns:
            Set of valid target entity types
        """
        if edge_type not in self._valid_combinations:
            return set()

        return {
            target
            for source, target in self._valid_combinations[edge_type]
            if source == source_type
        }

    def clear(self) -> None:
        """Clear all registered edge types."""
        self._valid_combinations.clear()
        self._canonical_uris.clear()


# Global registries (will be populated by generated code or domain models)
ENTITY_TYPES = EntityTypeRegistry()
EDGE_TYPES = EdgeTypeRegistry()
