# lib/logger.py
import os
import json
import ast
from datetime import datetime

def write_manifest(out_dir: str, test_data: dict, resolved: dict):
    """
    Creates/updates manifest.json under the per-test output dir.
    """
    os.makedirs(out_dir, exist_ok=True)
    manifest_path = os.path.join(out_dir, "manifest.json")

    manifest = {
        "suite_version": "v0.1",
        "test_id": test_data.get("test_id"),
        "source_testfile": test_data.get("_source_file", None),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "resolved": resolved,
        "test_definition": test_data
    }

    # If manifest exists: keep created_at from first creation
    if os.path.isfile(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                old = json.load(f)
            if isinstance(old, dict) and "created_at" in old:
                manifest["created_at"] = old["created_at"]
        except:
            pass

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"[MANIFEST] geschrieben: {manifest_path}")


def log_response(
    out_dir: str,
    test_id: str,
    prompt,
    response_text,
    model: str,
    client: str,
    runtime_seconds=None,
    input_type="text",
    run_index: int | None = None,
    context: dict | None = None,
    request_params: dict | None = None,
    media: dict | None = None,
    error: dict | None = None
):
    os.makedirs(out_dir, exist_ok=True)

    # Multi-Prompt
    if isinstance(response_text, list):
        responses = []
        for idx, r in enumerate(response_text, start=1):
            if isinstance(r, dict):
                block = r
            else:
                try:
                    block = ast.literal_eval(r)
                    if not isinstance(block, dict):
                        block = {"prompt": "", "response": str(r)}
                except:
                    block = {"prompt": "", "response": str(r)}

            prompt_txt = block.get("prompt", "")
            resp_txt = block.get("response", "")
            responses.append({
                "prompt_index": idx,
                "prompt": prompt_txt,
                "response": resp_txt,
                "runtime_seconds": block.get("runtime_seconds"),
                "tokens_estimate_words": len(str(resp_txt).split())
            })
        response_data = {"multi": True, "items": responses}
    else:
        resp_text = str(response_text)
        response_data = {
            "multi": False,
            "text": resp_text,
            "tokens_estimate_words": len(resp_text.split())
        }

    log_data = {
        "suite_version": "v0.1",
        "test_id": test_id,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "client": client,
        "model": model,
        "input": {
            "type": input_type,
            "prompt": prompt,
            "context": context or {}
        },
        "request_params": request_params or {},
        "media": media or {},
        "response": response_data,
        "meta": {
            "status": "error" if error else "success",
            "runtime_seconds": runtime_seconds if runtime_seconds is not None else -1
        },
        "error": error or {}
    }

    filename = f"run_{run_index:02d}.json" if run_index is not None else "run.json"
    filepath = os.path.join(out_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

    print(f"[LOG] Ergebnis gespeichert unter: {filepath}")
