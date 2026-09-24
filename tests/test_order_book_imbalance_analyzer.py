import pytest

from backend.app.analysis.order_book_imbalance_analyzer import (
    OrderBookImbalanceAnalyzer,
)


def test_order_book_imbalance_detects_bid_dominance():
    analyzer = OrderBookImbalanceAnalyzer()

    result = analyzer.analyze(
        bids=[
            (100.0, 6.0),
            (99.0, 4.0),
        ],
        asks=[
            (101.0, 3.0),
            (102.0, 2.0),
        ],
        depth=2,
    )

    assert result == {
        "bid_volume": pytest.approx(10.0),
        "ask_volume": pytest.approx(5.0),
        "total_volume": pytest.approx(15.0),
        "imbalance": pytest.approx(1.0 / 3.0),
        "state": "bid_dominant",
    }


def test_order_book_imbalance_detects_ask_dominance():
    analyzer = OrderBookImbalanceAnalyzer()

    result = analyzer.analyze(
        bids=[
            (100.0, 2.0),
            (99.0, 3.0),
        ],
        asks=[
            (101.0, 6.0),
            (102.0, 4.0),
        ],
        depth=2,
    )

    assert result == {
        "bid_volume": pytest.approx(5.0),
        "ask_volume": pytest.approx(10.0),
        "total_volume": pytest.approx(15.0),
        "imbalance": pytest.approx(-1.0 / 3.0),
        "state": "ask_dominant",
    }


def test_order_book_imbalance_detects_balanced_book():
    analyzer = OrderBookImbalanceAnalyzer()

    result = analyzer.analyze(
        bids=[
            (100.0, 4.0),
            (99.0, 6.0),
        ],
        asks=[
            (101.0, 5.0),
            (102.0, 5.0),
        ],
        depth=2,
    )

    assert result == {
        "bid_volume": pytest.approx(10.0),
        "ask_volume": pytest.approx(10.0),
        "total_volume": pytest.approx(20.0),
        "imbalance": pytest.approx(0.0),
        "state": "balanced",
    }


def test_order_book_imbalance_uses_only_requested_depth():
    analyzer = OrderBookImbalanceAnalyzer()

    result = analyzer.analyze(
        bids=[
            (100.0, 4.0),
            (99.0, 6.0),
            (98.0, 1000.0),
        ],
        asks=[
            (101.0, 2.0),
            (102.0, 3.0),
            (103.0, 1000.0),
        ],
        depth=2,
    )

    assert result == {
        "bid_volume": pytest.approx(10.0),
        "ask_volume": pytest.approx(5.0),
        "total_volume": pytest.approx(15.0),
        "imbalance": pytest.approx(1.0 / 3.0),
        "state": "bid_dominant",
    }


def test_order_book_imbalance_supports_depth_of_one():
    analyzer = OrderBookImbalanceAnalyzer()

    result = analyzer.analyze(
        bids=[
            (100.0, 8.0),
            (99.0, 100.0),
        ],
        asks=[
            (101.0, 2.0),
            (102.0, 100.0),
        ],
        depth=1,
    )

    assert result == {
        "bid_volume": pytest.approx(8.0),
        "ask_volume": pytest.approx(2.0),
        "total_volume": pytest.approx(10.0),
        "imbalance": pytest.approx(0.6),
        "state": "bid_dominant",
    }


def test_order_book_imbalance_does_not_modify_order_book():
    analyzer = OrderBookImbalanceAnalyzer()

    bids = [
        (100.0, 6.0),
        (99.0, 4.0),
    ]
    asks = [
        (101.0, 3.0),
        (102.0, 2.0),
    ]

    expected_bids = bids.copy()
    expected_asks = asks.copy()

    analyzer.analyze(
        bids=bids,
        asks=asks,
        depth=2,
    )

    assert bids == expected_bids
    assert asks == expected_asks


def test_order_book_imbalance_rejects_zero_depth():
    analyzer = OrderBookImbalanceAnalyzer()

    with pytest.raises(
        ValueError,
        match="depth must be greater than zero",
    ):
        analyzer.analyze(
            bids=[(100.0, 5.0)],
            asks=[(101.0, 5.0)],
            depth=0,
        )


