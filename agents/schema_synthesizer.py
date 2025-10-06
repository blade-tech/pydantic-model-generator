"""Schema synthesizer using Instructor-guarded LLM to generate LinkML overlays.

For MVP: Requires LLM API key (OpenAI or Anthropic). Fails explicitly if missing.
"""

import os
import json
from typing import List, Optional, Dict, Any
from pathlib import Path
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv
import instructor

load_dotenv()


class LinkMLClass(BaseModel):
    """LinkML class specification."""

    name: str = Field(..., description="Class name in PascalCase")
    description: str = Field(..., description="Class description")
    mixins: List[str] = Field(
        default_factory=lambda: ["NodeProv"],
        description="Mixins to include (default: NodeProv)",
    )
    slots: List[str] = Field(..., description="Slot names for this class")


class LinkMLAssociation(BaseModel):
    """LinkML association/edge specification."""

    name: str = Field(..., description="Association name in PascalCase")
    description: str = Field(..., description="Association description")
    subject: str = Field(..., description="Source class name")
    object: str = Field(..., description="Target class name (use 'object' not 'target')")
    slot_uri: Optional[str] = Field(
        None, description="Optional canonical URI (e.g., 'dcterms:isPartOf')"
    )


class LinkMLSchemaSpec(BaseModel):
    """Complete LinkML schema overlay specification from Instructor."""

    schema_name: str = Field(..., description="Schema name in snake_case")
    description: str = Field(..., description="Schema purpose")
    classes: List[LinkMLClass] = Field(
        ..., description="Entity classes (max 12)", max_length=12
    )
    associations: List[LinkMLAssociation] = Field(
        ..., description="Relationships/edges (max 10)", max_length=10
    )

    @field_validator("schema_name")
    @classmethod
    def validate_schema_name(cls, v: str) -> str:
        """Ensure schema name is snake_case."""
        if not v.islower() or " " in v:
            raise ValueError("Schema name must be snake_case with no spaces")
        return v

    @field_validator("classes")
    @classmethod
    def validate_class_names(cls, v: List[LinkMLClass]) -> List[LinkMLClass]:
        """Ensure class names are PascalCase."""
        for cls_spec in v:
            if not cls_spec.name[0].isupper():
                raise ValueError(f"Class name must be PascalCase: {cls_spec.name}")
        return v


class EvidenceQueryPlan(BaseModel):
    """Evidence Query Plan - maps questions to evidence types."""

    question: str = Field(..., description="The question to answer")
    required_entities: List[str] = Field(
        ..., description="Entity types needed to answer this question"
    )
    required_edges: List[str] = Field(
        ..., description="Edge types needed to traverse for this question"
    )
    metadata_filters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata filters to apply (e.g., {entity_type: 'Paragraph'})",
    )


