"""LinkML schema validation utilities."""

import yaml
from typing import Set, Dict, List, Tuple


def validate_linkml_schema(schema_yaml: str) -> Tuple[bool, List[str]]:
    """Validate LinkML schema for completeness.

    Checks:
    1. All slots referenced in classes are defined in slots section
    2. All enums referenced in ranges are defined in enums section

    Args:
        schema_yaml: LinkML schema as YAML string

    Returns:
        Tuple of (is_valid, error_messages)
    """
    try:
        schema = yaml.safe_load(schema_yaml)
    except yaml.YAMLError as e:
        return False, [f"Invalid YAML: {str(e)}"]

    errors = []

    # Get defined slots
    defined_slots = set(schema.get('slots', {}).keys())

    # Get defined enums
    defined_enums = set(schema.get('enums', {}).keys())

    # Get all classes
    classes = schema.get('classes', {})

    # Check each class for undefined slot references
    for class_name, class_def in classes.items():
        # Get slots used by this class
        class_slots = class_def.get('slots', [])

        for slot_name in class_slots:
            if slot_name not in defined_slots:
                errors.append(
                    f"Class '{class_name}' references undefined slot '{slot_name}'. "
                    f"Add this slot to the 'slots:' section."
                )

    # Check slot ranges for undefined enums
    for slot_name, slot_def in schema.get('slots', {}).items():
        slot_range = slot_def.get('range')

        if slot_range:
            # Check if range is a custom enum (not a built-in type)
            builtin_types = {
                'string', 'integer', 'float', 'boolean', 'date', 'datetime',
                'time', 'uri', 'uriorcurie', 'ncname', 'xsd:string',
                'xsd:integer', 'xsd:float', 'xsd:boolean', 'xsd:date',
                'xsd:dateTime', 'xsd:time', 'xsd:anyURI'
            }

            # Also check if it's a reference to another class
            referenced_classes = set(classes.keys())

            if (slot_range not in builtin_types and
                slot_range not in referenced_classes and
                slot_range.endswith('Enum') and
                slot_range not in defined_enums):
                errors.append(
                    f"Slot '{slot_name}' has range '{slot_range}' but this enum is not defined. "
                    f"Add '{slot_range}' to the 'enums:' section."
                )

    return len(errors) == 0, errors


def get_schema_completeness_report(schema_yaml: str) -> Dict:
    """Get detailed report on schema completeness.

    Returns statistics about defined vs undefined elements.

    Args:
        schema_yaml: LinkML schema as YAML string

    Returns:
        Dictionary with completeness statistics
    """
    try:
        schema = yaml.safe_load(schema_yaml)
    except yaml.YAMLError:
        return {"error": "Invalid YAML"}

    # Count elements
    num_classes = len(schema.get('classes', {}))
    num_slots_defined = len(schema.get('slots', {}))
    num_enums_defined = len(schema.get('enums', {}))

    # Count slot references
    slot_references = set()
    for class_def in schema.get('classes', {}).values():
        slot_references.update(class_def.get('slots', []))

    # Count enum references
    enum_references = set()
    for slot_def in schema.get('slots', {}).values():
        slot_range = slot_def.get('range', '')
        if slot_range.endswith('Enum'):
            enum_references.add(slot_range)

    return {
        "classes": num_classes,
        "slots_defined": num_slots_defined,
        "slots_referenced": len(slot_references),
        "slots_missing": len(slot_references - set(schema.get('slots', {}).keys())),
        "enums_defined": num_enums_defined,
        "enums_referenced": len(enum_references),
        "enums_missing": len(enum_references - set(schema.get('enums', {}).keys()))
    }


def auto_repair_schema(schema_yaml: str) -> Tuple[str, List[str]]:
    """Automatically repair common LinkML schema issues.

    Repairs:
    1. Missing 'id' slot when multiple classes reference it
    2. Other common missing slots that follow standard patterns

    Args:
        schema_yaml: LinkML schema as YAML string

    Returns:
        Tuple of (repaired_yaml, list_of_repairs_made)
    """
    try:
        schema = yaml.safe_load(schema_yaml)
    except yaml.YAMLError as e:
        return schema_yaml, [f"Could not repair: Invalid YAML - {str(e)}"]

    repairs_made = []

    # Get all slot references across classes
    slot_references = {}
    for class_name, class_def in schema.get('classes', {}).items():
        for slot_name in class_def.get('slots', []):
            if slot_name not in slot_references:
                slot_references[slot_name] = []
            slot_references[slot_name].append(class_name)

    # Get defined slots
    defined_slots = set(schema.get('slots', {}).keys())

    # Initialize slots section if it doesn't exist
    if 'slots' not in schema:
        schema['slots'] = {}

    # Repair missing 'id' slot if referenced by multiple classes
    if 'id' in slot_references and 'id' not in defined_slots:
        num_classes_using_id = len(slot_references['id'])
        schema['slots']['id'] = {
            'description': 'Unique identifier',
            'range': 'string',
            'identifier': True,
            'required': True
        }
        repairs_made.append(
            f"[OK] Auto-added 'id' slot definition (used by {num_classes_using_id} classes: {', '.join(slot_references['id'])})"
        )

    # Repair other common missing slots with standard patterns
    common_slot_patterns = {
        'name': {
            'description': 'Name or title',
            'range': 'string',
            'required': False
        },
        'description': {
            'description': 'Detailed description',
            'range': 'string',
            'required': False
        },
        'created_at': {
            'description': 'Creation timestamp',
            'range': 'datetime',
            'required': False
        },
        'updated_at': {
            'description': 'Last update timestamp',
            'range': 'datetime',
            'required': False
        }
    }

    for slot_name, slot_def in common_slot_patterns.items():
        if slot_name in slot_references and slot_name not in defined_slots:
            # Only auto-add if used by at least 2 classes (to avoid false positives)
            if len(slot_references[slot_name]) >= 2:
                schema['slots'][slot_name] = slot_def
                repairs_made.append(
                    f"[OK] Auto-added '{slot_name}' slot definition (used by {len(slot_references[slot_name])} classes)"
                )

    # Convert back to YAML
    if repairs_made:
        repaired_yaml = yaml.dump(schema, default_flow_style=False, sort_keys=False, allow_unicode=True)
        return repaired_yaml, repairs_made
    else:
        return schema_yaml, []
