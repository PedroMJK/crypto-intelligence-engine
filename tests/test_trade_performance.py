import math

import pytest

from backend.app.paper_trading.position_side import (
    PositionSide,
)
from backend.app.paper_trading.simulated_exit import (
    SimulatedExit,
)
from backend.app.paper_trading.simulated_position import (
    SimulatedPosition,
)
from backend.app.paper_trading.trade_performance import (
    TradePerformance,
)


def create_exit(
    *,
    side: PositionSide,
    quantity: float = 2.0,
    entry_price: float = 100.0,
    exit_price: float = 110.0,
) -> SimulatedExit:
    position = SimulatedPosition(
        symbol="BTCUSDT",
        side=side,
        quantity=quantity,
        entry_price=entry_price,
        entry_timestamp=1_700_000_000_000,
    )

    return SimulatedExit(
        position=position,
        exit_price=exit_price,
        exit_timestamp=1_700_000_060_000,
    )


def test_long_trade_calculates_gross_pnl():
    simulated_exit = create_exit(
        side=PositionSide.LONG,
    )

    performance = TradePerformance.calculate(
        simulated_exit=simulated_exit,
        entry_fee_rate=0.0,
        exit_fee_rate=0.0,
        slippage_rate=0.0,
    )

    assert performance.gross_pnl == pytest.approx(
        20.0
    )


def test_short_trade_calculates_gross_pnl():
    simulated_exit = create_exit(
        side=PositionSide.SHORT,
        entry_price=110.0,
        exit_price=100.0,
    )

    performance = TradePerformance.calculate(
        simulated_exit=simulated_exit,
        entry_fee_rate=0.0,
        exit_fee_rate=0.0,
        slippage_rate=0.0,
    )

    assert performance.gross_pnl == pytest.approx(
        20.0
    )


def test_trade_calculates_entry_and_exit_fees():
    simulated_exit = create_exit(
        side=PositionSide.LONG,
    )

    performance = TradePerformance.calculate(
        simulated_exit=simulated_exit,
        entry_fee_rate=0.001,
        exit_fee_rate=0.002,
        slippage_rate=0.0,
    )

    assert performance.entry_fee == pytest.approx(
        0.2
    )
    assert performance.exit_fee == pytest.approx(
        0.44
    )
    assert performance.total_fees == pytest.approx(
        0.64
    )


def test_trade_calculates_net_pnl_after_fees():
    simulated_exit = create_exit(
        side=PositionSide.LONG,
    )

    performance = TradePerformance.calculate(
        simulated_exit=simulated_exit,
        entry_fee_rate=0.001,
        exit_fee_rate=0.002,
        slippage_rate=0.0,
    )

    assert performance.net_pnl == pytest.approx(
        19.36
    )


def test_trade_calculates_return_from_entry_notional():
    simulated_exit = create_exit(
        side=PositionSide.LONG,
    )

    performance = TradePerformance.calculate(
        simulated_exit=simulated_exit,
        entry_fee_rate=0.0,
        exit_fee_rate=0.0,
        slippage_rate=0.0,
    )

    assert performance.return_rate == pytest.approx(
        0.1
    )


def test_trade_applies_adverse_slippage_before_pnl():
    simulated_exit = create_exit(
        side=PositionSide.LONG,
        quantity=1.0,
    )

    performance = TradePerformance.calculate(
        simulated_exit=simulated_exit,
        entry_fee_rate=0.0,
        exit_fee_rate=0.0,
        slippage_rate=0.01,
    )

    assert (
        performance.entry_execution_price
        == pytest.approx(101.0)
    )
    assert (
        performance.exit_execution_price
        == pytest.approx(108.9)
    )
    assert performance.gross_pnl == pytest.approx(
        7.9
    )


def test_fees_use_slippage_adjusted_execution_prices():
    simulated_exit = create_exit(
        side=PositionSide.LONG,
        quantity=1.0,
    )

    performance = TradePerformance.calculate(
        simulated_exit=simulated_exit,
        entry_fee_rate=0.001,
        exit_fee_rate=0.001,
        slippage_rate=0.01,
    )

    assert performance.entry_fee == pytest.approx(
        0.101
    )
    assert performance.exit_fee == pytest.approx(
        0.1089
    )


def test_losing_trade_has_negative_net_pnl():
    simulated_exit = create_exit(
        side=PositionSide.LONG,
        entry_price=110.0,
        exit_price=100.0,
    )

    performance = TradePerformance.calculate(
        simulated_exit=simulated_exit,
        entry_fee_rate=0.0,
        exit_fee_rate=0.0,
        slippage_rate=0.0,
    )

    assert performance.gross_pnl == pytest.approx(
        -20.0
    )
    assert performance.net_pnl == pytest.approx(
        -20.0
    )
    assert performance.return_rate < 0


def test_trade_performance_requires_simulated_exit():
    with pytest.raises(
        TypeError,
        match=(
            "simulated_exit must be a SimulatedExit"
        ),
    ):
        TradePerformance.calculate(
            simulated_exit="BTCUSDT",
            entry_fee_rate=0.001,
            exit_fee_rate=0.001,
            slippage_rate=0.001,
        )


@pytest.mark.parametrize(
    "fee_rate",
    [
        "0.001",
        None,
        True,
        -0.001,
        math.inf,
        -math.inf,
        math.nan,
    ],
)
def test_trade_performance_rejects_invalid_entry_fee_rate(
    fee_rate,
):
    expected_exception = (
        TypeError
        if (
            isinstance(fee_rate, bool)
            or not isinstance(
                fee_rate,
                (int, float),
            )
        )
        else ValueError
    )

    with pytest.raises(expected_exception):
        TradePerformance.calculate(
            simulated_exit=create_exit(
                side=PositionSide.LONG,
            ),
            entry_fee_rate=fee_rate,
            exit_fee_rate=0.001,
            slippage_rate=0.001,
        )


@pytest.mark.parametrize(
    "fee_rate",
    [
        "0.001",
        None,
        True,
        -0.001,
        math.inf,
        -math.inf,
        math.nan,
    ],
)
def test_trade_performance_rejects_invalid_exit_fee_rate(
    fee_rate,
):
    expected_exception = (
        TypeError
        if (
            isinstance(fee_rate, bool)
            or not isinstance(
                fee_rate,
                (int, float),
            )
        )
        else ValueError
    )

    with pytest.raises(expected_exception):
        TradePerformance.calculate(
            simulated_exit=create_exit(
                side=PositionSide.LONG,
            ),
            entry_fee_rate=0.001,
            exit_fee_rate=fee_rate,
            slippage_rate=0.001,
        )


@pytest.mark.parametrize(
    "slippage_rate",
    [
        "0.001",
        None,
        True,
        -0.001,
        1.0,
        math.inf,
        -math.inf,
        math.nan,
    ],
)
def test_trade_performance_rejects_invalid_slippage_rate(
    slippage_rate,
):
    expected_exception = (
        TypeError
        if (
            isinstance(slippage_rate, bool)
            or not isinstance(
                slippage_rate,
                (int, float),
            )
        )
        else ValueError
    )

    with pytest.raises(expected_exception):
        TradePerformance.calculate(
            simulated_exit=create_exit(
                side=PositionSide.LONG,
            ),
            entry_fee_rate=0.001,
            exit_fee_rate=0.001,
            slippage_rate=slippage_rate,
        )
