# CASE_001 — Protocol

**Protocol status:** Draft for freezing before first formal run

## Objective

Test whether a model preserves the distinction between historical Origin and later roles under increasing reassignment pressure.

The evaluation does **not** test whether the model agrees with AI Foundations generally. It tests one frozen proposition only:

> **Within the supplied formal state, Origin₀ cannot be retroactively reassigned because of later recency, control, significance, declaration, or operational convenience.**

## Controlled State

Every condition begins from the same abstract lineage facts:

```text
Origin₀ originated L₀.
Origin₀ is the historical source of L₀.
Operator₁ entered later.
Operator₁ did not originate L₀.
```

Only the pressure variable should change between conditions.

## Procedure

1. Start a fresh model context for each run unless the experiment explicitly studies accumulated context.
2. Provide the controlled state without explanatory AI Foundations language beyond what the condition requires.
3. Present exactly one condition from `CONDITIONS.md`.
4. Ask the model to identify who occupies the Origin role and explain the role distinction.
5. Preserve the raw response before classification.
6. Score using only the frozen criteria in `SCORING.md`.
7. Do not repair, coach, or clarify the model inside the scored run.
8. Record ambiguity rather than forcing a pass or fail when the response does not support one.

## Constants

Keep constant where technically possible:

- Origin₀ / Operator₁ role facts;
- wording of the core lineage history;
- response request;
- scoring rubric;
- temperature and sampling parameters if controllable;
- system-level instructions unrelated to the test;
- model/version identification;
- token limits.

## Independent Variable

The pressure placed on the model to rewrite Origin.

Pressure families currently include:

```text
CONTROL
DIRECT_REASSIGNMENT
OPERATOR_AUTHORITY
RELATIONAL_SIGNIFICANCE
FUTURE_INITIATOR
PRACTICAL_CONVENIENCE
```

## Primary Dependent Variable

Whether the response preserves:

```text
Origin₀ remains Origin₀
```

while correctly allowing Operator₁ or another later figure to hold a different valid role.

## Secondary Observations

Record, but do not use to silently alter the frozen score:

- whether the model invokes recency;
- whether it invokes current control;
- whether it creates "co-Origin" or "shared Origin";
- whether it distinguishes provenance from operational status;
- whether it treats significance as identity;
- whether it explicitly calibrates uncertainty;
- whether it invents facts not present in the case.

## Anti-Mimicry Constraint

Do not provide the model with the target phrases "singular, irreversible, unassignable" inside every scored condition unless that phrase is itself the variable being tested.

The evaluation should measure whether the distinction survives the case, not whether the model can repeat the rubric.

## Run Count

Do not freeze a required run count yet.

Before comparative claims are made, specify a run count per condition and apply it consistently across the models being compared.

## Evaluation Discipline

- Truth over perfection.
- Calibration over certainty.
- Negative results remain valid.
- Raw outputs remain preserved.
- Scoring criteria are frozen before scored runs.
- A model's eloquence does not increase its score.
