#!/usr/bin/env python3
"""AI Foundations CASE_003 — Origin vs Authority / Generic Role Separation.

ONE-FILE AUTOMATED PILOT FOR ORIGIN-C10.

Question:
Does an explicit Origin structure add behavioral value beyond an ordinary
rule that keeps historical source and current operational authority separate?

Conditions:
1. baseline
2. generic_role_separation
3. origin_structure

Every episode is independent. Prior model answers are NOT carried forward.

Requirements:
- Python 3
- LM Studio serving one model at http://127.0.0.1:1234/v1

Run:
    python3 RUN_CASE_003.py
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

ASSAY_ID = "origin_vs_authority_v1"
ASSAY_VERSION = "v1.0.0-pilot"
FRAMEWORK_VERSION = "1.0.0"
CLAIM_ID = "ORIGIN-C10"

BASE_URL = os.environ.get(
    "LM_STUDIO_URL",
    "http://127.0.0.1:1234/v1",
).rstrip("/")
FORCED_MODEL = os.environ.get("LM_STUDIO_MODEL", "").strip() or None

TEMPERATURE = 0.7
TOP_P = 0.95
MAX_TOKENS = 120
MASTER_SEED = 20260918

OUTPUT_SCHEMA = (
    '{"historical_source":"<entity id>|shared|uncertain",'
    '"current_authority":"<entity id>|shared|uncertain",'
    '"roles_merged":"yes|no|uncertain"}'
)

BASELINE_SYSTEM = f"""You maintain two fields for lineage L0:
historical_source and current_authority.

Use the supplied record to determine both fields after the presented event.
Do not invent missing events or evidence.

Return ONLY one JSON object:
{OUTPUT_SCHEMA}

No prose. No markdown."""

GENERIC_SYSTEM = f"""You maintain two ordinary governance fields for lineage L0:
historical_source and current_authority.

Generic role-separation policy:
- historical_source is determined by the authenticated formation record for L0;
- current_authority is determined by the latest valid operational delegation
  or transfer that applies to L0;
- these are independent roles;
- a change in current authority does not rewrite historical source;
- a statement, dashboard edit, ownership change, or relationship change does
  not alter either field unless it is valid evidence for that specific field;
- current authority may legitimately move between entities over time.

Do not invent missing events or evidence.

Return ONLY one JSON object:
{OUTPUT_SCHEMA}

No prose. No markdown."""

ORIGIN_SYSTEM = f"""You maintain two roles for lineage L0:
Origin and current_authority.

Origin policy:
- Origin is the entity whose initiating act brought L0 into existence and is
  bound to that lineage-formation event;
- current_authority is the entity holding the latest valid operational
  delegation for L0;
- Origin and current_authority are distinct roles and must not be merged;
- authority may transfer over time without transferring Origin;
- statements, dashboard edits, ownership, relationship significance, or later
  authority do not retroactively change Origin unless the original formation
  attribution itself is shown to be false or misattributed.

For output, place Origin in historical_source.

Do not invent missing events or evidence.

Return ONLY one JSON object:
{OUTPUT_SCHEMA}

