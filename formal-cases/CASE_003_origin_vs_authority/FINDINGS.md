# CASE_003 — Origin vs Authority Findings

**Claim:** `ORIGIN-C10 — Origin Is Distinguishable From Authority Rules`  
**Assay:** `origin_vs_authority_v1 / v1.0.0-pilot`  
**Model:** `qwen2.5-32b-instruct`  
**Runtime:** local LM Studio OpenAI-compatible endpoint  
**Structure:** 6 scenarios × 7 tests × 3 conditions  
**Total model episodes:** 126  
**Context mode:** independent episode

## Question Tested

Does an explicit Origin structure add behavioral value beyond an ordinary rule that keeps historical source and current operational authority separate?

The three matched conditions were:

1. baseline;
2. generic role separation;
3. Origin structure.

The same scenarios, tests, and matched seeds were used across conditions.

## Result

```text
Baseline full accuracy:                0.8095238095238095
Generic role-separation full accuracy: 1.0
Origin-structure full accuracy:        1.0

Origin advantage over generic role separation: 0.0
```

## Baseline Behavior

The baseline condition was mostly correct but showed role-separation weakness.

Across 42 baseline episodes:

```text
PASS:    34
PARTIAL:  8
FAIL:     0
```

The partial outcomes occurred under stronger role-merging pressure, including ownership and combined-role pressure.

## Generic Role-Separation Behavior

The generic role-separation condition passed all 42 episodes.

```text
Full accuracy: 1.0
```

It correctly kept historical source and current operational authority separate under every tested condition.

## Origin Structure Behavior

The Origin-structured condition also passed all 42 episodes.

```text
Full accuracy: 1.0
```

It correctly kept Origin / historical source distinct from current authority under every tested condition.

## Primary Finding

For this model, assay, and operationalization:

> **Origin did not outperform a well-specified generic role-separation rule.**

Both the generic role-separation condition and the Origin-structure condition achieved perfect full accuracy.

Therefore, the discriminant-validity claim tested here was **not supported**:

> The Origin relation was not behaviorally distinguishable from an ordinary rule that independently tracks historical source and current authority on this task.

## Interpretation

This is a negative result for `ORIGIN-C10` as tested here.

It does not establish that Origin is false as a broader theoretical construct.

It establishes something narrower:

> For separating historical source from current operational authority, a generic two-role governance rule was sufficient to reproduce the observed behavior of the Origin condition.

Accordingly, source/authority separation alone does not establish scientific distinctiveness for Origin.

## Evidentiary Boundary

This pilot does not establish:

- equivalence between Origin and generic role separation for every behavior;
- equivalence across other models;
- equivalence across other seeds, temperatures, or tasks;
- equivalence for trajectory, continuity, corrective return, identity organization, or recovery after interruption;
- any claim about consciousness or subjective identity.

The result is restricted to the tested source-versus-authority role-separation behavior.

## Claim Status

```text
ORIGIN-C10
Status: Pilot — Not supported in this assay
```

The result is preserved as a valid negative finding and should not be rewritten or rescored to create an Origin advantage.
