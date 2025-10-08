"""Default prompt templates for Claude AI services.

These prompts are exposed to users and can be customized.
"""

# Step 2: Ontology Research
ONTOLOGY_RESEARCH_SYSTEM = """You are an expert in knowledge representation and ontology mapping. Analyze the following business outcome and identify the key entities that need to be modeled."""

ONTOLOGY_RESEARCH_TASK = """Task:
1. Identify 2-8 key entities from this business description
2. For each entity, map it to a canonical ontology URI from these standard ontologies:
   - DoCO (Document Components Ontology): http://purl.org/spar/doco/
   - FaBiO (FRBR-aligned Bibliographic Ontology): http://purl.org/spar/fabio/
   - PROV-O (Provenance Ontology): http://www.w3.org/ns/prov#
   - FIBO (Financial Industry Business Ontology): https://spec.edmcouncil.org/fibo/ontology/
   - SKOS (Simple Knowledge Organization System): http://www.w3.org/2004/02/skos/core#

3. Provide a confidence score (0.0-1.0) for each mapping
4. Explain your reasoning for each mapping

Response Format (JSON):
{
  "entities": [
    {
      "entity_name": "string",
      "entity_type": "string",
      "ontology_uri": "string",
      "ontology_source": "string (DoCO|FaBiO|PROV-O|FIBO|SKOS)",
      "confidence": float,
      "reasoning": "string"
    }
  ]
}

Think step by step and show your reasoning."""

ONTOLOGY_RESEARCH_MCP_NOTICE = "\nNote: You have access to MCP tools (web search, documentation lookup) if you need to research domain-specific terminology or verify ontology mappings."


# Step 3: OutcomeSpec Generation
OUTCOME_SPEC_SYSTEM = """You are an expert in creating OutcomeSpecs for outcome-first Pydantic modeling."""

OUTCOME_SPEC_TASK = """Create an OutcomeSpec YAML that defines:
1. Outcome questions (3-5 questions this schema must answer)
2. Target entities (the entities identified above)
3. Validation queries (Cypher queries to test the schema)

OutcomeSpec Template:
```yaml
id: https://example.org/specs/your-outcome-name
name: Your Outcome Name
description: Brief description of the outcome
outcome_questions:
  - question: "What entities do I need to track?"
    target_entities: [Entity1, Entity2]
validation_queries:
  - name: "test_entity_creation"
    cypher: |
      MATCH (e:Entity1)
      RETURN e.field1, e.field2
```

Generate a complete OutcomeSpec for this business outcome."""


# Step 4: LinkML Schema Generation
LINKML_SCHEMA_SYSTEM = """You are an expert in LinkML schema design for Pydantic model generation."""

LINKML_SCHEMA_TASK = """Create a LinkML schema YAML following these CRITICAL RULES:

**CRITICAL RULE #1**: Every slot referenced in a class's `slots:` list MUST be defined in the top-level `slots:` section.
**CRITICAL RULE #2**: Define ALL slots in the `slots:` section BEFORE referencing them in any class.
**CRITICAL RULE #3**: Each slot must have a `range:` (e.g., string, integer, datetime, or an enum/class name).
**CRITICAL RULE #4**: COMPLETE THE SCHEMA - Do not stop mid-way. Prioritize finishing all slot definitions over verbose descriptions.
**CRITICAL RULE #5**: The `id` slot MUST be defined in the `slots:` section if ANY class uses it. Define it as:
```yaml
slots:
  id:
    description: Unique identifier
    range: string
    identifier: true
    required: true
```

⚠️ **COMMON MISTAKE**: Forgetting to define the `id` slot even though ALL classes use it. Check the slots section includes `id`!

⚠️ **OUTPUT PLANNING**: Before generating, count your slots. If you have 8 classes with ~10 slots each, you need ~80 slot definitions. Make descriptions concise to ensure you complete all definitions.

Schema Structure:
1. Metadata (id, name, description, imports, prefixes)
2. Classes section - define entities with `class_uri` and ProvenanceFields mixin
3. Slots section - define ALL fields used by ANY class (THIS IS THE MOST IMPORTANT SECTION)
4. Enums section (if needed) - define enum types

LinkML Schema Template:
```yaml
id: https://example.org/schemas/your-overlay
name: your_overlay
description: Schema for your outcome
imports:
  - ../core/provenance
prefixes:
  linkml: https://w3id.org/linkml/
  doco: http://purl.org/spar/doco/
  fabio: http://purl.org/spar/fabio/
  prov: http://www.w3.org/ns/prov#
  fibo: https://spec.edmcouncil.org/fibo/ontology/
  skos: http://www.w3.org/2004/02/skos/core#
default_prefix: your_overlay

classes:
  YourEntity:
    description: Description of entity
    class_uri: ontology:YourClass
    mixins:
      - ProvenanceFields
    slots:
      - field1        # MUST be defined in slots: section below
      - field2        # MUST be defined in slots: section below
      - status        # MUST be defined in slots: section below

slots:
  # Define ALL slots referenced above
  field1:
    description: Field description
    range: string
    required: true

  field2:
    description: Another field
    range: integer
    required: false

  status:
    description: Status of the entity
    range: StatusEnum    # Reference to enum defined below
    required: true

enums:
  StatusEnum:
    description: Possible status values
    permissible_values:
      active:
        description: Entity is active
      inactive:
        description: Entity is inactive
```

**VALIDATION CHECKLIST** (verify before generating):
✓ Every slot in every class's `slots:` list appears in the top-level `slots:` section
✓ Every slot has a `range:` (string, integer, datetime, boolean, or a defined type)
✓ Every enum referenced as a range is defined in the `enums:` section
✓ All classes have ProvenanceFields mixin
✓ All classes have a valid class_uri pointing to an ontology

Generate a complete LinkML schema for this outcome."""


