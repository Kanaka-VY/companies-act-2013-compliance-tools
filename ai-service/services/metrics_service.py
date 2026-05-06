import time
from threading import Lock


class MetricsService:
    def __init__(self):
        self._start_time = time.time()
        self._request_count = 0
        self._total_response_ms = 0.0
        self._lock = Lock()

    def record(self, response_ms: float) -> None:
        with self._lock:
            self._request_count += 1
            self._total_response_ms += response_ms

    def avg_response_ms(self) -> float:
        with self._lock:
            if self._request_count == 0:
                return 0.0
            return round(self._total_response_ms / self._request_count, 2)

    def uptime_seconds(self) -> int:
        return int(time.time() - self._start_time)
