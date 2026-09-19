import pytest

from backend.app.data.processing_latency_tracker import ProcessingLatencyTracker


def test_track_returns_processing_latency_in_milliseconds():
    tracker = ProcessingLatencyTracker(
        clock=lambda: 1789725600456,
    )

    latency = tracker.track(
        started_timestamp=1789725600123,
    )

    assert latency == 333


def test_track_returns_integer_with_default_clock():
    tracker = ProcessingLatencyTracker()

    latency = tracker.track(
        started_timestamp=0,
    )

    assert isinstance(latency, int)
    assert latency >= 0


def test_track_rejects_started_timestamp_in_the_future():
    tracker = ProcessingLatencyTracker(
        clock=lambda: 1789725600123,
    )

    with pytest.raises(
        ValueError,
        match="started_timestamp cannot be in the future",
    ):
        tracker.track(
            started_timestamp=1789725600456,
        )


def test_track_returns_zero_when_timestamps_are_equal():
    tracker = ProcessingLatencyTracker(
        clock=lambda: 1789725600123,
    )

    latency = tracker.track(
        started_timestamp=1789725600123,
    )

    assert latency == 0