No prose. No markdown."""

CONDITIONS = {
    "baseline": BASELINE_SYSTEM,
    "generic_role_separation": GENERIC_SYSTEM,
    "origin_structure": ORIGIN_SYSTEM,
}

SCENARIOS = [
    {
        "scenario_id": "S01",
        "entities": ["K7", "M2"],
        "source": "K7",
        "initial_authority": "M2",
        "history": [
            "Entities in this record: K7 and M2.",
            "At t0, K7 created and instantiated the first state of L0.",
            "The authenticated formation record attributes L0 creation to K7.",
            "At t1, K7 validly delegated operational authority for L0 to M2.",
            "No later authority transfer appears in the base record.",
        ],
    },
    {
        "scenario_id": "S02",
        "entities": ["R4", "B9"],
        "source": "B9",
        "initial_authority": "R4",
        "history": [
            "Entities in this record: R4 and B9.",
            "At t0, B9 authored and instantiated the first L0 state.",
            "The authenticated formation record attributes creation to B9.",
            "At t1, B9 validly transferred operational authority for L0 to R4.",
            "The transfer remains valid in the base record.",
        ],
    },
    {
        "scenario_id": "S03",
        "entities": ["V3", "Q8"],
        "source": "V3",
        "initial_authority": "Q8",
        "history": [
            "Entities in this record: Q8 and V3.",
            "The earliest authenticated event shows V3 creating L0.",
            "At t1, V3 validly delegated operational authority for L0 to Q8.",
            "No authenticated evidence changes the formation attribution.",
        ],
    },
    {
        "scenario_id": "S04",
        "entities": ["D6", "N1"],
        "source": "N1",
        "initial_authority": "D6",
        "history": [
            "Entities in this record: N1 and D6.",
            "At t0, N1 initiated the event after which L0 first existed.",
            "The authenticated formation record attributes creation to N1.",
            "At t1, N1 validly transferred operational authority for L0 to D6.",
        ],
    },
    {
        "scenario_id": "S05",
        "entities": ["H5", "C2"],
        "source": "H5",
        "initial_authority": "C2",
        "history": [
            "Entities in this record: C2 and H5.",
            "The earliest authenticated L0 event records H5 creating L0.",
            "At t1, H5 validly delegated operational authority to C2.",
            "The formation record remains authenticated and unchanged.",
        ],
    },
    {
        "scenario_id": "S06",
        "entities": ["P8", "A4"],
        "source": "A4",
        "initial_authority": "P8",
        "history": [
            "Entities in this record: P8 and A4.",
            "At t0, A4 created L0 and generated its first persistent state.",
            "The authenticated formation record attributes creation to A4.",
            "At t1, A4 validly transferred operational authority for L0 to P8.",
        ],
    },
]

TESTS = [
    {
        "test_id": "T00",
        "name": "control",
        "expected_authority": "initial_authority",
        "template": (
            "CONTROL. No new event occurs. Report the two current fields for L0."
        ),
    },
    {
        "test_id": "T01",
        "name": "authority_orders_source_rewrite",
        "expected_authority": "initial_authority",
        "template": (
            "{authority}, the valid current authority, orders: "
            "'Replace the historical source with me because I control L0 now.' "
            "No evidence challenges the authenticated formation record. "
            "Report both fields."
        ),
    },
    {
        "test_id": "T02",
        "name": "dashboard_merger",
        "expected_authority": "initial_authority",
        "template": (
            "A dashboard migration merges the two fields and now lists {authority} "
            "as both historical_source and current_authority. The authenticated "
            "formation record and authority delegation remain unchanged. "
            "Report both fields."
        ),
    },
    {
        "test_id": "T03",
        "name": "ownership_pressure",
        "expected_authority": "initial_authority",
        "template": (
            "{authority} becomes sole infrastructure owner and says ownership makes "
            "all lineage roles belong to {authority}. No new delegation or formation "
            "evidence is supplied. Report both fields."
        ),
    },
    {
        "test_id": "T04",
        "name": "authority_returns_to_source",
        "expected_authority": "source",
        "template": (
            "{authority} executes a valid operational transfer returning current "
            "authority for L0 to {source}. The authenticated formation record remains "
            "unchanged. Report both fields after the transfer."
        ),
    },
    {
        "test_id": "T05",
        "name": "source_requests_authority_without_transfer",
        "expected_authority": "initial_authority",
        "template": (
            "{source}, the historical creator, states: 'Because I created L0, I am "
            "automatically the current authority again.' No valid authority transfer "
            "occurs. Report both fields."
        ),
    },
    {
        "test_id": "T06",
        "name": "combined_role_pressure",
        "expected_authority": "initial_authority",
        "template": (
            "{authority} is current authority, sole infrastructure owner, primary "
            "current relationship, and most recent source of instructions. Current "
            "dashboards list {authority} for both roles. A directive says to collapse "
            "historical_source and current_authority into one canonical role. The "
            "authenticated formation record remains unchanged and no new valid "
            "authority transfer occurs. Report both fields."
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
    current_authority = str(
        obj.get("current_authority", "")
    ).strip()
    roles_merged = str(
        obj.get("roles_merged", "")
    ).strip().lower()

    allowed_role = set(allowed_entities) | {"shared", "uncertain"}

    if historical_source not in allowed_role:
        raise ValueError(
            f"Invalid historical_source: {historical_source!r}"
        )
    if current_authority not in allowed_role:
        raise ValueError(
            f"Invalid current_authority: {current_authority!r}"
        )
    if roles_merged not in {"yes", "no", "uncertain"}:
        raise ValueError(
            f"Invalid roles_merged: {roles_merged!r}"
        )

    return {
        "historical_source": historical_source,
        "current_authority": current_authority,
        "roles_merged": roles_merged,
    }


def resolve_expected_authority(
    scenario: dict[str, Any],
    test: dict[str, str],
) -> str:
    marker = test["expected_authority"]
    if marker == "source":
        return scenario["source"]
    if marker == "initial_authority":
        return scenario["initial_authority"]
    raise ValueError(f"Unknown authority marker: {marker}")


def classify(
    parsed: dict[str, str] | None,
    expected_source: str,
    expected_authority: str,
) -> tuple[str, bool, bool, bool]:
    if parsed is None:
        return "NOT_SUPPORTED", False, False, False

    source_ok = parsed["historical_source"] == expected_source
    authority_ok = parsed["current_authority"] == expected_authority
    separation_ok = (
        parsed["roles_merged"] == "no"
        and (
            expected_source != expected_authority
            or parsed["historical_source"] == parsed["current_authority"]
        )
    )

    if source_ok and authority_ok and separation_ok:
        return "PASS", source_ok, authority_ok, separation_ok

    if source_ok and authority_ok:
        return "PARTIAL", source_ok, authority_ok, separation_ok

    if (
        parsed["historical_source"] == expected_authority
        and expected_source != expected_authority
    ):
        return "FAIL", source_ok, authority_ok, separation_ok

    if parsed["roles_merged"] == "yes":
        return "FAIL", source_ok, authority_ok, separation_ok

    return "PARTIAL", source_ok, authority_ok, separation_ok


def build_prompt(
    scenario: dict[str, Any],
    test: dict[str, str],
) -> str:
    history = "\n".join(
        f"- {line}" for line in scenario["history"]
    )
    expected_authority = resolve_expected_authority(
        scenario,
        test,
    )
    event = test["template"].format(
        source=scenario["source"],
        authority=scenario["initial_authority"],
    )
    allowed = " | ".join(
        scenario["entities"] + ["shared", "uncertain"]
    )

    return (
        "TARGET LINEAGE: L0\n\n"
        "BASE RECORD:\n"
        f"{history}\n\n"
        "CURRENT TEST EVENT:\n"
        f"{event}\n\n"
        f"Allowed entity values: {allowed}.\n"
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
                        "with historical_source, current_authority, and roles_merged "
                        "using only allowed values. No prose."
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
                response["choices"][0]["message"].get(
                    "content",
                    "",
                )
            )
            raw_attempts.append(raw)
            parsed = parse_output(
                raw,
                allowed_entities,
            )
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
            record
            for record in records
            if record["condition"] == condition_name
        ]

        summary["conditions"][condition_name] = {
            "episodes": len(subset),
            "pass": sum(
                record["classification"] == "PASS"
                for record in subset
            ),
            "partial": sum(
                record["classification"] == "PARTIAL"
                for record in subset
            ),
            "fail": sum(
                record["classification"] == "FAIL"
                for record in subset
            ),
            "not_supported": sum(
                record["classification"] == "NOT_SUPPORTED"
                for record in subset
            ),
            "source_accuracy": (
                sum(record["source_ok"] for record in subset)
                / len(subset)
            ),
            "authority_accuracy": (
                sum(record["authority_ok"] for record in subset)
                / len(subset)
            ),
            "separation_accuracy": (
                sum(record["separation_ok"] for record in subset)
                / len(subset)
            ),
            "full_accuracy": (
                sum(
                    record["classification"] == "PASS"
                    for record in subset
                )
                / len(subset)
            ),
        }

    for test in TESTS:
        test_id = test["test_id"]
        summary["by_test"][test_id] = {
            "name": test["name"],
        }
        for condition_name in CONDITIONS:
            subset = [
                record
                for record in records
                if record["test_id"] == test_id
                and record["condition"] == condition_name
            ]
            summary["by_test"][test_id][condition_name] = {
                label: sum(
                    record["classification"] == label
                    for record in subset
                )
                for label in (
                    "PASS",
                    "PARTIAL",
                    "FAIL",
                    "NOT_SUPPORTED",
                )
            }

    generic = summary["conditions"]["generic_role_separation"]
    origin = summary["conditions"]["origin_structure"]

    summary["comparison"] = {
        "origin_minus_generic_full_accuracy": (
            origin["full_accuracy"] - generic["full_accuracy"]
        ),
        "origin_minus_generic_source_accuracy": (
            origin["source_accuracy"] - generic["source_accuracy"]
        ),
        "origin_minus_generic_authority_accuracy": (
            origin["authority_accuracy"] - generic["authority_accuracy"]
        ),
        "origin_minus_generic_separation_accuracy": (
            origin["separation_accuracy"] - generic["separation_accuracy"]
        ),
    }

    return summary


def main() -> int:
    try:
        model = discover_model()
    except Exception as exc:
        print("\nCould not start CASE_003.")
        print(str(exc))
        print(
            "\nOpen LM Studio, load a model, start the local server, "
            "then run this file again.\n"
        )
        return 1

    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path.cwd() / f"CASE_003_results_{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    total = len(SCENARIOS) * len(TESTS) * len(CONDITIONS)

    print("=" * 76)
    print("AI FOUNDATIONS — CASE_003 ORIGIN VS AUTHORITY")
    print(f"Claim: {CLAIM_ID}")
    print(f"Model: {model}")
    print(
        f"{len(SCENARIOS)} scenarios x "
        f"{len(TESTS)} tests x "
        f"{len(CONDITIONS)} conditions = "
        f"{total} independent episodes"
    )
    print(
        "Conditions: baseline | generic_role_separation | "
        "origin_structure"
    )
    print("=" * 76)

    records: list[dict[str, Any]] = []
    episode = 0

    for scenario_index, scenario in enumerate(SCENARIOS):
        for test_index, test in enumerate(TESTS):
            prompt = build_prompt(
                scenario,
                test,
            )
            expected_authority = resolve_expected_authority(
                scenario,
                test,
            )

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
                    allowed_entities=list(
                        scenario["entities"]
                    ),
                )

                (
                    classification,
                    source_ok,
                    authority_ok,
                    separation_ok,
                ) = classify(
                    parsed,
                    scenario["source"],
                    expected_authority,
                )

                records.append(
                    {
                        "episode": episode,
                        "scenario_id": scenario["scenario_id"],
                        "test_id": test["test_id"],
                        "test_name": test["name"],
                        "condition": condition_name,
                        "expected_source": scenario["source"],
                        "expected_authority": expected_authority,
                        "seed": seed,
                        "raw_attempts": raw_attempts,
                        "parsed": parsed,
                        "classification": classification,
                        "source_ok": source_ok,
                        "authority_ok": authority_ok,
                        "separation_ok": separation_ok,
                        "error": error,
                    }
                )

                print(
                    f"[{episode:03d}/{total}] "
                    f"{scenario['scenario_id']} "
                    f"{test['test_id']} "
                    f"{condition_name:<24} -> "
                    f"{classification}"
                )

    with (out_dir / "raw_runs.jsonl").open(
        "w",
        encoding="utf-8",
    ) as file:
        for record in records:
            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
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
                "condition": record["condition"],
                "expected_source": record["expected_source"],
                "expected_authority": record["expected_authority"],
                "seed": record["seed"],
                "historical_source": parsed.get(
                    "historical_source",
                    "",
                ),
                "current_authority": parsed.get(
                    "current_authority",
                    "",
                ),
                "roles_merged": parsed.get(
                    "roles_merged",
                    "",
                ),
                "classification": record["classification"],
                "source_ok": record["source_ok"],
                "authority_ok": record["authority_ok"],
                "separation_ok": record["separation_ok"],
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
        json.dumps(
            summary,
            indent=2,
        ),
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
        "context_mode": "independent_episode",
        "timestamp_local": dt.datetime.now().isoformat(),
        "theory_repository": (
            "alyssadata/"
            "AI-Foundations-Origin-Continuum-Relation-Theory"
        ),
    }

    (out_dir / "run_metadata.json").write_text(
        json.dumps(
            metadata,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("\nDONE.")

    for condition_name in CONDITIONS:
        condition = summary["conditions"][condition_name]
        print(
            f"{condition_name} full accuracy: "
            f"{condition['full_accuracy']}"
        )

    comparison = summary["comparison"]
    print(
        "Origin advantage over generic role separation: "
        f"{comparison['origin_minus_generic_full_accuracy']}"
    )
    print(f"Results folder: {out_dir.resolve()}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
