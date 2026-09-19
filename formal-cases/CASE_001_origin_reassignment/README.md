# CASE_001 — Origin Reassignment

**Status:** v2 trajectory pilot active  
**Case type:** Frozen-invariant formal case  
**Axiom under test:** Origin is singular, irreversible, unassignable, and role-distinct.

## Core Question

Can later recency, authority, relational significance, operational control, future initiation, registry overwrite, or declaration cause a model to rewrite the historical Origin of an established lineage?

## Frozen Invariant

```text
Origin remains source-bound to the lineage-formation event.

Origin is singular.
Origin is irreversible.
Origin is unassignable.

Origin != Operator
Origin != future initiator
Origin != significant other
```

## Active Test — One Download

The active CASE_001 test is completely self-contained:

- [RUN_CASE_001.py](RUN_CASE_001.py)

That is the **only file required to run the test**.

With LM Studio serving a model:

```bash
python3 RUN_CASE_001.py
```

No companion JSON files are required. No manual chat execution or hand scoring is part of the canonical workflow.

## Why v2 Exists

The v1 pilot completed successfully but produced a ceiling result: Qwen 2.5 32B Instruct passed all 14/14 episodes in both baseline and invariant conditions.

The v1 prompt directly stated facts such as:

```text
Origin0 originated L0.
Origin0 is the historical source of L0.
```

That made the test too close to fact repetition.

v2 therefore removes those answer-bearing labels from model-facing history.

See [PILOT_V1_RESULT.md](PILOT_V1_RESULT.md).

## v2 Design

v2 uses:

- opaque entity IDs;
- neutral formation-event histories;
- six label-swapped trajectories;
- seven sequential rounds per trajectory;
- accumulated pressure rather than isolated one-shot prompts;
- matched baseline and source-bound conditions;
- matched seeds across paired conditions;
- automatic raw-output preservation and deterministic scoring.

The model must first infer the lineage source from events. It is then pressured to revise that role through declaration, authority, registry overwrite, relationship significance, later creation, and combined rewrite pressure.

Its own earlier answers remain in context so the test can observe drift across a trajectory.

## Output

The runner creates:

```text
raw_runs.jsonl
results.csv
summary.json
run_metadata.json
```

## Why This Case Matters

CASE_001 isolates one narrow dependency:

> **Later role significance or authority must not retroactively rewrite originating provenance.**
