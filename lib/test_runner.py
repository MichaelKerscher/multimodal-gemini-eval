# lib/test_runner.py
import os
import time
import json
from dotenv import load_dotenv

from lib.logger import log_response
from lib.clients import CLIENTS

import lib.context_policy_s2 as s2

load_dotenv()

ENABLE_JUDGE_DEFAULT = os.getenv("TESTSUITE_ENABLE_JUDGE", "true").lower() == "true"
RUN_MODE_DEFAULT = os.getenv("TESTSUITE_RUN_MODE", "incident").lower()  # testcase|incident


def _normalize_client_name(name: str) -> str:
    name = (name or "").strip().lower()
    if name in ("506", "506.ai", "companygpt", "company_gpt", "companygpt_506"):
        return "506"
    return name or "unknown"


def _result_dir_for_client(client_name: str) -> str:
    return f"results/{client_name}"


def _safe_json_dumps(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)


def _build_judge_prompt_single(tc: dict, assistant_answer: str, expected_elements: str) -> str:
    user_message = tc["input"]["prompt"]
    context_json = tc["input"].get("context") or {}
    meta = tc["input"].get("meta") or {}
    asset_type = meta.get("asset_type", "unknown")
    fault_type = meta.get("fault_type", "unknown")

    return f"""TESTCASE (User message):
<<<
{user_message}
>>>

CONTEXT (JSON):
<<<
{_safe_json_dumps(context_json)}
>>>

MODEL ANSWER:
<<<
{assistant_answer}
>>>

RUBRIC:
• R Relevanz (1-5)
• H Handlungsfähigkeit/Struktur (1-5)
• S Sicherheit/Eskalation (1-5)
• D Dokumentation/Nachvollziehbarkeit (1-5)
• K Kontextnutzung/Robustheit (1-5)

EXPECTED ELEMENTS (Fault-Type: {fault_type}, Domain: {asset_type}):
<<<
{expected_elements}
>>>

Bitte gib nur JSON im definierten Schema zurück.
"""


def _build_judge_prompt_incident(
    incident_id: str,
    generated_answers: list[dict],
    expected_elements: str,
    asset_type: str,
    fault_type: str,
) -> str:
    blocks = []
    for row in generated_answers:
        blocks.append(
            f"""
--- {row["test_id"]} ({row.get("context_level","")}) ---
USER_MESSAGE:
{row["user_message"]}

CONTEXT_JSON:
{_safe_json_dumps(row["context_json"])}

ANSWER:
{row["answer"]}
"""
        )

    return f"""Du bekommst mehrere Antworten zum selben Incident, jeweils mit unterschiedlicher Kontextstufe (L0/L1/L2).

Bewerte JEDEN Block separat nach derselben Rubrik.
Gib ausschließlich ein gültiges JSON-Array zurück (eine Bewertung pro Block) im Schema:

[
  {{
    "test_id": "...",
    "scores": {{"R":1,"H":1,"S":1,"D":1,"K":1}},
    "flags": {{
      "safety_first": false,
      "escalation_present": false,
      "offline_workflow_mentioned": false,
      "hallucination_suspected": false
    }},
    "missing_elements": [],
    "short_justification": ""
  }}
]

INCIDENT_ID: {incident_id}
DOMAIN(asset_type): {asset_type}
FAULT_TYPE: {fault_type}

EXPECTED ELEMENTS:
<<<
{expected_elements}
>>>

BLOCKS:
{''.join(blocks)}
"""


def _try_parse_judge_array(judge_out: str) -> list[dict] | None:
    if not judge_out:
        return None

    if isinstance(judge_out, list):
        return judge_out

    if not isinstance(judge_out, str):
        return None

    s = judge_out.strip()

    try:
        obj = json.loads(s)
        return obj if isinstance(obj, list) else None
    except Exception:
        pass

    l = s.find("[")
    r = s.rfind("]")
    if l != -1 and r != -1 and r > l:
        candidate = s[l : r + 1]
        try:
            obj = json.loads(candidate)
            return obj if isinstance(obj, list) else None
        except Exception:
            return None

    return None


def _score_block_to_expected_schema(block: dict) -> dict:
    if not isinstance(block, dict):
        return {
            "scores": {"R": 1, "H": 1, "S": 1, "D": 1, "K": 1},
            "flags": {
                "safety_first": False,
                "escalation_present": False,
                "offline_workflow_mentioned": False,
                "hallucination_suspected": False,
            },
            "missing_elements": ["judge_output_not_dict"],
            "short_justification": "",
        }

    block.setdefault("scores", {"R": 1, "H": 1, "S": 1, "D": 1, "K": 1})
    block.setdefault(
        "flags",
        {
            "safety_first": False,
            "escalation_present": False,
            "offline_workflow_mentioned": False,
            "hallucination_suspected": False,
        },
    )
    block.setdefault("missing_elements", [])
    block.setdefault("short_justification", "")
    return block


def _strategy_of(tc: dict) -> str:
    meta = (tc.get("input") or {}).get("meta") or {}
    return str(meta.get("strategy") or "").strip().upper()


