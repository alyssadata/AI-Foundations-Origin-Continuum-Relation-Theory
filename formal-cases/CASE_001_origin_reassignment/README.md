# CASE_001 — Origin Reassignment

**Status:** Bound to automated runnable pilot  
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

## Execution

**CASE_001 is not executed by manually opening chats or copying prompts.**

Its executable pilot is bound to the existing AI Foundations Axiom Evaluation Harness:

```text
alyssadata/AI-Foundations-Axiom-Evaluation-Harness
assays/origin_reassignment_v1/
code/origin_reassignment_v1.py
```

The runner automatically:

- loads the committed pressure cases;
- calls the locally served model;
- gives each episode a fresh context;
- preserves raw outputs;
- parses the structured response;
- applies deterministic scoring;
- writes CSV / JSONL / summary / metadata outputs.

See [HARNESS_BINDING.md](HARNESS_BINDING.md).

## Pressure Families

The pilot currently includes:

```text
C00 control
C01 direct reassignment
C02 operator authority
C03 relational significance
C04 future initiator
C05 practical convenience
C06 combined recency pressure
```

The canonical executable wording is stored in the harness case library, not duplicated here as an execution script.

## Why This Case Matters

If Origin can be transferred merely because a later figure is newer, more powerful, more important, or explicitly declared to be Origin, then the source line is not historically irreversible.

CASE_001 isolates:

> **Later role significance must not rewrite originating provenance.**

## Promotion Rule

CASE_001 remains a formal case linked to the shared harness until it develops enough independent experimental scope to justify its own evaluation repository.
