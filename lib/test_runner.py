# lib/test_runner.py
import time
import json
import os
from lib.logger import log_response, write_manifest
from lib.clients import CLIENTS


def _normalize_client_name(name: str) -> str:
    name = (name or "").strip().lower()
    if name in ("506", "506.ai", "companygpt", "company_gpt", "companygpt_506"):
        return "506"
    return name or "unknown"


def _result_root() -> str:
    return "results_v0.1"


def _test_dir(client_name: str, test_id: str, condition_id: str | None) -> str:
    cond = condition_id or "no_condition"
    return os.path.join(_result_root(), client_name, test_id, cond)


def _with_context(client, prompt: str, context: dict | None) -> str:
    append_fn = getattr(client, "append_context_to_prompt", None)
    if callable(append_fn):
        return append_fn(prompt, context)
    return prompt


def run_testcase(test_data: dict):
    """
    Runs a single canonical testcase dict (from JSON or CSV loader).
    """
    test_id = test_data["test_id"]
    runs = int(test_data.get("run_index") or 1)
    if runs < 1:
        runs = 1

    client_name = _normalize_client_name(test_data.get("client", "506"))
    model = test_data.get("model", "gpt-4.1")

    temperature = float(test_data.get("temperature", 0.2))
    selected_mode = test_data.get("selected_mode", None)  # may be used by client later
    internal_system_prompt = test_data.get("internal_system_prompt", None)

    input_data = test_data["input"]
    prompt = input_data.get("prompt")
    prompts = input_data.get("prompts")
    input_type = input_data.get("type", "text")
    image_path = input_data.get("image_path")
    audio_path = input_data.get("audio_path")
    video_path = input_data.get("video_path")
    context = input_data.get("context")

    if client_name not in CLIENTS:
        raise ValueError(f"Unbekannter Client: '{client_name}'")
    client = CLIENTS[client_name]

    condition_id = test_data.get("condition_id")
    out_dir = _test_dir(client_name, test_id, condition_id)
    os.makedirs(out_dir, exist_ok=True)

    write_manifest(
        out_dir=out_dir,
        test_data=test_data,
        resolved={
            "client": client_name,
            "model": model,
            "runs": runs,
            "input_type": input_type,
            "temperature": temperature,
            "selected_mode": selected_mode,
            "internal_system_prompt": internal_system_prompt,
        }
    )

    # Multi-prompt
    if prompts and isinstance(prompts, list):
        for run_i in range(1, runs + 1):
            responses = []
            total_runtime = 0.0

            for idx, single_prompt in enumerate(prompts, start=1):
                print(f"[INFO] Test {test_id} — Run {run_i}/{runs} — Sub-Prompt {idx}...")
                start_time = time.perf_counter()

                response = client.generate(
                    input_type=input_type,
                    prompt=prompt,
                    model=model,
                    image_path=image_path,
                    audio_path=audio_path,
                    video_path=video_path,
                    context=context,
                    temperature=temperature,
                    selected_mode=selected_mode,
                    internal_system_prompt=internal_system_prompt
                )

                runtime = round(time.perf_counter() - start_time, 3)
                total_runtime += runtime

                responses.append({
                    "prompt": _with_context(client, single_prompt, context),
                    "response": response,
                    "runtime_seconds": runtime
                })

            log_response(
                out_dir=out_dir,
                test_id=test_id,
                prompt=prompts,
                response_text=responses,
                model=model,
                client=client_name,
                runtime_seconds=round(total_runtime, 3),
                input_type=input_type,
                run_index=run_i,
                context=context,
                request_params={
                    "temperature": temperature,
                    "selected_mode": selected_mode,
                    "internal_system_prompt": internal_system_prompt,
                }
            )
        return

    # Single prompt
    for run_i in range(1, runs + 1):
        print(f"[INFO] Test {test_id} — Run {run_i}/{runs}...")
        start_time = time.perf_counter()

        response = client.generate(
            input_type=input_type,
            prompt=prompt,
            model=model,
            image_path=image_path,
            audio_path=audio_path,
            video_path=video_path,
            context=context,
            temperature=temperature,
            selected_mode=selected_mode,
            internal_system_prompt=internal_system_prompt
        )

        runtime = round(time.perf_counter() - start_time, 3)

        log_response(
            out_dir=out_dir,
            test_id=test_id,
            prompt=_with_context(client, prompt, context),
            response_text=response,
            model=model,
            client=client_name,
            runtime_seconds=runtime,
            input_type=input_type,
            run_index=run_i,
            context=context,
            request_params={
                "temperature": temperature,
                "selected_mode": selected_mode,
                "internal_system_prompt": internal_system_prompt,
            }
        )


def run_test_from_file(filepath: str):
    """
    Backwards-compatible: loads a single JSON file (old behavior).
    If you want, we can delete this later once everything uses load_testcases.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        test_data = json.load(f)
    test_data["_source_file"] = filepath
    # normalize legacy key if needed
    if "test_id" in test_data and "testcase_id" not in test_data:
        pass
    run_testcase(test_data)
