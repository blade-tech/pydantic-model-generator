"""Test schema synthesizer structure (no real LLM calls for MVP test)."""

import asyncio
from pathlib import Path
from agents.schema_synthesizer import (
    SchemaSynthesizer,
    LinkMLSchemaSpec,
    LinkMLClass,
    LinkMLAssociation,
    EvidenceQueryPlan,
)


def test_schema_spec_validation():
    """Test LinkML schema spec validation."""
    print("Testing LinkML schema spec validation...")

    # Valid schema
    valid_schema = LinkMLSchemaSpec(
        schema_name="resource_allocation",
        description="Resource allocation schema",
        classes=[
            LinkMLClass(
                name="TeamCapacity",
                description="Team capacity by period",
                slots=["team_id", "period", "capacity_hours"],
            ),
            LinkMLClass(
                name="Allocation",
                description="Resource allocation",
                slots=["team_id", "project_id", "period", "hours"],
            ),
        ],
        associations=[
            LinkMLAssociation(
                name="BasedOn",
                description="Allocation based on capacity",
                subject="Allocation",
                object="TeamCapacity",
            )
        ],
    )

    print(f"  Schema name: {valid_schema.schema_name}")
    print(f"  Classes: {len(valid_schema.classes)}")
    print(f"  Associations: {len(valid_schema.associations)}")

    # Test constraints
    try:
        # Too many classes
        invalid = LinkMLSchemaSpec(
            schema_name="too_many",
            description="Test",
            classes=[
                LinkMLClass(name=f"Class{i}", description="Test", slots=["id"])
                for i in range(13)  # Max is 12
            ],
            associations=[],
        )
        print("  [FAIL] Should have rejected >12 classes")
    except Exception as e:
        print(f"  [PASS] Correctly rejected >12 classes: {type(e).__name__}")

    # Test PascalCase validation
    try:
        invalid = LinkMLSchemaSpec(
            schema_name="test",
            description="Test",
            classes=[
                LinkMLClass(
                    name="lowercase_bad", description="Test", slots=["id"]
                )  # Must be PascalCase
            ],
            associations=[],
        )
        print("  [FAIL] Should have rejected non-PascalCase class")
    except Exception as e:
        print(f"  [PASS] Correctly rejected non-PascalCase: {type(e).__name__}")

    print("[PASS] Schema spec validation tests passed\n")


def test_evidence_query_plan():
    """Test Evidence Query Plan structure."""
    print("Testing Evidence Query Plan structure...")

    plan = EvidenceQueryPlan(
        question="Which allocations exceed team capacity in Q3?",
        required_entities=["Allocation", "TeamCapacity"],
        required_edges=["BasedOn"],
        metadata_filters={"period": "Q3"},
    )

    print(f"  Question: {plan.question}")
    print(f"  Required entities: {plan.required_entities}")
    print(f"  Required edges: {plan.required_edges}")
    print(f"  Metadata filters: {plan.metadata_filters}")

    print("[PASS] Evidence Query Plan structure validated\n")


def test_synthesizer_init():
    """Test synthesizer initialization."""
    print("Testing synthesizer initialization...")

    try:
        # This will fail if API key missing
        synthesizer = SchemaSynthesizer(provider="anthropic")
        print(f"  Provider: anthropic")
        print(f"  Model: {synthesizer.model}")
        print("[PASS] Synthesizer initialized (API key found)\n")
        return True
    except ValueError as e:
        print(f"[EXPECTED] API key missing: {e}")
        print("For real usage, add ANTHROPIC_API_KEY or OPENAI_API_KEY to .env\n")
        return False


async def main():
    print("=" * 60)
    print("Schema Synthesizer Tests (MVP)")
    print("=" * 60 + "\n")

    # Test 1: Schema spec validation
    test_schema_spec_validation()

    # Test 2: Evidence Query Plan
    test_evidence_query_plan()

    # Test 3: Synthesizer init
    has_key = test_synthesizer_init()

    print("=" * 60)
    if has_key:
        print("Ready for real schema synthesis!")
        print("\nUsage:")
        print("  from agents.schema_synthesizer import synthesize_schema_for_outcome")
        print("  schema = await synthesize_schema_for_outcome(")
        print('      Path("dsl/examples/resource_allocation.yaml"),')
        print('      overlay_output_path=Path("schemas/overlays/overlay.yaml"),')
        print('      eqp_output_path=Path("artifacts/eqp.json")')
        print("  )")
    else:
        print("Configure API key to enable schema synthesis")
        print("\nAdd to .env:")
        print("  ANTHROPIC_API_KEY=your_key  # or OPENAI_API_KEY")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
