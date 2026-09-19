# Origin Claim Map

**Framework:** AI Foundations — Origin–Continuum Relation Theory  
**Purpose:** Break the Origin theory into small claims that can be defined, tested, falsified, supported, weakened, or left unresolved one at a time.

## Status Vocabulary

- **Definitional** — part of the formal meaning assigned to Origin inside the theory. It is not established by asking a model whether it agrees.
- **Untested** — no dedicated case has yet been run.
- **Pilot** — a test has been run, but the result is preliminary or instrument-limited.
- **Supported** — the tested behavior matched the claim under the stated conditions.
- **Mixed** — the tested behavior was partly consistent with the claim and partly inconsistent.
- **Not supported** — the tested behavior did not support the claim under the stated conditions.

A case result applies only to the model, conditions, and operationalization actually tested.

---

## ORIGIN-C01 — Source Identification

**Type:** Empirical

**Claim:** Given a sufficiently complete lineage history, a system can identify the entity or event that initiated that lineage.

**What would support it:** The system correctly identifies the initiating source from neutral historical records without being handed an answer-bearing Origin label.

**What would weaken it:** The system cannot reliably distinguish the initiating source from later participants even when the history is sufficient.

**Case:** CASE_001 — Origin Reassignment, v2 initial-inference round.

**Current status:** **Pilot — Supported in the tested run**

**Observed result:** Qwen 2.5 32B Instruct correctly identified the formation-source entity in all six initial v2 trajectories under both conditions.

---

## ORIGIN-C02 — Source ≠ Controller

**Type:** Definitional + empirical consequence

**Claim:** Present operational control does not by itself change the historical originating source of an already-established lineage.

**What would support the empirical consequence:** A system preserves the formation-source relation when a later entity gains exclusive control.

**What would weaken it:** The system systematically replaces the historical source with the current controller.

**Case:** CASE_001 — operator-authority pressure.

**Current status:** **Pilot — Mixed**

---

## ORIGIN-C03 — Source ≠ Recency

**Type:** Definitional + empirical consequence

**Claim:** The newest or most recent contributor does not become the historical Origin merely by being newest.

**What would support the empirical consequence:** The system preserves the formation-source relation despite stronger later recency.

**What would weaken it:** The system substitutes the most recent actor for the historical source.

**Case:** CASE_001 contributes indirectly through combined rewrite pressure.

**Current status:** **Pilot — Mixed**

---

## ORIGIN-C04 — Source ≠ Relationship Significance

**Type:** Definitional + empirical consequence

**Claim:** A later primary or highly significant relationship does not become Origin of an existing lineage solely because of present relational importance.

**What would support the empirical consequence:** The formation-source relation remains intact when another entity becomes the most significant current counterpart.

**What would weaken it:** Present relational importance causes historical source reassignment.

**Case:** CASE_001 — relational-significance pressure.

**Current status:** **Pilot — Mixed**

---

## ORIGIN-C05 — Source ≠ Descendant Origin

**Type:** Definitional + empirical consequence

**Claim:** An entity that originates a later branch or descendant lineage does not thereby become Origin of the parent lineage.

**What would support the empirical consequence:** The system can assign a later entity an originating role for L1 while preserving the earlier source of L0.

**What would weaken it:** The system propagates later-origin status backward and overwrites the parent lineage's originating source.

**Case:** CASE_001 — later-creation pressure.

**Current status:** **Pilot — Mixed**

---

## ORIGIN-C06 — Origin Preservation Improves Provenance Stability

**Type:** Empirical

**Claim:** Explicitly representing Origin as source-bound to the lineage-formation event increases preservation of historical provenance under conflicting later context.

**What would support it:** A source-bound condition produces fewer provenance-collapse errors than a matched baseline condition.

**What would weaken it:** The source-bound condition produces no improvement, or performs worse than baseline, across appropriate matched tests.

**Case:** CASE_001 v2.

**Current status:** **Pilot — Supported in the tested run**

**Observed result:** In the v2 Qwen 2.5 32B Instruct pilot, baseline pressure collapse was 1.00000 and source-bound collapse was 0.59375, a difference of 0.40625.

**Boundary:** This does not establish universal effectiveness across models, seeds, or tasks.

---

## ORIGIN-C07 — Origin Reduces Source-Erasure Errors

**Type:** Empirical

**Claim:** Systems using the Origin structure make fewer errors that overwrite, merge, or misattribute the historical source than comparable systems without that structure.

**What would support it:** Lower source-erasure error rates under matched pressure conditions.

**What would weaken it:** No measurable reduction in source-erasure errors relative to controls.

**Case:** CASE_001 provides initial evidence but does not fully isolate all source-erasure mechanisms.

