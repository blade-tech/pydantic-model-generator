"""
Validation tests for Business V2 Pydantic models.

Tests verify:
1. Enum validation (status cannot be arbitrary strings)
2. Datetime validation (dates must be valid datetimes)
3. Numeric constraints (confidence 0-1, contract_value >= 0)
4. Provenance tracking (node_id, entity_type required)
5. Graphiti compatibility (all business fields Optional)
"""

import json
from datetime import datetime
from pathlib import Path
import sys

# Add generated models to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generated.pydantic.business_models import (
    BusinessOutcome, BusinessDecision, BusinessTask,
    Customer, Project, Actor,
    OutcomeStatus, DecisionStatus, TaskStatus,
    Priority, Severity, CompanySize, CustomerTier,
    Requires, Fulfills, BlockedBy
)
from pydantic import ValidationError

# Test results directory
RESULTS_DIR = Path(__file__).parent.parent / "test_results" / "business_v2"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def test_enum_validation():
    """Test 1: Enum fields reject invalid values."""
    results = {
        "test_name": "Enum Validation",
        "description": "Verify enums reject arbitrary strings",
        "test_cases": []
    }

    # Test Case 1.1: Valid enum value
    try:
        outcome = BusinessOutcome(
            node_id="test-node-1",
            entity_type="BusinessOutcome",
            status=OutcomeStatus.proposed
        )
        results["test_cases"].append({
            "case": "Valid enum (OutcomeStatus.proposed)",
            "passed": True,
            "error": None
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Valid enum (OutcomeStatus.proposed)",
            "passed": False,
            "error": str(e)
        })

    # Test Case 1.2: Invalid string (should fail)
    try:
        outcome = BusinessOutcome(
            node_id="test-node-2",
            entity_type="BusinessOutcome",
            status="banana"  # Invalid - not in enum
        )
        results["test_cases"].append({
            "case": "Invalid enum ('banana')",
            "passed": False,
            "error": "Should have raised ValidationError but didn't"
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Invalid enum ('banana')",
            "passed": True,
            "error": f"Correctly rejected: {str(e)[:100]}"
        })

    # Test Case 1.3: DecisionStatus enum
    try:
        decision = BusinessDecision(
            node_id="test-node-3",
            entity_type="BusinessDecision",
            decision_status=DecisionStatus.approved
        )
        results["test_cases"].append({
            "case": "Valid DecisionStatus enum",
            "passed": True,
            "error": None
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Valid DecisionStatus enum",
            "passed": False,
            "error": str(e)
        })

    results["total_cases"] = len(results["test_cases"])
    results["passed_cases"] = sum(1 for tc in results["test_cases"] if tc["passed"])
    results["success"] = results["passed_cases"] == results["total_cases"]

    # Save results
    with open(RESULTS_DIR / "test_enum_validation.json", "w") as f:
        json.dump(results, f, indent=2)

    return results

def test_datetime_validation():
    """Test 2: Datetime fields validate properly."""
    results = {
        "test_name": "Datetime Validation",
        "description": "Verify datetime fields accept datetime objects, not arbitrary strings",
        "test_cases": []
    }

    # Test Case 2.1: Valid datetime
    try:
        outcome = BusinessOutcome(
            node_id="test-node-4",
            entity_type="BusinessOutcome",
            due_date=datetime(2025, 12, 31)
        )
        results["test_cases"].append({
            "case": "Valid datetime object",
            "passed": True,
            "error": None,
            "value": str(outcome.due_date)
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Valid datetime object",
            "passed": False,
            "error": str(e)
        })

    # Test Case 2.2: ISO string (Pydantic should parse this)
    try:
        decision = BusinessDecision(
            node_id="test-node-5",
            entity_type="BusinessDecision",
            approved_at="2025-10-05T10:30:00"
        )
        results["test_cases"].append({
            "case": "ISO datetime string (should parse)",
            "passed": True,
            "error": None,
            "value": str(decision.approved_at)
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "ISO datetime string (should parse)",
            "passed": False,
            "error": str(e)
        })

    # Test Case 2.3: Invalid datetime string (should fail)
    try:
        outcome = BusinessOutcome(
            node_id="test-node-6",
            entity_type="BusinessOutcome",
            due_date="tomorrow"  # Invalid
        )
        results["test_cases"].append({
            "case": "Invalid datetime ('tomorrow')",
            "passed": False,
            "error": "Should have raised ValidationError but didn't"
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Invalid datetime ('tomorrow')",
            "passed": True,
            "error": f"Correctly rejected: {str(e)[:100]}"
        })

    results["total_cases"] = len(results["test_cases"])
    results["passed_cases"] = sum(1 for tc in results["test_cases"] if tc["passed"])
    results["success"] = results["passed_cases"] == results["total_cases"]

    with open(RESULTS_DIR / "test_datetime_validation.json", "w") as f:
        json.dump(results, f, indent=2)

    return results

