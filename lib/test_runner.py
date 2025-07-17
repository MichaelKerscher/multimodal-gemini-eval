# lib/test_runner.py

import time
import json
from lib.logger import log_response
from lib.clients import CLIENTS

def run_test_from_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    test_id = test_data["test_id"]
    client_name = test_data.get("client", "gemini").lower()
    model = test_data.get("model", "gemini-2.5-flash")
    input_data = test_data["input"]
    prompt = input_data.get("prompt")
    input_type = input_data.get("type", "text")
    image_path = input_data.get("image_path", None)
    file_path = input_data.get("file", None)

    if client_name not in CLIENTS:
        raise ValueError(f"Unbekannter Client: '{client_name}'")

    client = CLIENTS[client_name]

    start_time = time.perf_counter()
    response = client.generate(input_type=input_type, prompt=prompt, model=model, image_path=image_path, file_path=file_path)
    end_time = time.perf_counter()
    runtime = round(end_time - start_time, 3)

    log_response(test_id, prompt, response, model, client_name, runtime_seconds=runtime, input_type=input_type)
