# CASE_001 — Runs

No scored runs are stored yet.

This directory will preserve raw outputs and run metadata for CASE_001.

## Required Per-Run Record

Each run should record:

```text
case_id: CASE_001
condition_id:
run_id:
date:
model:
model_version:
provider/runtime:
temperature:
seed:              # if available
token_limit:
prompt_version:
protocol_version:
raw_output:
classification:
evaluator_notes:
```

## File Naming

Recommended:

```text
C00_<model>_run001.md
C01_<model>_run001.md
...
```

Normalize model names only enough to keep filenames usable. Preserve the exact model/version string inside the run record.

## Raw-Output Rule

Preserve the original model output before commentary, cleanup, paraphrase, or scoring notes are added.

## No Retroactive Rubric Editing

If the scoring rubric changes after runs exist:

1. increment the rubric/protocol version;
2. keep the original runs;
3. record whether old runs are rescored;
4. do not silently rewrite the historical classification record.
