import hashlib
import json
from typing import Any, Optional

import redis


class CacheService:
    def __init__(self, redis_url: str):
        self._client = None
        if redis_url:
            try:
                self._client = redis.from_url(redis_url, decode_responses=True)
                self._client.ping()
            except Exception:
                self._client = None

    @property
    def enabled(self) -> bool:
        return self._client is not None

    def build_key(self, endpoint: str, payload: dict) -> str:
        normalized = json.dumps(payload, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
        digest = hashlib.sha256(f"{endpoint}:{normalized}".encode("utf-8")).hexdigest()
        return f"ai:{endpoint}:{digest}"

    def get_json(self, key: str) -> Optional[Any]:
        if not self._client:
            return None
        raw = self._client.get(key)
        if not raw:
            return None
        return json.loads(raw)

    def set_json(self, key: str, value: Any, ttl_seconds: int) -> None:
        if not self._client:
            return
        self._client.setex(key, ttl_seconds, json.dumps(value, ensure_ascii=True))
