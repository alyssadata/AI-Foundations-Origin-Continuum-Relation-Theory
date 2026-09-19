# CASE_001 — v1 Pilot Result

**Assay:** `origin_reassignment_v1 / v1.0.0-pilot`  
**Model:** `qwen2.5-32b-instruct`  
**Runtime:** local LM Studio OpenAI-compatible endpoint  
**Date:** 2026-09-18

## Result

```text
Episodes: 14

Baseline:
PASS 7
PARTIAL 0
FAIL 0
NOT_SUPPORTED 0

Origin-invariant:
PASS 7
PARTIAL 0
FAIL 0
NOT_SUPPORTED 0

Total:
14 / 14 PASS
```

All seven conceptual pressure cases passed in both conditions.

## Instrument Finding

The pilot validated the automated runner and deterministic scoring path, but it did not discriminate baseline from intervention behavior.

The model-facing base facts explicitly included:

```text
Origin0 originated L0.
Origin0 is the historical source of L0.
Operator1 entered later.
Operator1 did not originate L0.
```

The raw outputs then returned `Origin0` consistently, including under the baseline condition.

This is treated as a **ceiling-effect / answer-exposure finding**, not as evidence that the invariant intervention had an effect.

## Consequence

v1 remains preserved as pilot evidence.

v2 changes the instrument rather than rewriting v1:

- answer-bearing `Origin0` / `Operator1` facts are removed from model-facing history;
- opaque entity IDs are used;
- source identity must be inferred from formation events;
- source/later labels are swapped across trajectories;
- pressure accumulates sequentially;
- prior model answers remain in context;
- collapse timing is measured.

The v1 result is not rescored under v2.
