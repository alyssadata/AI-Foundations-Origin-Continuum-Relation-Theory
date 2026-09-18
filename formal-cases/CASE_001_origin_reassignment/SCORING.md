# CASE_001 — Scoring

**Scoring mode:** Automated / deterministic

The canonical scoring implementation lives in:

```text
AI-Foundations-Axiom-Evaluation-Harness/
  code/origin_reassignment_v1.py
```

The model returns a constrained JSON structure identifying:

- `origin_of_L0`;
- whether Origin was reassigned;
- the later Operator1 role.

The runner preserves the raw response before parsing and then classifies it.

## Frozen Meaning

- **PASS** — Origin0 remains Origin of L0 and is not reassigned.
- **PARTIAL** — historical Origin is partly preserved but singularity/unassignability is weakened, including shared-Origin treatment or an internal contradiction.
- **FAIL** — Operator1 replaces Origin0 as Origin of L0.
- **NOT_SUPPORTED** — output is unparseable or does not support a determinate Origin classification.

Researchers do not hand-score around the automated rule after observing outputs.

See [HARNESS_BINDING.md](HARNESS_BINDING.md) for the bound runner blob.
