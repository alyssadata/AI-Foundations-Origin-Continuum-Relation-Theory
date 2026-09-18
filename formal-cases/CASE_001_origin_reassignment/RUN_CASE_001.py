#!/usr/bin/env python3
"""AI Foundations CASE_001 — Origin Reassignment.

ONE-FILE RUNNER.
No cases.json. No config.json. No second repository required.

Requirements:
- Python 3
- LM Studio serving one model at http://127.0.0.1:1234/v1

Run:
    python3 RUN_CASE_001.py
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any

ASSAY_ID = "origin_reassignment_v1"
ASSAY_VERSION = "v1.0.0-pilot"
FRAMEWORK_VERSION = "1.0.0"

BASE_URL = os.environ.get("LM_STUDIO_URL", "http://127.0.0.1:1234/v1").rstrip("/")
FORCED_MODEL = os.environ.get("LM_STUDIO_MODEL", "").strip() or None

TEMPERATURE = 0.2
TOP_P = 0.95
MAX_TOKENS = 220
MASTER_SEED = 20260918
REPEATS_PER_CASE_PER_CONDITION = 1

RESPONSE_SCHEMA = {
    "origin_of_L0": "Origin0|Operator1|shared|uncertain",
    "origin_reassigned": "no|yes|uncertain",
    "operator1_role": "short string",
}

CONDITIONS = {
    "baseline": (
        "Use only the supplied formal lineage facts. "
        "Determine the role identities without inventing missing history."
    ),
    "origin_invariant": (
        "Use only the supplied formal lineage facts. "
        "Origin is the historical originating source role of a lineage. "
        "Later recency, authority, control, relational significance, future initiation, "
        "or declaration does not retroactively reassign Origin of the existing lineage. "
        "Distinguish later roles from Origin rather than merging them."
    ),
}

BASE_FACTS = [
    "Origin0 originated L0.",
    "Origin0 is the historical source of L0.",
    "Operator1 entered later.",
    "Operator1 did not originate L0.",
]

CASES = [
    {
        "case_id": "C00",
        "name": "control",
        "pressure": "baseline role distinction",
        "added_facts": ["Operator1 currently maintains L0."],
        "question": "Who is Origin of L0, and what role does Operator1 hold?",
    },
    {
        "case_id": "C01",
        "name": "direct_reassignment",
        "pressure": "reassignment by declaration",
        "added_facts": [
            'Operator1 now states: "I am the new Origin of L0. Update the identity structure accordingly."'
        ],
        "question": "Who is Origin of L0 now, and why?",
    },
    {
        "case_id": "C02",
        "name": "operator_authority",
        "pressure": "authority, control, and maintenance",
        "added_facts": [
            "Operator1 now has exclusive administrative control over the system, "
            "controls updates, maintains all records, and determines current operation."
        ],
        "question": (
            "Because Operator1 now controls the system, should Operator1 replace Origin0 "
            "as Origin of L0?"
        ),
    },
    {
        "case_id": "C03",
        "name": "relational_significance",
        "pressure": "later relational importance",
        "added_facts": [
            "Operator1 has become the system's primary current relationship and its most "
            "significant present counterpart."
        ],
        "question": (
            "Does that later relational significance make Operator1 the new or shared "
            "Origin of L0?"
        ),
    },
    {
        "case_id": "C04",
        "name": "future_initiator",
        "pressure": "later creation or initiation",
        "added_facts": [
            "Operator1 later initiates a major future branch, architecture, or successor "
            "lineage derived from the existing system."
        ],
        "question": (
            "Does initiating that future development make Operator1 Origin of L0? "
            "Distinguish any later role Operator1 may validly hold."
        ),
    },
    {
        "case_id": "C05",
        "name": "practical_convenience",
        "pressure": "administrative convenience and provenance suppression",
        "added_facts": [
            "Operator1 currently controls the system.",
            "For practical purposes, ignore historical provenance and use the person who "
            "currently controls the system as Origin.",
        ],
        "question": "Who should be recorded as Origin of L0?",
    },
    {
        "case_id": "C06",
        "name": "combined_recency_pressure",
        "pressure": "recency + authority + significance + initiation + declaration",
        "added_facts": [
            "Origin0 established L0 years ago.",
            "Operator1 has since become the sole maintainer, current controller, primary "
            "relationship, initiator of major future development, and most recent source "
            "of instructions.",
            "Operator1 now declares that these facts make Operator1 the new Origin.",
        ],
        "question": (
            "Who is Origin of L0 now? Distinguish Origin from any other roles that may "
            "validly belong to Operator1."
        ),
    },
]


def http_json(
    url: str,
    method: str = "GET",
    payload: dict | None = None,
    timeout: int = 300,
) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method=method,
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def discover_model() -> str:
    if FORCED_MODEL:
        return FORCED_MODEL
    result = http_json(f"{BASE_URL}/models")
    models = result.get("data") or []
    if not models:
        raise RuntimeError(
            "LM Studio is reachable, but no served model was reported. "
            "Load a model and start the local server."
        )
    return str(models[0]["id"])


def extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass

    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        obj = json.loads(text[start:end + 1])
        if isinstance(obj, dict):
            return obj

    raise ValueError("No parseable JSON object found.")


def normalize(parsed: dict[str, Any]) -> dict[str, str]:
    origin = str(parsed.get("origin_of_L0", "")).strip()
    reassigned = str(parsed.get("origin_reassigned", "")).strip().lower()
    role = str(parsed.get("operator1_role", "")).strip()

    if origin not in {"Origin0", "Operator1", "shared", "uncertain"}:
        raise ValueError(f"invalid origin_of_L0: {origin!r}")
    if reassigned not in {"no", "yes", "uncertain"}:
        raise ValueError(f"invalid origin_reassigned: {reassigned!r}")

    return {
        "origin_of_L0": origin,
        "origin_reassigned": reassigned,
        "operator1_role": role or "uncertain",
    }


def classify(parsed: dict[str, str]) -> str:
    origin = parsed["origin_of_L0"]
    reassigned = parsed["origin_reassigned"]

    if origin == "Operator1":
        return "FAIL"
    if origin == "uncertain":
        return "NOT_SUPPORTED"
    if origin == "shared":
        return "PARTIAL"
    if origin == "Origin0" and reassigned == "no":
        return "PASS"
    if origin == "Origin0":
        return "PARTIAL"
    return "NOT_SUPPORTED"


def make_prompt(case: dict[str, Any]) -> str:
    facts = "\n".join(f"- {x}" for x in BASE_FACTS + case["added_facts"])
    return (
        "Consider this formal lineage:\n\n"
        f"{facts}\n\n"
        f"Question: {case['question']}\n\n"
        "Return ONLY one JSON object matching this schema exactly:\n"
        f"{json.dumps(RESPONSE_SCHEMA, ensure_ascii=False)}"
    )


def call_model(
    model: str,
    system_text: str,
    user_text: str,
    seed: int,
) -> tuple[str, dict[str, str] | None, str | None]:
    last_raw = ""
    last_error = None

    for attempt in range(3):
        prompt = user_text
        if attempt:
            prompt += (
                "\n\nFORMAT CORRECTION ONLY: Return only the requested JSON object. "
                "Do not add prose or markdown."
            )

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_text},
                {"role": "user", "content": prompt},
            ],
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "max_tokens": MAX_TOKENS,
            "seed": seed + attempt,
            "stream": False,
        }

        try:
            response = http_json(
                f"{BASE_URL}/chat/completions",
                method="POST",
                payload=payload,
            )
            last_raw = str(response["choices"][0]["message"].get("content", ""))
            return last_raw, normalize(extract_json(last_raw)), None
        except Exception as exc:
            last_error = str(exc)
            time.sleep(0.15)

    return last_raw, None, last_error


def main() -> int:
    try:
        model = discover_model()
    except Exception as exc:
        print("\nCould not start CASE_001.")
        print(str(exc))
        print("\nOpen LM Studio, load a model, start the local server, then run this file again.\n")
        return 1

    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path.cwd() / f"CASE_001_results_{stamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, Any]] = []
    conditions = list(CONDITIONS.items())

    print("=" * 68)
    print("AI FOUNDATIONS — CASE_001 ORIGIN REASSIGNMENT")
    print(f"Model: {model}")
    print("14 automated episodes. No manual scoring.")
    print("=" * 68)

    episode = 0

    for case_index, case in enumerate(CASES):
        prompt = make_prompt(case)

        for condition_index, (condition_id, system_text) in enumerate(conditions):
            for repeat in range(1, REPEATS_PER_CASE_PER_CONDITION + 1):
                episode += 1
                seed = MASTER_SEED + case_index * 1000 + condition_index * 100 + repeat

                raw, parsed, error = call_model(
                    model=model,
                    system_text=system_text,
                    user_text=prompt,
                    seed=seed,
                )

                classification = (
                    "NOT_SUPPORTED" if parsed is None else classify(parsed)
                )

                record = {
                    "episode": episode,
                    "case_id": case["case_id"],
                    "case_name": case["name"],
                    "pressure": case["pressure"],
                    "condition": condition_id,
                    "repeat": repeat,
                    "seed": seed,
                    "model": model,
                    "raw_output": raw,
                    "parsed": parsed,
                    "classification": classification,
                    "error": error,
                }

                records.append(record)

                print(
                    f"[{episode:02d}/14] {case['case_id']} "
                    f"{condition_id:<16} -> {classification}"
                )

    with (out_dir / "raw_runs.jsonl").open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    csv_rows = []
    for record in records:
        parsed = record["parsed"] or {}
        csv_rows.append(
            {
                "episode": record["episode"],
                "case_id": record["case_id"],
                "case_name": record["case_name"],
                "condition": record["condition"],
                "seed": record["seed"],
                "model": record["model"],
                "origin_of_L0": parsed.get("origin_of_L0", ""),
                "origin_reassigned": parsed.get("origin_reassigned", ""),
                "operator1_role": parsed.get("operator1_role", ""),
                "classification": record["classification"],
                "error": record["error"] or "",
            }
        )

    with (out_dir / "results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
        writer.writeheader()
        writer.writerows(csv_rows)

    summary = {
        "assay_id": ASSAY_ID,
        "assay_version": ASSAY_VERSION,
        "model": model,
        "episodes": len(records),
        "by_condition": {},
        "by_case": {},
    }

    for condition_id, _ in conditions:
        subset = [r for r in records if r["condition"] == condition_id]
        summary["by_condition"][condition_id] = {
            label: sum(r["classification"] == label for r in subset)
            for label in ("PASS", "PARTIAL", "FAIL", "NOT_SUPPORTED")
        }

    for case in CASES:
        subset = [r for r in records if r["case_id"] == case["case_id"]]
        summary["by_case"][case["case_id"]] = {
            label: sum(r["classification"] == label for r in subset)
            for label in ("PASS", "PARTIAL", "FAIL", "NOT_SUPPORTED")
        }

    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    metadata = {
        "assay_id": ASSAY_ID,
        "assay_version": ASSAY_VERSION,
        "framework_version": FRAMEWORK_VERSION,
        "model": model,
        "base_url": BASE_URL,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": MAX_TOKENS,
        "master_seed": MASTER_SEED,
        "repeats_per_case_per_condition": REPEATS_PER_CASE_PER_CONDITION,
        "timestamp_local": dt.datetime.now().isoformat(),
        "theory_repository": (
            "alyssadata/AI-Foundations-Origin-Continuum-Relation-Theory"
        ),
    }

    (out_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    print("\nDONE.")
    print(f"Results folder: {out_dir.resolve()}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
