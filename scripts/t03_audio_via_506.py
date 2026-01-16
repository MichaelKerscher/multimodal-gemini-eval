import os
import json
import mimetypes
import hashlib
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("COMPANYGPT_BASE_URL", "https://companygpt.506.ai:3003").rstrip("/")
ORG_ID = os.getenv("COMPANYGPT_ORG_ID")
API_KEY = os.getenv("COMPANYGPT_API_KEY")
DATA_COLLECTION_ID = os.getenv("COMPANYGPT_DATA_COLLECTION_ID")

MODEL_ID = os.getenv("T03_MODEL_ID", "gemini-2.5-flash")
PROMPT = os.getenv("T03_PROMPT", "Um was geht es in der Audio?")
AUDIO_PATH = os.getenv("T03_AUDIO_PATH", r"data\unit_2.wav")

HASH_PREFIX_LEN = int(os.getenv("COMPANYGPT_HASH_PREFIX_LEN", "12"))

if not ORG_ID or not API_KEY or not DATA_COLLECTION_ID:
    raise SystemExit("Missing env: COMPANYGPT_ORG_ID / COMPANYGPT_API_KEY / COMPANYGPT_DATA_COLLECTION_ID")

HEADERS_AUTH = {
    "api-organization-id": ORG_ID,
    "api-key": API_KEY,
}


def make_session() -> requests.Session:
    """
    Robust session with retries for transient errors.
    Note: retries won't help a client-side write timeout, but helps 429/5xx.
    """
    s = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"],
        raise_on_status=False,
    )
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.mount("http://", HTTPAdapter(max_retries=retries))
    return s


def sha256_hex(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def upload_audio(session: requests.Session, audio_path: str) -> str:
    p = Path(audio_path)
    if not p.is_file():
        raise FileNotFoundError(f"Audio not found: {p}")

    digest = sha256_hex(p)
    upload_filename = f"{digest[:max(1, HASH_PREFIX_LEN)]}_{p.name}"

    mime, _ = mimetypes.guess_type(str(p))
    if not mime:
        mime = "application/octet-stream"

    url = f"{BASE_URL}/api/v1/public/uploadMedia"
    params = {"dataCollectionId": DATA_COLLECTION_ID, "replace": "false"}

    # IMPORTANT: No JSON content-type header for multipart
    # Use a long socket timeout; requests uses one timeout for connect/read (and upload can hit it).
    timeout = 900  # seconds

    print(f"[INFO] Uploading audio ({p.stat().st_size/1024/1024:.2f} MB) as: {upload_filename}")

    with p.open("rb") as f:
        files = {"media": (upload_filename, f, mime)}
        r = session.post(url, headers=HEADERS_AUTH, params=params, files=files, timeout=timeout)

    # Handle 409 reuse deterministically
    if r.status_code == 409:
        unique_title = f"{DATA_COLLECTION_ID}_{upload_filename}"
        print("[INFO] uploadMedia: 409 (already exists) -> reuse")
        return unique_title

    if r.status_code >= 400:
        raise RuntimeError(f"uploadMedia failed: {r.status_code} {r.text}")

    data = r.json()
    if isinstance(data, list) and data:
        unique_title = data[0].get("uniqueTitle")
        status = data[0].get("status")
    else:
        unique_title = data.get("uniqueTitle")
        status = data.get("status")

    print(f"[INFO] uploadMedia status: {status}")

    if not unique_title:
        # Fallback to deterministic pattern observed in your tenant
        unique_title = f"{DATA_COLLECTION_ID}_{upload_filename}"
        print("[WARN] uniqueTitle missing in response -> using derived uniqueTitle")

    return unique_title


def chat_no_stream(session: requests.Session, unique_title: str) -> str:
    url = f"{BASE_URL}/api/v1/public/chatNoStream"
    params = {"internalSystemPrompt": "true"}

    payload = {
        "model": {"id": MODEL_ID},
        "messages": [{
            "role": "user",
            "content": PROMPT,
            "references": [],
            "sources": []
        }],
        "roleId": "",
        "temperature": 0.2,
        "selectedMode": "BASIC",
        "selectedFiles": [unique_title],
        # Crucial for stability across runs:
        "selectedDataCollections": [DATA_COLLECTION_ID],
    }

    timeout = 900  # allow server-side processing/transcription
    r = session.post(
        url,
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        params=params,
        data=json.dumps(payload),
        timeout=timeout
    )

    if r.status_code >= 400:
        raise RuntimeError(f"chatNoStream failed: {r.status_code} {r.text}")

    data = r.json()
    return data.get("content", "")


def main():
    session = make_session()

    unique_title = upload_audio(session, AUDIO_PATH)
    print(f"[INFO] uniqueTitle: {unique_title}")

    print("[INFO] Calling chatNoStream...")
    out = chat_no_stream(session, unique_title)

    print("\n===== MODEL OUTPUT =====\n")
    print(out or "[EMPTY OUTPUT]")


if __name__ == "__main__":
    main()

