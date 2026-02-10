# lib/test_loader.py
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import csv


def _safe_json_loads(s: str) -> Any:
    if s is None:
        return None
    s = str(s).strip()
    if not s:
        return None
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        # if user puts invalid JSON, keep as raw string so it can be debugged
        return {"_raw": s, "_error": "invalid_json"}


def load_testcases(path: str) -> List[Dict[str, Any]]:
    """
    Loads JSON (single testcase spec) or CSV (multiple rows) and returns
    a list of canonical test_data dicts that match your runner's expectations.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Testfile nicht gefunden: {p}")

    suffix = p.suffix.lower()
    if suffix == ".json":
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        # Normalize into list
        data["_source_file"] = str(p)
        return [data]

    if suffix == ".csv":
        return load_testcases_from_csv(str(p))

    raise ValueError(f"Nicht unterstützter Dateityp: {suffix}. Erlaubt: .json, .csv")


def load_testcases_from_csv(path: str) -> List[Dict[str, Any]]:
    """
    CSV → list of canonical testcases.

    Expected minimal columns (based on your lamp_testcases_v01.csv):
      - testcase_id
      - user_message
      - context_json (JSON string or empty)

    Optional columns supported:
      - client, model, run_index, input_type
      - image_path, audio_path, video_path
      - temperature, selected_mode, internal_system_prompt
      - incident_id, context_level (kept as metadata)
    """
    out: List[Dict[str, Any]] = []

    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row_i, row in enumerate(reader, start=1):
            testcase_id = (row.get("testcase_id") or "").strip()
            if not testcase_id:
                raise ValueError(f"CSV Zeile {row_i}: testcase_id fehlt.")

            user_message = (row.get("user_message") or "").strip()
            if not user_message:
                raise ValueError(f"CSV Zeile {row_i} ({testcase_id}): user_message fehlt.")

            context_json = _safe_json_loads(row.get("context_json", "")) or {}
            if not isinstance(context_json, dict):
                # allow context_json to be list/etc but runner expects dict => wrap
                context_json = {"_value": context_json}

            # Keep CSV metadata for later analysis (incident_id, context_level etc.)
            csv_meta = {
                "incident_id": (row.get("incident_id") or "").strip(),
                "context_level": (row.get("context_level") or "").strip(),
                "csv_row": row_i,
            }

            condition_id = (row.get("context_level") or "").strip() or "unknown"

            # Canonical test_data for your runner
            test_data = {
                "test_id": testcase_id,
                "condition_id": condition_id,
                "_source_file": path,
                "client": (row.get("client") or "506").strip(),
                "model": (row.get("model") or "gpt-4.1").strip(),  # set your 506 default here
                "run_index": int((row.get("run_index") or "1").strip()),
                "temperature": float((row.get("temperature") or "0.2").strip()),
                "selected_mode": (row.get("selected_mode") or "BASIC").strip(),
                "internal_system_prompt": (row.get("internal_system_prompt") or "true").strip().lower() == "true",
                "input": {
                    "type": (row.get("input_type") or "text").strip(),
                    "prompt": user_message,
                    # map context_json into the same place your runner already expects
                    "context": context_json,
                    # optional media paths
                    "image_path": (row.get("image_path") or "").strip() or None,
                    "audio_path": (row.get("audio_path") or "").strip() or None,
                    "video_path": (row.get("video_path") or "").strip() or None,
                    # extra meta for later aggregation / analysis
                    "meta": csv_meta,
                },
            }

            out.append(test_data)

    return out
