import os
import json
import mimetypes
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()


BASE_URL = os.getenv("COMPANYGPT_BASE_URL", "https://companygpt.506.ai:3003").rstrip("/")
ORG_ID = os.getenv("COMPANYGPT_ORG_ID")
API_KEY = os.getenv("COMPANYGPT_API_KEY")

if not ORG_ID or not API_KEY:
    raise SystemExit("Missing COMPANYGPT_ORG_ID or COMPANYGPT_API_KEY in environment/.env")

HEADERS = {
    "api-organization-id": ORG_ID,
    "api-key": API_KEY,
}

# Datastorage/DataCollection aus der URL:
DATA_COLLECTION_ID = "f9807daa-9c43-4a51-a7c8-17ae454beeef"

MODEL_ID = "gemini-2.5-flash"
PROMPT = "Was ist auf diesem Bild zu sehen? Bitte beschreibe die Szene und relevante Details."


def upload_media(image_path: str, data_collection_id: str) -> str:
    """
    Uploads an image via 506 uploadMedia endpoint and returns uniqueTitle.
    """
    img = Path(image_path)
    if not img.exists():
        raise FileNotFoundError(f"Image not found: {img}")

    mime, _ = mimetypes.guess_type(str(img))
    if not mime:
        mime = "application/octet-stream"

    url = f"{BASE_URL}/api/v1/public/uploadMedia"
    params = {
        "dataCollectionId": data_collection_id,
        "replace": "false",
    }

    with img.open("rb") as f:
        files = {
            "media": (img.name, f, mime),
        }
        r = requests.post(url, headers=HEADERS, params=params, files=files, timeout=120)

    if r.status_code >= 400:
        raise RuntimeError(f"uploadMedia failed: {r.status_code} {r.text}")

    data = r.json()
    if isinstance(data, list) and data:
        unique_title = data[0].get("uniqueTitle")
    else:
        unique_title = data.get("uniqueTitle")

    if not unique_title:
        raise RuntimeError(f"uploadMedia response did not contain uniqueTitle: {data}")

    return unique_title


def chat_no_stream(model_id: str, prompt: str, selected_files: list[str]) -> dict:
    """
    Calls chatNoStream with selectedFiles.
    """
    url = f"{BASE_URL}/api/v1/public/chatNoStream"
    params = {
        "internalSystemPrompt": "true",
    }

    payload = {
        "model": {"id": model_id},
        "messages": [{
            "role": "user",
            "content": prompt,
            "references": [],
            "sources": [],
        }],
        "roleId": "",
        "temperature": 0.2,
        "selectedMode": "BASIC",
        "selectedFiles": selected_files,
        "selectedDataCollections": [],
    }

    r = requests.post(url, headers={**HEADERS, "Content-Type": "application/json"}, params=params, data=json.dumps(payload), timeout=120)
    if r.status_code >= 400:
        raise RuntimeError(f"chatNoStream failed: {r.status_code} {r.text}")

    return r.json()


def main():
    
    image_path = os.getenv("T02_IMAGE_PATH", r"data\transformator.jpg")

    print(f"[INFO] Uploading: {image_path}")
    unique_title = upload_media(image_path, DATA_COLLECTION_ID)
    print(f"[INFO] uniqueTitle: {unique_title}")

    print("[INFO] Calling chatNoStream...")
    res = chat_no_stream(MODEL_ID, PROMPT, [unique_title])

    content = res.get("content", "")
    print("\n===== MODEL OUTPUT =====\n")
    print(content)


if __name__ == "__main__":
    main()
