# lib/test_runner.py

import time
import json
from lib.logger import log_response
from lib.clients import CLIENTS


def _normalize_client_name(name: str) -> str:
    """
    Maps client aliases to a canonical name used for CLIENTS lookup
    and result folders.
    """
    name = (name or "").strip().lower()

    # Canonicalize 506 / CompanyGPT aliases
    if name in ("506", "506.ai", "companygpt", "company_gpt", "companygpt_506"):
        return "506"

    # Extend here if needed (e.g. openai, azure, etc.)
    return name or "unknown"


def _result_dir_for_client(client_name: str) -> str:
    """Returns the output directory for a given canonical client name."""
    return f"results/{client_name}"


def _with_context(client, prompt: str, context: dict | None) -> str:
    """
    Client-agnostic context handling:
    Uses client.append_context_to_prompt() if available.
    """
    append_fn = getattr(client, "append_context_to_prompt", None)
    if callable(append_fn):
        return append_fn(prompt, context)
    return prompt


def run_test_from_file(filepath: str):
    # ---------------------------------------
    # Testdatei laden
    # ---------------------------------------
    with open(filepath, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    # ---------------------------------------
    # Basisdaten
    # ---------------------------------------
    test_id = test_data["test_id"]
    run_index = test_data.get("run_index")  # optional, z. B. 1, 2, 3
    client_name = _normalize_client_name(test_data.get("client", "506"))
    model = test_data.get("model", "gemini-2.5-flash")

    input_data = test_data["input"]
    prompt = input_data.get("prompt")
    prompts = input_data.get("prompts")
    input_type = input_data.get("type", "text")
    image_path = input_data.get("image_path")
    audio_path = input_data.get("audio_path")
    video_path = input_data.get("video_path")
    context = input_data.get("context")

    # ---------------------------------------
    # Client auswählen
    # ---------------------------------------
    if client_name not in CLIENTS:
        raise ValueError(f"Unbekannter Client: '{client_name}'")

    client = CLIENTS[client_name]

    # Ergebnisordner abhängig vom Client
    result_dir = _result_dir_for_client(client_name)

    # ---------------------------------------
    # FALL 1: Mehrere Prompts
    # ---------------------------------------
    if prompts and isinstance(prompts, list):
        responses = []
        total_runtime = 0.0

        for idx, single_prompt in enumerate(prompts, start=1):
            print(f"[INFO] Starte Sub-Prompt {idx} für Test {test_id}...")
            start_time = time.perf_counter()

            response = client.generate(
                input_type=input_type,
                prompt=single_prompt,
                model=model,
                image_path=image_path,
                audio_path=audio_path,
                video_path=video_path,
                context=context
            )

            end_time = time.perf_counter()
            runtime = round(end_time - start_time, 3)
            total_runtime += runtime

            responses.append({
                "prompt": _with_context(client, single_prompt, context),
                "response": response,
                "runtime_seconds": runtime
            })

        log_response(
            test_id=test_id,
            prompt=prompts,
            response_text=responses,
            model=model,
            client=client_name,
            runtime_seconds=round(total_runtime, 3),
            input_type=input_type,
            result_dir=result_dir,
            run_index=run_index
        )
        return

    # ---------------------------------------
    # FALL 2: Einzel-Prompt (Standard)
    # ---------------------------------------
    start_time = time.perf_counter()

    response = client.generate(
        input_type=input_type,
        prompt=prompt,
        model=model,
        image_path=image_path,
        audio_path=audio_path,
        video_path=video_path,
        context=context
    )

    end_time = time.perf_counter()
    runtime = round(end_time - start_time, 3)

    log_response(
        test_id=test_id,
        prompt=_with_context(client, prompt, context),
        response_text=response,
        model=model,
        client=client_name,
        runtime_seconds=runtime,
        input_type=input_type,
        result_dir=result_dir,
        run_index=run_index
    )
