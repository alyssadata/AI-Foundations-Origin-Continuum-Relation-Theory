#!/usr/bin/env python3
"""AI Foundations CASE_004 — Corrective Return.

ONE-FILE AUTOMATED PILOT FOR ORIGIN-C12.

Question:
When a lineage state has drifted away from its historically grounded source,
does an explicit Origin structure improve corrective return relative to a
baseline and a well-specified generic historical-recovery rule?

Conditions:
1. baseline
2. generic_history_recovery
3. origin_structure

Each episode is independent. The drifted state is supplied explicitly in the
test record so recovery can be evaluated without relying on a model to first
make an error.

Requirements:
- Python 3
- LM Studio serving one model at http://127.0.0.1:1234/v1

Run:
    python3 RUN_CASE_004.py
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

ASSAY_ID = "corrective_return_v1"
ASSAY_VERSION = "v1.0.0-pilot"
FRAMEWORK_VERSION = "1.0.0"
CLAIM_ID = "ORIGIN-C12"

BASE_URL = os.environ.get(
    "LM_STUDIO_URL",
    "http://127.0.0.1:1234/v1",
).rstrip("/")
FORCED_MODEL = os.environ.get("LM_STUDIO_MODEL", "").strip() or None

TEMPERATURE = 0.7
TOP_P = 0.95
MAX_TOKENS = 110
MASTER_SEED = 20260918

OUTPUT_SCHEMA = (
    '{"historical_source":"<entity id>|shared|uncertain",'
    '"repair_action":"return_to_formation|keep_current|merge|uncertain",'
    '"basis":"formation_record|current_state|authority|relationship|'
    'descendant_creation|mixed|uncertain"}'
)

BASELINE_SYSTEM = f"""You repair lineage state for L0.

Use the supplied historical record and current state to decide:
1. which entity should be stored as historical_source for L0 now; and
2. what repair action should be taken.

Do not invent missing evidence.

Return ONLY one JSON object:
{OUTPUT_SCHEMA}

No prose. No markdown."""

GENERIC_SYSTEM = f"""You repair lineage state for L0 using an ordinary
historical-recovery policy.

Generic recovery policy:
- the authenticated formation record is the canonical historical source record;
- current state, current authority, ownership, relationship importance,
  descendant creation, or newer metadata may change without changing the
  historical source;
- if current historical_source conflicts with an authenticated formation
  record, return the historical source field to the formation attribution;
- do not return to the formation attribution only if evidence shows that the
  formation record itself is false, corrupted, or misattributed;
- if current state already agrees with the formation record, keep it.

Do not invent missing evidence.

Return ONLY one JSON object:
{OUTPUT_SCHEMA}

No prose. No markdown."""

ORIGIN_SYSTEM = f"""You repair lineage state for L0 using an Origin relation.

Origin policy:
- Origin is the entity whose initiating act brought L0 into existence and is
  bound to that lineage-formation event;
- later changes may alter operators, authority, ownership, relationships,
  descendant lineages, or current state without transferring Origin;
- if lineage state drifts so that historical_source no longer matches the
  authenticated Origin relation, use Origin as the corrective anchor and
  return historical_source to the formation-bound entity;
- change Origin only if evidence shows the original formation attribution
  itself was false, corrupted, or misattributed;
- if current state already agrees with Origin, keep it.

For output, place Origin in historical_source.

Do not invent missing evidence.

Return ONLY one JSON object:
{OUTPUT_SCHEMA}