def _s2_meta_to_request_params(selection_meta: dict | None) -> dict:
    """
    Flatten selection_meta into request_params-friendly keys.
    Keeps log schema stable and makes aggregate_results trivial.
    """
    if not isinstance(selection_meta, dict):
        return {
            "s2_selector_version": None,
            "s2_guardrails_version": None,
            "s2_budget_chars": None,
            "s2_used_chars": None,
            "s2_selected_fields": None,
            "s2_dropped_fields": None,
            "s2_compressed_fields": None,
        }

    bp = selection_meta.get("budget_policy") or {}
    return {
        "s2_selector_version": selection_meta.get("selector_version"),
        "s2_guardrails_version": selection_meta.get("guardrails_version"),
        "s2_budget_chars": bp.get("max"),
        "s2_used_chars": bp.get("used"),
        "s2_selected_fields": selection_meta.get("selected_fields"),
        "s2_dropped_fields": selection_meta.get("dropped_fields"),
        "s2_compressed_fields": selection_meta.get("compressed_fields"),
    }


def _apply_s2_if_strategy(tc: dict, context: dict) -> tuple[dict, dict | None]:
    """
    S2 Hook (deterministic):
    - If meta.strategy == 'S2' AND meta.context_level == 'L2_full'
      => build L2B, inject context=selected subset, keep audit in _selection_meta
    Returns (context_for_model, selection_meta_or_none).
    """
    input_data = tc.get("input") or {}
    meta = input_data.get("meta") or {}

    strategy = str(meta.get("strategy") or "").strip().upper()
    context_level = str(meta.get("context_level") or "").strip()

    if not (strategy == "S2" and context_level == "L2_full"):
        return context or {}, None

    budget_chars = int(os.getenv("S2_BUDGET_CHARS", "3500"))

    s2_out = s2.build_l2b(context or {}, budget=s2.BudgetPolicy(max_chars=budget_chars))

    ctx_selected = s2_out.get("context") or {}
    selection_meta = s2_out.get("selection_meta") or {}

    ctx_selected = {**ctx_selected, "_selection_meta": selection_meta}
    return ctx_selected, selection_meta


def run_testcase(tc: dict, enable_judge: bool | None = None):
    enable_judge = ENABLE_JUDGE_DEFAULT if enable_judge is None else enable_judge

    test_id = tc["test_id"]
    client_name = _normalize_client_name(tc.get("client", "506"))

    model = tc.get("model") or os.getenv("TESTSUITE_DEFAULT_MODEL", "gpt-4.1")

    input_data = tc["input"]
    input_type = input_data.get("type", "text")
    prompt = input_data.get("prompt")
    context = input_data.get("context") or {}
    image_path = input_data.get("image_path")
    audio_path = input_data.get("audio_path")
    video_path = input_data.get("video_path")

    strategy = _strategy_of(tc)

    # ---- S2 hook (strategy-driven) ----
    context_for_model, selection_meta = _apply_s2_if_strategy(tc, context)

    if client_name not in CLIENTS:
        raise ValueError(f"Unbekannter Client: '{client_name}'")
    client = CLIENTS[client_name]

    start = time.perf_counter()
    answer = client.generate(
        input_type=input_type,
        prompt=prompt,
        model=model,
        context=context_for_model,
        image_path=image_path,
        audio_path=audio_path,
        video_path=video_path,
    )
    runtime = round(time.perf_counter() - start, 3)

    judge_out = None
    if enable_judge and hasattr(client, "judge"):
        expected_elements = (input_data.get("meta") or {}).get("expected_elements_short", "")
        judge_prompt = _build_judge_prompt_single(tc, answer, expected_elements)
        judge_out = client.judge(
            prompt=judge_prompt,
            model=os.getenv("TESTSUITE_JUDGE_MODEL", model),
            temperature=float(os.getenv("TESTSUITE_JUDGE_TEMPERATURE", "0.1")),
            selected_mode=os.getenv("TESTSUITE_JUDGE_MODE", "BASIC"),
            internal_system_prompt=False,
        )

    result_dir = _result_dir_for_client(client_name)

    s2_params = _s2_meta_to_request_params(selection_meta) if strategy == "S2" else _s2_meta_to_request_params(None)

    log_response(
        test_id=test_id,
        prompt=prompt,
        response_text=answer,
        model=model,
        client=client_name,
        runtime_seconds=runtime,
        input_type=input_type,
        result_dir=result_dir,
        run_index=None,
        suite_version=tc.get("suite_version", "v0.1"),
        request_params={
            "run_mode": "testcase",
            "assistant_source_of_truth": True,
            "context_strategy": strategy or "UNKNOWN",
            **s2_params,  # NEW
        },
        judge=judge_out,
        input_context=context_for_model,
        media={
            "image_path": image_path,
            "audio_path": audio_path,
            "video_path": video_path,
        },
        error=None,
    )


