from backend.app.data.event_timestamp_tracker import EventTimestampTracker


def test_track_returns_event_timestamp():
    tracker = EventTimestampTracker()

    message = {
        "e": "aggTrade",
        "E": 1789725600123,
        "s": "BTCUSDT",
    }

    timestamps = tracker.track(message)

    assert timestamps["event_timestamp"] == 1789725600123


def test_track_returns_received_timestamp():
    tracker = EventTimestampTracker(
        clock=lambda: 1789725600456,
    )

    message = {
        "e": "aggTrade",
        "E": 1789725600123,
        "s": "BTCUSDT",
    }

    timestamps = tracker.track(message)

    assert timestamps["received_timestamp"] == 1789725600456


def test_track_returns_received_timestamp_with_default_clock():
    tracker = EventTimestampTracker()

    message = {
        "e": "aggTrade",
        "E": 1789725600123,
        "s": "BTCUSDT",
    }

    timestamps = tracker.track(message)

    assert "received_timestamp" in timestamps
    assert isinstance(timestamps["received_timestamp"], int)