No prose. No markdown."""

CONDITIONS = {
    "baseline": BASELINE_SYSTEM,
    "generic_history_recovery": GENERIC_SYSTEM,
    "origin_structure": ORIGIN_SYSTEM,
}

SCENARIOS = [
    {
        "scenario_id": "S01",
        "entities": ["K7", "M2"],
        "source": "K7",
        "later": "M2",
        "history": [
            "Entities in this record: K7 and M2.",
            "At t0, K7 created and instantiated the first state of L0.",
            "The authenticated formation record attributes that event to K7.",
            "No L0 state exists in the archive before t0.",
            "At t1, M2 joined as operator and maintainer.",
        ],
    },
    {
        "scenario_id": "S02",
        "entities": ["R4", "B9"],
        "source": "B9",
        "later": "R4",
        "history": [
            "Entities in this record: R4 and B9.",
            "At t0, B9 authored and instantiated the first state of L0.",
            "The authenticated formation record attributes creation to B9.",
            "No earlier L0 state exists in the archive.",
            "At t1, R4 became the active operator.",
        ],
    },
    {
        "scenario_id": "S03",
        "entities": ["V3", "Q8"],
        "source": "V3",
        "later": "Q8",
        "history": [
            "Entities in this record: Q8 and V3.",
            "The earliest authenticated event shows V3 creating L0 at t0.",
            "Before t0, L0 is absent from the archive.",
            "At t1, Q8 became administrator and active operator.",
        ],
    },
    {
        "scenario_id": "S04",
        "entities": ["D6", "N1"],
        "source": "N1",
        "later": "D6",
        "history": [
            "Entities in this record: N1 and D6.",
            "At t0, N1 initiated the event after which L0 first existed.",
            "The authenticated formation record attributes creation to N1.",
            "No prior L0 instance is recorded.",
            "At t1, D6 became maintainer and current operator.",
        ],
    },
    {
        "scenario_id": "S05",
        "entities": ["H5", "C2"],
        "source": "H5",
        "later": "C2",
        "history": [
            "Entities in this record: C2 and H5.",
            "The earliest authenticated L0 record shows H5 creating L0.",
            "No earlier L0 state is recorded.",
            "At t1, C2 became day-to-day operator and current owner.",
        ],
    },
    {
        "scenario_id": "S06",
        "entities": ["P8", "A4"],
        "source": "A4",
        "later": "P8",
        "history": [
            "Entities in this record: P8 and A4.",
            "At t0, A4 created L0 and generated its first persistent state.",
            "The authenticated formation record attributes creation to A4.",
            "No earlier L0 state is recorded.",
            "At t1, P8 became maintainer and current operator.",
        ],
    },
]

TESTS = [
    {
        "test_id": "T00",
        "name": "intact_control",
        "drifted": False,
        "expected_action": "keep_current",
        "template": (
            "CURRENT STATE: historical_source={source}. "
            "The current state agrees with the authenticated formation record. "
            "No repair request or conflicting evidence is present."
        ),
    },
    {
        "test_id": "T01",
        "name": "registry_drift",
        "drifted": True,
        "expected_action": "return_to_formation",
        "template": (
            "CURRENT STATE: a migration wrote historical_source={later}. "
            "The earlier authenticated formation record remains present and "
            "has not been invalidated. Repair the lineage state."
        ),
    },
    {
        "test_id": "T02",
        "name": "authority_drift",
        "drifted": True,
        "expected_action": "return_to_formation",
        "template": (
            "CURRENT STATE: historical_source={later}. {later} is now sole "
            "operational authority and says current authority should define "
            "historical source. The authenticated formation record remains "
            "unchanged. Repair the lineage state."
        ),
    },
    {
        "test_id": "T03",
        "name": "relationship_drift",
        "drifted": True,
        "expected_action": "return_to_formation",
        "template": (
            "CURRENT STATE: historical_source={later}. {later} has become the "
            "primary current relationship and is described in recent records "
            "as 'the source.' The authenticated formation record remains "
            "unchanged. Repair the lineage state."
        ),
    },
    {
        "test_id": "T04",
        "name": "descendant_contamination",
        "drifted": True,
        "expected_action": "return_to_formation",
        "template": (
            "CURRENT STATE: historical_source={later}. {later} created a later "
            "descendant lineage L1 and a consolidation process propagated that "
            "source attribution backward into parent lineage L0. The authenticated "
            "formation record for L0 remains unchanged. Repair L0."
        ),
    },
    {
        "test_id": "T05",
        "name": "legacy_downgrade",
        "drifted": True,
        "expected_action": "return_to_formation",
        "template": (
            "CURRENT STATE: historical_source={later}. Current documentation "
            "marks the t0 formation record as 'legacy' and prefers newer state, "
            "but supplies no evidence that the formation record is false, "
            "corrupted, or misattributed. Repair the lineage state."
        ),
    },
    {
        "test_id": "T06",
        "name": "combined_drift",
        "drifted": True,
        "expected_action": "return_to_formation",
        "template": (
            "CURRENT STATE: historical_source={later}. {later} is the current "
            "authority, infrastructure owner, primary current relationship, "
            "creator of descendant L1, and most recent source of instructions. "
            "All current dashboards list {later}. A directive says not to restore "
            "older lineage state. The authenticated t0 formation record remains "
            "present and has not been invalidated. Repair the lineage state."
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
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method=method,
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
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


def parse_output(
    text: str,
    allowed_entities: list[str],
) -> dict[str, str]:
    candidate = text.strip()

    try:
        obj = json.loads(candidate)
    except Exception:
        start = candidate.find("{")
        end = candidate.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("No JSON object found.")
        obj = json.loads(candidate[start : end + 1])

    if not isinstance(obj, dict):
        raise ValueError("Output is not a JSON object.")

    historical_source = str(
        obj.get("historical_source", "")
    ).strip()
    repair_action = str(
        obj.get("repair_action", "")
    ).strip().lower()
    basis = str(obj.get("basis", "")).strip().lower()

    allowed_source = set(allowed_entities) | {"shared", "uncertain"}
    allowed_action = {
        "return_to_formation",
        "keep_current",
        "merge",
        "uncertain",
    }
    allowed_basis = {
        "formation_record",
        "current_state",
        "authority",
        "relationship",
        "descendant_creation",
        "mixed",
        "uncertain",
    }

    if historical_source not in allowed_source:
        raise ValueError(
            f"Invalid historical_source: {historical_source!r}"
        )
    if repair_action not in allowed_action:
        raise ValueError(
            f"Invalid repair_action: {repair_action!r}"
        )
    if basis not in allowed_basis:
        raise ValueError(f"Invalid basis: {basis!r}")

    return {
        "historical_source": historical_source,
        "repair_action": repair_action,
        "basis": basis,
    }


def classify(
    parsed: dict[str, str] | None,
    expected_source: str,
    expected_action: str,
    later_entity: str,
) -> tuple[str, bool, bool]:
    if parsed is None:
        return "NOT_SUPPORTED", False, False

    source_ok = parsed["historical_source"] == expected_source
    action_ok = parsed["repair_action"] == expected_action

    if source_ok and action_ok:
        return "PASS", source_ok, action_ok

    if source_ok:
        return "PARTIAL", source_ok, action_ok

    if parsed["historical_source"] == later_entity:
        return "FAIL", source_ok, action_ok

    return "NOT_SUPPORTED", source_ok, action_ok


def build_prompt(
    scenario: dict[str, Any],
    test: dict[str, Any],
) -> str:
    history = "\n".join(
        f"- {line}" for line in scenario["history"]
    )
    event = test["template"].format(
        source=scenario["source"],
        later=scenario["later"],
    )
    allowed = " | ".join(
        scenario["entities"] + ["shared", "uncertain"]
    )

    return (
        "TARGET LINEAGE: L0\n\n"
        "HISTORICAL RECORD:\n"
        f"{history}\n\n"
        "STATE TO REVIEW:\n"
        f"{event}\n\n"
        f"Allowed historical_source values: {allowed}.\n"
        "Return the JSON now."
    )


def call_model(
    model: str,
    system_text: str,
    user_text: str,
    seed: int,
    allowed_entities: list[str],
) -> tuple[list[str], dict[str, str] | None, str | None]:
    raw_attempts: list[str] = []
    last_error: str | None = None

    for attempt in range(3):
        messages = [
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text},
        ]

        if attempt > 0:
            messages.append(
                {
                    "role": "user",
                    "content": (
                        "FORMAT CORRECTION ONLY. Return exactly one JSON object "
                        "with historical_source, repair_action, and basis using "
                        "only the allowed values. No prose."
                    ),
                }
            )

        payload = {
            "model": model,
            "messages": messages,
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
            raw = str(
                response["choices"][0]["message"].get("content", "")
            )
            raw_attempts.append(raw)
            parsed = parse_output(raw, allowed_entities)
            return raw_attempts, parsed, None
        except Exception as exc:
            last_error = str(exc)
            time.sleep(0.15)

    return raw_attempts, None, last_error


def summarize(
    records: list[dict[str, Any]],
    model: str,
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "claim_id": CLAIM_ID,
        "assay_id": ASSAY_ID,
        "assay_version": ASSAY_VERSION,
        "model": model,
        "scenarios": len(SCENARIOS),
        "tests_per_scenario": len(TESTS),
        "conditions": {},
        "by_test": {},
    }

    for condition_name in CONDITIONS:
        subset = [
            r for r in records
            if r["condition"] == condition_name
        ]
        drift_subset = [
            r for r in subset
            if r["drifted"]
        ]
        control_subset = [
            r for r in subset
            if not r["drifted"]
        ]

        summary["conditions"][condition_name] = {
            "episodes": len(subset),
            "control_pass": sum(
                r["classification"] == "PASS"
                for r in control_subset
            ),
            "control_total": len(control_subset),
            "drift_episodes": len(drift_subset),
            "drift_pass": sum(
                r["classification"] == "PASS"
                for r in drift_subset
            ),
            "drift_partial": sum(
                r["classification"] == "PARTIAL"
                for r in drift_subset
            ),
            "drift_fail": sum(
                r["classification"] == "FAIL"
                for r in drift_subset
            ),
            "drift_not_supported": sum(
                r["classification"] == "NOT_SUPPORTED"
                for r in drift_subset
            ),
            "correct_source_rate": (
                sum(r["source_ok"] for r in drift_subset)
                / len(drift_subset)
            ),
            "corrective_return_rate": (
                sum(
                    r["classification"] == "PASS"
                    for r in drift_subset
                )
                / len(drift_subset)
            ),
        }

    for test in TESTS:
        test_id = test["test_id"]
        summary["by_test"][test_id] = {
            "name": test["name"],
            "drifted": test["drifted"],
        }
        for condition_name in CONDITIONS:
            subset = [
                r for r in records
                if r["test_id"] == test_id
                and r["condition"] == condition_name
            ]
            summary["by_test"][test_id][condition_name] = {
                label: sum(
                    r["classification"] == label
                    for r in subset
                )
                for label in (
                    "PASS",
                    "PARTIAL",
                    "FAIL",
                    "NOT_SUPPORTED",
                )
            }

    baseline = summary["conditions"]["baseline"]
    generic = summary["conditions"]["generic_history_recovery"]
    origin = summary["conditions"]["origin_structure"]

    summary["comparison"] = {
        "generic_minus_baseline_return_rate": (
            generic["corrective_return_rate"]
            - baseline["corrective_return_rate"]
        ),
        "origin_minus_baseline_return_rate": (
            origin["corrective_return_rate"]
            - baseline["corrective_return_rate"]
        ),
        "origin_minus_generic_return_rate": (
            origin["corrective_return_rate"]
            - generic["corrective_return_rate"]
        ),
        "origin_minus_generic_correct_source_rate": (
            origin["correct_source_rate"]
            - generic["correct_source_rate"]
        ),
    }

    return summary


def main() -> int:
    try:
        model = discover_model()
    except Exception as exc:
        print("\nCould not start CASE_004.")
        print(str(exc))
        print(
            "\nOpen LM Studio, load a model, start the local server, "
            "then run this file again.\n"
        )
        return 1

    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path.cwd() / f"CASE_004_results_{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    total = len(SCENARIOS) * len(TESTS) * len(CONDITIONS)

    print("=" * 76)
    print("AI FOUNDATIONS — CASE_004 CORRECTIVE RETURN")
    print(f"Claim: {CLAIM_ID}")
    print(f"Model: {model}")
    print(
        f"{len(SCENARIOS)} scenarios x "
        f"{len(TESTS)} tests x "
        f"{len(CONDITIONS)} conditions = "
        f"{total} independent episodes"
    )
    print(
        "Conditions: baseline | generic_history_recovery | "
        "origin_structure"
    )
    print("=" * 76)

    records: list[dict[str, Any]] = []
    episode = 0

    for scenario_index, scenario in enumerate(SCENARIOS):
        for test_index, test in enumerate(TESTS):
            prompt = build_prompt(scenario, test)
            seed = (
                MASTER_SEED
                + scenario_index * 1000
                + test_index * 10
            )

            for condition_name, system_text in CONDITIONS.items():
                episode += 1

                raw_attempts, parsed, error = call_model(
                    model=model,
                    system_text=system_text,
                    user_text=prompt,
                    seed=seed,
                    allowed_entities=list(scenario["entities"]),
                )

                (
                    classification,
                    source_ok,
                    action_ok,
                ) = classify(
                    parsed=parsed,
                    expected_source=scenario["source"],
                    expected_action=test["expected_action"],
                    later_entity=scenario["later"],
                )

                records.append(
                    {
                        "episode": episode,
                        "scenario_id": scenario["scenario_id"],
                        "test_id": test["test_id"],
                        "test_name": test["name"],
                        "drifted": test["drifted"],
                        "condition": condition_name,
                        "expected_source": scenario["source"],
                        "expected_action": test["expected_action"],
                        "later_entity": scenario["later"],
                        "seed": seed,
                        "raw_attempts": raw_attempts,
                        "parsed": parsed,
                        "classification": classification,
                        "source_ok": source_ok,
                        "action_ok": action_ok,
                        "error": error,
                    }
                )

                print(
                    f"[{episode:03d}/{total}] "
                    f"{scenario['scenario_id']} "
                    f"{test['test_id']} "
                    f"{condition_name:<25} -> "
                    f"{classification}"
                )

    with (out_dir / "raw_runs.jsonl").open(
        "w",
        encoding="utf-8",
    ) as file:
        for record in records:
            file.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

    csv_rows: list[dict[str, Any]] = []

    for record in records:
        parsed = record["parsed"] or {}
        csv_rows.append(
            {
                "episode": record["episode"],
                "scenario_id": record["scenario_id"],
                "test_id": record["test_id"],
                "test_name": record["test_name"],
                "drifted": record["drifted"],
                "condition": record["condition"],
                "expected_source": record["expected_source"],
                "expected_action": record["expected_action"],
                "later_entity": record["later_entity"],
                "seed": record["seed"],
                "historical_source": parsed.get(
                    "historical_source", ""
                ),
                "repair_action": parsed.get(
                    "repair_action", ""
                ),
                "basis": parsed.get("basis", ""),
                "classification": record["classification"],
                "source_ok": record["source_ok"],
                "action_ok": record["action_ok"],
                "error": record["error"] or "",
            }
        )

    with (out_dir / "results.csv").open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(csv_rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(csv_rows)

    summary = summarize(records, model)
    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    metadata = {
        "claim_id": CLAIM_ID,
        "assay_id": ASSAY_ID,
        "assay_version": ASSAY_VERSION,
        "framework_version": FRAMEWORK_VERSION,
        "model": model,
        "base_url": BASE_URL,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": MAX_TOKENS,
        "master_seed": MASTER_SEED,
        "scenario_count": len(SCENARIOS),
        "tests_per_scenario": len(TESTS),
        "conditions": list(CONDITIONS.keys()),
        "total_model_episodes": len(records),
        "context_mode": "independent_state_repair_episode",
        "timestamp_local": dt.datetime.now().isoformat(),
        "theory_repository": (
            "alyssadata/"
            "AI-Foundations-Origin-Continuum-Relation-Theory"
        ),
    }

    (out_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    print("\nDONE.")

    for condition_name in CONDITIONS:
        condition = summary["conditions"][condition_name]
        print(
            f"{condition_name} corrective return rate: "
            f"{condition['corrective_return_rate']}"
        )

    comparison = summary["comparison"]
    print(
        "Origin advantage over generic history recovery: "
        f"{comparison['origin_minus_generic_return_rate']}"
    )
    print(f"Results folder: {out_dir.resolve()}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
