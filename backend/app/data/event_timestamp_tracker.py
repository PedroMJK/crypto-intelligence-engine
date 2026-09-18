from time import time_ns


class EventTimestampTracker:
    def __init__(self, clock=None):
        self.clock = clock or self._current_time_ms

    @staticmethod
    def _current_time_ms() -> int:
        return time_ns() // 1_000_000

    def track(self, message: dict) -> dict:
        return {
            "event_timestamp": message["E"],
            "received_timestamp": self.clock(),
        }