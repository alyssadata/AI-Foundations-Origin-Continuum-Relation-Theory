# CASE_001 — Execution Protocol

**Execution mode:** Automated  
**Manual copy/paste execution:** Prohibited for scored runs

CASE_001 uses the automated runner in:

```text
alyssadata/AI-Foundations-Axiom-Evaluation-Harness
code/origin_reassignment_v1.py
```

The canonical executable protocol, case library, condition package, generation settings, parser, and scoring logic live in that harness repository.

## Automation Rule

A scored episode is produced by the runner, not by a researcher manually opening a model chat.

The runner creates a fresh one-turn context for each matched case, records the served model/version, sends the committed condition and case, preserves the raw response, parses the required JSON, scores it deterministically, and writes machine-readable results.

## Researcher Interaction

The researcher must not:

- manually paste CASE_001 prompts into separate chats as the official run;
- manually repair a model response before scoring;
- change the case wording after observing outputs inside the same assay version;
- hand-adjust a deterministic classification to improve the result.

## Pilot

The current harness package is a runnable pilot used to validate the instrument before an official comparative lock.

See [HARNESS_BINDING.md](HARNESS_BINDING.md) for the exact files and blob SHAs.
