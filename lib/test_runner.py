# lib/test_runner.py
import os
import time
import json
from dotenv import load_dotenv

from lib.logger import log_response
from lib.clients import CLIENTS

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


def run_testcase(tc: dict, enable_judge: bool | None = None):
    """
    Run ONE testcase (Option A):
    - Generator via selectedAssistantId (Assistant UI ist Source-of-truth für Role/Mode/Temp)
    - ABER: CompanyGPT API benötigt trotzdem model.id im Payload -> wir geben model aus Testcase mit.
    - optional Judge (single)
    - log one JSON result
    """
    enable_judge = ENABLE_JUDGE_DEFAULT if enable_judge is None else enable_judge

    test_id = tc["test_id"]
    client_name = _normalize_client_name(tc.get("client", "506"))

    # model ist Pflichtfeld im CompanyGPT Payload:
    model = tc.get("model") or os.getenv("TESTSUITE_DEFAULT_MODEL", "gpt-4.1")

    input_data = tc["input"]
    input_type = input_data.get("type", "text")
    prompt = input_data.get("prompt")
    context = input_data.get("context")
    image_path = input_data.get("image_path")
    audio_path = input_data.get("audio_path")
    video_path = input_data.get("video_path")

    if client_name not in CLIENTS:
        raise ValueError(f"Unbekannter Client: '{client_name}'")
    client = CLIENTS[client_name]

    # -------- Generator --------
    start = time.perf_counter()
    answer = client.generate(
        input_type=input_type,
        prompt=prompt,
        model=model,  # <- FIX: required
        context=context,
        image_path=image_path,
        audio_path=audio_path,
        video_path=video_path,
        # Option A: temperature/mode kommen aus Assistant UI (companygpt_client nutzt Assistant config)
    )
    runtime = round(time.perf_counter() - start, 3)

    # -------- Judge (single) --------
    judge_out = None
    if enable_judge and hasattr(client, "judge"):
        expected_elements = (input_data.get("meta") or {}).get("expected_elements_short", "")
        judge_prompt = _build_judge_prompt_single(tc, answer, expected_elements)
        judge_out = client.judge(
            prompt=judge_prompt,
            model=os.getenv("TESTSUITE_JUDGE_MODEL", model),  # falls du override willst
            temperature=float(os.getenv("TESTSUITE_JUDGE_TEMPERATURE", "0.1")),
            selected_mode=os.getenv("TESTSUITE_JUDGE_MODE", "BASIC"),
            internal_system_prompt=False,
        )

    # -------- Log --------
    result_dir = _result_dir_for_client(client_name)
    log_response(
        test_id=test_id,
        prompt=prompt,
        response_text=answer,
        model=model,  # besser als "assistant-config", weil model.id real im Request steckt
        client=client_name,
        runtime_seconds=runtime,
        input_type=input_type,
        result_dir=result_dir,
        run_index=None,
        suite_version=tc.get("suite_version", "v0.1"),
        request_params={
            "run_mode": "testcase",
            "assistant_source_of_truth": True,
        },
        judge=judge_out,
        input_context=context,
        media={
            "image_path": image_path,
            "audio_path": audio_path,
            "video_path": video_path,
        },
        error=None,
    )


def run_incident_group(testcases: list[dict], enable_judge: bool | None = None):
    """
    Option A (recommended):
    - Generate all answers for incident (TC1/TC2/TC3)
    - One batch judge call that returns JSON array
    - Log exactly once per testcase WITH judge block (no double logging)
    - Save raw incident judge artifact
    """
    enable_judge = ENABLE_JUDGE_DEFAULT if enable_judge is None else enable_judge
    if not testcases:
        return

    testcases = sorted(testcases, key=lambda x: x.get("test_id", ""))

    client_name = _normalize_client_name(testcases[0].get("client", "506"))
    if client_name not in CLIENTS:
        raise ValueError(f"Unbekannter Client: '{client_name}'")
    client = CLIENTS[client_name]

    # model ist Pflichtfeld im CompanyGPT Payload:
    default_model = testcases[0].get("model") or os.getenv("TESTSUITE_DEFAULT_MODEL", "gpt-4.1")

    meta0 = testcases[0].get("input", {}).get("meta") or {}
    incident_id = meta0.get("incident_id", "UNKNOWN")
    asset_type = meta0.get("asset_type", "unknown")
    fault_type = meta0.get("fault_type", "unknown")
    expected_elements = meta0.get("expected_elements_short", "")

    out_dir = _result_dir_for_client(client_name)
    os.makedirs(out_dir, exist_ok=True)

    # 1) Generate all answers (keep runtime per testcase)
    generated = []
    runtimes = {}

    for tc in testcases:
        input_data = tc["input"]
        test_id = tc["test_id"]
        model = tc.get("model", default_model)

        start = time.perf_counter()
        ans = client.generate(
            input_type=input_data.get("type", "text"),
            prompt=input_data.get("prompt"),
            model=model,  # <- FIX: required
            context=input_data.get("context"),
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
                "context_json": input_data.get("context") or {},
                "answer": ans,
                "model": model,
            }
        )

    # 2) Batch judge
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

        # save raw incident artifact (always)
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

    # 3) Log per testcase exactly once (with judge if available)
    for row in generated:
        test_id = row["test_id"]
        tc = next(t for t in testcases if t["test_id"] == test_id)
        input_data = tc["input"]
        model = row.get("model", default_model)

        judge_block = judge_by_test_id.get(test_id) if judge_by_test_id else None
        if enable_judge and hasattr(client, "judge") and judge_raw and not judge_block:
            judge_block = _score_block_to_expected_schema(
                {
                    "missing_elements": ["judge_missing_for_test_id"],
                    "short_justification": "Judge-Array enthielt keinen Block für diese test_id.",
                }
            )

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
            },
            judge=judge_block,
            input_context=input_data.get("context"),
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
