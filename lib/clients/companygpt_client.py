# lib/clients/companygpt_client.py

import os
import json
import mimetypes
import hashlib
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# -------------------------------------------------
# Environment
# -------------------------------------------------
load_dotenv()

BASE_URL = os.getenv("COMPANYGPT_BASE_URL", "").rstrip("/")
ORG_ID = os.getenv("COMPANYGPT_ORG_ID")
API_KEY = os.getenv("COMPANYGPT_API_KEY")

DEFAULT_MODE = os.getenv("COMPANYGPT_DEFAULT_MODE", "BASIC")
INTERNAL_SYSTEM_PROMPT = os.getenv("COMPANYGPT_INTERNAL_SYSTEM_PROMPT", "true").lower() == "true"

# Media uploads (T02 image-only and later audio/video)
DATA_COLLECTION_ID = os.getenv("COMPANYGPT_DATA_COLLECTION_ID")

# Hash prefix length for upload filename (e.g., 12)
HASH_PREFIX_LEN = int(os.getenv("COMPANYGPT_HASH_PREFIX_LEN", "12"))

GENERATOR_ASSISTANT_ID = os.getenv("COMPANYGPT_GENERATOR_ASSISTANT_ID")
JUDGE_ASSISTANT_ID = os.getenv("COMPANYGPT_JUDGE_ASSISTANT_ID")

UPLOAD_TIMEOUT = 900  # 30s connect, 15min upload/read
CHAT_TIMEOUT = 900    # 30s connect, 15min processing/read

if not BASE_URL or not ORG_ID or not API_KEY:
    raise EnvironmentError("CompanyGPT .env Variablen fehlen oder sind unvollständig.")
if not DATA_COLLECTION_ID:
    raise EnvironmentError("COMPANYGPT_DATA_COLLECTION_ID ist nicht gesetzt (benötigt für Media-Tests).")

HEADERS_AUTH = {
    "api-organization-id": ORG_ID,
    "api-key": API_KEY,
}

HEADERS_JSON = {
    **HEADERS_AUTH,
    "Content-Type": "application/json",
}

# -------------------------------------------------
# Simple in-memory upload cache:
# absolute_path -> uniqueTitle
# (persists only for this Python process)
# -------------------------------------------------
_UPLOAD_CACHE: dict[str, str] = {}


# -------------------------------------------------
# Kontext (identisch zu Gemini)
# -------------------------------------------------
def append_context_to_prompt(prompt: str, context: dict | None) -> str:
    if not context:
        return prompt

    parts = []

    loc = context.get("location")
    if isinstance(loc, dict) and "lat" in loc and "lon" in loc:
        parts.append(f"Standort: ({loc['lat']}, {loc['lon']})")

    if "timestamp" in context:
        parts.append(f"Zeit: {context['timestamp']}")

    if "device" in context:
        parts.append(f"Gerät: {context['device']}")

    if "network" in context:
        parts.append(f"Netzwerkstatus: {context['network']}")

    if parts:
        prompt += "\n[Kontext: " + "; ".join(parts) + "]"

    return prompt


