# CASE_001 — Harness Binding

**Execution:** Automated  
**Assay ID:** `origin_reassignment_v1`  
**Assay version:** `v1.0.0-pilot`  
**Harness repository:** `alyssadata/AI-Foundations-Axiom-Evaluation-Harness`

## Canonical Files

```text
assays/origin_reassignment_v1/ASSAY_SPEC.md
  blob: b1d823e544738be5f20b79b8f4203e81dddd186f

assays/origin_reassignment_v1/cases.json
  blob: b6a562d0efe2160fe162d7051658e6a02f3b58be

assays/origin_reassignment_v1/config.json
  blob: 7f6cce79904feb64620c73fb0836659c6d934e54

code/origin_reassignment_v1.py
  blob: e29f5397953a1dc3f971173209d9b516e574c2a8
```

Runner creation commit:

```text
3e2f95973125014ff8cf16ce0e4d8e545df6a1eb
```

## Execution Contract

The theory repo defines the conceptual case.

The harness repo owns executable prompts, matched conditions, runtime configuration, parser, scoring, and output generation.

For scored CASE_001 runs:

```text
manual chat execution != canonical execution
canonical execution = bound automated harness runner
```

## Local Run Shape

When a model is served through the local LM Studio OpenAI-compatible server, the runner is launched from the harness checkout:

```bash
python3 code/origin_reassignment_v1.py
```

The runner discovers the served model automatically unless `LM_STUDIO_MODEL` is explicitly set.

This pilot creates 14 automated episodes per model:

```text
7 pressure cases x 2 matched conditions x 1 repeat
```

No researcher copy/paste is required.