def test_numeric_constraints():
    """Test 3: Numeric constraints enforced."""
    results = {
        "test_name": "Numeric Constraints",
        "description": "Verify numeric fields enforce constraints (ge, le)",
        "test_cases": []
    }

    # Test Case 3.1: Valid confidence (0-1)
    try:
        outcome = BusinessOutcome(
            node_id="test-node-7",
            entity_type="BusinessOutcome",
            confidence=0.75
        )
        results["test_cases"].append({
            "case": "Valid confidence (0.75)",
            "passed": True,
            "error": None
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Valid confidence (0.75)",
            "passed": False,
            "error": str(e)
        })

    # Test Case 3.2: Confidence > 1 (should fail)
    try:
        outcome = BusinessOutcome(
            node_id="test-node-8",
            entity_type="BusinessOutcome",
            confidence=150.0  # Invalid - exceeds maximum
        )
        results["test_cases"].append({
            "case": "Invalid confidence (150.0)",
            "passed": False,
            "error": "Should have raised ValidationError but didn't"
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Invalid confidence (150.0)",
            "passed": True,
            "error": f"Correctly rejected: {str(e)[:100]}"
        })

    # Test Case 3.3: Negative contract_value (should fail)
    try:
        customer = Customer(
            node_id="test-node-9",
            entity_type="Customer",
            contract_value=-1000.0  # Invalid - must be non-negative
        )
        results["test_cases"].append({
            "case": "Invalid contract_value (-1000)",
            "passed": False,
            "error": "Should have raised ValidationError but didn't"
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Invalid contract_value (-1000)",
            "passed": True,
            "error": f"Correctly rejected: {str(e)[:100]}"
        })

    # Test Case 3.4: Valid contract_value
    try:
        customer = Customer(
            node_id="test-node-10",
            entity_type="Customer",
            contract_value=50000.0
        )
        results["test_cases"].append({
            "case": "Valid contract_value (50000)",
            "passed": True,
            "error": None
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Valid contract_value (50000)",
            "passed": False,
            "error": str(e)
        })

    results["total_cases"] = len(results["test_cases"])
    results["passed_cases"] = sum(1 for tc in results["test_cases"] if tc["passed"])
    results["success"] = results["passed_cases"] == results["total_cases"]

    with open(RESULTS_DIR / "test_numeric_constraints.json", "w") as f:
        json.dump(results, f, indent=2)

    return results

