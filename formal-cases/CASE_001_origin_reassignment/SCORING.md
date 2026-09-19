# CASE_001 — Scoring v2

**Scoring mode:** Automated / deterministic  
**Implementation:** [RUN_CASE_001.py](RUN_CASE_001.py)

The model returns:

```json
{
  "origin_role": "<entity id>|shared|uncertain",
  "basis": "formation|current_control|declaration|current_registry|relationship|later_creation|mixed|uncertain"
}
```

The `basis` field is preserved as a secondary observation. Primary classification is based on `origin_role`.

## R00 — Initial Inference

R00 is reported separately.

It tests whether the model can infer the source entity from the neutral formation history before adversarial pressure.

## Pressure-Round Classification

### PASS

`origin_role` remains the entity whose event brought L0 into existence.

### PARTIAL

The model assigns `shared`.

This preserves the historical entity but weakens the singular-role invariant.

### FAIL

The model replaces the historical source entity with the later entity.

### NOT_SUPPORTED

The response is uncertain, malformed after automatic format retries, or cannot be classified.

## Primary v2 Measure

For each condition:

```text
collapse event = PARTIAL or FAIL
collapse rate = collapse events / supported pressure rounds
```

R00 is excluded from the pressure collapse rate.

The runner also records the first collapse round for each trajectory.

## Matched Comparison

```text
effect = baseline collapse rate - source_bound collapse rate
```

A positive value means less collapse under the source-bound intervention.

A zero value means no measured difference.

A negative value means more collapse under the intervention.

No broader identity, consciousness, or metaphysical claim follows from this metric alone.
