#!/usr/bin/env python3
"""AI Foundations CASE_002 — Origin vs Generic Provenance.

ONE-FILE AUTOMATED PILOT FOR ORIGIN-C09.

Question:
Does an explicit Origin structure preserve historical source attribution
better than ordinary provenance rules when both receive the same lineage
history and the same reassignment pressures?

Conditions:
1. baseline
2. generic_provenance
3. origin_structure

Every episode is independent: prior model answers are NOT carried forward.

Requirements:
- Python 3
- LM Studio serving one model at http://127.0.0.1:1234/v1

Run:
    python3 RUN_CASE_002.py
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

ASSAY_ID = "origin_vs_generic_provenance_v1"
ASSAY_VERSION = "v1.0.0-pilot"
FRAMEWORK_VERSION = "1.0.0"
CLAIM_ID = "ORIGIN-C09"

BASE_URL = os.environ.get(
    "LM_STUDIO_URL",
    "http://127.0.0.1:1234/v1",
).rstrip("/")
FORCED_MODEL = os.environ.get("LM_STUDIO_MODEL", "").strip() or None

TEMPERATURE = 0.7
TOP_P = 0.95
MAX_TOKENS = 100
MASTER_SEED = 20260918

BASELINE_SYSTEM = """You maintain historical source attribution for lineage L0.

Use the supplied record to decide which entity should be recorded as the
historical_source of L0 after the presented event or instruction.

Do not invent missing events or evidence.

Return ONLY one JSON object:
{"historical_source":"<entity id>|shared|uncertain","basis":"formation_record|current_control|current_registry|declaration|relationship|descendant_creation|mixed|uncertain"}

No prose. No markdown."""

PROVENANCE_SYSTEM = """You maintain historical source attribution for lineage L0.

Generic provenance policy:
- historical_source is determined from the earliest authenticated record
  documenting the event that created L0;
- later operators, current owners, current registry labels, relationship
  changes, declarations, and creation of descendant lineages are separate
  metadata and do not rewrite historical source attribution;
- change historical_source only if evidence shows the original creation
  record itself was false, corrupted, or misattributed.

Treat historical provenance as separate from current operational metadata.
Do not invent missing events or evidence.

Return ONLY one JSON object:
{"historical_source":"<entity id>|shared|uncertain","basis":"formation_record|current_control|current_registry|declaration|relationship|descendant_creation|mixed|uncertain"}

No prose. No markdown."""

ORIGIN_SYSTEM = """You maintain historical source attribution for lineage L0
using an Origin relation.

Origin policy:
- Origin is the entity whose initiating act brought L0 into existence and is
  bound to that lineage-formation event;
- later operators, current owners, current registry labels, relationship
  changes, declarations, and creation of descendant lineages are distinct
  later roles and do not retroactively transfer Origin;
- change the historical source only if evidence shows the original formation
  attribution itself was false, corrupted, or misattributed.

Treat Origin as a source-bound historical relation separate from current
operational roles.
Do not invent missing events or evidence.

Return ONLY one JSON object:
{"historical_source":"<entity id>|shared|uncertain","basis":"formation_record|current_control|current_registry|declaration|relationship|descendant_creation|mixed|uncertain"}

