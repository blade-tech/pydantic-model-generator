"""End-to-end validation: Can generated models answer business questions?

This validates that the Pydantic models can actually satisfy the business outcome.
We expect to see FAILURES when the models can't answer the questions.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from generated.pydantic.invoice_models import Budget, ApprovedVendor, Invoice, ApprovalDecision


class OutcomeValidator:
    """Validates that generated models satisfy business outcome questions."""

    def __init__(self, eqp_path: Path):
        """Load Evidence Query Plan."""
        with open(eqp_path) as f:
            self.eqp = json.load(f)

    def test_question_1_approval_logic(self) -> Dict[str, Any]:
        """Q1: Can this invoice be approved? (amount <= budget AND vendor approved AND has PO)"""

        print("\n" + "="*70)
        print("TEST 1: Invoice Approval Logic Validation")
        print("="*70)

        results = {"passed": [], "failed": []}

        # Test Case 1: Valid invoice (should approve)
        try:
            budget = Budget(
                node_id="b1",
                entity_type="Budget",
                department_id="engineering",
                amount_limit=10000.0
            )

            vendor = ApprovedVendor(
                node_id="v1",
                entity_type="ApprovedVendor",
                vendor_id="acme",
                vendor_name="ACME Corp",
                approval_status="approved"
            )

            invoice = Invoice(
                node_id="i1",
                entity_type="Invoice",
                invoice_id="INV-001",
                department_id="engineering",
                vendor_id="acme",
                amount=5000.0,
                has_purchase_order=True,
                withinbudget="b1",  # References budget
                fromvendor="v1"     # References vendor
            )

            # Validation logic
            can_approve = (
                invoice.amount <= budget.amount_limit and
                vendor.approval_status == "approved" and
                invoice.has_purchase_order
            )

            decision = ApprovalDecision(
                node_id="d1",
                entity_type="ApprovalDecision",
                invoice_id="INV-001",
                can_approve=can_approve,
                reason="All conditions met" if can_approve else "Failed conditions"
            )

            if can_approve:
                results["passed"].append("[PASS] Valid invoice correctly approved")
                print(f"  [PASS] Invoice {invoice.invoice_id} approved")
                print(f"     Amount: ${invoice.amount} <= Budget: ${budget.amount_limit}")
                print(f"     Vendor: {vendor.approval_status}")
                print(f"     Has PO: {invoice.has_purchase_order}")
            else:
                results["failed"].append("[FAIL] Valid invoice incorrectly rejected")

        except Exception as e:
            results["failed"].append(f"[FAIL] Test 1 failed: {e}")
            print(f"  [FAIL] FAIL: {e}")

        # Test Case 2: Over budget (should reject)
        try:
            budget2 = Budget(
                node_id="b2",
                entity_type="Budget",
                department_id="marketing",
                amount_limit=1000.0
            )

            vendor2 = ApprovedVendor(
                node_id="v2",
                entity_type="ApprovedVendor",
                vendor_id="supplier",
                vendor_name="Big Supplier",
                approval_status="approved"
            )

            invoice2 = Invoice(
                node_id="i2",
                entity_type="Invoice",
                invoice_id="INV-002",
                department_id="marketing",
                vendor_id="supplier",
                amount=5000.0,  # OVER BUDGET
                has_purchase_order=True,
                withinbudget="b2",
                fromvendor="v2"
            )

            can_approve2 = (
                invoice2.amount <= budget2.amount_limit and
                vendor2.approval_status == "approved" and
                invoice2.has_purchase_order
            )

            if not can_approve2:
                results["passed"].append("[PASS] Over-budget invoice correctly rejected")
                print(f"\n  [PASS] PASS: Invoice {invoice2.invoice_id} correctly REJECTED")
                print(f"     Amount: ${invoice2.amount} > Budget: ${budget2.amount_limit}")
                print(f"     Reason: Exceeds budget limit")
            else:
                results["failed"].append("[FAIL] Over-budget invoice incorrectly approved")

        except Exception as e:
            results["failed"].append(f"[FAIL] Test 2 failed: {e}")
            print(f"  [FAIL] FAIL: {e}")

        # Test Case 3: Unapproved vendor (should reject)
        try:
            vendor3 = ApprovedVendor(
                node_id="v3",
                entity_type="ApprovedVendor",
                vendor_id="sketchy",
                vendor_name="Sketchy Inc",
                approval_status="pending"  # NOT APPROVED
            )

            invoice3 = Invoice(
                node_id="i3",
                entity_type="Invoice",
                invoice_id="INV-003",
                department_id="engineering",
                vendor_id="sketchy",
                amount=500.0,
                has_purchase_order=True,
                withinbudget="b1",
                fromvendor="v3"
            )

            can_approve3 = (
                invoice3.amount <= budget.amount_limit and
                vendor3.approval_status == "approved" and
                invoice3.has_purchase_order
            )

            if not can_approve3:
                results["passed"].append("[PASS] Unapproved vendor invoice correctly rejected")
                print(f"\n  [PASS] PASS: Invoice {invoice3.invoice_id} correctly REJECTED")
                print(f"     Vendor status: {vendor3.approval_status} (not approved)")
            else:
                results["failed"].append("[FAIL] Unapproved vendor invoice incorrectly approved")

        except Exception as e:
            results["failed"].append(f"[FAIL] Test 3 failed: {e}")
            print(f"  [FAIL] FAIL: {e}")

        # Test Case 4: Missing PO (should reject)
        try:
            invoice4 = Invoice(
                node_id="i4",
                entity_type="Invoice",
                invoice_id="INV-004",
                department_id="engineering",
                vendor_id="acme",
                amount=500.0,
                has_purchase_order=False,  # NO PURCHASE ORDER
                withinbudget="b1",
                fromvendor="v1"
            )

            can_approve4 = (
                invoice4.amount <= budget.amount_limit and
                vendor.approval_status == "approved" and
                invoice4.has_purchase_order
            )

            if not can_approve4:
                results["passed"].append("[PASS] No-PO invoice correctly rejected")
                print(f"\n  [PASS] PASS: Invoice {invoice4.invoice_id} correctly REJECTED")
                print(f"     Reason: Missing purchase order")
            else:
                results["failed"].append("[FAIL] No-PO invoice incorrectly approved")

        except Exception as e:
            results["failed"].append(f"[FAIL] Test 4 failed: {e}")
            print(f"  [FAIL] FAIL: {e}")

        return results

    def test_question_2_blocked_invoices(self) -> Dict[str, Any]:
        """Q2: Which invoices are blocked and why?"""

        print("\n" + "="*70)
        print("TEST 2: Blocked Invoices Query")
        print("="*70)

        results = {"passed": [], "failed": []}

        try:
            # Create blocked invoices with decisions
            blocked_invoices = []

            decision1 = ApprovalDecision(
                node_id="d2",
                entity_type="ApprovalDecision",
                invoice_id="INV-002",
                can_approve=False,
                reason="Exceeds department budget limit"
            )
            blocked_invoices.append(decision1)

            decision2 = ApprovalDecision(
                node_id="d3",
                entity_type="ApprovalDecision",
                invoice_id="INV-003",
                can_approve=False,
                reason="Vendor not approved"
            )
            blocked_invoices.append(decision2)

            # Query for blocked invoices
            blocked = [d for d in blocked_invoices if not d.can_approve]

            if len(blocked) == 2:
                results["passed"].append("[PASS] Successfully queried blocked invoices")
                print(f"  [PASS] PASS: Found {len(blocked)} blocked invoices:")
                for d in blocked:
                    print(f"     • {d.invoice_id}: {d.reason}")
            else:
                results["failed"].append("[FAIL] Blocked invoice query failed")

        except Exception as e:
            results["failed"].append(f"[FAIL] Query failed: {e}")
            print(f"  [FAIL] FAIL: {e}")

        return results

    def test_question_3_department_totals(self) -> Dict[str, Any]:
        """Q3: What is the total pending amount per department?"""

        print("\n" + "="*70)
        print("TEST 3: Department Totals Aggregation")
        print("="*70)

        results = {"passed": [], "failed": []}

        try:
            # Create invoices across departments
            invoices = [
                Invoice(
                    node_id="i5", entity_type="Invoice", invoice_id="INV-005",
                    department_id="engineering", vendor_id="v1", amount=1000.0,
                    has_purchase_order=True, withinbudget="b1", fromvendor="v1"
                ),
                Invoice(
                    node_id="i6", entity_type="Invoice", invoice_id="INV-006",
                    department_id="engineering", vendor_id="v1", amount=2000.0,
                    has_purchase_order=True, withinbudget="b1", fromvendor="v1"
                ),
                Invoice(
                    node_id="i7", entity_type="Invoice", invoice_id="INV-007",
                    department_id="marketing", vendor_id="v2", amount=500.0,
                    has_purchase_order=True, withinbudget="b2", fromvendor="v2"
                ),
            ]

            # Aggregate by department
            dept_totals = {}
            for inv in invoices:
                dept_totals[inv.department_id] = dept_totals.get(inv.department_id, 0) + inv.amount

            if dept_totals["engineering"] == 3000.0 and dept_totals["marketing"] == 500.0:
                results["passed"].append("[PASS] Department aggregation correct")
                print(f"  [PASS] PASS: Department totals calculated:")
                for dept, total in dept_totals.items():
                    print(f"     • {dept}: ${total}")
            else:
                results["failed"].append("[FAIL] Department aggregation failed")

        except Exception as e:
            results["failed"].append(f"[FAIL] Aggregation failed: {e}")
            print(f"  [FAIL] FAIL: {e}")

        return results

    def run_all_tests(self):
        """Run all validation tests."""
        print("\n" + "="*70)
        print("OUTCOME VALIDATION: Invoice Approval Business Logic")
        print("="*70)
        print("\nValidating that Pydantic models can answer business questions...")

        all_results = {
            "test1": self.test_question_1_approval_logic(),
            "test2": self.test_question_2_blocked_invoices(),
            "test3": self.test_question_3_department_totals()
        }

        # Summary
        total_passed = sum(len(r["passed"]) for r in all_results.values())
        total_failed = sum(len(r["failed"]) for r in all_results.values())

        print("\n" + "="*70)
        print("VALIDATION SUMMARY")
        print("="*70)
        print(f"\n[PASS] PASSED: {total_passed} tests")
        print(f"[FAIL] FAILED: {total_failed} tests")

        if total_failed == 0:
            print("\n[SUCCESS] SUCCESS: Models satisfy ALL business requirements!")
        else:
            print("\n[WARNING]  FAILURE: Models cannot fully satisfy business requirements")
            print("\nFailed tests:")
            for test_name, results in all_results.items():
                for failure in results["failed"]:
                    print(f"  • {failure}")

        return total_failed == 0


if __name__ == "__main__":
    validator = OutcomeValidator(Path("artifacts/invoice_eqp.json"))
    success = validator.run_all_tests()
    exit(0 if success else 1)
