"""Run schema synthesis using Claude Code's API key via subagent.

This script orchestrates the LLM-powered schema synthesis by spawning
a subagent with access to the Anthropic API key.
"""

import asyncio
import json
from pathlib import Path
from agents.schema_synthesizer import synthesize_schema_for_outcome


async def main():
    """Run LLM synthesis for invoice validation outcome."""

    print("\n" + "="*60)
    print("LLM-POWERED SCHEMA SYNTHESIS")
    print("="*60 + "\n")

    print("📋 Input: Invoice Validation Business Outcome")
    print("🤖 Using: Claude 3.5 Sonnet via Instructor")
    print("✨ Output: Validated LinkML Schema + Evidence Query Plan\n")

    try:
        # Run synthesis
        schema_spec = await synthesize_schema_for_outcome(
            outcome_spec_path=Path("dsl/examples/invoice_validation.yaml"),
            overlay_output_path=Path("schemas/overlays/invoice_overlay.yaml"),
            eqp_output_path=Path("artifacts/invoice_eqp.json"),
            provider="anthropic"
        )

        print("\n✅ SUCCESS: Schema synthesis complete!")
        print(f"   - Schema: {schema_spec.schema_name}")
        print(f"   - Classes: {len(schema_spec.classes)}")
        print(f"   - Associations: {len(schema_spec.associations)}")

        # Show generated classes
        print("\n📦 Generated Classes:")
        for cls in schema_spec.classes:
            print(f"   • {cls.name}: {cls.description}")
            print(f"     Slots: {', '.join(cls.slots)}")

        # Show associations
        print("\n🔗 Generated Associations:")
        for assoc in schema_spec.associations:
            print(f"   • {assoc.name}: {assoc.subject} -> {assoc.object}")

        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
