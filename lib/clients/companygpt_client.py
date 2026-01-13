# lib/clients/companygpt_client.py

import os
import json
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

if not BASE_URL or not ORG_ID or not API_KEY:
    raise EnvironmentError("CompanyGPT .env Variablen fehlen oder sind unvollständig.")

HEADERS = {
    "Content-Type": "application/json",
    "api-organization-id": ORG_ID,
    "api-key": API_KEY,
}

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
# Core API Call (no streaming)
# -------------------------------------------------
def _chat_no_stream(
    model_id: str,
    prompt: str,
    temperature: float = 0.2,
    selected_mode: str = "BASIC"
) -> str:
    url = f"{BASE_URL}/api/v1/public/chatNoStream"
    params = {
        "internalSystemPrompt": "true" if INTERNAL_SYSTEM_PROMPT else "false"
    }

    payload = {
        "model": { "id": model_id },
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "references": [],
                "sources": []
            }
        ],
        "roleId": "",
        "temperature": temperature,
        "selectedMode": selected_mode,
        "selectedFiles": [],
        "selectedDataCollections": []
    }

    response = requests.post(
        url,
        headers=HEADERS,
        params=params,
        data=json.dumps(payload),
        timeout=60
    )

    response.raise_for_status()
    result = response.json()

    return result.get("content", "")


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
    context: dict = None
) -> str:

    if input_type != "text":
        return f"[CompanyGPT] Input-Typ '{input_type}' in Step 06 nicht unterstützt."

    prompt_with_context = append_context_to_prompt(prompt, context)

    try:
        return _chat_no_stream(
            model_id=model,
            prompt=prompt_with_context,
            temperature=0.2,
            selected_mode=DEFAULT_MODE
        )
    except Exception as e:
        return f"[CompanyGPT ERROR] {e}"
