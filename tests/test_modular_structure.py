"""
Modular Structure Integration Test

Verifies:
1. Core modules work (provenance, ids, registries, plugin_loader)
2. Domain plugin discovery works
3. Business domain loads correctly
4. Global registries populate correctly
"""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from graphmodels.core import (
    NodeProv,
    EdgeProv,
    make_node_id,
    make_edge_id,
    register_domain,
    get_entity_model,
    get_edge_model,
    list_entity_types,
    list_edge_types,
    list_domains,
    discover_domains,
    load_all_domains,
)

# Test results directory
RESULTS_DIR = project_root / "test_results" / "module_verification"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def test_core_imports():
    """Test 1: Core modules import correctly."""
    print("Test 1: Testing core imports...")

    results = {
        "test_name": "Core Imports Test",
        "test_cases": []
    }

    # Test NodeProv
    results["test_cases"].append({
        "case": "NodeProv imported",
        "passed": NodeProv is not None,
    })

    # Test EdgeProv
    results["test_cases"].append({
        "case": "EdgeProv imported",
        "passed": EdgeProv is not None,
    })

    # Test make_node_id
    try:
        node_id = make_node_id("TestEntity", "test-label")
        results["test_cases"].append({
            "case": "make_node_id() works",
            "passed": node_id.startswith("node:testentity:"),
            "value": node_id
        })
    except Exception as e:
        results["test_cases"].append({
            "case": "make_node_id() works",
            "passed": False,
            "error": str(e)
        })

    # Test make_edge_id
    try:
        edge_id = make_edge_id("TestRelation", "node:a:123", "node:b:456")
        results["test_cases"].append({
            "case": "make_edge_id() works",
            "passed": edge_id.startswith("rel:testrelation:"),
            "value": edge_id
        })
    except Exception as e:
        results["test_cases"].append({
            "case": "make_edge_id() works",
            "passed": False,
            "error": str(e)
        })

    results["total_cases"] = len(results["test_cases"])
    results["passed_cases"] = sum(1 for tc in results["test_cases"] if tc["passed"])
    results["success"] = results["passed_cases"] == results["total_cases"]

    with open(RESULTS_DIR / "test_core_imports.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"  Result: {'PASSED' if results['success'] else 'FAILED'} ({results['passed_cases']}/{results['total_cases']} cases)")
    return results


def test_domain_discovery():
    """Test 2: Domain discovery works."""
    print("Test 2: Testing domain discovery...")

    results = {
        "test_name": "Domain Discovery Test",
        "test_cases": []
    }

    domains_path = project_root / "graphmodels" / "domains"

    # Test discover_domains
    try:
        discovered = discover_domains(domains_path)
        results["test_cases"].append({
            "case": "discover_domains() finds business domain",
            "passed": "business" in discovered,
            "discovered": discovered
        })
    except Exception as e:
        results["test_cases"].append({
            "case": "discover_domains() finds business domain",
            "passed": False,
            "error": str(e)
        })

    results["total_cases"] = len(results["test_cases"])
    results["passed_cases"] = sum(1 for tc in results["test_cases"] if tc["passed"])
    results["success"] = results["passed_cases"] == results["total_cases"]

    with open(RESULTS_DIR / "test_domain_discovery.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"  Result: {'PASSED' if results['success'] else 'FAILED'} ({results['passed_cases']}/{results['total_cases']} cases)")
    return results


def test_plugin_loading():
    """Test 3: Plugin loading populates global registries."""
    print("Test 3: Testing plugin loading...")

    results = {
        "test_name": "Plugin Loading Test",
        "test_cases": []
    }

    domains_path = project_root / "graphmodels" / "domains"

    # Load all domains
    try:
        loaded = load_all_domains(domains_path)
        results["test_cases"].append({
            "case": "load_all_domains() loads business",
            "passed": "business" in loaded,
            "loaded": loaded
        })
    except Exception as e:
        results["test_cases"].append({
            "case": "load_all_domains() loads business",
            "passed": False,
            "error": str(e)
        })

    # Check global registry
    try:
        entity_types = list_entity_types()
        results["test_cases"].append({
            "case": "Global entity registry populated (10 expected)",
            "passed": len(entity_types) == 10,
            "count": len(entity_types),
            "types": entity_types
        })
    except Exception as e:
        results["test_cases"].append({
            "case": "Global entity registry populated (10 expected)",
            "passed": False,
            "error": str(e)
        })

    try:
        edge_types = list_edge_types()
        results["test_cases"].append({
            "case": "Global edge registry populated (7 expected)",
            "passed": len(edge_types) == 7,
            "count": len(edge_types),
            "types": edge_types
        })
    except Exception as e:
        results["test_cases"].append({
            "case": "Global edge registry populated (7 expected)",
            "passed": False,
            "error": str(e)
        })

    # Test model retrieval
    try:
        model_cls = get_entity_model('BusinessOutcome')
        results["test_cases"].append({
            "case": "get_entity_model('BusinessOutcome') works",
            "passed": model_cls is not None and model_cls.__name__ == 'BusinessOutcome',
            "model_name": model_cls.__name__ if model_cls else None
        })
    except Exception as e:
        results["test_cases"].append({
            "case": "get_entity_model('BusinessOutcome') works",
            "passed": False,
            "error": str(e)
        })

    try:
        model_cls = get_edge_model('Requires')
        results["test_cases"].append({
            "case": "get_edge_model('Requires') works",
            "passed": model_cls is not None and model_cls.__name__ == 'Requires',
            "model_name": model_cls.__name__ if model_cls else None
        })
    except Exception as e:
        results["test_cases"].append({
            "case": "get_edge_model('Requires') works",
            "passed": False,
            "error": str(e)
        })

    # Test list_domains
    try:
        domains = list_domains()
        results["test_cases"].append({
            "case": "list_domains() returns ['business']",
            "passed": domains == ['business'],
            "domains": domains
        })
    except Exception as e:
        results["test_cases"].append({
            "case": "list_domains() returns ['business']",
            "passed": False,
            "error": str(e)
        })

    results["total_cases"] = len(results["test_cases"])
    results["passed_cases"] = sum(1 for tc in results["test_cases"] if tc["passed"])
    results["success"] = results["passed_cases"] == results["total_cases"]

    with open(RESULTS_DIR / "test_plugin_loading.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"  Result: {'PASSED' if results['success'] else 'FAILED'} ({results['passed_cases']}/{results['total_cases']} cases)")
    return results


def run_all_tests():
    """Run all modular structure tests."""
    print("=" * 70)
    print("Modular Structure - Integration Tests")
    print("=" * 70)
    print()

    all_results = []

    # Test 1: Core imports
    result1 = test_core_imports()
    all_results.append(result1)
    print()

    # Test 2: Domain discovery
    result2 = test_domain_discovery()
    all_results.append(result2)
    print()

    # Test 3: Plugin loading
    result3 = test_plugin_loading()
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
