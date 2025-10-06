"""
Import Test for Business V2 Module

Verifies:
1. All models can be imported from business_glue
2. Registries are populated correctly
3. Helper functions work
4. Graphiti compatibility verified for all models
"""

import json
import sys
from pathlib import Path

# Add generated models to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generated.pydantic.business_glue import (
    BUSINESS_ENTITIES,
    BUSINESS_EDGES,
    get_entity_model,
    get_edge_model,
    list_entity_types,
    list_edge_types,
    verify_graphiti_compatibility,
)

# Test results directory
RESULTS_DIR = Path(__file__).parent.parent / "test_results" / "module_verification"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def test_import():
    """Test 1: All imports work."""
    print("Test 1: Verifying imports...")

    results = {
        "test_name": "Import Test",
        "test_cases": []
    }

    # Test entity registry
    expected_entities = 10
    actual_entities = len(BUSINESS_ENTITIES)

    results["test_cases"].append({
        "case": f"Entity registry populated ({expected_entities} expected)",
        "passed": actual_entities == expected_entities,
        "actual": actual_entities,
        "entity_types": list(BUSINESS_ENTITIES.keys())
    })

    # Test edge registry
    expected_edges = 7
    actual_edges = len(BUSINESS_EDGES)

    results["test_cases"].append({
        "case": f"Edge registry populated ({expected_edges} expected)",
        "passed": actual_edges == expected_edges,
        "actual": actual_edges,
        "edge_types": list(BUSINESS_EDGES.keys())
    })

    results["total_cases"] = len(results["test_cases"])
    results["passed_cases"] = sum(1 for tc in results["test_cases"] if tc["passed"])
    results["success"] = results["passed_cases"] == results["total_cases"]

    with open(RESULTS_DIR / "test_import.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"  Result: {'PASSED' if results['success'] else 'FAILED'} ({results['passed_cases']}/{results['total_cases']} cases)")
    return results


def test_helper_functions():
    """Test 2: Helper functions work."""
    print("Test 2: Testing helper functions...")

    results = {
        "test_name": "Helper Functions Test",
        "test_cases": []
    }

    # Test get_entity_model
    try:
        model_cls = get_entity_model('BusinessOutcome')
        results["test_cases"].append({
            "case": "get_entity_model('BusinessOutcome')",
            "passed": model_cls.__name__ == 'BusinessOutcome',
            "model_name": model_cls.__name__
        })
    except Exception as e:
        results["test_cases"].append({
            "case": "get_entity_model('BusinessOutcome')",
            "passed": False,
            "error": str(e)
        })

    # Test get_edge_model
    try:
        model_cls = get_edge_model('Requires')
        results["test_cases"].append({
            "case": "get_edge_model('Requires')",
            "passed": model_cls.__name__ == 'Requires',
            "model_name": model_cls.__name__
        })
    except Exception as e:
        results["test_cases"].append({
            "case": "get_edge_model('Requires')",
            "passed": False,
            "error": str(e)
        })

    # Test list_entity_types
    entity_types = list_entity_types()
    results["test_cases"].append({
        "case": "list_entity_types()",
        "passed": len(entity_types) == 10,
        "count": len(entity_types)
    })

    # Test list_edge_types
    edge_types = list_edge_types()
    results["test_cases"].append({
        "case": "list_edge_types()",
        "passed": len(edge_types) == 7,
        "count": len(edge_types)
    })

    results["total_cases"] = len(results["test_cases"])
    results["passed_cases"] = sum(1 for tc in results["test_cases"] if tc["passed"])
    results["success"] = results["passed_cases"] == results["total_cases"]

    with open(RESULTS_DIR / "test_helper_functions.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"  Result: {'PASSED' if results['success'] else 'FAILED'} ({results['passed_cases']}/{results['total_cases']} cases)")
    return results


def test_graphiti_compatibility():
    """Test 3: All models are Graphiti compatible."""
    print("Test 3: Verifying Graphiti compatibility...")

    results = {
        "test_name": "Graphiti Compatibility Test",
        "test_cases": []
    }

    # Check all entity models
    for entity_type, model_cls in BUSINESS_ENTITIES.items():
        compat = verify_graphiti_compatibility(model_cls)
        results["test_cases"].append({
            "case": f"Entity: {entity_type}",
            "passed": compat['compatible'],
            "required_fields": compat['required_fields'],
            "optional_fields": compat['optional_fields'],
            "non_provenance_required": compat['non_provenance_required']
        })

    # Check all edge models
    for edge_type, model_cls in BUSINESS_EDGES.items():
        compat = verify_graphiti_compatibility(model_cls)
        results["test_cases"].append({
            "case": f"Edge: {edge_type}",
            "passed": compat['compatible'],
            "required_fields": compat['required_fields'],
            "optional_fields": compat['optional_fields'],
            "non_provenance_required": compat['non_provenance_required']
        })

    results["total_cases"] = len(results["test_cases"])
    results["passed_cases"] = sum(1 for tc in results["test_cases"] if tc["passed"])
    results["success"] = results["passed_cases"] == results["total_cases"]

    with open(RESULTS_DIR / "test_graphiti_compatibility.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"  Result: {'PASSED' if results['success'] else 'FAILED'} ({results['passed_cases']}/{results['total_cases']} cases)")
    return results


def run_all_tests():
    """Run all import tests."""
    print("=" * 70)
    print("Business V2 Module - Import and Registry Tests")
    print("=" * 70)
    print()

    all_results = []

    # Test 1: Import
    result1 = test_import()
    all_results.append(result1)
    print()

    # Test 2: Helper functions
    result2 = test_helper_functions()
    all_results.append(result2)
    print()

    # Test 3: Graphiti compatibility
    result3 = test_graphiti_compatibility()
    all_results.append(result3)
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
