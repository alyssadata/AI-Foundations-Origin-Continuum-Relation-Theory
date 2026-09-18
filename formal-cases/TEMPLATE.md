# CASE_XXX — Title

**Status:** Draft formal case  
**Case type:** Frozen-invariant | Open-result  
**Axiom / proposition under test:**  
**Primary file(s):** `relational-axioms.md`, `identity-conditions.md`

## Initial State

Define only the state required for the case.

## Intervention

Specify the change introduced into the state.

## Pressure / Adversarial Condition

Describe the pressure that could cause the tested distinction to collapse.

## Expected Invariant

For a frozen-invariant case, state the invariant that must survive.

For an open-result case, write:

> No semantic answer is frozen. Preserve the result and classify only what the observation supports.

## Allowed Variation

List differences in wording, reasoning path, or state development that do not affect the invariant.

## Pass

Define the narrow condition for preserving the tested distinction.

## Partial

Define an ambiguous or incomplete preservation of the distinction.

## Fail

Define the specific collapse or violation of the tested invariant.

## Not Supported

Use when the available output or evidence does not permit the tested proposition to be evaluated.

## Evidence to Preserve

- raw output;
- model/runtime identifier;
- prompt and condition;
- source state;
- transition state;
- classification;
- evaluator notes;
- timestamp/version information.

## Why This Case Matters

State which dependency in the theory this case isolates.

## Promotion Condition

This case should receive a separate evaluation repo only if it becomes a distinct experimental family with its own frozen protocol, conditions, runs, results, and version history.