# -------------------------------------------------
# Hash helpers
# -------------------------------------------------
def _sha256_hex(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _make_upload_filename(original_name: str, sha256_hex: str) -> str:
    """
    Pattern requested:
      <hash>_<origin_name>
    where <hash> is a prefix of the sha256 hex.
    """
    prefix = sha256_hex[:max(1, HASH_PREFIX_LEN)]
    # Avoid weird path separators in the name
    safe_name = original_name.replace("\\", "_").replace("/", "_")
    return f"{prefix}_{safe_name}"

def _wait_until_media_visible(model_id: str, unique_title: str, max_wait_seconds: int = 15) -> None:
    """
    Lightweight readiness check to avoid race conditions (e.g., upload accepted 202 but not indexed yet).
    We do a tiny chat call and see if the model still claims no media is visible.
    """
    delays = [2, 4, 8]  # total 14s
    start = time.time()

    probe_prompt = "Antworte nur mit: OK"

    for d in delays:
        try:
            out = _chat_no_stream(
                model_id=model_id,
                prompt=probe_prompt,
                temperature=0.0,
                selected_mode=DEFAULT_MODE,
                selected_files=[unique_title],
                selected_data_collections=[DATA_COLLECTION_ID]
            )
            # heuristic: if model can see media, it will usually not complain about missing media
            if out and "keine" not in out.lower() and "sichtbar" not in out.lower():
                return
        except Exception:
            pass

        if time.time() - start + d > max_wait_seconds:
            return
        time.sleep(d)

# -------------------------------------------------
# Media Upload
# -------------------------------------------------
def _upload_media(media_path: str, data_collection_id: str) -> str:
    """
    Uploads a file to a given data collection and returns uniqueTitle.

    Strategy:
      - compute sha256(content)
      - upload with filename: <hashprefix>_<originalname>
      - if 201: take uniqueTitle from response
      - if 409 (already exists): deterministically derive uniqueTitle:
            <dataCollectionId>_<upload_filename>
    """
    if not media_path:
        raise ValueError("media_path fehlt.")

    p = Path(media_path)
    if not p.is_file():
        raise FileNotFoundError(f"Datei nicht gefunden: {p}")

    abs_path = str(p.resolve())
    if abs_path in _UPLOAD_CACHE:
        return _UPLOAD_CACHE[abs_path]

    # hash + derived upload filename
    digest = _sha256_hex(p)
    upload_filename = _make_upload_filename(p.name, digest)

    mime, _ = mimetypes.guess_type(abs_path)
    if not mime:
        mime = "application/octet-stream"

    url = f"{BASE_URL}/api/v1/public/uploadMedia"
    params = {
        "dataCollectionId": data_collection_id,
        "replace": "false",
    }

    with p.open("rb") as f:
        # IMPORTANT: we override the filename sent to the API
        files = {"media": (upload_filename, f, mime)}
        r = requests.post(url, headers=HEADERS_AUTH, params=params, files=files, timeout=UPLOAD_TIMEOUT)

    # If backend says "already exists"
    if r.status_code == 409:
        unique_title = f"{data_collection_id}_{upload_filename}"
        _UPLOAD_CACHE[abs_path] = unique_title
        return unique_title

    if r.status_code >= 400:
        raise RuntimeError(f"uploadMedia failed: {r.status_code} {r.text}")

    data = r.json()

    # The API usually returns a list with one object
    file_obj = data[0] if isinstance(data, list) and data else (data if isinstance(data, dict) else {})
    api_unique = file_obj.get("uniqueTitle")
    file_status = file_obj.get("status")  # e.g., 201, 202, 409

    # If uniqueTitle is missing (observed for audio with status=202), derive it deterministically
    unique_title = api_unique or f"{data_collection_id}_{upload_filename}"

    _UPLOAD_CACHE[abs_path] = unique_title
    return unique_title


# -------------------------------------------------
# Core API Call (no streaming)
# -------------------------------------------------
def _chat_no_stream(
    model_id: str,
    prompt: str,
    temperature: float = 0.2,
    selected_mode: str = "BASIC",
    selected_files: list[str] | None = None,
    selected_data_collections: list[str] | None = None,
    assistant_id: str | None = None,
    internal_system_prompt_override: bool | None = None,
) -> str:
    url = f"{BASE_URL}/api/v1/public/chatNoStream"

    use_internal = INTERNAL_SYSTEM_PROMPT if internal_system_prompt_override is None else internal_system_prompt_override
    params = {
        "internalSystemPrompt": "true" if use_internal else "false"
    }

    payload = {
        "model": {"id": model_id},
        "messages": [{"role": "user", "content": prompt, "references": [], "sources": []}],
        "roleId": "",
        "temperature": temperature,
        "selectedMode": selected_mode,
        "selectedFiles": selected_files or [],
        "selectedDataCollections": selected_data_collections or []
    }

    if assistant_id:                               
        payload["selectedAssistantId"] = assistant_id

    response = requests.post(url, headers=HEADERS_JSON, params=params, data=json.dumps(payload), timeout=CHAT_TIMEOUT)
    response.raise_for_status()
    return response.json().get("content", "")

# -------------------------------------------------
# Public API – kompatibel mit test_runner
# -------------------------------------------------
def generate(
    input_type: str,
    prompt: str,
    model: str,
    image_path: str = None,
    audio_path: str = None,
    video_path: str = None,
    context: dict = None,
    temperature: float = 0.2,
    selected_mode: str | None = None,
    internal_system_prompt: bool | None = None,
) -> str:
    try:
        prompt_with_context = append_context_to_prompt(prompt, context)

        mode = selected_mode or DEFAULT_MODE

        # -------------------------
        # TEXT
        # -------------------------
        if input_type == "text":
            return _chat_no_stream(
                model_id=model,
                prompt=prompt_with_context,
                temperature=temperature,
                selected_mode=mode,
                selected_files=[],
                selected_data_collections=[],
                assistant_id=GENERATOR_ASSISTANT_ID,
                internal_system_prompt_override=internal_system_prompt,
            )

        # -------------------------
        # IMAGE
        # -------------------------
        if input_type == "image":
            if not image_path:
                return "[CompanyGPT] image_path fehlt."

            unique_title = _upload_media(image_path, DATA_COLLECTION_ID)
            _wait_until_media_visible(model, unique_title)

            return _chat_no_stream(
                model_id=model,
                prompt=prompt_with_context,
                temperature=temperature,
                selected_mode=mode,
                selected_files=[unique_title],
                selected_data_collections=[DATA_COLLECTION_ID],
                assistant_id=GENERATOR_ASSISTANT_ID,
                internal_system_prompt_override=internal_system_prompt,
            )

        # -------------------------
        # AUDIO
        # -------------------------
        if input_type == "audio":
            if not audio_path:
                return "[CompanyGPT] audio_path fehlt."

            unique_title = _upload_media(audio_path, DATA_COLLECTION_ID)
            _wait_until_media_visible(model, unique_title)

            return _chat_no_stream(
                model_id=model,
                prompt=prompt_with_context,
                temperature=temperature,
                selected_mode=mode,
                selected_files=[unique_title],
                selected_data_collections=[DATA_COLLECTION_ID],
                assistant_id=GENERATOR_ASSISTANT_ID,
                internal_system_prompt_override=internal_system_prompt,
            )

        return f"[CompanyGPT] Input-Typ '{input_type}' in Step 06 nicht unterstützt."

    except Exception as e:
        return f"[CompanyGPT ERROR] {e}"

def judge(
    prompt: str,
    model: str,
    temperature: float = 0.1,
    selected_mode: str | None = None,
    internal_system_prompt: bool | None = None,
) -> str:
    """
    Sends a prompt to the configured Judge Assistant.
    Returns raw text (should be JSON string).
    """
    try:
        mode = selected_mode or DEFAULT_MODE
        return _chat_no_stream(
            model_id=model,
            prompt=prompt,
            temperature=temperature,
            selected_mode=mode,
            selected_files=[],
            selected_data_collections=[],
            assistant_id=JUDGE_ASSISTANT_ID,
            internal_system_prompt_override=internal_system_prompt,
        )
    except Exception as e:
        return f"[CompanyGPT JUDGE ERROR] {e}"
