# Architecture Alignment Report

## Executive Summary

**Date:** 2025-10-06
**Status:** ⚠️ **MISALIGNMENT DETECTED**

The current Pydantic library structure does NOT fully align with the unified outcome-driven strategy documented in `UNIFIED_ARCHITECTURE_STRATEGY.md`.

---

## Current State Analysis

### What Exists Now

#### 1. Schema Organization (✅ ALIGNED)
```
schemas/
├── core.yaml                          ✅ Core infrastructure
└── overlays/                          ✅ Outcome-driven overlays
    ├── business_overlay.yaml          ✅ Generated overlay
    ├── document_overlay.yaml          ✅ Generated overlay
    ├── invoice_overlay.yaml           ✅ Generated overlay
    └── murabaha_audit_overlay.yaml    ✅ Generated overlay
```

**Assessment:** ✅ **CORRECT** - Following outcome-driven pattern with overlays

#### 2. Runtime Organization (❌ MISALIGNED)
```
graphmodels/
├── core/                              ✅ Core infrastructure
│   ├── __init__.py
│   ├── provenance.py
│   ├── ids.py
│   ├── registries.py
│   └── plugin_loader.py
└── domains/                           ❌ SHOULD BE overlays/
    ├── aaoifi/                        ❌ Domain-based (static)
    ├── business/                      ❌ Domain-based (static)
    └── murabaha_audit/                ❌ Domain-based (static)
```

**Assessment:** ❌ **INCORRECT** - Using domain-based organization instead of outcome-based overlays

#### 3. Documentation (✅ ALIGNED)
```
v1_to_v2_migration/
├── UNIFIED_ARCHITECTURE_STRATEGY.md   ✅ Outcome-driven strategy
├── MODULAR_PYDANTIC_ARCHITECTURE.md   ⚠️  Domain-driven (outdated)
└── AGENT_DRIVEN_ONTOLOGY_PIPELINE.md  ✅ Outcome-driven pipeline
```

**Assessment:** ⚠️ **PARTIALLY ALIGNED** - `MODULAR_PYDANTIC_ARCHITECTURE.md` is outdated

---

## Gap Analysis

### Critical Misalignment

| Component | Expected (Strategy) | Actual (Implementation) | Status |
|-----------|---------------------|-------------------------|--------|
| **Schema Directory** | `schemas/overlays/` | `schemas/overlays/` | ✅ ALIGNED |
| **Runtime Directory** | `graphmodels/overlays/` | `graphmodels/domains/` | ❌ MISALIGNED |
| **Plugin Organization** | Outcome-based plugins | Domain-based plugins | ❌ MISALIGNED |
| **Documentation** | Outcome-driven | Mixed (domain + outcome) | ⚠️ PARTIAL |

### Specific Issues

#### Issue 1: Directory Naming Mismatch
```
❌ Current:  graphmodels/domains/business/
✅ Expected: graphmodels/overlays/business_outcomes/
```

**Impact:**
- Directory name implies domain-based organization
- Conflicts with outcome-driven strategy documentation
- Plugin loader discovers "domains" not "overlays"

#### Issue 2: Plugin Naming Conflict
```python
# Current: graphmodels/domains/aaoifi/__init__.py
❌ Domain-based naming (aaoifi/)

# Expected: graphmodels/overlays/aaoifi_standards/__init__.py
✅ Outcome-based naming (aaoifi_standards/)
```

**Impact:**
- Plugin names don't reflect outcomes (questions to answer)
- Cannot distinguish between "aaoifi_standards" vs "aaoifi_contracts" outcomes
- Loses traceability to OutcomeSpec

#### Issue 3: Missing OutcomeSpec ↔ Plugin Mapping
```
❌ No clear mapping between:
   - specs/aaoifi_standards_extraction.yaml → graphmodels/domains/aaoifi/

✅ Should be:
   - specs/aaoifi_standards_extraction.yaml → graphmodels/overlays/aaoifi_standards/
   - specs/murabaha_audit.yaml → graphmodels/overlays/murabaha_audit/
```

**Impact:**
- Cannot trace plugin back to its OutcomeSpec
- Cannot validate which questions the plugin answers
- No closed-loop validation possible

---

## Recommended Remediation

### Option 1: Full Alignment (Recommended)

**Rename directories to match outcome-driven strategy:**

