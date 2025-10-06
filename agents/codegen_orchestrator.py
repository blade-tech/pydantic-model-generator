"""Codegen orchestrator - runs LinkML lint and Pydantic generation."""

import subprocess
from pathlib import Path
from typing import Tuple, Optional


class CodegenError(Exception):
    """Raised when codegen fails."""

    pass


class CodegenOrchestrator:
    """Orchestrates LinkML linting and Pydantic code generation."""

    def __init__(self):
        """Initialize codegen orchestrator."""
        pass

    def lint_schema(self, schema_path: Path) -> Tuple[bool, str]:
        """Run linkml lint on schema.

        Args:
            schema_path: Path to LinkML YAML schema

        Returns:
            Tuple of (success, output_message)
        """
        try:
            result = subprocess.run(
                ["linkml", "lint", str(schema_path)],
                capture_output=True,
                text=True,
                check=False,
            )

            # Accept warnings (exit code 1) as non-blocking for MVP
            if result.returncode in [0, 1]:
                if "warning" in result.stdout.lower():
                    return True, f"Schema lint passed with warnings (acceptable for MVP)"
                return True, "Schema lint passed"
            else:
                return False, f"Lint errors:\n{result.stdout}\n{result.stderr}"

        except FileNotFoundError:
            raise CodegenError(
                "linkml command not found. Install with: pip install linkml"
            )
        except Exception as e:
            raise CodegenError(f"Lint failed: {e}") from e

    def generate_pydantic(
        self, schema_path: Path, output_path: Path
    ) -> Tuple[bool, str]:
        """Generate Pydantic models from LinkML schema.

        Args:
            schema_path: Path to LinkML YAML schema
            output_path: Path to save generated Pydantic code

        Returns:
            Tuple of (success, output_message)
        """
        try:
            # Run linkml generate pydantic
            result = subprocess.run(
                ["linkml", "generate", "pydantic", str(schema_path)],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                return False, f"Generation failed:\n{result.stdout}\n{result.stderr}"

            # Save generated code
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result.stdout)

            return True, f"Generated Pydantic models at {output_path}"

        except FileNotFoundError:
            raise CodegenError(
                "linkml command not found. Install with: pip install linkml"
            )
        except Exception as e:
            raise CodegenError(f"Generation failed: {e}") from e

    def smoke_test_import(self, module_path: Path) -> Tuple[bool, str]:
        """Test that generated module imports successfully.

        Args:
            module_path: Path to generated Python module

        Returns:
            Tuple of (success, output_message)
        """
        try:
            # Convert path to module name (e.g., generated/pydantic/models.py -> generated.pydantic.models)
            module_parts = module_path.with_suffix("").parts
            # Find where 'generated' starts
            try:
                gen_idx = module_parts.index("generated")
                module_name = ".".join(module_parts[gen_idx:])
            except ValueError:
                # Fallback: assume last 3 parts (generated.pydantic.models)
                if len(module_parts) >= 3:
                    module_name = ".".join(module_parts[-3:])
                else:
                    module_name = ".".join(module_parts)

            result = subprocess.run(
                ["python", "-c", f"import {module_name}"],
                capture_output=True,
                text=True,
                check=False,
                cwd=Path.cwd(),  # Ensure correct working directory
            )

            if result.returncode == 0:
                return True, f"Import successful: {module_name}"
            else:
                return False, f"Import failed:\n{result.stderr}"

        except Exception as e:
            return False, f"Smoke test error: {e}"

    def run_full_pipeline(
        self, schema_path: Path, output_path: Path
    ) -> Tuple[bool, str]:
        """Run complete codegen pipeline: lint -> generate -> smoke test.

        Args:
            schema_path: Path to LinkML YAML schema
            output_path: Path to save generated Pydantic code

        Returns:
            Tuple of (success, output_message)
        """
        messages = []

        # Step 1: Lint
        print("Step 1: Linting schema...")
        lint_success, lint_msg = self.lint_schema(schema_path)
        messages.append(f"[LINT] {lint_msg}")

        if not lint_success:
            return False, "\n".join(messages)

        # Step 2: Generate Pydantic
        print("Step 2: Generating Pydantic models...")
        gen_success, gen_msg = self.generate_pydantic(schema_path, output_path)
        messages.append(f"[CODEGEN] {gen_msg}")

        if not gen_success:
            return False, "\n".join(messages)

        # Step 3: Smoke test import
        print("Step 3: Smoke testing import...")
        test_success, test_msg = self.smoke_test_import(output_path)
        messages.append(f"[IMPORT] {test_msg}")

        if not test_success:
            return False, "\n".join(messages)

        return True, "\n".join(messages)


def run_codegen(
    schema_path: Path,
    output_path: Path = Path("generated/pydantic/models.py"),
) -> bool:
    """Convenience function to run codegen pipeline.

    Args:
        schema_path: Path to LinkML YAML schema
        output_path: Path to save generated Pydantic code

    Returns:
        True if successful, False otherwise
    """
    orchestrator = CodegenOrchestrator()
    success, message = orchestrator.run_full_pipeline(schema_path, output_path)

    print("\n" + "=" * 60)
    print("CODEGEN PIPELINE RESULT")
    print("=" * 60)
    print(message)
    print("=" * 60)

    return success
