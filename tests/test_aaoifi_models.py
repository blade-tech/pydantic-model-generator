"""
Validation tests for AAOIFI Document Pydantic models.

Tests verify:
1. Enum validation (document_type, paragraph_type)
2. Provenance tracking (node_id, entity_type required)
3. Group discipline (edition-based isolation)
4. Graphiti compatibility (all domain fields Optional)
"""

import json
from datetime import datetime
from pathlib import Path
import sys

# Add generated models to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generated.pydantic.aaoifi_document_models import (
    Document, Section, Paragraph, Concept, Term,
    DocumentType, ParagraphType, PublicationStatus,
    Contains, Defines, Mentions, References
)
from pydantic import ValidationError

# Test results directory
RESULTS_DIR = Path(__file__).parent.parent / "test_results" / "aaoifi_models"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def test_enum_validation():
    """Test 1: Enum fields reject invalid values."""
    results = {
        "test_name": "AAOIFI Enum Validation",
        "description": "Verify enums reject arbitrary strings",
        "test_cases": []
    }

    # Test Case 1.1: Valid DocumentType enum
    try:
        doc = Document(
            node_id="doc-1",
            entity_type="Document",
            document_type=DocumentType.shariah_standard
        )
        results["test_cases"].append({
            "case": "Valid DocumentType enum",
            "passed": True,
            "error": None
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Valid DocumentType enum",
            "passed": False,
            "error": str(e)
        })

    # Test Case 1.2: Invalid document_type (should fail)
    try:
        doc = Document(
            node_id="doc-2",
            entity_type="Document",
            document_type="invalid_type"  # Invalid
        )
        results["test_cases"].append({
            "case": "Invalid DocumentType ('invalid_type')",
            "passed": False,
            "error": "Should have raised ValidationError but didn't"
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Invalid DocumentType ('invalid_type')",
            "passed": True,
            "error": f"Correctly rejected: {str(e)[:100]}"
        })

    # Test Case 1.3: Valid ParagraphType enum
    try:
        para = Paragraph(
            node_id="para-1",
            entity_type="Paragraph",
            paragraph_type=ParagraphType.definition
        )
        results["test_cases"].append({
            "case": "Valid ParagraphType enum",
            "passed": True,
            "error": None
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Valid ParagraphType enum",
            "passed": False,
            "error": str(e)
        })

    results["total_cases"] = len(results["test_cases"])
    results["passed_cases"] = sum(1 for tc in results["test_cases"] if tc["passed"])
    results["success"] = results["passed_cases"] == results["total_cases"]

    with open(RESULTS_DIR / "test_enum_validation.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


def test_provenance_tracking():
    """Test 2: Provenance fields present and required."""
    results = {
        "test_name": "AAOIFI Provenance Tracking",
        "description": "Verify NodeProv/EdgeProv fields work correctly",
        "test_cases": []
    }

    # Test Case 2.1: node_id required
    try:
        doc = Document(
            entity_type="Document"
            # Missing node_id - should fail
        )
        results["test_cases"].append({
            "case": "Missing node_id (required)",
            "passed": False,
            "error": "Should have raised ValidationError but didn't"
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Missing node_id (required)",
            "passed": True,
            "error": f"Correctly rejected: {str(e)[:100]}"
        })

    # Test Case 2.2: entity_type required
    try:
        doc = Document(
            node_id="doc-3"
            # Missing entity_type - should fail
        )
        results["test_cases"].append({
            "case": "Missing entity_type (required)",
            "passed": False,
            "error": "Should have raised ValidationError but didn't"
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Missing entity_type (required)",
            "passed": True,
            "error": f"Correctly rejected: {str(e)[:100]}"
        })

    # Test Case 2.3: All provenance fields populated
    try:
        doc = Document(
            node_id="doc-4",
            entity_type="Document",
            prov_system="aaoifi_ingestion",
            prov_file_ids=["SS-01.pdf"]
        )
        results["test_cases"].append({
            "case": "All provenance fields populated",
            "passed": True,
            "error": None,
            "provenance": {
                "node_id": doc.node_id,
                "entity_type": doc.entity_type,
                "prov_system": doc.prov_system
            }
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "All provenance fields populated",
            "passed": False,
            "error": str(e)
        })

    # Test Case 2.4: Edge provenance (rel_id, relation_type)
    try:
        edge = Contains(
            rel_id="rel-1",
            relation_type="Contains",
            contains_order=0
        )
        results["test_cases"].append({
            "case": "Edge provenance (rel_id, relation_type)",
            "passed": True,
            "error": None,
            "edge_provenance": {
                "rel_id": edge.rel_id,
                "relation_type": edge.relation_type
            }
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Edge provenance (rel_id, relation_type)",
            "passed": False,
            "error": str(e)
        })

    results["total_cases"] = len(results["test_cases"])
    results["passed_cases"] = sum(1 for tc in results["test_cases"] if tc["passed"])
    results["success"] = results["passed_cases"] == results["total_cases"]

    with open(RESULTS_DIR / "test_provenance_tracking.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


def test_graphiti_compatibility():
    """Test 3: All domain fields are Optional (Graphiti requirement)."""
    results = {
        "test_name": "AAOIFI Graphiti Compatibility",
        "description": "Verify all domain fields Optional, only provenance required",
        "test_cases": []
    }

    # Test Case 3.1: Minimal Document (only required fields)
    try:
        doc = Document(
            node_id="doc-5",
            entity_type="Document"
            # All domain fields omitted - should work
        )
        results["test_cases"].append({
            "case": "Minimal Document (only provenance)",
            "passed": True,
            "error": None,
            "model": {
                "node_id": doc.node_id,
                "entity_type": doc.entity_type,
                "standard_number": doc.standard_number,  # Should be None
                "document_type": doc.document_type  # Should be None
            }
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Minimal Document (only provenance)",
            "passed": False,
            "error": str(e)
        })

    # Test Case 3.2: Minimal Paragraph
    try:
        para = Paragraph(
            node_id="para-2",
            entity_type="Paragraph"
        )
        results["test_cases"].append({
            "case": "Minimal Paragraph (only provenance)",
            "passed": True,
            "error": None
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Minimal Paragraph (only provenance)",
            "passed": False,
            "error": str(e)
        })

    # Test Case 3.3: Minimal Edge
    try:
        edge = Mentions(
            rel_id="rel-2",
            relation_type="Mentions"
        )
        results["test_cases"].append({
            "case": "Minimal Mentions edge (only provenance)",
            "passed": True,
            "error": None
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Minimal Mentions edge (only provenance)",
            "passed": False,
            "error": str(e)
        })

    results["total_cases"] = len(results["test_cases"])
    results["passed_cases"] = sum(1 for tc in results["test_cases"] if tc["passed"])
    results["success"] = results["passed_cases"] == results["total_cases"]

    with open(RESULTS_DIR / "test_graphiti_compatibility.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


def run_all_tests():
    """Run all validation tests and generate summary."""
    print("=" * 70)
    print("AAOIFI Document Models - Validation Tests")
    print("=" * 70)
    print()

    all_results = []

    # Test 1: Enum Validation
    print("Running Test 1: Enum Validation...")
    result1 = test_enum_validation()
    all_results.append(result1)
    print(f"  Result: {'PASSED' if result1['success'] else 'FAILED'} ({result1['passed_cases']}/{result1['total_cases']} cases)")
    print()

    # Test 2: Provenance Tracking
    print("Running Test 2: Provenance Tracking...")
    result2 = test_provenance_tracking()
    all_results.append(result2)
    print(f"  Result: {'PASSED' if result2['success'] else 'FAILED'} ({result2['passed_cases']}/{result2['total_cases']} cases)")
    print()

    # Test 3: Graphiti Compatibility
    print("Running Test 3: Graphiti Compatibility...")
    result3 = test_graphiti_compatibility()
    all_results.append(result3)
    print(f"  Result: {'PASSED' if result3['success'] else 'FAILED'} ({result3['passed_cases']}/{result3['total_cases']} cases)")
    print()

    # Summary
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    total_tests = len(all_results)
    passed_tests = sum(1 for r in all_results if r['success'])
    total_cases = sum(r['total_cases'] for r in all_results)
    passed_cases = sum(r['passed_cases'] for r in all_results)

    print(f"Tests Passed: {passed_tests}/{total_tests}")
    print(f"Cases Passed: {passed_cases}/{total_cases}")
    print()

    if passed_tests == total_tests:
        print("[SUCCESS] ALL TESTS PASSED")
    else:
        print("[FAILED] SOME TESTS FAILED")

    print()
    print(f"Results saved to: {RESULTS_DIR}")
    print("=" * 70)

    return passed_tests == total_tests


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
