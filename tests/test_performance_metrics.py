import math

import pytest

from backend.app.paper_trading.performance_metrics import (
    PerformanceMetrics,
)
from backend.app.paper_trading.trade_performance import (
    TradePerformance,
)


def create_trade(
    *,
    gross_pnl: float,
    entry_fee: float,
    exit_fee: float,
    net_pnl: float,
    return_rate: float,
) -> TradePerformance:
    return TradePerformance(
        entry_execution_price=100.0,
        exit_execution_price=110.0,
        gross_pnl=gross_pnl,
        entry_fee=entry_fee,
        exit_fee=exit_fee,
        total_fees=entry_fee + exit_fee,
        net_pnl=net_pnl,
        return_rate=return_rate,
    )


def test_metrics_count_total_trades():
    trades = [
        create_trade(
            gross_pnl=10.0,
            entry_fee=1.0,
            exit_fee=1.0,
            net_pnl=8.0,
            return_rate=0.08,
        ),
        create_trade(
            gross_pnl=-5.0,
            entry_fee=1.0,
            exit_fee=1.0,
            net_pnl=-7.0,
            return_rate=-0.07,
        ),
    ]

    metrics = PerformanceMetrics.calculate(
        trades
    )

    assert metrics.total_trades == 2


def test_metrics_classify_trades_by_net_pnl():
    trades = [
        create_trade(
            gross_pnl=10.0,
            entry_fee=1.0,
            exit_fee=1.0,
            net_pnl=8.0,
            return_rate=0.08,
        ),
        create_trade(
            gross_pnl=-5.0,
            entry_fee=1.0,
            exit_fee=1.0,
            net_pnl=-7.0,
            return_rate=-0.07,
        ),
        create_trade(
            gross_pnl=2.0,
            entry_fee=1.0,
            exit_fee=1.0,
            net_pnl=0.0,
            return_rate=0.0,
        ),
    ]

    metrics = PerformanceMetrics.calculate(
        trades
    )

    assert metrics.winning_trades == 1
    assert metrics.losing_trades == 1
    assert metrics.breakeven_trades == 1


def test_metrics_calculate_win_rate():
    trades = [
        create_trade(
            gross_pnl=10.0,
            entry_fee=1.0,
            exit_fee=1.0,
            net_pnl=8.0,
            return_rate=0.08,
        ),
        create_trade(
            gross_pnl=5.0,
            entry_fee=1.0,
            exit_fee=1.0,
            net_pnl=3.0,
            return_rate=0.03,
        ),
        create_trade(
            gross_pnl=-5.0,
            entry_fee=1.0,
            exit_fee=1.0,
            net_pnl=-7.0,
            return_rate=-0.07,
        ),
        create_trade(
            gross_pnl=2.0,
            entry_fee=1.0,
            exit_fee=1.0,
            net_pnl=0.0,
            return_rate=0.0,
        ),
    ]

    metrics = PerformanceMetrics.calculate(
        trades
    )

    assert metrics.win_rate == pytest.approx(
        0.5
    )


def test_metrics_aggregate_gross_pnl():
    trades = [
        create_trade(
            gross_pnl=10.0,
            entry_fee=1.0,
            exit_fee=1.0,
            net_pnl=8.0,
            return_rate=0.08,
        ),
        create_trade(
            gross_pnl=-5.0,
            entry_fee=1.0,
            exit_fee=1.0,
            net_pnl=-7.0,
            return_rate=-0.07,
        ),
    ]

    metrics = PerformanceMetrics.calculate(
        trades
    )

    assert metrics.gross_pnl == pytest.approx(
        5.0
    )


def test_metrics_aggregate_total_fees():
    trades = [
        create_trade(
            gross_pnl=10.0,
            entry_fee=1.0,
            exit_fee=2.0,
            net_pnl=7.0,
            return_rate=0.07,
        ),
        create_trade(
            gross_pnl=5.0,
            entry_fee=0.5,
            exit_fee=0.5,
            net_pnl=4.0,
            return_rate=0.04,
        ),
    ]

    metrics = PerformanceMetrics.calculate(
        trades
    )

    assert metrics.total_fees == pytest.approx(
        4.0
    )


def test_metrics_aggregate_net_pnl():
    trades = [
        create_trade(
            gross_pnl=10.0,
            entry_fee=1.0,
            exit_fee=1.0,
            net_pnl=8.0,
            return_rate=0.08,
        ),
        create_trade(
            gross_pnl=-5.0,
            entry_fee=1.0,
            exit_fee=1.0,
            net_pnl=-7.0,
            return_rate=-0.07,
        ),
    ]

    metrics = PerformanceMetrics.calculate(
        trades
    )

    assert metrics.net_pnl == pytest.approx(
        1.0
    )


def test_empty_trade_collection_returns_zero_metrics():
    metrics = PerformanceMetrics.calculate([])

    assert metrics.total_trades == 0
    assert metrics.winning_trades == 0
    assert metrics.losing_trades == 0
    assert metrics.breakeven_trades == 0
    assert metrics.win_rate == 0.0
    assert metrics.gross_pnl == 0.0
    assert metrics.total_fees == 0.0
    assert metrics.net_pnl == 0.0


def test_metrics_accept_tuple_of_trades():
    trade = create_trade(
        gross_pnl=10.0,
        entry_fee=1.0,
        exit_fee=1.0,
        net_pnl=8.0,
        return_rate=0.08,
    )

    metrics = PerformanceMetrics.calculate(
        (trade,)
    )

    assert metrics.total_trades == 1
    assert metrics.net_pnl == pytest.approx(
        8.0
    )


@pytest.mark.parametrize(
    "trades",
    [
        None,
        "trade",
        123,
        True,
    ],
)
def test_metrics_require_trade_collection(
    trades,
):
    with pytest.raises(
        TypeError,
        match=(
            "trades must be a list or tuple"
        ),
    ):
        PerformanceMetrics.calculate(trades)


@pytest.mark.parametrize(
    "invalid_trade",
    [
        None,
        "trade",
        123,
        True,
        math.nan,
    ],
)
def test_metrics_require_trade_performance_items(
    invalid_trade,
):
    with pytest.raises(
        TypeError,
        match=(
            "all trades must be "
            "TradePerformance instances"
        ),
    ):
        PerformanceMetrics.calculate(
            [invalid_trade]
        )
