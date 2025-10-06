"""OutcomeSpec DSL - Pydantic schema for defining business outcomes.

This module provides the schema for specifying business outcomes that drive
the LinkML schema generation process. An OutcomeSpec captures:
- What business outcome we need
- What evidence is required
- What queries must be answerable
- What entities and relationships exist
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class EvidenceSpec(BaseModel):
    """Specification for required evidence to support an outcome."""

    name: str = Field(..., description="Name of the evidence type")
    description: str = Field(..., description="What this evidence represents")
    must_have_slots: List[str] = Field(
        default_factory=list, description="Required slots/fields for this evidence"
    )


class EntitySpec(BaseModel):
    """Specification for a target entity in the outcome."""

    name: str = Field(..., description="Entity class name")
    description: str = Field(..., description="What this entity represents")
    must_have_slots: Optional[List[str]] = Field(
        default=None, description="Required slots/fields for this entity"
    )


class RelationSpec(BaseModel):
    """Specification for a relationship/edge between entities."""

    name: str = Field(..., description="Relationship name (PascalCase)")
    subject: str = Field(..., description="Source entity type")
    object: str = Field(..., description="Target entity type")
    description: Optional[str] = Field(default=None, description="What this relationship means")


class OntologyHint(BaseModel):
    """Reference to external ontologies for semantic alignment."""

    prefix: str = Field(..., description="Ontology prefix (e.g., 'dcterms', 'prov')")
    base_uri: str = Field(..., description="Base URI for the ontology")
    include_classes: Optional[List[str]] = Field(
        default=None,
        description="Specific classes to include from this ontology (empty = all relevant)",
    )


class GraphitiConstraints(BaseModel):
    """Constraints specific to Graphiti graph storage."""

    use_entity_type_metadata: bool = Field(
        default=True, description="Store business type in entity_type metadata (Graphiti workaround)"
    )
    edge_names_pascal_case: bool = Field(
        default=True, description="Enforce PascalCase naming for edge types"
    )
    stamp_uri_on_edges: bool = Field(
        default=True,
        description="Stamp canonical URI on edges when aligned to standards",
    )


class OutcomeSpec(BaseModel):
    """Complete specification for a business outcome.

    This drives the entire pipeline:
    1. LLM reads this to generate LinkML overlay
    2. LinkML generates Pydantic models
    3. Models enable ingestion and retrieval
    4. Retrieval enables answering the specified questions
    """

    outcome_name: str = Field(..., description="Name of the business outcome")
    context_summary: str = Field(
        ..., description="Brief context explaining what this outcome achieves"
    )
    required_evidence: List[EvidenceSpec] = Field(
        ..., description="Evidence types required to support this outcome"
    )
    queries_we_must_answer: List[str] = Field(
        ..., description="Natural language questions this schema must enable answering"
    )
    target_entities: List[EntitySpec] = Field(
        default_factory=list, description="Key entities for this outcome"
    )
    relations: List[RelationSpec] = Field(
        default_factory=list, description="Relationships between entities"
    )
    ontologies: List[OntologyHint] = Field(
        default_factory=list, description="External ontologies to align with"
    )
    graphiti_constraints: GraphitiConstraints = Field(
        default_factory=GraphitiConstraints, description="Graphiti-specific constraints"
    )

    def summary(self) -> str:
        """Generate a summary table of the outcome spec."""
        lines = [
            f"Outcome: {self.outcome_name}",
            f"Context: {self.context_summary}",
            f"\nRequired Evidence ({len(self.required_evidence)}):",
        ]

        for ev in self.required_evidence:
            slots = ", ".join(ev.must_have_slots) if ev.must_have_slots else "none specified"
            lines.append(f"  - {ev.name}: {ev.description}")
            lines.append(f"    Slots: {slots}")

        lines.append(f"\nQueries to Answer ({len(self.queries_we_must_answer)}):")
        for q in self.queries_we_must_answer:
            lines.append(f"  - {q}")

        lines.append(f"\nTarget Entities ({len(self.target_entities)}):")
        for ent in self.target_entities:
            lines.append(f"  - {ent.name}: {ent.description}")

        lines.append(f"\nRelationships ({len(self.relations)}):")
        for rel in self.relations:
            lines.append(f"  - {rel.name}: {rel.subject} -> {rel.object}")

        if self.ontologies:
            lines.append(f"\nOntologies ({len(self.ontologies)}):")
            for ont in self.ontologies:
                lines.append(f"  - {ont.prefix}: {ont.base_uri}")

        return "\n".join(lines)
