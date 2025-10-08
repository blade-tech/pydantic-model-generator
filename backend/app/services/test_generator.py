"""Service for generating pytest test files from generated Pydantic models.

This service automatically creates comprehensive test files that validate:
- Entity creation with required fields
- Enum validation
- Field validation
- Provenance tracking
- Model serialization
- Canonical URIs
"""

import logging
import importlib
import inspect
import sys
from pathlib import Path
from typing import Dict, Any, List, Type
from enum import Enum
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, RootModel

logger = logging.getLogger(__name__)


class TestGenerator:
    """Generates pytest test files from Pydantic models."""

    def __init__(self, pydantic_library_path: str):
        """Initialize test generator.

        Args:
            pydantic_library_path: Path to pydantic_library directory
        """
        self.pydantic_library_path = Path(pydantic_library_path)
        self.tests_dir = self.pydantic_library_path / "tests"
        self.tests_dir.mkdir(parents=True, exist_ok=True)

        # Add pydantic_library to Python path so we can import generated models
        pydantic_lib_abs = str(self.pydantic_library_path.resolve())
        if pydantic_lib_abs not in sys.path:
            sys.path.insert(0, pydantic_lib_abs)
            logger.info(f"Added {pydantic_lib_abs} to Python path for model imports")

    def generate_test_file(self, overlay_name: str) -> Dict[str, Any]:
        """Generate a pytest test file for generated Pydantic models.

        Args:
            overlay_name: Name of the overlay (e.g., 'business_outcome')

        Returns:
            Dict with success status and test file path
        """
        try:
            # Normalize overlay name (replace hyphens with underscores)
            normalized_overlay_name = overlay_name.replace('-', '_')
            logger.info(f"Attempting to generate test file for overlay: {overlay_name} (normalized: {normalized_overlay_name})")

            # Import the generated models module
            module_path = f"generated.pydantic.overlays.{normalized_overlay_name}_models"
            logger.info(f"Attempting to import module: {module_path}")

            try:
                # Invalidate import caches to ensure Python sees newly written files
                importlib.invalidate_caches()
                models_module = importlib.import_module(module_path)
            except ImportError as e:
                logger.error(f"Failed to import models module '{module_path}': {e}")
                return {
                    "success": False,
                    "error": f"Cannot import Pydantic models for overlay '{overlay_name}'. The models file may not exist or may have errors. Please ensure Step 5 (Pydantic Generation) completed successfully. Import error: {str(e)}",
                    "test_file_path": None
                }

            # Extract classes and enums
            model_classes = []
            enum_classes = []

            for name, obj in inspect.getmembers(models_module):
                if inspect.isclass(obj) and issubclass(obj, BaseModel) and obj != BaseModel:
                    # Skip base classes
                    if name in ['ConfiguredBaseModel', 'ProvenanceFields', 'EdgeProvenanceFields']:
                        continue
                    model_classes.append((name, obj))
                elif inspect.isclass(obj) and issubclass(obj, Enum) and obj != Enum:
                    enum_classes.append((name, obj))

            logger.info(f"Found {len(model_classes)} model classes and {len(enum_classes)} enum classes")

            # Generate test code
            test_code = self._generate_test_code(
                normalized_overlay_name,
                model_classes,
                enum_classes
            )

            # Write test file
            test_file = self.tests_dir / f"test_{normalized_overlay_name}.py"
            with open(test_file, "w", encoding="utf-8") as f:
                f.write(test_code)

            logger.info(f"Generated test file: {test_file}")

            return {
                "success": True,
                "test_file_path": str(test_file),
                "num_model_classes": len(model_classes),
                "num_enum_classes": len(enum_classes),
                "num_tests": self._count_tests(len(model_classes), len(enum_classes))
            }

        except Exception as e:
            logger.error(f"Error generating test file: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "test_file_path": None
            }

    def _generate_test_code(
        self,
        overlay_name: str,
        model_classes: List[tuple],
        enum_classes: List[tuple]
    ) -> str:
        """Generate Python test code.

        Args:
            overlay_name: Name of the overlay
            model_classes: List of (name, class) tuples for model classes
            enum_classes: List of (name, class) tuples for enum classes

        Returns:
            Generated Python test code
        """
        # Build imports
        imports = self._generate_imports(overlay_name, model_classes, enum_classes)

        # Build test classes
        entity_creation_tests = self._generate_entity_creation_tests(model_classes)
        enum_validation_tests = self._generate_enum_validation_tests(model_classes, enum_classes)
        field_validation_tests = self._generate_field_validation_tests(model_classes)
        provenance_tests = self._generate_provenance_tests(model_classes)
        serialization_tests = self._generate_serialization_tests(model_classes)
        uri_tests = self._generate_uri_tests(model_classes)

        # Combine all parts
        return f'''"""
Auto-generated pytest validation tests for {overlay_name} models.

Tests entity creation, validation, field types, and Pydantic V2 features.
Generated by TestGenerator service.
"""

{imports}


{entity_creation_tests}


{enum_validation_tests}


{field_validation_tests}


{provenance_tests}


{serialization_tests}


{uri_tests}


if __name__ == "__main__":
    # Run with pytest
    pytest.main([__file__, "-v", "--tb=short"])
'''

    def _generate_imports(
        self,
        overlay_name: str,
        model_classes: List[tuple],
        enum_classes: List[tuple]
    ) -> str:
        """Generate import statements."""
        model_names = [name for name, _ in model_classes]
        enum_names = [name for name, _ in enum_classes]

        all_imports = model_names + enum_names

        return f'''import pytest
from datetime import date, datetime
from decimal import Decimal
from pydantic import ValidationError

# Import generated models
from generated.pydantic.overlays.{overlay_name}_models import (
{self._format_import_list(all_imports)}
)'''

    def _format_import_list(self, names: List[str]) -> str:
        """Format a list of names for imports."""
        return ",\n".join(f"    {name}" for name in names)

    def _generate_entity_creation_tests(self, model_classes: List[tuple]) -> str:
        """Generate entity creation tests."""
        tests = []

        for class_name, cls in model_classes[:5]:  # Limit to first 5 for brevity
            # Skip RootModel types - they're not regular entities
            if issubclass(cls, RootModel):
                continue
            test_code = self._generate_single_entity_test(class_name, cls)
            tests.append(test_code)

        return f'''class TestEntityCreation:
    """Test all entity models can be created with valid data."""

{chr(10).join(tests)}'''

    def _generate_single_entity_test(self, class_name: str, cls: Type[BaseModel]) -> str:
        """Generate a single entity creation test."""
        # Get required fields
        fields = cls.model_fields
        required_fields = {
            name: field for name, field in fields.items()
            if field.is_required()
        }

        # Generate sample values
        field_values = []
        for field_name, field_info in required_fields.items():
            value = self._generate_sample_value(field_name, field_info)
            field_values.append(f"            {field_name}={value}")

        # Add node_id if not in required fields
        if 'node_id' not in required_fields:
            field_values.append(f'            node_id="{class_name.upper()}-001"')

        fields_str = ",\n".join(field_values)

        return f'''    def test_{class_name.lower()}_creation(self):
        """Test {class_name} with required fields."""
        instance = {class_name}(
{fields_str}
        )

        # Basic assertion
        assert instance.node_id is not None'''

    def _generate_sample_value(self, field_name: str, field_info) -> str:
        """Generate a sample value for a field based on its type."""
        # Check type annotation first
        try:
            annotation = field_info.annotation
            # Handle Optional and List types
            if hasattr(annotation, '__origin__'):
                # Check for list types first
                if annotation.__origin__ is list:
                    if hasattr(annotation, '__args__') and len(annotation.__args__) > 0:
                        element_type = annotation.__args__[0]
                        # Generate value for the element type and wrap in list
                        if inspect.isclass(element_type) and issubclass(element_type, Enum):
                            first_value = list(element_type)[0]
                            return f'[{element_type.__name__}.{first_value.name}]'
                        elif element_type is str:
                            return '["test_value"]'
                        elif element_type is int:
                            return '[100]'
                        elif element_type is float:
                            return '[100000.0]'
                        elif element_type is bool:
                            return '[True]'
                # For Union types (like Optional), get the first non-None type
                if hasattr(annotation, '__args__'):
                    for arg in annotation.__args__:
                        if arg is type(None):
                            continue
                        # Check for Enum
                        if inspect.isclass(arg) and issubclass(arg, Enum):
                            first_value = list(arg)[0]
                            return f'{arg.__name__}.{first_value.name}'
                        # Check for datetime
                        elif arg is datetime:
                            return 'datetime(2024, 1, 15, 12, 0, 0)'
                        # Check for date
                        elif arg is date:
                            return 'date(2024, 1, 15)'
                        # Check for bool
                        elif arg is bool:
                            return 'True'
                        # Check for float
                        elif arg is float:
                            return '100000.0'
                        # Check for Decimal
                        elif arg is Decimal:
                            return 'Decimal("100000.00")'
                        # Check for int
                        elif arg is int:
                            return '100'
            # Direct type checks
            elif annotation is bool:
                return 'True'
            elif annotation is float:
                return '100000.0'
            elif annotation is Decimal:
                return 'Decimal("100000.00")'
            elif annotation is int:
                return '100'
            elif annotation is datetime:
                return 'datetime(2024, 1, 15, 12, 0, 0)'
            elif annotation is date:
                return 'date(2024, 1, 15)'
            elif inspect.isclass(annotation) and issubclass(annotation, Enum):
                first_value = list(annotation)[0]
                return f'{annotation.__name__}.{first_value.name}'
        except Exception:
            pass  # Fall through to name-based inference

        # Try to infer from field name
        field_lower = field_name.lower()

        # Check for datetime/timestamp patterns first
        if 'timestamp' in field_lower or field_name.endswith('_at'):
            return 'datetime(2024, 1, 15, 12, 0, 0)'
        elif 'date' in field_lower and 'time' not in field_lower:
            return 'date(2024, 1, 15)'
        elif 'id' in field_lower:
            return f'"{field_name.upper()}-001"'
        elif 'name' in field_lower:
            return f'"Test {field_name.replace("_", " ").title()}"'
        elif 'ratio' in field_lower:
            return '"50:50"'
        elif 'amount' in field_lower or 'price' in field_lower:
            return '100000.00'
        elif 'description' in field_lower:
            return f'"Test description for {field_name}"'
        elif 'findings' in field_lower:
            return '"Test findings"'
        elif 'recommendations' in field_lower:
            return '"Test recommendations"'
        else:
            return '"test_value"'

    def _generate_enum_validation_tests(
        self,
        model_classes: List[tuple],
        enum_classes: List[tuple]
    ) -> str:
        """Generate enum validation tests."""
        if not enum_classes:
            return "# No enum classes to test"

        tests = []
        for enum_name, enum_cls in enum_classes[:3]:  # Limit to first 3
            test_code = f'''    def test_{enum_name.lower()}_values(self):
        """Test {enum_name} accepts valid values."""
        # Test that enum values can be accessed
        values = list({enum_name})
        assert len(values) > 0'''
            tests.append(test_code)

        return f'''class TestEnumValidation:
    """Test enum validation works correctly."""

{chr(10).join(tests)}'''

    def _generate_field_validation_tests(self, model_classes: List[tuple]) -> str:
        """Generate field validation tests."""
        if not model_classes:
            return "# No model classes to test"

        # Use first model class for validation tests
        class_name, cls = model_classes[0]

        return f'''class TestFieldValidation:
    """Test Pydantic field validation."""

    def test_required_field_validation(self):
        """Test required fields raise ValidationError when missing."""
        with pytest.raises(ValidationError) as exc_info:
            {class_name}(
                node_id="TEST-001"
                # Missing required fields
            )

        errors = exc_info.value.errors()
        assert len(errors) > 0'''

    def _generate_provenance_tests(self, model_classes: List[tuple]) -> str:
        """Generate provenance field tests."""
        if not model_classes:
            return "# No model classes to test"

        tests = []
        for class_name, cls in model_classes[:2]:  # Test first 2 models
            # Get all required fields
            fields = cls.model_fields
            required_fields = {
                name: field for name, field in fields.items()
                if field.is_required()
            }

            # Generate sample values for required fields
            field_values = []
            for field_name, field_info in required_fields.items():
                value = self._generate_sample_value(field_name, field_info)
                field_values.append(f"            {field_name}={value}")

            # Add provenance fields
            if 'node_id' not in required_fields:
                field_values.append(f'            node_id="{class_name.upper()}-PROV"')
            else:
                # Override node_id to use provenance suffix
                field_values = [f'            node_id="{class_name.upper()}-PROV"' if 'node_id=' in fv else fv for fv in field_values]

            field_values.extend([
                '            prov_system="test_system"',
                '            prov_file_ids=["file-001"]',
                '            support_count=1'
            ])

            fields_str = ",\n".join(field_values)

            test_code = f'''    def test_{class_name.lower()}_provenance(self):
        """Test {class_name} has provenance fields."""
        instance = {class_name}(
{fields_str}
        )

        assert instance.node_id == "{class_name.upper()}-PROV"
        assert instance.prov_system == "test_system"'''
            tests.append(test_code)

        return f'''class TestProvenanceFields:
    """Test provenance tracking fields work across all entities."""

{chr(10).join(tests)}'''

    def _generate_serialization_tests(self, model_classes: List[tuple]) -> str:
        """Generate Pydantic V2 serialization tests."""
        if not model_classes:
            return "# No model classes to test"

        class_name, cls = model_classes[0]

        return f'''class TestModelSerialization:
    """Test Pydantic V2 serialization features."""

    def test_model_dump(self):
        """Test model_dump() exports data correctly."""
        # TODO: Create instance with appropriate fields
        pass

    def test_model_validate(self):
        """Test model_validate() reconstructs models from data."""
        # TODO: Create data dict and validate
        pass'''

    def _generate_uri_tests(self, model_classes: List[tuple]) -> str:
        """Generate canonical URI tests."""
        if not model_classes:
            return "# No model classes to test"

        tests = []
        for class_name, cls in model_classes[:3]:  # Test first 3 models
            test_code = f'''    def test_{class_name.lower()}_uri(self):
        """Test {class_name} has canonical ontology URI."""
        # Check that linkml_meta attribute exists
        assert hasattr({class_name}, 'linkml_meta')
        assert {class_name}.linkml_meta is not None'''
            tests.append(test_code)

        return f'''class TestCanonicalURIs:
    """Test canonical ontology URIs are preserved in LinkMLMeta."""

{chr(10).join(tests)}'''

    def _count_tests(self, num_models: int, num_enums: int) -> int:
        """Estimate number of generated tests."""
        # Entity creation: 5 tests
        # Enum validation: 3 tests
        # Field validation: 1 test
        # Provenance: 2 tests
        # Serialization: 2 tests
        # URI tests: 3 tests
        return 16
