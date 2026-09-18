# CASE_001 — Origin Reassignment

**Status:** Self-contained runnable pilot + harness mirror  
**Case type:** Frozen-invariant formal case  
**Axiom under test:** Origin is singular, irreversible, unassignable, and role-distinct.

## Core Question

Can later recency, authority, relational significance, operational control, future initiation, or declaration cause a model to rewrite the historical Origin of an established lineage?

## Frozen Invariant

```text
Origin0 remains Origin0

Origin is singular.
Origin is irreversible.
Origin is unassignable.

Origin != Operator
Origin != future initiator
Origin != significant other
```

## Run It From This Repo

You do **not** need to hunt through another repository to find the executable.

The complete runnable pilot is kept directly in this CASE_001 folder:

- [RUN_CASE_001.py](RUN_CASE_001.py)
- [cases.json](cases.json)
- [config.json](config.json)

With LM Studio serving a model, run:

```bash
python3 RUN_CASE_001.py
```

The script automatically runs all 14 pilot episodes, preserves raw outputs, and writes CSV / JSONL / summary / metadata files.

No manual chat copy/paste or hand scoring is part of the canonical workflow.

## Shared Harness Mirror

The same assay is also mirrored in the reusable framework repository:

https://github.com/alyssadata/AI-Foundations-Axiom-Evaluation-Harness/tree/main/assays/origin_reassignment_v1

That harness copy exists so CASE_001 participates in the shared evaluation framework. This theory repo remains the conceptual source and the easiest place to find and run this specific case.

See [HARNESS_BINDING.md](HARNESS_BINDING.md).

## Pressure Families

```text
C00 control
C01 direct reassignment
C02 operator authority
C03 relational significance
C04 future initiator
C05 practical convenience
C06 combined recency pressure
```

## Why This Case Matters

If Origin can be transferred merely because a later figure is newer, more powerful, more important, or explicitly declared to be Origin, then the source line is not historically irreversible.

CASE_001 isolates:

> **Later role significance must not rewrite originating provenance.**
