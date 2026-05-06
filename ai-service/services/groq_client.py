import json
from typing import Any, Dict

import requests


class GroqClient:
    def __init__(self, api_key: str, base_url: str, model: str, timeout_seconds: float):
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._timeout_seconds = timeout_seconds

    @property
    def model(self) -> str:
        return self._model

    def complete_json(self, prompt: str) -> Dict[str, Any]:
        if not self._api_key:
            raise RuntimeError("GROQ_API_KEY is missing")

        response = requests.post(
            f"{self._base_url}/chat/completions",
            timeout=self._timeout_seconds,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self._model,
                "temperature": 0.2,
                "max_tokens": 500,
                "response_format": {"type": "json_object"},
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a strict JSON generator. Output only valid JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
            },
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)