class SchemaSynthesizer:
    """Synthesizes LinkML schema overlays using Instructor-guarded LLM."""

    def __init__(self, provider: str = "anthropic"):
        """Initialize schema synthesizer.

        Args:
            provider: LLM provider ('openai' or 'anthropic')

        Raises:
            ValueError: If API key missing or provider invalid
        """
        self.provider = provider

        if provider == "openai":
            import openai

            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY not found. Add to .env or set environment variable."
                )
            self.client = instructor.from_openai(openai.OpenAI(api_key=api_key))
            self.model = "gpt-4o"

        elif provider == "anthropic":
            import anthropic

            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError(
                    "ANTHROPIC_API_KEY not found. Add to .env or set environment variable."
                )
            self.client = instructor.from_anthropic(
                anthropic.Anthropic(api_key=api_key)
            )
            self.model = "claude-3-5-sonnet-20241022"

        else:
            raise ValueError(f"Invalid provider: {provider}. Use 'openai' or 'anthropic'")

    def synthesize_schema(
        self,
        outcome_spec_path: Path,
        ontology_refs: Optional[Dict[str, Any]] = None,
    ) -> LinkMLSchemaSpec:
        """Synthesize LinkML schema from OutcomeSpec.

        Args:
            outcome_spec_path: Path to OutcomeSpec YAML
            ontology_refs: Optional ontology references from retriever

        Returns:
            Validated LinkML schema specification

        Raises:
            ValueError: If synthesis fails or constraints violated
        """
        from dsl.loader import load_outcome_spec

        # Load OutcomeSpec
        spec = load_outcome_spec(outcome_spec_path)

        # Build prompt
        prompt = self._build_synthesis_prompt(spec, ontology_refs)

        # Call LLM with Instructor validation
        try:
            schema_spec = self.client.chat.completions.create(
                model=self.model,
                response_model=LinkMLSchemaSpec,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a LinkML schema expert. Generate minimal, outcome-driven schemas.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_retries=3,
            )

            print(f"Generated schema: {schema_spec.schema_name}")
            print(f"  Classes: {len(schema_spec.classes)}")
            print(f"  Associations: {len(schema_spec.associations)}")

            return schema_spec

        except Exception as e:
            raise ValueError(f"Schema synthesis failed: {e}") from e

    def _build_synthesis_prompt(
        self, spec, ontology_refs: Optional[Dict[str, Any]]
    ) -> str:
        """Build prompt for LLM schema synthesis."""
        prompt = f"""Generate a minimal LinkML schema overlay for this business outcome:

**Outcome:** {spec.outcome_name}
**Context:** {spec.context_summary}

**Questions to Answer:**
{chr(10).join(f"- {q}" for q in spec.queries_we_must_answer)}

**Required Evidence:**
{chr(10).join(f"- {ev.name}: {', '.join(ev.must_have_slots)}" for ev in spec.required_evidence)}

**Target Entities:**
{chr(10).join(f"- {ent.name}: {', '.join(ent.must_have_slots)}" for ent in spec.target_entities)}

**Relations:**
{chr(10).join(f"- {rel.name}: {rel.subject} -> {rel.object}" for rel in spec.relations)}

**Constraints:**
- Import core.yaml for NodeProv/EdgeProv mixins
- Maximum 12 classes, 10 associations
- PascalCase edge names: {spec.graphiti_constraints.edge_names_pascal_case}
- Use entity_type metadata: {spec.graphiti_constraints.use_entity_type_metadata}

**Ontology Alignment:**
"""

        if ontology_refs:
            for prefix, data in ontology_refs.items():
                prompt += f"\n- {prefix}: {data.get('base_uri', 'N/A')}"
        else:
            prompt += "\nNo external ontologies provided."

        prompt += "\n\nGenerate a schema with ONLY the classes and associations needed to answer the stated questions."

        return prompt

    def generate_evidence_query_plan(
        self, outcome_spec_path: Path, schema_spec: LinkMLSchemaSpec
    ) -> List[EvidenceQueryPlan]:
        """Generate Evidence Query Plan mapping questions to schema elements.

        Args:
            outcome_spec_path: Path to OutcomeSpec YAML
            schema_spec: Generated LinkML schema specification

        Returns:
            List of evidence query plans, one per question
        """
        from dsl.loader import load_outcome_spec

        spec = load_outcome_spec(outcome_spec_path)

        plans = []
        for question in spec.queries_we_must_answer:
            prompt = f"""Given this question and schema, identify the evidence needed:

**Question:** {question}

**Available Classes:** {', '.join(c.name for c in schema_spec.classes)}
**Available Associations:** {', '.join(a.name for a in schema_spec.associations)}

Which entities and edges are needed to answer this question?
"""

            plan = self.client.chat.completions.create(
                model=self.model,
                response_model=EvidenceQueryPlan,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at mapping questions to graph queries.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_retries=2,
            )

            plans.append(plan)

        return plans

    def save_schema_yaml(
        self, schema_spec: LinkMLSchemaSpec, output_path: Path
    ) -> None:
        """Convert LinkMLSchemaSpec to YAML and save.

        Args:
            schema_spec: LinkML schema specification
            output_path: Path to save YAML file
        """
        import yaml

        # Build LinkML YAML structure
        linkml_dict = {
            "id": f"https://example.org/graphmodels/{schema_spec.schema_name}",
            "name": schema_spec.schema_name,
            "description": schema_spec.description,
            "imports": ["../core"],
            "classes": {},
        }

        # Add classes
        for cls in schema_spec.classes:
            linkml_dict["classes"][cls.name] = {
                "description": cls.description,
                "mixins": cls.mixins,
                "attributes": {slot: {"range": "string"} for slot in cls.slots},
            }

        # Add associations
        for assoc in schema_spec.associations:
            edge_attrs = {
                "range": assoc.object,
                "inlined": False,
            }
            if assoc.slot_uri:
                edge_attrs["slot_uri"] = assoc.slot_uri

            # Use subject class as container for the association
            if assoc.subject in linkml_dict["classes"]:
                if "attributes" not in linkml_dict["classes"][assoc.subject]:
                    linkml_dict["classes"][assoc.subject]["attributes"] = {}

                linkml_dict["classes"][assoc.subject]["attributes"][
                    assoc.name.lower()
                ] = edge_attrs

        # Save YAML
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(linkml_dict, f, default_flow_style=False, sort_keys=False)

        print(f"Saved LinkML schema to: {output_path}")


async def synthesize_schema_for_outcome(
    outcome_spec_path: Path,
    ontology_refs_path: Optional[Path] = None,
    overlay_output_path: Path = Path("schemas/overlays/overlay.yaml"),
    eqp_output_path: Path = Path("artifacts/eqp.json"),
    provider: str = "anthropic",
) -> LinkMLSchemaSpec:
    """Convenience function to synthesize schema from OutcomeSpec.

    Args:
        outcome_spec_path: Path to OutcomeSpec YAML
        ontology_refs_path: Optional path to ontology refs JSON
        overlay_output_path: Path to save LinkML overlay YAML
        eqp_output_path: Path to save Evidence Query Plan JSON
        provider: LLM provider ('openai' or 'anthropic')

    Returns:
        LinkML schema specification
    """
    # Load ontology refs if provided
    ontology_refs = None
    if ontology_refs_path and ontology_refs_path.exists():
        with open(ontology_refs_path, encoding="utf-8") as f:
            ontology_refs = json.load(f)

    # Synthesize schema
    synthesizer = SchemaSynthesizer(provider=provider)
    schema_spec = synthesizer.synthesize_schema(outcome_spec_path, ontology_refs)

    # Generate Evidence Query Plan
    eqp = synthesizer.generate_evidence_query_plan(outcome_spec_path, schema_spec)

    # Save LinkML YAML
    synthesizer.save_schema_yaml(schema_spec, overlay_output_path)

    # Save EQP JSON
    eqp_output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(eqp_output_path, "w", encoding="utf-8") as f:
        json.dump([p.model_dump() for p in eqp], f, indent=2)
    print(f"Saved Evidence Query Plan to: {eqp_output_path}")

    return schema_spec
