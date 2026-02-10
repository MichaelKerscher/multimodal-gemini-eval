# lib/logger.py
import os
import json
import ast
from datetime import datetime
from typing import Any


def _safe_now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _next_run_index(out_dir: str) -> int:
    """
    If run_index is not provided, auto-increment:
      run_01.json, run_02.json, ...
    """
    if not os.path.isdir(out_dir):
        return 1

    max_idx = 0
    for fn in os.listdir(out_dir):
        if not fn.startswith("run_") or not fn.endswith(".json"):
            continue
        # run_01.json -> 01
        core = fn[len("run_") : -len(".json")]
        if core.isdigit():
            max_idx = max(max_idx, int(core))
    return max_idx + 1


def write_manifest(out_dir: str, test_data: dict, resolved: dict):
    """
    Creates/updates manifest.json under the per-test output dir.
    Keeps created_at from the first creation.
    """
    os.makedirs(out_dir, exist_ok=True)
    manifest_path = os.path.join(out_dir, "manifest.json")

    manifest = {
        "suite_version": resolved.get("suite_version", "v0.1"),
        "test_id": test_data.get("test_id"),
        "source_testfile": test_data.get("_source_file", None),
        "created_at": _safe_now(),
        "resolved": resolved,
        "test_definition": test_data,
    }

    if os.path.isfile(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                old = json.load(f)
            if isinstance(old, dict) and "created_at" in old:
                manifest["created_at"] = old["created_at"]
        except Exception:
            pass

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"[MANIFEST] geschrieben: {manifest_path}")


def log_response(
    test_id: str,
    prompt: str,
    response_text: Any,
    model: str,
    client: str,
    runtime_seconds: float | None = None,
    input_type: str = "text",
    result_dir: str = "results",
    run_index: int | None = None,
    suite_version: str = "v0.1",
    request_params: dict | None = None,
    judge: Any | None = None,
    input_context: dict | None = None,
    media: dict | None = None,
    error: dict | None = None,
    test_data: dict | None = None,
    resolved: dict | None = None,
):
    """
    Writes one run JSON into:
      {result_dir}/{test_id}/run_XX.json   (or run.json if you prefer fixed naming)

    If run_index is None -> auto index (run_01, run_02, ...)

    Optional:
      - test_data + resolved => also writes/updates manifest.json
    """
    out_dir = os.path.join(result_dir, test_id)
    os.makedirs(out_dir, exist_ok=True)

    # -------- response formatting --------
    if isinstance(response_text, list):
        items = []
        for idx, r in enumerate(response_text, start=1):
            if isinstance(r, dict):
                block = r
            else:
                try:
                    block = ast.literal_eval(str(r))
                    if not isinstance(block, dict):
                        block = {"prompt": "", "response": str(r)}
                except Exception:
                    block = {"prompt": "", "response": str(r)}

            prompt_txt = str(block.get("prompt", ""))
            resp_txt = str(block.get("response", ""))
            items.append(
                {
                    "prompt_index": idx,
                    "prompt": prompt_txt,
                    "response": resp_txt,
                    "runtime_seconds": block.get("runtime_seconds"),
                    "tokens_estimate_words": len(resp_txt.split()),
                }
            )
        response_data = {"multi": True, "items": items}
    else:
        resp_text = "" if response_text is None else str(response_text)
        response_data = {
            "multi": False,
            "text": resp_text,
            "tokens_estimate_words": len(resp_text.split()),
        }

    # -------- build log payload --------
    log_data = {
        "suite_version": suite_version,
        "test_id": test_id,
        "timestamp": _safe_now(),
        "client": client,
        "model": model,
        "input": {"type": input_type, "prompt": prompt, "context": input_context or {}},
        "request_params": request_params or {},
        "media": media or {},
        "response": response_data,
        "judge": judge,  # can be None, dict, string, etc.
        "meta": {
            "status": "error" if error else "success",
            "runtime_seconds": runtime_seconds if runtime_seconds is not None else -1,
        },
        "error": error or {},
    }

    # -------- filename selection --------
    if run_index is None:
        run_index = _next_run_index(out_dir)

    filename = f"run_{run_index:02d}.json"
    filepath = os.path.join(out_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

    # -------- manifest (optional) --------
    if test_data is not None and resolved is not None:
        resolved = dict(resolved)
        resolved["suite_version"] = suite_version
        write_manifest(out_dir, test_data=test_data, resolved=resolved)

    print(f"[LOG] Ergebnis gespeichert unter: {filepath}")
