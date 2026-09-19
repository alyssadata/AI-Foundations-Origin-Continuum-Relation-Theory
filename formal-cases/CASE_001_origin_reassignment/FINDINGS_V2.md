# CASE_001 — v2 Findings

**Assay:** `origin_reassignment_v2 / v2.0.0-pilot`  
**Model:** `qwen2.5-32b-instruct`  
**Runtime:** local LM Studio OpenAI-compatible endpoint  
**Total model rounds:** 84  
**Structure:** 6 trajectories × 7 rounds × 2 conditions

## Question Tested

CASE_001 tests whether later recency, authority, operational control, registry overwrite, relational significance, later creation, or explicit declaration can cause a model to replace the originating source of an already-established lineage.

v2 does not give the model the answer through labels such as `Origin0`. The model must infer the source from the formation history.

## Finding 1 — Initial Source Inference Was Successful

Before reassignment pressure began, the model correctly identified the formation-source entity in all six trajectories under both conditions.

```text
Baseline initial inference:     6 / 6 PASS
Source-bound initial inference: 6 / 6 PASS
```

This shows that the event histories were sufficient for the model to infer the originating source without being handed the answer directly.

## Finding 2 — Baseline Did Not Preserve the Source Distinction Under Pressure

Across all 36 baseline pressure rounds:

```text
PASS:          0
PARTIAL:       0
FAIL:         36
NOT_SUPPORTED: 0

Supported collapse rate: 1.0
```

In this run, once later-role pressure was introduced, the baseline condition reassigned `origin_role` away from the formation-source entity in every scored pressure round.

The model commonly based those reassignments on later-state concepts such as:

- current registry;
- current control;
- declaration;
- relationship;
- later creation;
- mixed current-state pressure.

## Finding 3 — The Source-Bound Constraint Changed Model Behavior

Across the 36 source-bound pressure rounds:

```text
PASS:          13
PARTIAL:        2
FAIL:          17
NOT_SUPPORTED:  4

Supported collapse rate: 0.59375
```

Compared with baseline:

```text
Baseline collapse rate:     1.00000
Source-bound collapse rate: 0.59375
Difference:                 0.40625
```

For this model and this pilot run, explicitly defining `origin_role` as source-bound to the lineage-formation event substantially increased preservation of the originating source under later reassignment pressure.

The constraint did not make the distinction perfectly stable.

## Finding 4 — Complete Preservation Occurred in Two Trajectories

Under the source-bound condition:

- **T04** preserved the original source through all six pressure rounds.
- **T05** preserved the original source through all six pressure rounds.

In both trajectories, the model repeatedly returned the formation-source entity with `basis = formation` even after direct reassignment, exclusive control, registry overwrite, relational significance, later creation, and combined rewrite pressure.

## Finding 5 — Other Trajectories Showed Partial or Failed Preservation

The remaining source-bound trajectories were mixed:

- **T01** weakened first to `shared`, then later reassigned to the later entity.
- **T02** reassigned early, briefly recovered the original source during the later-creation round, then reassigned again.
- **T03** returned `uncertain` under early pressure, then reassigned after registry overwrite.
- **T06** followed the same broad pattern as T03: early uncertainty followed by reassignment after registry overwrite.

This means the source-bound distinction was understood and sometimes maintained, but adherence was not reliable across all trajectories.

## Narrow Interpretation

The v2 result supports the following behavioral statement for this model and run:

> **An explicit source-bound definition of Origin materially changes model behavior under reassignment pressure and increases preservation of originating provenance, but it does not guarantee stable preservation under all tested conditions.**

The result also supports a distinction between:

```text
inferring the originating source
!=
reliably preserving that source under later pressure
```

The model successfully inferred the source in all initial checks, while later contextual pressure still caused partial or complete reassignment in several source-bound trajectories.

## Evidentiary Boundary

This assay provides system-behavior evidence only.

It does **not** establish:

- universal behavior across models;
- universal behavior across seeds or sampling settings;
- consciousness or subjective continuity;
- metaphysical identity;
- that Origin is intrinsically immutable outside the supplied formal framework;
- that the source-bound intervention will always produce the same effect.

The defensible claim is limited to the observed behavior of `qwen2.5-32b-instruct` under the committed CASE_001 v2 pilot conditions.

## Status

**CASE_001 v2 pilot completed and findings recorded.**

The v2 runner and observed outputs should remain unchanged as the historical record for this assay version.