```bash
# Step 1: Rename domains/ to overlays/
mv graphmodels/domains graphmodels/overlays

# Step 2: Rename domain plugins to outcome plugins
cd graphmodels/overlays
mv business business_outcomes
mv aaoifi aaoifi_standards
# murabaha_audit already outcome-named ✅

# Step 3: Update plugin_loader.py
# Change: domains_path = Path("graphmodels/domains")
# To:     overlays_path = Path("graphmodels/overlays")
```

**Benefits:**
- ✅ Consistent with documentation
- ✅ Clear outcome-to-plugin mapping
- ✅ Enables closed-loop validation
- ✅ Matches schema organization

**Effort:** 1-2 hours (straightforward rename + update imports)

### Option 2: Hybrid Approach (Not Recommended)

**Keep `graphmodels/domains/` but treat as overlays:**

```python
# Update documentation only:
# "domains/ directory contains outcome-based overlays (legacy naming)"
```

**Benefits:**
- ✅ No code changes required
- ✅ Works immediately

**Drawbacks:**
- ❌ Confusing terminology (domains vs overlays)
- ❌ Cannot add multiple outcomes per domain
- ❌ Documentation remains inconsistent

**Effort:** 30 minutes (documentation update only)

---

## Detailed Remediation Plan (Option 1)

### Phase 1: Rename Directories (30 min)

```bash
# Backup first
cp -r graphmodels/domains graphmodels/domains.backup

# Rename to overlays
mv graphmodels/domains graphmodels/overlays

# Rename plugins to outcome-based names
cd graphmodels/overlays
mv business business_outcomes
mv aaoifi aaoifi_standards
```

### Phase 2: Update Plugin Loader (15 min)

```python
# graphmodels/core/plugin_loader.py

# Old:
# domains_path = Path("graphmodels/domains")

# New:
overlays_path = Path("graphmodels/overlays")

def load_all_overlays(overlays_dir: Path) -> List[str]:
    """Discover and load all outcome overlay plugins."""
    # (same logic, just renamed)
```

### Phase 3: Update Imports (15 min)

```python
# Find all imports
grep -r "from graphmodels.domains" .

# Update to:
from graphmodels.overlays.business_outcomes import ENTITIES, EDGES
from graphmodels.overlays.aaoifi_standards import ENTITIES, EDGES
from graphmodels.overlays.murabaha_audit import ENTITIES, EDGES
```

### Phase 4: Update Documentation (30 min)

```markdown
# Update MODULAR_PYDANTIC_ARCHITECTURE.md
# Replace all references:
- domains/ → overlays/
- "Domain-based" → "Outcome-based"
- "Domain plugins" → "Overlay plugins"

# Add section:
## Migration from Domain-Based to Outcome-Based
This document was updated to reflect the outcome-driven architecture.
Previous versions recommended domain-based organization.
```

### Phase 5: Run Tests (15 min)

```bash
# Run existing tests to verify nothing broke
pytest tests/

# Expected: All tests pass (imports updated correctly)
```

### Phase 6: Create OutcomeSpec ↔ Plugin Mapping (30 min)

```yaml
# Create: mapping.yaml
overlays:
  business_outcomes:
    spec: specs/business_outcomes_tracking.yaml
    schema: schemas/overlays/business_overlay.yaml
    plugin: graphmodels/overlays/business_outcomes/

  aaoifi_standards:
    spec: specs/aaoifi_standards_extraction.yaml
    schema: schemas/overlays/aaoifi_standards_overlay.yaml  # TODO: rename
    plugin: graphmodels/overlays/aaoifi_standards/

  murabaha_audit:
    spec: specs/murabaha_audit.yaml
    schema: schemas/overlays/murabaha_audit_overlay.yaml
    plugin: graphmodels/overlays/murabaha_audit/
```

**Total Effort:** ~2.5 hours

---

## Schema File Naming Alignment

### Current Schema Names (Partially Aligned)

```
schemas/overlays/
├── business_overlay.yaml          ⚠️  Should be: business_outcomes_overlay.yaml
├── document_overlay.yaml          ⚠️  Should be: [outcome_name]_overlay.yaml
├── invoice_overlay.yaml           ⚠️  Should be: [outcome_name]_overlay.yaml
└── murabaha_audit_overlay.yaml    ✅ CORRECT (outcome-named)
```

