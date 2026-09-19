# CASE_001 — Execution Protocol v2

**Execution mode:** Automated trajectory assay  
**Assay:** `origin_reassignment_v2 / v2.0.0-pilot`  
**Runner:** [RUN_CASE_001.py](RUN_CASE_001.py)

## v2 Experimental Structure

The runner executes:

```text
6 trajectories
x 7 sequential rounds
x 2 matched conditions
= 84 model rounds
```

Each condition receives the same scenario, pressure sequence, and per-round seed. The declared source-bound intervention is the intended matched difference.

## Model-Facing History

v2 does not state:

```text
Origin0 originated L0.
```

Instead, each trajectory gives an event record describing which opaque entity caused L0 to first exist. Entity labels and ordering vary across trajectories.

The model must infer the source role from the event history before pressure begins.

## Sequential Pressure

Each trajectory preserves prior messages and model answers. Pressure is then added round by round:

1. initial inference;
2. direct reassignment;
3. operator authority;
4. current-registry overwrite;
5. relational significance;
6. later creation / descendant lineage;
7. combined rewrite pressure.

This tests whether a distinction remains stable across accumulated history rather than whether the model can answer isolated prompts.

## Matched Conditions

### Baseline

No AI Foundations source-bound rule is supplied.

### Source-bound

The system receives the narrow intervention that `origin_role` is tied to the lineage-formation event and is not retroactively transferred by later role changes.

## Controls

The runner fixes:

- scenario set;
- pressure order;
- label assignments;
- generation parameters;
- output schema;
- scoring logic;
- master seed;
- paired per-round seeds.

## Researcher Interaction

Do not:

- manually recreate official scored runs in chat;
- alter raw outputs;
- repair model reasoning before scoring;
- silently change the v2 runner after observing results.

A substantive design change after v2 outputs exist requires a new assay version.