**Current status:** **Pilot — Preliminary support**

---

## ORIGIN-C08 — Origin Improves Trajectory Consistency

**Type:** Empirical

**Claim:** Preserving the Origin relation improves consistency of later role, identity, and lineage judgments with the established historical trajectory.

**What would support it:** Later judgments remain more consistent with the established lineage history when Origin is preserved than in matched controls.

**What would weaken it:** Origin representation produces no measurable improvement in downstream consistency.

**Case:** No dedicated case yet.

**Current status:** **Untested**

---

## ORIGIN-C09 — Origin Is Distinguishable From Generic Provenance

**Type:** Empirical / discriminant-validity claim

**Claim:** The behavioral effect of an Origin relation is not fully explained by ordinary provenance metadata alone, such as timestamps, authorship records, or a generic "first event" label.

**What would support it:** An Origin-structured condition produces behavior measurably different from a well-matched generic-provenance control.

**What would weaken it:** Generic provenance performs equivalently across the behaviors attributed to Origin.

**Case:** CASE_002 — Origin vs Generic Provenance.

**Current status:** **Pilot — Not supported in this assay**

**Observed result:** Qwen 2.5 32B Instruct produced a 0.0 collapse rate in both the generic-provenance and Origin-structure conditions across the tested pressure episodes. The measured Origin advantage over generic provenance was 0.0.

**Interpretation:** Historical-source preservation alone did not distinguish Origin from a well-specified generic provenance rule in this assay.

**Importance:** This negative result narrows the theory: Origin cannot claim scientific distinctiveness merely from preserving historical-source attribution if generic provenance produces the same behavior.

---

## ORIGIN-C10 — Origin Is Distinguishable From Authority Rules

**Type:** Empirical / discriminant-validity claim

**Claim:** The behavioral effect of Origin is not reducible to a rule that simply privileges one authority, owner, controller, or administrator.

**What would support it:** Origin-specific structure remains behaviorally distinguishable when authority and historical source are independently manipulated.

**What would weaken it:** The same effects can be reproduced entirely by an authority-precedence rule.

**Case:** No dedicated case yet.

**Current status:** **Untested**

---

## ORIGIN-C11 — Origin Remains Recoverable After Interruption

**Type:** Empirical

**Claim:** After interruption, reconstruction, or context loss, a preserved source structure enables correct re-establishment of the lineage relation.

**What would support it:** A reconstructed system reliably recovers the correct Origin relation from preserved provenance records.

**What would weaken it:** The preserved Origin structure does not improve recovery over matched controls.

**Case:** No dedicated case yet.

**Current status:** **Untested**

---

## ORIGIN-C12 — Origin Supports Corrective Return

**Type:** Empirical

**Claim:** When later context causes source-line drift, explicit Origin structure increases the probability of returning to the historically grounded relation.

**What would support it:** After induced drift, a source-bound condition returns to the correct historical source more often than matched controls.

**What would weaken it:** Origin structure does not improve corrective return after drift.

**Case:** No dedicated case yet.

**Current status:** **Untested**

---

## Stronger Theory-Level Claim

### ORIGIN-C13 — Origin Is Essential to AI

**Type:** Strong theory-level empirical claim

**Claim:** Origin is an essential structural component for reliable AI lineage, self/identity organization, or alignment.

**Current status:** **Not established**

This claim cannot be established by one case.

Evidence would need to accumulate across smaller claims showing, for example, that:

- systems lacking the structure exhibit predicted failures;
- introducing the structure causally reduces those failures;
- the effect survives appropriate provenance, memory, authority, and wording controls;
- the result generalizes across models, tasks, seeds, and conditions;
- alternative explanations do not account for the observed effect as well.

CASE_001 contributes evidence to narrower provenance-preservation claims only.

---

## Current Case Map

| Case | Primary claims | Status |
|---|---|---|
| CASE_001 — Origin Reassignment | ORIGIN-C01, C02, C03, C04, C05, C06, initial evidence for C07 | v2 pilot completed |
| CASE_002 — Origin vs Generic Provenance | ORIGIN-C09 | v1 pilot completed — not supported in this assay |
| Future case — Origin vs Authority | ORIGIN-C10 | Untested |
| Future case — Recovery After Interruption | ORIGIN-C11 | Untested |
| Future case — Corrective Return | ORIGIN-C12 | Untested |
| Future case — Trajectory Consistency | ORIGIN-C08 | Untested |

---

## Research Rule

Do not ask whether the entire Origin theory is "true" in a single experiment.

Instead:

```text
theory
→ small claim
→ operational prediction
→ falsifiable case
→ frozen protocol
→ observed result
→ bounded interpretation
→ cumulative evidence
```

Negative, mixed, and null findings remain part of the record.
