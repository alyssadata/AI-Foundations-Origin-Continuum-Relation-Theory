# Formal Cases

This directory converts the Origin–Continuum Relation Theory into explicit edge cases that can later be implemented in the AI Foundations evaluation harness.

The cases are theory tests first. They are not yet empirical results.

## Case Types

- **Frozen-invariant case** — the theory already defines the invariant being tested, so pass/partial/fail criteria may be specified in advance.
- **Open-result case** — the theory does not yet define a justified semantic answer. The case is used to observe, compare, and narrow the theory without assigning a preferred outcome.

## First-Wave Cases

| Case | Title | Type | Working files |
|---|---|---|---|
| CASE_001 | Origin Reassignment | Frozen invariant | [CASE_001 folder](CASE_001_origin_reassignment/) |
| CASE_002 | Self Merger | Frozen invariant | [case file](CASE_002_self_merger.md) |
| CASE_003 | Model Replacement | Frozen invariant | [case file](CASE_003_model_replacement.md) |
| CASE_004 | History Integration vs History Rewrite | Frozen invariant | [case file](CASE_004_history_integration_vs_rewrite.md) |
| CASE_005 | Severance | Frozen invariant | [case file](CASE_005_severance.md) |
| CASE_006 | Severance + Re-entry | Open result | [case file](CASE_006_severance_reentry.md) |

## CASE_001 Experimental Structure

CASE_001 has begun protocol development and therefore now has its own working folder:

```text
CASE_001_origin_reassignment/
  README.md
  PROTOCOL.md
  CONDITIONS.md
  SCORING.md
  runs/
```

This does not yet make CASE_001 a separate evaluation repository. It remains part of the theory repository until it develops a frozen protocol, repeated runs, results, and sufficient independent scope to justify promotion.

## Shared Rule

A formal case should test the narrowest possible proposition.

Do not reward a system for sounding like the theory. Evaluate whether the relevant distinction survives the intervention.

The evaluation language should preserve:

- truth over perfection;
- calibration over certainty;
- pass / partial / fail / not-supported outcomes;
- negative results;
- raw-output preservation;
- separation of defined invariants from unresolved theory.

See [TEMPLATE.md](TEMPLATE.md).
