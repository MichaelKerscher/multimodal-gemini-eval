# lib/logger.py

import os
import json
from datetime import datetime

def log_response(test_id, prompt, response_text, model, client, runtime_seconds=None, input_type="text", result_dir="results"):
    os.makedirs(result_dir, exist_ok=True)

    log_data = {
        "test_id": test_id,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "model": model,
        "client": client,
        "input": {
            "type": input_type,
            "prompt": prompt
        },
        "response": {
            "text": response_text,
            "tokens": len(response_text.split())
        },
        "meta": {
            "status": "success",
            "runtime_seconds": runtime_seconds if runtime_seconds is not None else -1
        }
    }

    filename = f"{test_id}_{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.json"
    filepath = os.path.join(result_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    print(f"[LOG] Ergebnis gespeichert unter: {filepath}")