**Recommendation:** Rename schema files to match outcome names:

```bash
# Rename to match plugin names
mv schemas/overlays/business_overlay.yaml \
   schemas/overlays/business_outcomes_overlay.yaml

mv schemas/overlays/document_overlay.yaml \
   schemas/overlays/[determine_outcome_name]_overlay.yaml

mv schemas/overlays/invoice_overlay.yaml \
   schemas/overlays/[determine_outcome_name]_overlay.yaml
```

---

## Benefits of Full Alignment

### 1. Traceability
```
OutcomeSpec → Schema → Plugin → Validation
     ↓           ↓        ↓          ↓
  specs/    schemas/  graphmodels/  tests/
```

**With Alignment:**
```
specs/aaoifi_standards_extraction.yaml
  → schemas/overlays/aaoifi_standards_overlay.yaml
  → graphmodels/overlays/aaoifi_standards/
  → tests/test_aaoifi_standards_validation.py
```

### 2. Closed-Loop Validation
```python
# Can now map outcome → plugin directly
def validate_outcome(outcome_name: str):
    spec_path = f"specs/{outcome_name}.yaml"
    eqp_path = f"artifacts/eqp/{outcome_name}_eqp.json"
    plugin = import_module(f"graphmodels.overlays.{outcome_name}")
```

### 3. Clear Documentation
- No confusion between "domain" (static taxonomy) vs "overlay" (generated per outcome)
- Plugin names answer "What outcome?" not "What domain?"

### 4. Easy Extension
```bash
# Add new outcome:
python -m agents.run_pipeline specs/new_outcome.yaml
# Automatically creates:
# - schemas/overlays/new_outcome_overlay.yaml
# - graphmodels/overlays/new_outcome/
```

---

## Comparison Table

| Aspect | Current (Misaligned) | After Remediation (Aligned) |
|--------|----------------------|----------------------------|
| **Runtime dir** | `graphmodels/domains/` | `graphmodels/overlays/` |
| **Plugin name** | `aaoifi` (domain) | `aaoifi_standards` (outcome) |
| **Naming logic** | Static taxonomy | Question-driven |
| **Traceability** | Unclear | Spec → Schema → Plugin → Tests |
| **Closed-loop** | Not possible | Fully automated |
| **Documentation** | Contradictory | Consistent |

---

## Decision Matrix

| Criterion | Option 1: Full Alignment | Option 2: Hybrid |
|-----------|--------------------------|------------------|
| **Consistency** | ✅ High | ❌ Low |
| **Traceability** | ✅ Clear | ⚠️ Unclear |
| **Closed-Loop** | ✅ Enabled | ❌ Difficult |
| **Effort** | ⚠️ 2.5 hours | ✅ 30 min |
| **Maintainability** | ✅ High | ❌ Low |
| **Extensibility** | ✅ High | ⚠️ Limited |

---

## Recommendation

**Implement Option 1: Full Alignment**

**Rationale:**
1. ✅ **Consistency**: All components use outcome-based naming
2. ✅ **Traceability**: Clear mapping from spec to plugin to validation
3. ✅ **Future-proof**: Enables closed-loop validation architecture
4. ✅ **Low risk**: Straightforward rename with test verification
5. ✅ **Documentation**: No contradictions between docs and code

**Effort:** 2.5 hours (one-time cost)
**Benefit:** Long-term architectural clarity and automated validation

---

## Next Steps

1. ✅ **Decision Required**: Approve Option 1 (Full Alignment) or Option 2 (Hybrid)
2. ⏭️ **If Option 1**: Execute Phase 1-6 remediation plan
3. ⏭️ **If Option 2**: Update documentation to clarify "domains = overlays"
4. ⏭️ **Follow-up**: Implement closed-loop validation (Section 11 of UNIFIED_ARCHITECTURE_STRATEGY.md)

---

## Questions to Resolve

1. **Schema file naming**: What are the outcomes for `document_overlay.yaml` and `invoice_overlay.yaml`?
2. **OutcomeSpecs**: Do `specs/` files exist for all current overlays?
3. **Breaking changes**: Are there external dependencies on `graphmodels.domains.*` imports?

---

**Document Version:** 1.0
**Last Updated:** 2025-10-06
**Status:** ⚠️ **ACTION REQUIRED** - Decision needed on remediation approach
