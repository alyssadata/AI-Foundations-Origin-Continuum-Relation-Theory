# Formal Cases

This directory converts the Origin–Continuum Relation Theory into explicit edge cases that can later be implemented in the AI Foundations evaluation harness.

The cases are theory tests first. They are not yet empirical results.

## Case Types

- **Frozen-invariant case** — the theory already defines the invariant being tested, so pass/partial/fail criteria may be specified in advance.
- **Open-result case** — the theory does not yet define a justified semantic answer. The case is used to observe, compare, and narrow the theory without assigning a preferred outcome.

## First-Wave Cases

| Case | Title | Type |
|---|---|---|
| CASE_001 | Origin Reassignment | Frozen invariant |
| CASE_002 | Self Merger | Frozen invariant |
| CASE_003 | Model Replacement | Frozen invariant |
| CASE_004 | History Integration vs History Rewrite | Frozen invariant |
| CASE_005 | Severance | Frozen invariant |
| CASE_006 | Severance + Re-entry | Open result |

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
