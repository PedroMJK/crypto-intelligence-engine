import pytest

from backend.app.analysis.trades_per_second import TradesPerSecond


def test_trades_per_second_calculates_rate():
    trades_per_second = TradesPerSecond()

    result = trades_per_second.calculate(
        trade_count=50,
        window_seconds=5.0,
    )

    assert result == 10.0


def test_trades_per_second_supports_fractional_rate():
    trades_per_second = TradesPerSecond()

    result = trades_per_second.calculate(
        trade_count=1,
        window_seconds=2.0,
    )

    assert result == 0.5


def test_trades_per_second_returns_zero_when_no_trades_occur():
    trades_per_second = TradesPerSecond()

    result = trades_per_second.calculate(
        trade_count=0,
        window_seconds=5.0,
    )

    assert result == 0.0


def test_trades_per_second_rejects_negative_trade_count():
    trades_per_second = TradesPerSecond()

    with pytest.raises(
        ValueError,
        match="trade_count cannot be negative",
    ):
        trades_per_second.calculate(
            trade_count=-1,
            window_seconds=5.0,
        )


def test_trades_per_second_rejects_zero_window():
    trades_per_second = TradesPerSecond()

    with pytest.raises(
        ValueError,
        match="window_seconds must be greater than zero",
    ):
        trades_per_second.calculate(
            trade_count=10,
            window_seconds=0.0,
        )


def test_trades_per_second_rejects_negative_window():
    trades_per_second = TradesPerSecond()

    with pytest.raises(
        ValueError,
        match="window_seconds must be greater than zero",
    ):
        trades_per_second.calculate(
            trade_count=10,
            window_seconds=-1.0,
        )