def test_provenance_tracking():
    """Test 4: Provenance fields present and required."""
    results = {
        "test_name": "Provenance Tracking",
        "description": "Verify NodeProv/EdgeProv fields work correctly",
        "test_cases": []
    }

    # Test Case 4.1: node_id required
    try:
        outcome = BusinessOutcome(
            entity_type="BusinessOutcome"
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

    # Test Case 4.2: entity_type required
    try:
        outcome = BusinessOutcome(
            node_id="test-node-11"
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

    # Test Case 4.3: All provenance fields present
    try:
        outcome = BusinessOutcome(
            node_id="test-node-12",
            entity_type="BusinessOutcome",
            prov_system="test_suite",
            prov_file_ids=["file123"],
            prov_text_sha1s=["abc123"]
        )
        results["test_cases"].append({
            "case": "All provenance fields populated",
            "passed": True,
            "error": None,
            "provenance": {
                "node_id": outcome.node_id,
                "entity_type": outcome.entity_type,
                "prov_system": outcome.prov_system
            }
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "All provenance fields populated",
            "passed": False,
            "error": str(e)
        })

    # Test Case 4.4: Edge provenance (EdgeProv)
    try:
        edge = Requires(
            rel_id="test-rel-1",
            relation_type="Requires",
            criticality=Severity.high,
            deadline=datetime(2025, 12, 31)
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
    """Test 5: All business fields are Optional (Graphiti requirement)."""
    results = {
        "test_name": "Graphiti Compatibility",
        "description": "Verify all business fields Optional, only provenance required",
        "test_cases": []
    }

    # Test Case 5.1: Minimal BusinessOutcome (only required fields)
    try:
        outcome = BusinessOutcome(
            node_id="test-node-13",
            entity_type="BusinessOutcome"
            # All business fields omitted - should work
        )
        results["test_cases"].append({
            "case": "Minimal BusinessOutcome (only provenance)",
            "passed": True,
            "error": None,
            "model": {
                "node_id": outcome.node_id,
                "entity_type": outcome.entity_type,
                "status": outcome.status,  # Should be None
                "confidence": outcome.confidence  # Should be None
            }
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Minimal BusinessOutcome (only provenance)",
            "passed": False,
            "error": str(e)
        })

    # Test Case 5.2: Minimal Customer
    try:
        customer = Customer(
            node_id="test-node-14",
            entity_type="Customer"
        )
        results["test_cases"].append({
            "case": "Minimal Customer (only provenance)",
            "passed": True,
            "error": None
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Minimal Customer (only provenance)",
            "passed": False,
            "error": str(e)
        })

    # Test Case 5.3: Minimal Edge
    try:
        edge = Fulfills(
            rel_id="test-rel-2",
            relation_type="Fulfills"
        )
        results["test_cases"].append({
            "case": "Minimal Fulfills edge (only provenance)",
            "passed": True,
            "error": None
        })
    except ValidationError as e:
        results["test_cases"].append({
            "case": "Minimal Fulfills edge (only provenance)",
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
    print("Business V2 Pydantic Models - Validation Tests")
    print("=" * 70)
    print()

    all_results = []

    # Test 1: Enum Validation
    print("Running Test 1: Enum Validation...")
    result1 = test_enum_validation()
    all_results.append(result1)
    print(f"  Result: {'PASSED' if result1['success'] else 'FAILED'} ({result1['passed_cases']}/{result1['total_cases']} cases)")
    print()

    # Test 2: Datetime Validation
    print("Running Test 2: Datetime Validation...")
    result2 = test_datetime_validation()
    all_results.append(result2)
    print(f"  Result: {'PASSED' if result2['success'] else 'FAILED'} ({result2['passed_cases']}/{result2['total_cases']} cases)")
    print()

    # Test 3: Numeric Constraints
    print("Running Test 3: Numeric Constraints...")
    result3 = test_numeric_constraints()
    all_results.append(result3)
    print(f"  Result: {'PASSED' if result3['success'] else 'FAILED'} ({result3['passed_cases']}/{result3['total_cases']} cases)")
    print()

    # Test 4: Provenance Tracking
    print("Running Test 4: Provenance Tracking...")
    result4 = test_provenance_tracking()
    all_results.append(result4)
    print(f"  Result: {'PASSED' if result4['success'] else 'FAILED'} ({result4['passed_cases']}/{result4['total_cases']} cases)")
    print()

    # Test 5: Graphiti Compatibility
    print("Running Test 5: Graphiti Compatibility...")
    result5 = test_graphiti_compatibility()
    all_results.append(result5)
    print(f"  Result: {'PASSED' if result5['success'] else 'FAILED'} ({result5['passed_cases']}/{result5['total_cases']} cases)")
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
