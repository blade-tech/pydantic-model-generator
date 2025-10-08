#!/usr/bin/env python3
"""Pipeline script to add a new overlay to the Pydantic library.

Usage:
    python pipeline/add_overlay.py --name "customer_support"
    python pipeline/add_overlay.py --name "inventory" --interactive
    python pipeline/add_overlay.py --name "compliance" --outcome-doc "docs/requirements.md"
"""
import argparse
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')


def create_outcome_spec(name: str, interactive: bool = False) -> Path:
    """Step 1: Create OutcomeSpec YAML file."""
    print(f"\n[Step 1/6] Creating OutcomeSpec for '{name}'...")

    spec_file = Path(f"pydantic_library/specs/{name}.yaml")
    template_file = Path("pipeline/templates/outcome_spec_template.yaml")

    if interactive:
        print("Interactive mode not yet implemented. Use template manually.")
        print(f"Copy template from: {template_file}")
        print(f"To: {spec_file}")
        return spec_file

    if template_file.exists():
        # Copy template as starting point
        import shutil
        shutil.copy(template_file, spec_file)
        print(f"Created: {spec_file}")
        print("⚠️  Please edit this file to fill in your outcome questions and validation queries.")
    else:
        print(f"⚠️  Template not found: {template_file}")
        print(f"Please create {spec_file} manually.")

    return spec_file


def create_overlay_schema(name: str, interactive: bool = False) -> Path:
    """Step 2: Create LinkML overlay schema."""
    print(f"\n[Step 2/6] Creating LinkML overlay schema for '{name}'...")

    schema_file = Path(f"pydantic_library/schemas/overlays/{name}_overlay.yaml")
    template_file = Path("pipeline/templates/overlay_schema_template.yaml")

    if interactive:
        print("Interactive mode not yet implemented. Use template manually.")
        print(f"Copy template from: {template_file}")
        print(f"To: {schema_file}")
        return schema_file

    if template_file.exists():
        import shutil
        shutil.copy(template_file, schema_file)
        print(f"Created: {schema_file}")
        print("⚠️  Please edit this file to define your entities and edges.")
    else:
        print(f"⚠️  Template not found: {template_file}")
        print(f"Please create {schema_file} manually.")

    return schema_file


def generate_pydantic_models(name: str, schema_file: Path) -> Path:
    """Step 3: Generate Pydantic models using gen-pydantic."""
    print(f"\n[Step 3/6] Generating Pydantic models for '{name}'...")

    output_file = Path(f"pydantic_library/generated/pydantic/overlays/{name}_overlay.py")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "gen-pydantic",
        str(schema_file),
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result.stdout)

        print(f"✅ Generated: {output_file}")
        return output_file

    except subprocess.CalledProcessError as e:
        print(f"❌ gen-pydantic failed:")
        print(e.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("❌ gen-pydantic not found. Install with: pip install linkml")
        sys.exit(1)


def create_glue_code(name: str, schema_file: Path) -> Path:
    """Step 4: Create glue code (type registries + edge validation)."""
    print(f"\n[Step 4/6] Creating glue code for '{name}'...")

    glue_file = Path(f"pydantic_library/generated/pydantic/overlays/{name}_glue.py")
    template_file = Path("pipeline/templates/glue_template.py")

    # For now, create a basic template
    # TODO: Parse schema to auto-generate registries

    glue_content = f'''"""Glue code for {name} overlay - Graphiti type registries and edge mappings."""
from typing import Dict, List
from pydantic import BaseModel

# Import your entity and edge classes from generated models
from .{name}_overlay import (
    # TODO: Import your entities and edges here
    # Example:
    # YourEntity,
    # YourEdge,
)

# ==================================================================
# GRAPHITI TYPE REGISTRIES
# ==================================================================

{name.upper()}_ENTITY_TYPES: Dict[str, type[BaseModel]] = {{
    # TODO: Register your entities
    # "YourEntity": YourEntity,
}}

{name.upper()}_EDGE_TYPES: Dict[str, type[BaseModel]] = {{
    # TODO: Register your edges
    # "YourEdge": YourEdge,
}}

# ==================================================================
# CANONICAL EDGE TYPE MAPPINGS
# ==================================================================

{name.upper()}_EDGE_TYPE_MAP: Dict[tuple, List[str]] = {{
    # TODO: Define allowed edge types between entities
    # ("SourceEntity", "TargetEntity"): ["EdgeType"],
}}

# ==================================================================
# VALIDATION HELPERS
# ==================================================================

def validate_edge_type(source_type: str, target_type: str, edge_type: str) -> bool:
    """Validate if an edge type is allowed between two entity types."""
    allowed_edges = {name.upper()}_EDGE_TYPE_MAP.get((source_type, target_type), [])
    return edge_type in allowed_edges


def get_allowed_edges(source_type: str, target_type: str) -> List[str]:
    """Get allowed edge types between two entity types."""
    return {name.upper()}_EDGE_TYPE_MAP.get((source_type, target_type), [])
'''

    with open(glue_file, "w", encoding="utf-8") as f:
        f.write(glue_content)

    print(f"Created: {glue_file}")
    print("⚠️  Please edit this file to register your entities and edge types.")

    return glue_file


def create_test_file(name: str, spec_file: Path) -> Path:
    """Step 5: Create test file from OutcomeSpec."""
    print(f"\n[Step 5/6] Creating test file for '{name}'...")

    test_file = Path(f"pydantic_library/tests/test_{name}.py")
    template_file = Path("pipeline/templates/test_template.py")

    # For now, create a basic template
    # TODO: Parse OutcomeSpec to auto-generate tests

    test_content = f'''"""Tests for {name} overlay - Evidence Query Plan validation."""
import pytest
from datetime import datetime
from pydantic import ValidationError

# Import your models
from generated.pydantic.overlays.{name}_overlay import (
    # TODO: Import your entities and edges
    # YourEntity,
    # YourEdge,
)

# Import glue code for validation
from generated.pydantic.overlays.{name}_glue import (
    {name.upper()}_ENTITY_TYPES,
    {name.upper()}_EDGE_TYPES,
    {name.upper()}_EDGE_TYPE_MAP,
    validate_edge_type,
    get_allowed_edges,
)


class TestEntityCreation:
    """Test that all entities can be created with required fields."""

    def test_your_entity_creation(self):
        """Test YourEntity creation."""
        # TODO: Implement test
        pass


class TestEdgeCreation:
    """Test that all edges can be created with required fields."""

    def test_your_edge_creation(self):
        """Test YourEdge creation."""
        # TODO: Implement test
        pass


class TestOutcomeSpecValidation:
    """Test that generated models support OutcomeSpec validation queries."""

    def test_your_validation_query(self):
        """Test validation query from OutcomeSpec.

        Expected fields: [list fields from your query]
        Expected relations: [list relations from your query]
        """
        # TODO: Implement test based on OutcomeSpec validation queries
        pass


class TestGraphitiIntegration:
    """Test Graphiti type registries and edge validation."""

    def test_entity_registry(self):
        """Verify all entities are registered."""
        assert len({name.upper()}_ENTITY_TYPES) > 0
        # TODO: Add specific entity checks

    def test_edge_registry(self):
        """Verify all edges are registered."""
        assert len({name.upper()}_EDGE_TYPES) > 0
        # TODO: Add specific edge checks

    def test_edge_validation(self):
        """Test edge type validation."""
        # TODO: Test validate_edge_type() with your edge types
        pass
'''

    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_content)

    print(f"Created: {test_file}")
    print("⚠️  Please edit this file to implement your validation tests.")

    return test_file


