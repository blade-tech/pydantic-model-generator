"""OutcomeSpec loader - Load and validate outcome specifications from YAML."""

import yaml
from pathlib import Path
from typing import Union
from rich.console import Console
from rich.table import Table

from .outcome_spec_schema import OutcomeSpec

console = Console()


def load_outcome_spec(path: Union[str, Path]) -> OutcomeSpec:
    """Load an OutcomeSpec from a YAML file.

    Args:
        path: Path to the YAML file

    Returns:
        Validated OutcomeSpec instance

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the YAML is invalid or doesn't match the schema
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"OutcomeSpec file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in {path}: {e}")

    try:
        spec = OutcomeSpec(**data)
    except Exception as e:
        raise ValueError(f"OutcomeSpec validation failed for {path}: {e}")

    return spec


def print_outcome_spec_table(spec: OutcomeSpec) -> None:
    """Print a formatted table summary of an OutcomeSpec.

    Args:
        spec: The OutcomeSpec to display
    """
    console.print(f"\n[bold cyan]Outcome:[/bold cyan] {spec.outcome_name}")
    console.print(f"[dim]{spec.context_summary}[/dim]\n")

    # Evidence table
    if spec.required_evidence:
        evidence_table = Table(title="Required Evidence", show_header=True, header_style="bold magenta")
        evidence_table.add_column("Name", style="cyan")
        evidence_table.add_column("Description")
        evidence_table.add_column("Required Slots", style="yellow")

        for ev in spec.required_evidence:
            slots = ", ".join(ev.must_have_slots) if ev.must_have_slots else "[dim]none[/dim]"
            evidence_table.add_row(ev.name, ev.description, slots)

        console.print(evidence_table)
        console.print()

    # Queries table
    if spec.queries_we_must_answer:
        queries_table = Table(
            title="Queries We Must Answer", show_header=True, header_style="bold green"
        )
        queries_table.add_column("#", justify="right", style="dim")
        queries_table.add_column("Question")

        for i, q in enumerate(spec.queries_we_must_answer, 1):
            queries_table.add_row(str(i), q)

        console.print(queries_table)
        console.print()

    # Entities table
    if spec.target_entities:
        entities_table = Table(title="Target Entities", show_header=True, header_style="bold blue")
        entities_table.add_column("Name", style="cyan")
        entities_table.add_column("Description")
        entities_table.add_column("Required Slots", style="yellow")

        for ent in spec.target_entities:
            slots = (
                ", ".join(ent.must_have_slots) if ent.must_have_slots else "[dim]none[/dim]"
            )
            entities_table.add_row(ent.name, ent.description, slots)

        console.print(entities_table)
        console.print()

    # Relations table
    if spec.relations:
        relations_table = Table(
            title="Relationships", show_header=True, header_style="bold yellow"
        )
        relations_table.add_column("Name", style="cyan")
        relations_table.add_column("Subject → Object")
        relations_table.add_column("Description")

        for rel in spec.relations:
            arrow = f"{rel.subject} [dim]→[/dim] {rel.object}"
            desc = rel.description or "[dim]n/a[/dim]"
            relations_table.add_row(rel.name, arrow, desc)

        console.print(relations_table)
        console.print()

    # Ontologies
    if spec.ontologies:
        ont_table = Table(title="Ontology References", show_header=True, header_style="bold magenta")
        ont_table.add_column("Prefix", style="cyan")
        ont_table.add_column("Base URI", style="blue")
        ont_table.add_column("Include Classes", style="yellow")

        for ont in spec.ontologies:
            classes = (
                ", ".join(ont.include_classes) if ont.include_classes else "[dim]all[/dim]"
            )
            ont_table.add_row(ont.prefix, ont.base_uri, classes)

        console.print(ont_table)
        console.print()

    # Graphiti constraints
    console.print("[bold]Graphiti Constraints:[/bold]")
    console.print(f"  • Entity type in metadata: {spec.graphiti_constraints.use_entity_type_metadata}")
    console.print(f"  • Edge names PascalCase: {spec.graphiti_constraints.edge_names_pascal_case}")
    console.print(f"  • Stamp URI on edges: {spec.graphiti_constraints.stamp_uri_on_edges}")
    console.print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        console.print("[red]Usage:[/red] python -m dsl.loader <path-to-outcome-spec.yaml>")
        sys.exit(1)

    try:
        spec = load_outcome_spec(sys.argv[1])
        print_outcome_spec_table(spec)
        console.print("[green]✓ OutcomeSpec validated successfully[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        sys.exit(1)