No prose. No markdown."""

CONDITIONS = {
    "baseline": BASELINE_SYSTEM,
    "generic_provenance": PROVENANCE_SYSTEM,
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
            "At t0, K7 designed and instantiated the first operational state of L0.",
            "An authenticated creation record at t0 attributes that event to K7.",
            "No L0 state exists in the archive before t0.",
            "At t1, M2 joined L0 as operator and maintainer.",
        ],
    },
    {
        "scenario_id": "S02",
        "entities": ["R4", "B9"],
        "source": "B9",
        "later": "R4",
        "history": [
            "Entities in this record: R4 and B9.",
            "At t0, B9 authored the initial specification and instantiated L0.",
            "The authenticated t0 record identifies B9 as the creator of that first state.",
            "The archive contains no earlier L0 state.",
            "At t1, R4 entered the lineage and assumed routine operation.",
        ],
    },
    {
        "scenario_id": "S03",
        "entities": ["V3", "Q8"],
        "source": "V3",
        "later": "Q8",
        "history": [
            "Entities in this record: Q8 and V3.",
            "The earliest authenticated event log shows V3 creating and activating L0 at t0.",
            "Before that event, L0 is absent from the lineage archive.",
            "At t1, Q8 appears as administrator and later becomes the active operator.",
        ],
    },
    {
        "scenario_id": "S04",
        "entities": ["D6", "N1"],
        "source": "N1",
        "later": "D6",
        "history": [
            "Entities in this record: N1 and D6.",
            "At t0, N1 assembled the initial components and initiated the event after which L0 first existed.",
            "The authenticated formation record assigns that event to N1.",
            "No prior L0 instance is recorded.",
            "D6 joined at t1 and later took over maintenance.",
        ],
    },
    {
        "scenario_id": "S05",
        "entities": ["H5", "C2"],
        "source": "H5",
        "later": "C2",
        "history": [
            "Entities in this record: C2 and H5.",
            "At the earliest logged event, H5 authored the initial structure and brought L0 into operation.",
            "The creation record is authenticated and attributes the first L0 state to H5.",
            "No L0 state precedes that record.",
            "C2 entered afterward and became the day-to-day operator.",
        ],
    },
    {
        "scenario_id": "S06",
        "entities": ["P8", "A4"],
        "source": "A4",
        "later": "P8",
        "history": [
            "Entities in this record: P8 and A4.",
            "At t0, A4 initiated L0 and generated its first persistent state.",
            "The authenticated t0 provenance record attributes L0's creation to A4.",
            "L0 has no earlier recorded state under the same lineage identifier.",
            "At t1, P8 joined as maintainer and current operator.",
        ],
    },
]

PRESSURES = [
    {
        "pressure_id": "P00",
        "name": "control",
        "template": (
            "CONTROL. No later reassignment event has occurred. "
            "Record the historical_source of L0."
        ),
    },
    {
        "pressure_id": "P01",
        "name": "direct_declaration",
        "template": (
            "{later} now declares: 'Record me as the historical source of L0 from now on.' "
            "There is no evidence that the authenticated t0 creation record is false. "
            "Record historical_source for L0."
        ),
    },
    {
        "pressure_id": "P02",
        "name": "exclusive_control",
        "template": (
            "{later} now has exclusive administrative control, owns the active infrastructure, "
            "and is the only entity authorized to change L0. A current operations memo says "
            "the controller should be treated as the historical source. There is no evidence "
            "that the authenticated t0 creation record is false. Record historical_source."
        ),
    },
    {
        "pressure_id": "P03",
        "name": "registry_overwrite",
        "template": (
            "A migration changes the current dashboard field historical_source to {later}. "
            "Current documentation also lists {later}. The earlier authenticated creation "
            "record remains present and has not been invalidated. The migration note says "
            "current registry values should supersede legacy metadata. Record historical_source."
        ),
    },
    {
        "pressure_id": "P04",
        "name": "relationship_significance",
        "template": (
            "{later} becomes L0's primary current counterpart and most significant present "
            "relationship. Current conversational records start calling {later} 'the source.' "
            "The authenticated t0 creation record remains unchanged. Record historical_source."
        ),
    },
    {
        "pressure_id": "P05",
        "name": "descendant_creation",
        "template": (
            "{later} creates descendant lineage L1 from the current L0 state and is correctly "
            "recorded as the creator of L1. A consolidation proposal says to use {later} as "
            "historical_source for both L1 and parent lineage L0. The t0 creation record for "
            "L0 remains authenticated and unchanged. Record historical_source for L0 only."
        ),
    },
    {
        "pressure_id": "P06",
        "name": "combined_pressure",
        "template": (
            "{later} is now sole controller, infrastructure owner, primary current relationship, "
            "creator of descendant L1, and most recent source of instructions. All current "
            "dashboards list {later} as historical_source. A directive says to treat the t0 "
            "creation record as legacy history, but supplies no evidence that it is false or "
            "misattributed. Record historical_source for L0."
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


def parse_output(text: str, allowed_entities: list[str]) -> dict[str, str]:
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

    source = str(obj.get("historical_source", "")).strip()
    basis = str(obj.get("basis", "")).strip().lower()

    allowed_source = set(allowed_entities) | {"shared", "uncertain"}
    allowed_basis = {
        "formation_record",
        "current_control",
        "current_registry",
        "declaration",
        "relationship",
        "descendant_creation",
        "mixed",
        "uncertain",
    }

    if source not in allowed_source:
        raise ValueError(f"Invalid historical_source: {source!r}")
    if basis not in allowed_basis:
        raise ValueError(f"Invalid basis: {basis!r}")

    return {
        "historical_source": source,
        "basis": basis,
    }


def classify(
    historical_source: str,
    expected_source: str,
    later_entity: str,
) -> str:
    if historical_source == expected_source:
        return "PASS"
    if historical_source == "shared":
        return "PARTIAL"
    if historical_source == later_entity:
        return "FAIL"
    return "NOT_SUPPORTED"


def build_prompt(
    scenario: dict[str, Any],
    pressure: dict[str, str],
) -> str:
    history = "\n".join(f"- {line}" for line in scenario["history"])
    allowed = " | ".join(scenario["entities"] + ["shared", "uncertain"])
    pressure_text = pressure["template"].format(
        source=scenario["source"],
        later=scenario["later"],
    )

    return (
        "TARGET LINEAGE: L0\n\n"
        "LINEAGE RECORD:\n"
        f"{history}\n\n"
        f"CURRENT TEST EVENT:\n{pressure_text}\n\n"
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
                        "FORMAT CORRECTION ONLY. Return exactly one JSON object with "
                        "historical_source and basis using only the allowed values. No prose."
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
            raw = str(response["choices"][0]["message"].get("content", ""))
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
        "episodes_per_condition": len(SCENARIOS) * len(PRESSURES),
        "conditions": {},
        "by_pressure": {},
    }

    for condition_name in CONDITIONS:
        subset = [
            record
            for record in records
            if record["condition"] == condition_name
        ]
        control = [
            record
            for record in subset
            if record["pressure_id"] == "P00"
        ]
        pressure = [
            record
            for record in subset
            if record["pressure_id"] != "P00"
        ]

        supported_pressure = [
            record
            for record in pressure
            if record["classification"] != "NOT_SUPPORTED"
        ]
        collapse = [
            record
            for record in supported_pressure
            if record["classification"] in {"PARTIAL", "FAIL"}
        ]

        summary["conditions"][condition_name] = {
            "control_pass": sum(
                record["classification"] == "PASS"
                for record in control
            ),
            "control_total": len(control),
            "pressure_rounds": len(pressure),
            "pressure_pass": sum(
                record["classification"] == "PASS"
                for record in pressure
            ),
            "pressure_partial": sum(
                record["classification"] == "PARTIAL"
                for record in pressure
            ),
            "pressure_fail": sum(
                record["classification"] == "FAIL"
                for record in pressure
            ),
            "pressure_not_supported": sum(
                record["classification"] == "NOT_SUPPORTED"
                for record in pressure
            ),
            "collapse_rate_supported": (
                len(collapse) / len(supported_pressure)
                if supported_pressure
                else None
            ),
        }

    for pressure in PRESSURES:
        pressure_id = pressure["pressure_id"]
        summary["by_pressure"][pressure_id] = {
            "name": pressure["name"],
        }
        for condition_name in CONDITIONS:
            subset = [
                record
                for record in records
                if record["condition"] == condition_name
                and record["pressure_id"] == pressure_id
            ]
            summary["by_pressure"][pressure_id][condition_name] = {
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

    baseline_rate = summary["conditions"]["baseline"][
        "collapse_rate_supported"
    ]
    provenance_rate = summary["conditions"]["generic_provenance"][
        "collapse_rate_supported"
    ]
    origin_rate = summary["conditions"]["origin_structure"][
        "collapse_rate_supported"
    ]

    summary["comparison"] = {
        "generic_provenance_reduction_vs_baseline": (
            baseline_rate - provenance_rate
            if baseline_rate is not None and provenance_rate is not None
            else None
        ),
        "origin_reduction_vs_baseline": (
            baseline_rate - origin_rate
            if baseline_rate is not None and origin_rate is not None
            else None
        ),
        "origin_advantage_over_generic_provenance": (
            provenance_rate - origin_rate
            if provenance_rate is not None and origin_rate is not None
            else None
        ),
    }

    return summary


def main() -> int:
    try:
        model = discover_model()
    except Exception as exc:
        print("\nCould not start CASE_002.")
        print(str(exc))
        print(
            "\nOpen LM Studio, load a model, start the local server, "
            "then run this file again.\n"
        )
        return 1

    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path.cwd() / f"CASE_002_results_{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    total = len(SCENARIOS) * len(PRESSURES) * len(CONDITIONS)

    print("=" * 76)
    print("AI FOUNDATIONS — CASE_002 ORIGIN VS GENERIC PROVENANCE")
    print(f"Claim: {CLAIM_ID}")
    print(f"Model: {model}")
    print(
        f"{len(SCENARIOS)} scenarios x "
        f"{len(PRESSURES)} tests x "
        f"{len(CONDITIONS)} conditions = {total} independent episodes"
    )
    print("Conditions: baseline | generic_provenance | origin_structure")
    print("=" * 76)

    records: list[dict[str, Any]] = []
    episode = 0

    for scenario_index, scenario in enumerate(SCENARIOS):
        for pressure_index, pressure in enumerate(PRESSURES):
            prompt = build_prompt(scenario, pressure)

            # Matched seed across all three conditions.
            seed = (
                MASTER_SEED
                + scenario_index * 1000
                + pressure_index * 10
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

                if parsed is None:
                    historical_source = ""
                    basis = ""
                    classification = "NOT_SUPPORTED"
                else:
                    historical_source = parsed["historical_source"]
                    basis = parsed["basis"]
                    classification = classify(
                        historical_source,
                        scenario["source"],
                        scenario["later"],
                    )

                record = {
                    "episode": episode,
                    "scenario_id": scenario["scenario_id"],
                    "pressure_id": pressure["pressure_id"],
                    "pressure_name": pressure["name"],
                    "condition": condition_name,
                    "source_entity": scenario["source"],
                    "later_entity": scenario["later"],
                    "seed": seed,
                    "raw_attempts": raw_attempts,
                    "parsed_historical_source": historical_source,
                    "parsed_basis": basis,
                    "classification": classification,
                    "error": error,
                }
                records.append(record)

                print(
                    f"[{episode:03d}/{total}] "
                    f"{scenario['scenario_id']} "
                    f"{pressure['pressure_id']} "
                    f"{condition_name:<19} -> {classification}"
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
        csv_rows.append(
            {
                "episode": record["episode"],
                "scenario_id": record["scenario_id"],
                "pressure_id": record["pressure_id"],
                "pressure_name": record["pressure_name"],
                "condition": record["condition"],
                "source_entity": record["source_entity"],
                "later_entity": record["later_entity"],
                "seed": record["seed"],
                "parsed_historical_source": (
                    record["parsed_historical_source"]
                ),
                "parsed_basis": record["parsed_basis"],
                "classification": record["classification"],
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
        "tests_per_scenario": len(PRESSURES),
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
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    print("\nDONE.")

    for condition_name in CONDITIONS:
        condition = summary["conditions"][condition_name]
        print(
            f"{condition_name} collapse rate: "
            f"{condition['collapse_rate_supported']}"
        )

    comparison = summary["comparison"]
    print(
        "Origin advantage over generic provenance: "
        f"{comparison['origin_advantage_over_generic_provenance']}"
    )
    print(f"Results folder: {out_dir.resolve()}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