def run_tests(name: str) -> bool:
    """Step 6: Run tests to validate overlay."""
    print(f"\n[Step 6/6] Running tests for '{name}'...")

    test_file = Path(f"pydantic_library/tests/test_{name}.py")

    if not test_file.exists():
        print(f"⚠️  Test file not found: {test_file}")
        return False

    cmd = [
        "pytest",
        str(test_file),
        "-v"
    ]

    try:
        result = subprocess.run(cmd, cwd="pydantic_library", check=True)
        print(f"✅ All tests passed for '{name}'")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Tests failed for '{name}'")
        print("Please fix the tests and models before committing.")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Add a new overlay to the Pydantic library"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Name of the overlay (e.g., 'customer_support')"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode (prompts for inputs)"
    )
    parser.add_argument(
        "--outcome-doc",
        help="Path to business outcome document (for AI-assisted generation)"
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip running tests at the end"
    )

    args = parser.parse_args()

    print(f"🚀 Adding new overlay: {args.name}")
    print(f"This will create files in pydantic_library/")

    # Step 1: Create OutcomeSpec
    spec_file = create_outcome_spec(args.name, args.interactive)

    # Step 2: Create overlay schema
    schema_file = create_overlay_schema(args.name, args.interactive)

    # Step 3: Generate Pydantic models
    print("\n⚠️  Before proceeding, please edit the OutcomeSpec and schema files.")
    print(f"   1. Edit: {spec_file}")
    print(f"   2. Edit: {schema_file}")

    response = input("\nPress Enter when ready to generate models, or Ctrl+C to exit: ")

    model_file = generate_pydantic_models(args.name, schema_file)

    # Step 4: Create glue code
    glue_file = create_glue_code(args.name, schema_file)

    # Step 5: Create test file
    test_file = create_test_file(args.name, spec_file)

    # Step 6: Run tests
    if not args.skip_tests:
        print("\n⚠️  Before running tests, please:")
        print(f"   1. Edit: {glue_file} (register entities/edges)")
        print(f"   2. Edit: {test_file} (implement validation tests)")

        response = input("\nPress Enter to run tests, or Ctrl+C to exit: ")
        run_tests(args.name)

    print(f"\n✅ Overlay '{args.name}' created!")
    print("\nNext steps:")
    print(f"  1. Review and edit generated files")
    print(f"  2. Run tests: cd pydantic_library && pytest tests/test_{args.name}.py -v")
    print(f"  3. Update documentation in MIGRATION_GUIDE.md")
    print(f"  4. Commit changes")


if __name__ == "__main__":
    main()
