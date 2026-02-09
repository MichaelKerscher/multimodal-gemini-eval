import os
import json
import time
import mimetypes
import hashlib
from pathlib import Path

import requests
from dotenv import load_dotenv

# ----------------------------
# Env
# ----------------------------
load_dotenv()

BASE_URL = os.getenv("COMPANYGPT_BASE_URL", "").rstrip("/")
ORG_ID = os.getenv("COMPANYGPT_ORG_ID")
API_KEY = os.getenv("COMPANYGPT_API_KEY")
DC_ID = os.getenv("COMPANYGPT_DATA_COLLECTION_ID")

MODEL_ID = os.getenv("COMPANYGPT_MODEL_ID", "gemini-2.5-flash")
DEFAULT_MODE = os.getenv("COMPANYGPT_DEFAULT_MODE", "BASIC")
INTERNAL_SYSTEM_PROMPT = os.getenv("COMPANYGPT_INTERNAL_SYSTEM_PROMPT", "true").lower() == "true"

HASH_PREFIX_LEN = int(os.getenv("COMPANYGPT_HASH_PREFIX_LEN", "12"))

# T09 defaults
VIDEO_PATH = os.getenv("T09_VIDEO_PATH", "data/strand.mp4")
PROMPT = os.getenv("T09_PROMPT", "Was passiert in diesem Video?")

if not BASE_URL or not ORG_ID or not API_KEY or not DC_ID:
    raise EnvironmentError(
        "Fehlende .env Variablen: COMPANYGPT_BASE_URL, COMPANYGPT_ORG_ID, COMPANYGPT_API_KEY, COMPANYGPT_DATA_COLLECTION_ID"
    )

HEADERS_AUTH = {
    "api-organization-id": ORG_ID,
    "api-key": API_KEY,
}
HEADERS_JSON = {
    **HEADERS_AUTH,
    "Content-Type": "application/json",
}

# 30s connect, lange read (Video upload / processing)
UPLOAD_TIMEOUT = 900
CHAT_TIMEOUT = 900

# ----------------------------
# Hash + upload name
# ----------------------------
def sha256_hex(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def make_upload_filename(original_name: str, digest: str) -> str:
    prefix = digest[:max(1, HASH_PREFIX_LEN)]
    safe = original_name.replace("\\", "_").replace("/", "_")
    return f"{prefix}_{safe}"

# ----------------------------
# uploadMedia
# ----------------------------
def upload_media(file_path: str) -> tuple[str, int]:
    p = Path(file_path)
    if not p.is_file():
        raise FileNotFoundError(f"Datei nicht gefunden: {p}")

    digest = sha256_hex(p)
    upload_filename = make_upload_filename(p.name, digest)

    mime, _ = mimetypes.guess_type(str(p))
    if not mime:
        mime = "application/octet-stream"

    url = f"{BASE_URL}/api/v1/public/uploadMedia"
    params = {"dataCollectionId": DC_ID, "replace": "false"}

    with p.open("rb") as f:
        files = {"media": (upload_filename, f, mime)}
        r = requests.post(url, headers=HEADERS_AUTH, params=params, files=files, timeout=UPLOAD_TIMEOUT)

    # 409 = already exists: uniqueTitle ist deterministisch
    if r.status_code == 409:
        unique_title = f"{DC_ID}_{upload_filename}"
        return unique_title, 409

    if r.status_code >= 400:
        raise RuntimeError(f"uploadMedia failed: {r.status_code} {r.text}")

    # 506 antwortet typischerweise: [{filename, uniqueTitle, createdAt, status}]
    data = r.json()
    obj = data[0] if isinstance(data, list) and data else {}
    unique_title = obj.get("uniqueTitle") or f"{DC_ID}_{upload_filename}"
    status = int(obj.get("status") or r.status_code)

    return unique_title, status

# ----------------------------
# chatNoStream
# ----------------------------
def chat_no_stream(prompt: str, unique_title: str) -> str:
    url = f"{BASE_URL}/api/v1/public/chatNoStream"
    params = {"internalSystemPrompt": "true" if INTERNAL_SYSTEM_PROMPT else "false"}

    payload = {
        "model": {"id": MODEL_ID},
        "messages": [
            {"role": "user", "content": prompt, "references": [], "sources": []}
        ],
        "roleId": "",
        "temperature": 0.2,
        "selectedMode": DEFAULT_MODE,
        "selectedFiles": [unique_title],
        "selectedDataCollections": [DC_ID],
    }

    r = requests.post(url, headers=HEADERS_JSON, params=params, data=json.dumps(payload), timeout=CHAT_TIMEOUT)
    r.raise_for_status()
    return (r.json() or {}).get("content", "")

# ----------------------------
# readiness retry
# ----------------------------
def wait_until_visible(unique_title: str, max_wait: int = 45) -> None:
    # falls 202 / Indexing Delay: wir probieren ein paar Mal mit kurzem Prompt
    delays = [2, 4, 8, 12, 15]  # total 41s
    probe = "Antworte nur mit: OK"

    start = time.time()
    for d in delays:
        try:
            out = chat_no_stream(probe, unique_title)
            # Heuristik: wenn es NICHT "kein video sichtbar" o.ä. sagt, nehmen wir es als bereit
            low = (out or "").lower()
            if out and ("sichtbar" not in low and "kann" not in low and "leider" not in low):
                return
        except Exception:
            pass

        if time.time() - start + d > max_wait:
            return
        time.sleep(d)

def main():
    p = Path(VIDEO_PATH)
    size_mb = p.stat().st_size / (1024 * 1024)

    print(f"[INFO] Uploading video ({size_mb:.2f} MB): {VIDEO_PATH}")
    unique_title, upload_status = upload_media(VIDEO_PATH)
    print(f"[INFO] uploadMedia status: {upload_status}")
    print(f"[INFO] uniqueTitle: {unique_title}")

    # Falls Verarbeitung verzögert ist, kurz warten
    wait_until_visible(unique_title, max_wait=45)

    print("[INFO] Calling chatNoStream...")

    out = chat_no_stream(PROMPT, unique_title)

    print("\n===== MODEL OUTPUT =====\n")
    print(out)

if __name__ == "__main__":
    main()
