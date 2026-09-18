import pytest

from backend.app.data.duplicate_event_detector import DuplicateEventDetector


def test_first_aggregate_trade_is_not_duplicate():
    detector = DuplicateEventDetector()

    message = {
        "e": "aggTrade",
        "E": 1789725600123,
        "s": "BTCUSDT",
        "a": 123456,
    }

    is_duplicate = detector.is_duplicate(message)

    assert is_duplicate is False


def test_repeated_aggregate_trade_is_duplicate():
    detector = DuplicateEventDetector()

    message = {
        "e": "aggTrade",
        "E": 1789725600123,
        "s": "BTCUSDT",
        "a": 123456,
    }

    detector.is_duplicate(message)
    is_duplicate = detector.is_duplicate(message)

    assert is_duplicate is True


def test_different_aggregate_trades_are_not_duplicates():
    detector = DuplicateEventDetector()

    first_message = {
        "e": "aggTrade",
        "E": 1789725600123,
        "s": "BTCUSDT",
        "a": 123456,
    }

    second_message = {
        "e": "aggTrade",
        "E": 1789725600123,
        "s": "BTCUSDT",
        "a": 123457,
    }

    detector.is_duplicate(first_message)
    is_duplicate = detector.is_duplicate(second_message)

    assert is_duplicate is False


def test_same_aggregate_trade_id_for_different_symbols_is_not_duplicate():
    detector = DuplicateEventDetector()

    first_message = {
        "e": "aggTrade",
        "E": 1789725600123,
        "s": "BTCUSDT",
        "a": 123456,
    }

    second_message = {
        "e": "aggTrade",
        "E": 1789725600124,
        "s": "ETHUSDT",
        "a": 123456,
    }

    detector.is_duplicate(first_message)
    is_duplicate = detector.is_duplicate(second_message)

    assert is_duplicate is False


def test_first_event_without_aggregate_trade_id_is_not_duplicate():
    detector = DuplicateEventDetector()

    message = {
        "e": "24hrMiniTicker",
        "E": 1789725600123,
        "s": "BTCUSDT",
        "c": "65000.00",
    }

    is_duplicate = detector.is_duplicate(message)

    assert is_duplicate is False


def test_same_event_with_different_key_order_is_duplicate():
    detector = DuplicateEventDetector()

    first_message = {
        "e": "aggTrade",
        "E": 1789725600123,
        "s": "BTCUSDT",
        "a": 123456,
    }

    second_message = {
        "a": 123456,
        "s": "BTCUSDT",
        "E": 1789725600123,
        "e": "aggTrade",
    }

    detector.is_duplicate(first_message)
    is_duplicate = detector.is_duplicate(second_message)

    assert is_duplicate is True


def test_old_event_is_forgotten_when_history_limit_is_reached():
    detector = DuplicateEventDetector(max_events=2)

    first_message = {
        "e": "aggTrade",
        "s": "BTCUSDT",
        "a": 123456,
    }

    second_message = {
        "e": "aggTrade",
        "s": "BTCUSDT",
        "a": 123457,
    }

    third_message = {
        "e": "aggTrade",
        "s": "BTCUSDT",
        "a": 123458,
    }

    detector.is_duplicate(first_message)
    detector.is_duplicate(second_message)
    detector.is_duplicate(third_message)

    is_duplicate = detector.is_duplicate(first_message)

    assert is_duplicate is False


def test_rejects_non_positive_history_limit():
    with pytest.raises(
        ValueError,
        match="max_events must be greater than zero",
    ):
        DuplicateEventDetector(max_events=0)
