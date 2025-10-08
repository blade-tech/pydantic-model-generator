"""Subprocess service for executing gen-pydantic and pytest.

This service handles:
1. Real subprocess execution (gen-pydantic, pytest)
2. File writes to ../pydantic_library/
3. Stdout/stderr capture
4. Error handling and validation
5. Automatic duplicate slot detection and fixing
6. Overlay name normalization (hyphens to underscores)

NO MOCKS - Real subprocess calls.
"""

import logging
import subprocess
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class SubprocessService:
    """Service for subprocess execution."""

    def __init__(self, pydantic_library_path: str):
        """Initialize subprocess service.

        Args:
            pydantic_library_path: Path to pydantic_library directory
        """
        self.pydantic_library_path = Path(pydantic_library_path).resolve()
        if not self.pydantic_library_path.exists():
            raise FileNotFoundError(
                f"Pydantic library not found at: {self.pydantic_library_path}"
            )
        logger.info(f"Initialized subprocess service with library path: {self.pydantic_library_path}")

    def _fix_duplicate_slots(self, linkml_content: str) -> str:
        """Fix duplicate slot names in LinkML schema by adding class-specific prefixes.

        Args:
            linkml_content: Original LinkML YAML content

        Returns:
            Fixed LinkML YAML content with unique slot names
        """
        import re

        lines = linkml_content.split('\n')

        # Phase 1: Find all slot definitions and detect duplicates
        slot_definitions = {}  # slot_name -> [line_numbers]
        slot_section_start = None

        for i, line in enumerate(lines):
            if line.strip() == 'slots:':
                slot_section_start = i
            elif slot_section_start is not None and line.startswith('  ') and ':' in line and not line.startswith('    '):
                # This is a top-level slot definition
                slot_name = line.split(':')[0].strip()
                if slot_name and not slot_name.startswith('#'):
                    if slot_name not in slot_definitions:
                        slot_definitions[slot_name] = []
                    slot_definitions[slot_name].append(i)

        # Find duplicates
        duplicates = {name: indices for name, indices in slot_definitions.items() if len(indices) > 1}

        if not duplicates:
            logger.info("No duplicate slots found")
            return linkml_content

        logger.info(f"Found {len(duplicates)} duplicate slot names: {list(duplicates.keys())}")

        # Phase 2: Find which classes use these slots to determine appropriate prefixes
        class_slots = {}  # class_name -> [slot_names]
        current_class = None
        in_slots_section = False

        for i, line in enumerate(lines):
            if line.startswith('  ') and ':' in line and not line.startswith('    ') and 'class_uri:' in lines[min(i+1, len(lines)-1)]:
                current_class = line.split(':')[0].strip()
                class_slots[current_class] = []
                in_slots_section = False
            elif current_class and line.strip() == 'slots:':
                in_slots_section = True
            elif current_class and in_slots_section:
                if line.startswith('      - '):
                    slot_name = line.strip()[2:]  # Remove '- '
                    class_slots[current_class].append(slot_name)
                elif not line.startswith('      '):
                    in_slots_section = False

        # Phase 3: Rename duplicate slots with class-specific prefixes
        slot_renames = {}  # old_name -> {line_number -> new_name}

        for dup_slot_name, dup_indices in duplicates.items():
            # Find which classes use this slot
            using_classes = [cls for cls, slots in class_slots.items() if dup_slot_name in slots]

            for idx, line_num in enumerate(dup_indices):
                if idx == 0:
                    # Keep first occurrence as-is
                    continue

                # Try to infer class name from context or use generic prefix
                context_class = None
                for cls in using_classes:
                    if idx < len(using_classes):
                        context_class = using_classes[idx]
                        break

                if context_class:
                    # Use class name as prefix (lowercase)
                    prefix = context_class.lower()
                    new_name = f"{prefix}_{dup_slot_name}"
                else:
                    # Fallback: use numeric suffix
                    new_name = f"{dup_slot_name}_{idx + 1}"

                if dup_slot_name not in slot_renames:
                    slot_renames[dup_slot_name] = {}
                slot_renames[dup_slot_name][line_num] = new_name

                logger.info(f"Will rename duplicate slot '{dup_slot_name}' at line {line_num} to '{new_name}'")

        # Phase 4: Apply renames to slot definitions
        for slot_name, renames in slot_renames.items():
            for line_num, new_name in renames.items():
                old_line = lines[line_num]
                new_line = old_line.replace(f"{slot_name}:", f"{new_name}:", 1)
                lines[line_num] = new_line

        # Phase 5: Update class slot references
        current_class = None
        in_slots_section = False

        for i, line in enumerate(lines):
            if line.startswith('  ') and ':' in line and not line.startswith('    '):
                potential_class = line.split(':')[0].strip()
                if potential_class in class_slots:
                    current_class = potential_class
                    in_slots_section = False
            elif current_class and line.strip() == 'slots:':
                in_slots_section = True
            elif current_class and in_slots_section:
                if line.startswith('      - '):
                    old_slot_ref = line.strip()[2:]
                    # Check if this slot was renamed
                    for old_name, renames in slot_renames.items():
                        if old_slot_ref == old_name:
                            # Find which renamed version this class should use
                            # Try to match by class name
                            target_new_name = None
                            for line_num, new_name in renames.items():
                                if current_class.lower() in new_name.lower():
                                    target_new_name = new_name
                                    break

                            if target_new_name:
                                lines[i] = line.replace(old_slot_ref, target_new_name)
                                logger.info(f"Updated slot reference in {current_class}: {old_slot_ref} -> {target_new_name}")
                elif not line.startswith('      '):
                    in_slots_section = False

        return '\n'.join(lines)

    def generate_pydantic_models(
        self,
        overlay_name: str,
        linkml_schema_content: str
    ) -> Dict[str, Any]:
        """Generate Pydantic models using gen-pydantic subprocess.

        Steps:
        1. Write LinkML schema to pydantic_library/schemas/overlays/{overlay_name}_overlay.yaml
        2. Execute gen-pydantic command
        3. Write output to pydantic_library/generated/pydantic/overlays/{overlay_name}_models.py
        4. Return result with success status and output

        Args:
            overlay_name: Name of the overlay (e.g., 'customer_support')
            linkml_schema_content: LinkML schema YAML content

        Returns:
            Dict with success status, output path, generated code, and any errors
        """
        try:
            # Normalize overlay name for Python module (replace hyphens with underscores)
            normalized_overlay_name = overlay_name.replace('-', '_')
            if normalized_overlay_name != overlay_name:
                logger.info(f"Normalized overlay name: '{overlay_name}' -> '{normalized_overlay_name}'")

            # Fix duplicate slot names before writing
            logger.info(f"Checking for duplicate slots in schema")
            linkml_schema_content = self._fix_duplicate_slots(linkml_schema_content)

            # Write LinkML schema file
            schema_dir = self.pydantic_library_path / "schemas" / "overlays"
            schema_dir.mkdir(parents=True, exist_ok=True)
            schema_file = schema_dir / f"{overlay_name}_overlay.yaml"

            logger.info(f"Writing LinkML schema to: {schema_file}")
            with open(schema_file, "w", encoding="utf-8") as f:
                f.write(linkml_schema_content)

            # Execute gen-pydantic with UTF-8 encoding for Windows compatibility
            logger.info(f"Executing gen-pydantic for {overlay_name}")
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            result = subprocess.run(
                ["gen-pydantic", str(schema_file)],
                capture_output=True,
                text=True,
                check=False,
                encoding="utf-8",
                env=env
            )

            if result.returncode != 0:
                logger.error(f"gen-pydantic failed: {result.stderr}")
                return {
                    "success": False,
                    "output_path": None,
                    "python_code": None,
                    "stderr": result.stderr,
                    "timestamp": datetime.utcnow().isoformat()
                }

            # Write generated Python models
            output_dir = self.pydantic_library_path / "generated" / "pydantic" / "overlays"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"{normalized_overlay_name}_models.py"

            logger.info(f"Writing generated models to: {output_file}")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result.stdout)

            return {
                "success": True,
                "output_path": str(output_file),
                "python_code": result.stdout,
                "stderr": None,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Error generating Pydantic models: {e}", exc_info=True)
            return {
                "success": False,
                "output_path": None,
                "python_code": None,
                "stderr": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def run_tests(
        self,
        overlay_name: str
    ) -> Dict[str, Any]:
        """Run pytest on generated models.

        Args:
            overlay_name: Name of the overlay to test

        Returns:
            Dict with test results (success, counts, duration, individual tests)
        """
        try:
            # Normalize overlay name (replace hyphens with underscores)
            normalized_overlay_name = overlay_name.replace('-', '_')
            test_file = self.pydantic_library_path / "tests" / f"test_{normalized_overlay_name}.py"

            if not test_file.exists():
                logger.warning(f"Test file not found: {test_file}")
                return {
                    "success": False,
                    "total_tests": 0,
                    "passed": 0,
                    "failed": 0,
                    "skipped": 0,
                    "duration": 0.0,
                    "tests": [],
                    "stdout": f"Test file not found: {test_file}",
                    "timestamp": datetime.utcnow().isoformat()
                }

            # Execute pytest with JSON output and UTF-8 encoding for Windows compatibility
            logger.info(f"Running pytest for {overlay_name}")
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONPATH"] = str(self.pydantic_library_path)
            result = subprocess.run(
                [
                    "pytest",
                    str(test_file),
                    "-v",
                    "--tb=short",
                    "--json-report",
                    "--json-report-file=test_report.json"
                ],
                capture_output=True,
                text=True,
                check=False,
                cwd=str(self.pydantic_library_path),
                encoding="utf-8",
                env=env
            )

            # Log pytest execution results
            logger.info(f"Pytest exit code: {result.returncode}")
            if result.stderr:
                logger.error(f"Pytest stderr: {result.stderr}")
            if result.stdout:
                logger.info(f"Pytest stdout (first 500 chars): {result.stdout[:500]}")

            # Parse test results
            report_file = self.pydantic_library_path / "test_report.json"
            if report_file.exists():
                with open(report_file, "r", encoding="utf-8") as f:
                    report = json.load(f)

                tests = []
                for test in report.get("tests", []):
                    tests.append({
                        "test_name": test.get("nodeid", "unknown"),
                        "status": test.get("outcome", "unknown"),
                        "duration": test.get("duration", 0.0),
                        "error_message": test.get("call", {}).get("longrepr", None)
                    })

                summary = report.get("summary", {})
                return {
                    "success": result.returncode == 0,
                    "total_tests": summary.get("total", 0),
                    "passed": summary.get("passed", 0),
                    "failed": summary.get("failed", 0),
                    "skipped": summary.get("skipped", 0),
                    "duration": report.get("duration", 0.0),
                    "tests": tests,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                # Fallback: return stderr/stdout for debugging
                logger.warning(f"JSON report file not found at {report_file}")
                logger.warning("This usually means pytest-json-report plugin is not installed or pytest failed to run")

                error_output = result.stderr if result.stderr else result.stdout

                return {
                    "success": False,
                    "total_tests": 0,
                    "passed": 0,
                    "failed": 0,
                    "skipped": 0,
                    "duration": 0.0,
                    "tests": [],
                    "stdout": result.stdout,
                    "stderr": result.stderr or "JSON report file not generated - pytest-json-report may not be installed",
                    "timestamp": datetime.utcnow().isoformat()
                }

        except Exception as e:
            logger.error(f"Error running tests: {e}", exc_info=True)
            return {
                "success": False,
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "duration": 0.0,
                "tests": [],
                "stdout": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def get_library_coverage(self) -> Dict[str, Any]:
        """Get statistics about pydantic_library coverage.

        Scans schemas/overlays/ directory and counts entities.

        Returns:
            Dict with coverage statistics
        """
        try:
            overlays_dir = self.pydantic_library_path / "schemas" / "overlays"
            if not overlays_dir.exists():
                return {
                    "total_overlays": 0,
                    "total_entities": 0,
                    "total_edges": 0,
                    "overlays": [],
                    "last_updated": datetime.utcnow().isoformat()
                }

            overlays = []
            total_entities = 0
            total_edges = 0

            for schema_file in overlays_dir.glob("*_overlay.yaml"):
                # Read and parse YAML (simplified - real implementation would use yaml library)
                with open(schema_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Count entities (classes) and edges (relationships)
                # Simplified counting - real implementation would parse YAML properly
                entity_count = content.count("class_uri:")
                edge_count = content.count("range:")  # Approximation

                overlay_name = schema_file.stem.replace("_overlay", "")
                overlays.append({
                    "name": overlay_name,
                    "file": str(schema_file.name),
                    "entities": entity_count,
                    "edges": edge_count
                })

                total_entities += entity_count
                total_edges += edge_count

            return {
                "total_overlays": len(overlays),
                "total_entities": total_entities,
                "total_edges": total_edges,
                "overlays": overlays,
                "last_updated": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Error getting library coverage: {e}", exc_info=True)
            return {
                "total_overlays": 0,
                "total_entities": 0,
                "total_edges": 0,
                "overlays": [],
                "last_updated": datetime.utcnow().isoformat()
            }
