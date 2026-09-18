from backend.app.data.out_of_order_event_detector import OutOfOrderEventDetector


def test_first_event_is_not_out_of_order():
    detector = OutOfOrderEventDetector()

    message = {
        "e": "aggTrade",
        "E": 1789725600123,
        "s": "BTCUSDT",
    }

    is_out_of_order = detector.is_out_of_order(message)

    assert is_out_of_order is False


def test_newer_event_is_not_out_of_order():
    detector = OutOfOrderEventDetector()

    first_message = {
        "e": "aggTrade",
        "E": 1789725600123,
        "s": "BTCUSDT",
    }

    second_message = {
        "e": "aggTrade",
        "E": 1789725600124,
        "s": "BTCUSDT",
    }

    detector.is_out_of_order(first_message)
    is_out_of_order = detector.is_out_of_order(second_message)

    assert is_out_of_order is False


def test_older_event_is_out_of_order():
    detector = OutOfOrderEventDetector()

    first_message = {
        "e": "aggTrade",
        "E": 1789725600124,
        "s": "BTCUSDT",
    }

    second_message = {
        "e": "aggTrade",
        "E": 1789725600123,
        "s": "BTCUSDT",
    }

    detector.is_out_of_order(first_message)
    is_out_of_order = detector.is_out_of_order(second_message)

    assert is_out_of_order is True


def test_different_symbols_have_independent_event_order():
    detector = OutOfOrderEventDetector()

    btc_message = {
        "e": "aggTrade",
        "E": 1789725600200,
        "s": "BTCUSDT",
    }

    eth_message = {
        "e": "aggTrade",
        "E": 1789725600100,
        "s": "ETHUSDT",
    }

    detector.is_out_of_order(btc_message)
    is_out_of_order = detector.is_out_of_order(eth_message)

    assert is_out_of_order is False


def test_different_event_types_have_independent_event_order():
    detector = OutOfOrderEventDetector()

    trade_message = {
        "e": "aggTrade",
        "E": 1789725600200,
        "s": "BTCUSDT",
    }

    candle_message = {
        "e": "kline",
        "E": 1789725600100,
        "s": "BTCUSDT",
    }

    detector.is_out_of_order(trade_message)
    is_out_of_order = detector.is_out_of_order(candle_message)

    assert is_out_of_order is False


def test_out_of_order_event_does_not_move_latest_timestamp_backwards():
    detector = OutOfOrderEventDetector()

    latest_message = {
        "e": "aggTrade",
        "E": 1789725600300,
        "s": "BTCUSDT",
    }

    oldest_message = {
        "e": "aggTrade",
        "E": 1789725600100,
        "s": "BTCUSDT",
    }

    intermediate_message = {
        "e": "aggTrade",
        "E": 1789725600200,
        "s": "BTCUSDT",
    }

    detector.is_out_of_order(latest_message)
    detector.is_out_of_order(oldest_message)
    is_out_of_order = detector.is_out_of_order(intermediate_message)

    assert is_out_of_order is True


def test_equal_timestamp_is_not_out_of_order():
    detector = OutOfOrderEventDetector()

    first_message = {
        "e": "aggTrade",
        "E": 1789725600123,
        "s": "BTCUSDT",
    }

    second_message = {
        "e": "aggTrade",
        "E": 1789725600123,
        "s": "BTCUSDT",
    }

    detector.is_out_of_order(first_message)
    is_out_of_order = detector.is_out_of_order(second_message)

    assert is_out_of_order is False