def test_order_book_imbalance_rejects_negative_depth():
    analyzer = OrderBookImbalanceAnalyzer()

    with pytest.raises(
        ValueError,
        match="depth must be greater than zero",
    ):
        analyzer.analyze(
            bids=[(100.0, 5.0)],
            asks=[(101.0, 5.0)],
            depth=-1,
        )


def test_order_book_imbalance_rejects_non_integer_depth():
    analyzer = OrderBookImbalanceAnalyzer()

    with pytest.raises(
        TypeError,
        match="depth must be an integer",
    ):
        analyzer.analyze(
            bids=[(100.0, 5.0)],
            asks=[(101.0, 5.0)],
            depth=1.5,
        )


def test_order_book_imbalance_rejects_empty_bids():
    analyzer = OrderBookImbalanceAnalyzer()

    with pytest.raises(
        ValueError,
        match="bids and asks must not be empty",
    ):
        analyzer.analyze(
            bids=[],
            asks=[(101.0, 5.0)],
            depth=1,
        )


def test_order_book_imbalance_rejects_empty_asks():
    analyzer = OrderBookImbalanceAnalyzer()

    with pytest.raises(
        ValueError,
        match="bids and asks must not be empty",
    ):
        analyzer.analyze(
            bids=[(100.0, 5.0)],
            asks=[],
            depth=1,
        )


def test_order_book_imbalance_rejects_zero_total_volume():
    analyzer = OrderBookImbalanceAnalyzer()

    with pytest.raises(
        ValueError,
        match="total order book volume must be greater than zero",
    ):
        analyzer.analyze(
            bids=[(100.0, 0.0)],
            asks=[(101.0, 0.0)],
            depth=1,
        )


def test_order_book_imbalance_rejects_non_positive_bid_price():
    analyzer = OrderBookImbalanceAnalyzer()

    with pytest.raises(
        ValueError,
        match="bid price must be greater than zero",
    ):
        analyzer.analyze(
            bids=[
                (0.0, 5.0),
            ],
            asks=[
                (101.0, 5.0),
            ],
            depth=1,
        )


def test_order_book_imbalance_rejects_non_positive_ask_price():
    analyzer = OrderBookImbalanceAnalyzer()

    with pytest.raises(
        ValueError,
        match="ask price must be greater than zero",
    ):
        analyzer.analyze(
            bids=[
                (100.0, 5.0),
            ],
            asks=[
                (-1.0, 5.0),
            ],
            depth=1,
        )


def test_order_book_imbalance_rejects_negative_bid_quantity():
    analyzer = OrderBookImbalanceAnalyzer()

    with pytest.raises(
        ValueError,
        match="bid quantity cannot be negative",
    ):
        analyzer.analyze(
            bids=[
                (100.0, -5.0),
            ],
            asks=[
                (101.0, 5.0),
            ],
            depth=1,
        )


def test_order_book_imbalance_rejects_negative_ask_quantity():
    analyzer = OrderBookImbalanceAnalyzer()

    with pytest.raises(
        ValueError,
        match="ask quantity cannot be negative",
    ):
        analyzer.analyze(
            bids=[
                (100.0, 5.0),
            ],
            asks=[
                (101.0, -5.0),
            ],
            depth=1,
        )
        
        
def test_order_book_imbalance_uses_available_levels_when_depth_exceeds_book_size():
    analyzer = OrderBookImbalanceAnalyzer()

    result = analyzer.analyze(
        bids=[
            (100.0, 4.0),
            (99.0, 6.0),
        ],
        asks=[
            (101.0, 3.0),
        ],
        depth=5,
    )

    assert result == {
        "bid_volume": pytest.approx(10.0),
        "ask_volume": pytest.approx(3.0),
        "total_volume": pytest.approx(13.0),
        "imbalance": pytest.approx(7.0 / 13.0),
        "state": "bid_dominant",
    }