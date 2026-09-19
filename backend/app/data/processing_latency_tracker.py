from time import time_ns


class ProcessingLatencyTracker:
    def __init__(self, clock=None):
        self.clock = clock or self._current_time_ms

    @staticmethod
    def _current_time_ms() -> int:
        return time_ns() // 1_000_000

    def track(self, started_timestamp: int) -> int:
        current_timestamp = self.clock()

        if started_timestamp > current_timestamp:
            raise ValueError("started_timestamp cannot be in the future")

        return current_timestamp - started_timestamp
