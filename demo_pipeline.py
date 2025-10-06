"""End-to-end pipeline demo: OutcomeSpec -> LinkML -> Pydantic models.

This demonstrates the full MVP pipeline visually.
"""

import asyncio
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.markdown import Markdown

# Import pipeline components
from dsl.loader import load_outcome_spec
from agents.schema_synthesizer import synthesize_schema_for_outcome
from agents.codegen_orchestrator import run_codegen

console = Console(force_terminal=True, legacy_windows=False)


async def demo_full_pipeline(
    outcome_spec_path: Path = Path("dsl/examples/resource_allocation.yaml"),
    use_real_llm: bool = False,
):
    """Run full pipeline demo with visual output.

    Args:
        outcome_spec_path: Path to OutcomeSpec YAML
        use_real_llm: If True, uses real LLM (requires API key). If False, uses mock.
    """
    console.print("\n")
    console.print(
        Panel.fit(
            "[bold cyan]Outcome-First Pydantic Model Generator[/bold cyan]\n"
            "[dim]Natural Language -> LinkML -> Pydantic[/dim]",
            border_style="cyan",
        )
    )

    # ========================================
    # STEP 1: Load OutcomeSpec
    # ========================================
    console.print("\n[bold]Step 1: Load OutcomeSpec[/bold]", style="yellow")

    spec = load_outcome_spec(outcome_spec_path)

    # Display OutcomeSpec summary
    table = Table(title="OutcomeSpec Summary", show_header=True, header_style="bold")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Outcome Name", spec.outcome_name)
    table.add_row("Context", spec.context_summary)
    table.add_row("Questions to Answer", str(len(spec.queries_we_must_answer)))
    table.add_row("Required Evidence", str(len(spec.required_evidence)))
    table.add_row("Target Entities", str(len(spec.target_entities)))
    table.add_row("Relations", str(len(spec.relations)))

    console.print(table)

    # Display questions
    console.print("\n[bold cyan]Questions to Answer:[/bold cyan]")
    for i, q in enumerate(spec.queries_we_must_answer, 1):
        console.print(f"  {i}. {q}", style="dim")

    # ========================================
    # STEP 2: Schema Synthesis
    # ========================================
    console.print("\n[bold]Step 2: Synthesize LinkML Schema[/bold]", style="yellow")

    if use_real_llm:
        console.print(
            "[cyan]Using real LLM to generate schema...[/cyan]", style="dim"
        )

        try:
            schema_spec = await synthesize_schema_for_outcome(
                outcome_spec_path,
                overlay_output_path=Path("schemas/overlays/overlay.yaml"),
                eqp_output_path=Path("artifacts/eqp.json"),
                provider="anthropic",
            )

            # Display schema summary
            schema_table = Table(
                title="Generated Schema", show_header=True, header_style="bold"
            )
            schema_table.add_column("Component", style="cyan")
            schema_table.add_column("Count", style="white")

            schema_table.add_row("Schema Name", schema_spec.schema_name)
            schema_table.add_row("Classes", str(len(schema_spec.classes)))
            schema_table.add_row("Associations", str(len(schema_spec.associations)))

            console.print(schema_table)

            # Display classes
            console.print("\n[bold cyan]Classes:[/bold cyan]")
            for cls in schema_spec.classes:
                console.print(
                    f"  • {cls.name}: {', '.join(cls.slots)}", style="dim"
                )

            # Display associations
            console.print("\n[bold cyan]Associations:[/bold cyan]")
            for assoc in schema_spec.associations:
                console.print(
                    f"  • {assoc.name}: {assoc.subject} -> {assoc.object}",
                    style="dim",
                )

        except Exception as e:
            console.print(f"[red]Schema synthesis failed: {e}[/red]")
            console.print(
                "[yellow]Tip: Add ANTHROPIC_API_KEY or OPENAI_API_KEY to .env[/yellow]"
            )
            return

    else:
        # Mock schema for demo without LLM
        console.print(
            "[yellow]Using mock schema (set use_real_llm=True for real synthesis)[/yellow]",
            style="dim",
        )

        mock_linkml = """id: https://example.org/graphmodels/resource_allocation
name: resource_allocation
description: Resource allocation schema
imports:
  - ../core

classes:
  TeamCapacity:
    description: Team capacity by period
    mixins:
      - NodeProv
    attributes:
      team_id:
        range: string
      period:
        range: string
      capacity_hours:
        range: integer

  BudgetConstraint:
    description: Budget constraints by project
    mixins:
      - NodeProv
    attributes:
      project_id:
        range: string
      currency:
        range: string
      amount:
        range: float

  Allocation:
    description: Resource allocation
    mixins:
      - NodeProv
    attributes:
      team_id:
        range: string
      project_id:
        range: string
      period:
        range: string
      hours:
        range: integer
      basedon:
        range: TeamCapacity
        inlined: false
      constrainedby:
        range: BudgetConstraint
        inlined: false
"""

        # Save mock schema
        mock_path = Path("schemas/overlays/overlay.yaml")
        mock_path.parent.mkdir(parents=True, exist_ok=True)
        with open(mock_path, "w", encoding="utf-8") as f:
            f.write(mock_linkml)

        console.print(
            f"[green]Created mock LinkML schema at {mock_path}[/green]", style="dim"
        )

        # Display mock schema
        console.print("\n[bold cyan]Mock LinkML Schema:[/bold cyan]")
        console.print(
            Syntax(mock_linkml, "yaml", theme="monokai", line_numbers=True)
        )

    # ========================================
    # STEP 3: Codegen (LinkML -> Pydantic)
    # ========================================
    console.print("\n[bold]Step 3: Generate Pydantic Models[/bold]", style="yellow")

    schema_path = Path("schemas/overlays/overlay.yaml")
    output_path = Path("generated/pydantic/models.py")

    console.print(
        f"[cyan]Running LinkML codegen: {schema_path} -> {output_path}[/cyan]",
        style="dim",
    )

    success = run_codegen(schema_path, output_path)

    if success:
        console.print(
            f"\n[green][PASS] Pydantic models generated successfully![/green]",
            style="bold",
        )

        # Display generated code preview
        if output_path.exists():
            with open(output_path, encoding="utf-8") as f:
                generated_code = f.read()

            # Show first 50 lines
            preview_lines = generated_code.split("\n")[:50]
            preview = "\n".join(preview_lines)

            console.print("\n[bold cyan]Generated Pydantic Models (preview):[/bold cyan]")
            console.print(
                Syntax(
                    preview + "\n...",
                    "python",
                    theme="monokai",
                    line_numbers=True,
                )
            )

            console.print(
                f"\n[dim]Full code at: {output_path} ({len(generated_code.split(chr(10)))} lines)[/dim]"
            )

    else:
        console.print(
            "[red][FAIL] Codegen failed - check errors above[/red]", style="bold"
        )
        return

    # ========================================
    # SUMMARY
    # ========================================
    console.print("\n")
    console.print(
        Panel.fit(
            "[bold green][PASS] Pipeline Complete![/bold green]\n\n"
            f"[cyan]Input:[/cyan] {outcome_spec_path}\n"
            f"[cyan]LinkML Schema:[/cyan] {schema_path}\n"
            f"[cyan]Pydantic Models:[/cyan] {output_path}\n\n"
            "[dim]Next: Use these models for graph ingestion and evaluation[/dim]",
            border_style="green",
            title="Pipeline Summary",
        )
    )

    console.print("\n[bold]What You Can Do Next:[/bold]", style="yellow")
    console.print("  1. Inspect generated models:", style="dim")
    console.print(f"     cat {output_path}", style="cyan")
    console.print("  2. Import and use in Python:", style="dim")
    console.print(
        "     from generated.pydantic.models import TeamCapacity, Allocation",
        style="cyan",
    )
    console.print("  3. Iterate on OutcomeSpec and re-run pipeline", style="dim")
    console.print(
        f"     python demo_pipeline.py  # will regenerate from {outcome_spec_path}",
        style="cyan",
    )
    console.print()


async def main():
    """Run demo with configuration."""
    console.print(
        "\n[bold]Choose demo mode:[/bold]", style="yellow"
    )
    console.print("  1. Mock (no API keys needed, uses predefined schema)")
    console.print("  2. Real LLM (requires ANTHROPIC_API_KEY or OPENAI_API_KEY)\n")

    # For this demo, we'll use mock mode by default
    use_real = False

    # Check if API keys exist
    import os
    from dotenv import load_dotenv

    load_dotenv()
    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
    has_openai = bool(os.getenv("OPENAI_API_KEY"))

    if has_anthropic or has_openai:
        console.print(
            "[green]API key found - you can set use_real=True for real synthesis[/green]",
            style="dim",
        )

    await demo_full_pipeline(
        outcome_spec_path=Path("dsl/examples/resource_allocation.yaml"),
        use_real_llm=use_real,
    )


if __name__ == "__main__":
    asyncio.run(main())
