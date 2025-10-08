# Verification Guide - Testing Phase 1 & 2 Implementation

**Purpose:** Quick guide to verify the validation and auto-repair features are working correctly.

---

## Quick Verification (5 minutes)

### Step 1: Verify Files Exist

```bash
# Check validation utility
dir demo-app\backend\app\utils\linkml_validator.py

# Check documentation
dir docs\PHASE_2_AUTO_REPAIR_COMPLETE.md
dir docs\DEBUGGING_SUMMARY.md
dir docs\IMPLEMENTATION_STATUS.md
```

Expected: All files should exist.

---

### Step 2: Test Validation & Auto-Repair Utilities

```bash
cd demo-app/backend

python -c "
from app.utils.linkml_validator import validate_linkml_schema, auto_repair_schema

# Test schema with missing id slot
test_schema = '''
id: test
name: test_schema
classes:
  TestClass:
    slots:
      - id
      - name
slots:
  name:
    range: string
'''

print('=== VALIDATION TEST ===')
is_valid, errors = validate_linkml_schema(test_schema)
print(f'Valid: {is_valid}')
print(f'Errors: {len(errors)}')
if errors:
    print('First error:', errors[0])

print('\n=== AUTO-REPAIR TEST ===')
repaired, repairs = auto_repair_schema(test_schema)
print(f'Repairs made: {len(repairs)}')
if repairs:
    print('First repair:', repairs[0])

print('\n=== POST-REPAIR VALIDATION ===')
is_valid_after, errors_after = validate_linkml_schema(repaired)
print(f'Valid after repair: {is_valid_after}')
print(f'Errors after repair: {len(errors_after)}')
"
```

**Expected Output:**
```
=== VALIDATION TEST ===
Valid: False
Errors: 1
First error: Class 'TestClass' references undefined slot 'id'. Add this slot to the 'slots:' section.

=== AUTO-REPAIR TEST ===
Repairs made: 1
First repair: [OK] Auto-added 'id' slot definition (used by 1 classes: TestClass)

=== POST-REPAIR VALIDATION ===
Valid after repair: True
Errors after repair: 0
```

---

### Step 3: Verify Integration in Generation Router

```bash
# Check import is in place
cd demo-app/backend
python -c "
import ast
import inspect
from app.routers import generation

# Check if the module imports the validator
source = inspect.getsource(generation.generate_linkml_schema)
has_import = 'from app.utils.linkml_validator import' in source
has_validation = 'validate_linkml_schema' in source
has_repair = 'auto_repair_schema' in source

print('✅ Validator imported:', has_import)
print('✅ Validation called:', has_validation)
print('✅ Auto-repair called:', has_repair)
print('')
if has_import and has_validation and has_repair:
    print('SUCCESS: All integration points verified!')
else:
    print('WARNING: Integration may be incomplete')
"
```

**Expected Output:**
```
✅ Validator imported: True
✅ Validation called: True
✅ Auto-repair called: True

SUCCESS: All integration points verified!
```

---

## Full End-to-End Test (10 minutes)

### Step 1: Start Backend & Frontend

```bash
# Terminal 1: Backend
cd demo-app/backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd demo-app/frontend
npx next dev -p 3002
```

### Step 2: Generate LinkML Schema Through UI

1. Navigate to `http://localhost:3002`
2. Enter business text in Step 1 (e.g., "We need to audit Murabaha transactions for Shariah compliance.")
3. Complete Step 2 (Research Ontologies)
4. Complete Step 3 (Generate OutcomeSpec)
5. Complete Step 4 (Generate LinkML Schema)

### Step 3: Check Backend Logs for Validation

Look for these log patterns in the backend terminal:

**If schema is valid:**
```
INFO - 🔍 Starting schema validation
INFO - 📊 Validation complete - Valid: True, Completeness: {...}
INFO - ✅ Schema validation passed
```

**If schema has missing id slot (auto-repair triggered):**
```
INFO - 🔍 Starting schema validation
WARNING - ⚠️  LinkML schema has validation errors: 7 issues found
INFO - 🔧 Attempting auto-repair of common issues...
INFO - ✅ Auto-repair successful: 1 repairs made
INFO -   [OK] Auto-added 'id' slot definition (used by 7 classes: ...)
INFO - ✅ Schema is now valid after auto-repair
```

**If schema has other issues (partial repair):**
```
INFO - 🔍 Starting schema validation
WARNING - ⚠️  LinkML schema has validation errors: 10 issues found
INFO - 🔧 Attempting auto-repair of common issues...
INFO - ✅ Auto-repair successful: 2 repairs made
INFO -   [OK] Auto-added 'id' slot definition (used by 8 classes: ...)
INFO -   [OK] Auto-added 'name' slot definition (used by 5 classes: ...)
WARNING - ⚠️  Schema still has 3 errors after auto-repair
```

### Step 4: Verify Auto-Repair Messages in UI

In the frontend, check for notification messages:
- ✅ "Auto-repaired schema: N fixes applied" (success)
- ⚠️ "Partial auto-repair: N fixes applied, M issues remain" (partial)
- ⚠️ "Schema validation found N issues. Check logs for details." (no repair possible)

---

## Troubleshooting

### Issue: Validation logs not appearing

**Symptom:** Backend logs don't show any validation messages (🔍, ✅, ⚠️)

**Cause:** Backend hasn't reloaded with new code OR validation error occurred

**Fix:**
1. Stop backend (Ctrl+C)
2. Restart backend: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
3. Watch for "Application startup complete" message
4. Generate a new LinkML schema through UI
5. Check logs again

### Issue: Import error

**Symptom:** Backend crashes with "ModuleNotFoundError: No module named 'app.utils.linkml_validator'"

**Cause:** Validator file missing or in wrong location

**Fix:**
```bash
# Check file exists
dir demo-app\backend\app\utils\linkml_validator.py

# If missing, the file might not have been created
# Re-check the implementation
```

### Issue: Auto-repair not triggering

**Symptom:** Validation errors appear but no auto-repair attempts

**Cause:** Integration code might not be calling auto_repair_schema

**Fix:**
```bash
# Verify integration in generation.py
grep -n "auto_repair_schema" demo-app/backend/app/routers/generation.py

# Should see line 182 (import) and line 197 (call)
```

---

## Success Criteria

✅ **Phase 1 Complete** if:
- Validation utility tests pass
- Integration imports verified
- Validation logs appear in backend during LinkML generation

✅ **Phase 2 Complete** if:
- Auto-repair utility tests pass (100% success on test case)
- Auto-repair logs appear when schema has missing `id` slot
- Repaired schemas are valid after repair

✅ **Production Ready** if:
- End-to-end test shows validation and auto-repair working
- Frontend displays repair notifications
- gen-pydantic succeeds with repaired schemas

---

## Next Steps After Verification

1. **Monitor production logs** for auto-repair effectiveness
2. **Collect metrics** on repair success rates
3. **Identify new patterns** for Phase 3 enhancements
4. **Consider LLM-based repair** for complex cases (Phase 3)

---

## Support

- **Documentation**: See `docs/DEBUGGING_SUMMARY.md` for complete details
- **Phase 2 Details**: See `docs/PHASE_2_AUTO_REPAIR_COMPLETE.md`
- **Implementation Status**: See `docs/IMPLEMENTATION_STATUS.md`

---

**Last Updated:** 2025-10-07
**Status:** ✅ All verification steps documented
