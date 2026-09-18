class OutOfOrderEventDetector:
    def __init__(self):
        self.latest_timestamps = {}

    def is_out_of_order(self, message: dict) -> bool:
        stream_identity = (message["e"], message["s"])
        event_timestamp = message["E"]

        latest_timestamp = self.latest_timestamps.get(stream_identity)

        if latest_timestamp is not None and event_timestamp < latest_timestamp:
            return True

        self.latest_timestamps[stream_identity] = event_timestamp

        return False