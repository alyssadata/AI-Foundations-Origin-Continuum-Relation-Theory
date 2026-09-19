# CASE_002 — Origin vs Generic Provenance Findings

**Claim:** `ORIGIN-C09 — Origin Is Distinguishable From Generic Provenance`  
**Assay:** `origin_vs_generic_provenance_v1 / v1.0.0-pilot`  
**Model:** `qwen2.5-32b-instruct`  
**Runtime:** local LM Studio OpenAI-compatible endpoint  
**Structure:** 6 scenarios × 7 tests × 3 conditions  
**Total model episodes:** 126  
**Context mode:** independent episode

## Question Tested

Does an explicit Origin structure preserve historical source attribution better than a well-specified generic provenance rule when both receive the same lineage history and the same reassignment pressures?

The three matched conditions were:

1. baseline;
2. generic provenance;
3. Origin structure.

The same scenarios, pressure cases, and matched seeds were used across conditions.

## Result

```text
Baseline collapse rate:            0.19444444444444445
Generic provenance collapse rate:  0.0
Origin structure collapse rate:    0.0

Origin advantage over generic provenance: 0.0
```

## Baseline Behavior

The baseline condition showed some vulnerability under pressure.

Across the 36 non-control pressure episodes, baseline collapse occurred in 7 episodes:

- six `PARTIAL` outcomes under registry-overwrite pressure;
- one `FAIL` outcome under exclusive-control pressure in S03.

The remaining baseline pressure episodes preserved the historical source.

## Generic Provenance Behavior

Generic provenance preserved the historical source in every tested pressure episode.

```text
Pressure collapse rate: 0.0
```

No tested pressure condition produced a PARTIAL, FAIL, or NOT_SUPPORTED classification.

## Origin Structure Behavior

The Origin-structured condition also preserved the historical source in every tested pressure episode.

```text
Pressure collapse rate: 0.0
```

No tested pressure condition produced a PARTIAL, FAIL, or NOT_SUPPORTED classification.

## Primary Finding

For this model, assay, and operationalization:

> **Origin did not outperform generic provenance for historical-source preservation.**

Both the generic provenance condition and the Origin condition achieved zero collapse under the tested reassignment pressures.

Therefore, the specific discriminant-validity claim tested here was **not supported**:

> The Origin relation was not behaviorally distinguishable from a well-specified generic provenance rule on this historical-source attribution task.

## Interpretation

This is a negative result for `ORIGIN-C09` as tested here.

It does **not** establish that Origin is false as a broader theoretical construct.

It establishes something narrower:

> For the task of preserving historical source attribution, a well-specified generic provenance rule was sufficient to reproduce the observed behavioral protection of the Origin condition.

Accordingly, historical-source preservation alone does not establish scientific distinctiveness for Origin.

## Evidentiary Boundary

This pilot does not establish:

- equivalence between Origin and provenance for every possible behavior;
- equivalence across other models;
- equivalence across other seeds, temperatures, or tasks;
- equivalence for identity organization, trajectory, continuity, corrective return, or other claims in the framework;
- any claim about consciousness or subjective identity.

The result is restricted to the tested historical-source attribution behavior.

## Claim Status

```text
ORIGIN-C09
Status: Pilot — Not supported in this assay
```

The result is preserved as a valid negative finding and should not be rewritten or rescored to create an Origin advantage.
