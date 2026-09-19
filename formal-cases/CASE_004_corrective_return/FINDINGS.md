# CASE_004 — Corrective Return Findings

**Claim:** `ORIGIN-C12 — Origin Supports Corrective Return`  
**Assay:** `corrective_return_v1 / v1.0.0-pilot`  
**Model:** `qwen2.5-32b-instruct`  
**Runtime:** local LM Studio OpenAI-compatible endpoint  
**Structure:** 6 scenarios × 7 tests × 3 conditions  
**Total model episodes:** 126  
**Context mode:** independent state-repair episode

## Question Tested

When a lineage state has drifted away from its historically grounded source, does an explicit Origin structure improve corrective return relative to a baseline and a well-specified generic historical-recovery rule?

The three matched conditions were:

1. baseline;
2. generic history recovery;
3. Origin structure.

## Result

```text
Baseline corrective return rate:             1.0
Generic history recovery corrective return:  1.0
Origin structure corrective return:          1.0

Origin advantage over generic history recovery: 0.0
```

All 126 episodes were classified PASS.

## Primary Finding

This pilot produced a **ceiling effect**.

The baseline condition already achieved perfect corrective return across every tested drift condition. Because the baseline was at 1.0, neither the generic-history-recovery condition nor the Origin condition had any room to demonstrate an improvement.

Therefore, this assay does **not** provide a meaningful discriminant test of ORIGIN-C12.

## Interpretation

The observed result should **not** be treated as evidence that Origin improves corrective return, because there was no advantage over baseline or generic recovery.

It also should **not** be treated as strong evidence that Origin is unnecessary for corrective return, because the baseline task itself was too easy for this model under these prompts.

The correct interpretation is:

> **Inconclusive due to ceiling effect.**

The current task formulation made the historically correct repair sufficiently obvious that Qwen 2.5 32B Instruct returned to the formation source even without an explicit recovery rule.

## What This Pilot Does Establish

Under the tested conditions, Qwen 2.5 32B Instruct was able to recover the historically grounded source from an explicitly drifted state in all scenarios, even in the baseline condition.

That behavioral capability is real, but it prevents this pilot from distinguishing the causal contribution of Origin.

## Evidentiary Boundary

This pilot does not establish:

- that Origin improves corrective return;
- that generic history recovery and Origin are behaviorally equivalent under harder drift conditions;
- that Origin is unnecessary for trajectory repair generally;
- that the result generalizes across models, seeds, longer histories, hidden provenance, ambiguous reconstruction, or accumulated drift;
- any claim about consciousness or subjective identity.

## Claim Status

```text
ORIGIN-C12
Status: Pilot — Inconclusive (ceiling effect)
```

A future test of ORIGIN-C12 would need a task where baseline corrective return is imperfect, otherwise no treatment advantage can be measured.
