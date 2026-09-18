from collections import deque
import json


class DuplicateEventDetector:
    def __init__(self, max_events: int = 1000):
        if max_events <= 0:
            raise ValueError("max_events must be greater than zero")

        self.max_events = max_events
        self.seen_events = set()
        self.event_history = deque()

    def is_duplicate(self, message: dict) -> bool:
        event_identity = json.dumps(
            message,
            sort_keys=True,
            separators=(",", ":"),
        )

        if event_identity in self.seen_events:
            return True

        if len(self.event_history) >= self.max_events:
            oldest_event = self.event_history.popleft()
            self.seen_events.remove(oldest_event)

        self.seen_events.add(event_identity)
        self.event_history.append(event_identity)

        return False