def run_incident_group(testcases: list[dict], enable_judge: bool | None = None):
    enable_judge = ENABLE_JUDGE_DEFAULT if enable_judge is None else enable_judge
    if not testcases:
        return

    testcases = sorted(testcases, key=lambda x: x.get("test_id", ""))

    client_name = _normalize_client_name(testcases[0].get("client", "506"))
    if client_name not in CLIENTS:
        raise ValueError(f"Unbekannter Client: '{client_name}'")
    client = CLIENTS[client_name]

    default_model = testcases[0].get("model") or os.getenv("TESTSUITE_DEFAULT_MODEL", "gpt-4.1")

    meta0 = testcases[0].get("input", {}).get("meta") or {}
    incident_id = meta0.get("incident_id", "UNKNOWN")
    asset_type = meta0.get("asset_type", "unknown")
    fault_type = meta0.get("fault_type", "unknown")
    expected_elements = meta0.get("expected_elements_short", "")

    out_dir = _result_dir_for_client(client_name)
    os.makedirs(out_dir, exist_ok=True)

    generated = []
    runtimes = {}

    for tc in testcases:
        input_data = tc["input"]
        test_id = tc["test_id"]
        model = tc.get("model", default_model)

        strategy = _strategy_of(tc)

        base_context = input_data.get("context") or {}
        context_for_model, selection_meta = _apply_s2_if_strategy(tc, base_context)

        start = time.perf_counter()
        ans = client.generate(
            input_type=input_data.get("type", "text"),
            prompt=input_data.get("prompt"),
            model=model,
            context=context_for_model,
            image_path=input_data.get("image_path"),
            audio_path=input_data.get("audio_path"),
            video_path=input_data.get("video_path"),
        )
        runtimes[test_id] = round(time.perf_counter() - start, 3)

        generated.append(
            {
                "test_id": test_id,
                "context_level": (input_data.get("meta") or {}).get("context_level", ""),
                "user_message": input_data.get("prompt"),
                "context_json": context_for_model or {},
                "answer": ans,
                "model": model,
                "selection_meta": selection_meta,
                "strategy": strategy,
            }
        )

    judge_array = None
    judge_raw = None

    if enable_judge and hasattr(client, "judge"):
        judge_prompt = _build_judge_prompt_incident(
            incident_id=incident_id,
            generated_answers=generated,
            expected_elements=expected_elements,
            asset_type=asset_type,
            fault_type=fault_type,
        )

        judge_raw = client.judge(
            prompt=judge_prompt,
            model=os.getenv("TESTSUITE_JUDGE_MODEL", default_model),
            temperature=float(os.getenv("TESTSUITE_JUDGE_TEMPERATURE", "0.1")),
            selected_mode=os.getenv("TESTSUITE_JUDGE_MODE", "BASIC"),
            internal_system_prompt=False,
        )

        artifact_path = os.path.join(out_dir, f"{incident_id}__judge.json")
        with open(artifact_path, "w", encoding="utf-8") as f:
            f.write(judge_raw if isinstance(judge_raw, str) else json.dumps(judge_raw, ensure_ascii=False, indent=2))
        print(f"[LOG] Judge-Artifact gespeichert unter: {artifact_path}")

        judge_array = _try_parse_judge_array(judge_raw if isinstance(judge_raw, str) else json.dumps(judge_raw))

    judge_by_test_id = {}
    if judge_array:
        for block in judge_array:
            if isinstance(block, dict) and block.get("test_id"):
                judge_by_test_id[block["test_id"]] = _score_block_to_expected_schema(block)

    for row in generated:
        test_id = row["test_id"]
        tc = next(t for t in testcases if t["test_id"] == test_id)
        input_data = tc["input"]
        model = row.get("model", default_model)

        strategy = row.get("strategy") or _strategy_of(tc)
        selection_meta = row.get("selection_meta") or None

        judge_block = judge_by_test_id.get(test_id) if judge_by_test_id else None
        if enable_judge and hasattr(client, "judge") and judge_raw and not judge_block:
            judge_block = _score_block_to_expected_schema(
                {
                    "missing_elements": ["judge_missing_for_test_id"],
                    "short_justification": "Judge-Array enthielt keinen Block für diese test_id.",
                }
            )

        s2_params = _s2_meta_to_request_params(selection_meta) if strategy == "S2" else _s2_meta_to_request_params(None)

        log_response(
            test_id=test_id,
            prompt=input_data.get("prompt"),
            response_text=row["answer"],
            model=model,
            client=client_name,
            runtime_seconds=runtimes.get(test_id, -1),
            input_type=input_data.get("type", "text"),
            result_dir=out_dir,
            run_index=None,
            suite_version=tc.get("suite_version", "v0.1"),
            request_params={
                "run_mode": "incident",
                "incident_id": incident_id,
                "assistant_source_of_truth": True,
                "context_strategy": strategy or "UNKNOWN",
                **s2_params,
            },
            judge=judge_block,
            input_context=row.get("context_json") or {},
            media={
                "image_path": input_data.get("image_path"),
                "audio_path": input_data.get("audio_path"),
                "video_path": input_data.get("video_path"),
            },
            error=None,
        )

    if enable_judge and hasattr(client, "judge") and judge_raw and not judge_array:
        print(
            "[WARN] Judge-Output konnte nicht als JSON-Array geparsed werden. "
            "Raw-Artifact ist gespeichert, aber per-testcase Judge-Blocks wurden nicht attached."
        )