def build_ontology_research_prompt(
    business_text: str,
    user_context: str = None,
    use_mcp_tools: bool = False,
    custom_prompt: str = None
) -> str:
    """Build the ontology research prompt.

    Args:
        business_text: Business outcome description
        user_context: Optional user context
        use_mcp_tools: Whether MCP tools are enabled
        custom_prompt: Optional custom prompt template (overrides default)

    Returns:
        Complete prompt string
    """
    if custom_prompt:
        # User provided custom prompt - just insert business text and context
        prompt = custom_prompt
        prompt = prompt.replace("{business_text}", business_text)
        if user_context:
            prompt = prompt.replace("{user_context}", user_context)
        return prompt

    # Build default prompt
    prompt_parts = [ONTOLOGY_RESEARCH_SYSTEM]

    if use_mcp_tools:
        prompt_parts.append(ONTOLOGY_RESEARCH_MCP_NOTICE)

    prompt_parts.append(f"\n\nBusiness Outcome:\n{business_text}")

    if user_context and user_context.strip():
        prompt_parts.append(f"\n\nUser Context and Instructions:\n{user_context}")

    prompt_parts.append(f"\n\n{ONTOLOGY_RESEARCH_TASK}")

    return "".join(prompt_parts)


def build_outcome_spec_prompt(
    business_text: str,
    entities_str: str,
    custom_prompt: str = None
) -> str:
    """Build the OutcomeSpec generation prompt.

    Args:
        business_text: Business outcome description
        entities_str: Formatted string of entities
        custom_prompt: Optional custom prompt template

    Returns:
        Complete prompt string
    """
    if custom_prompt:
        prompt = custom_prompt
        prompt = prompt.replace("{business_text}", business_text)
        prompt = prompt.replace("{entities}", entities_str)
        return prompt

    return f"""{OUTCOME_SPEC_SYSTEM}

Business Outcome:
{business_text}

Identified Entities:
{entities_str}

{OUTCOME_SPEC_TASK}"""


def build_linkml_schema_prompt(
    outcome_spec: str,
    entities_str: str,
    custom_prompt: str = None
) -> str:
    """Build the LinkML schema generation prompt.

    Args:
        outcome_spec: OutcomeSpec YAML/dict
        entities_str: Formatted string of entities with ontology mappings
        custom_prompt: Optional custom prompt template

    Returns:
        Complete prompt string
    """
    if custom_prompt:
        prompt = custom_prompt
        prompt = prompt.replace("{outcome_spec}", str(outcome_spec))
        prompt = prompt.replace("{entities}", entities_str)
        return prompt

    return f"""{LINKML_SCHEMA_SYSTEM}

OutcomeSpec:
{outcome_spec}

Entities with Ontology Mappings:
{entities_str}

{LINKML_SCHEMA_TASK}"""
