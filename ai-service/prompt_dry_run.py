import json
import time

import requests


BASE_URL = "http://localhost:8000"
FIVE_REAL_INPUTS = [
    "Vendor KYC evidence missing for two high-value suppliers.",
    "Privileged account review was not completed in Q1.",
    "PII export logs are retained for only 7 days.",
    "No documented approval for emergency production access.",
    "Disaster recovery drill not executed in the last 12 months.",
]


def post(endpoint: str, record: str):
    start = time.perf_counter()
    res = requests.post(f"{BASE_URL}{endpoint}", json={"record": record}, timeout=5)
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    return res.status_code, elapsed_ms, res.json()


if __name__ == "__main__":
    results = []
    for idx, record in enumerate(FIVE_REAL_INPUTS, start=1):
        row = {"input_index": idx, "record": record, "calls": {}}
        for endpoint in ["/describe", "/recommend", "/generate-report"]:
            status, elapsed_ms, payload = post(endpoint, record)
            row["calls"][endpoint] = {"status": status, "elapsed_ms": elapsed_ms, "payload": payload}
        results.append(row)
    print(json.dumps(results, indent=2))
