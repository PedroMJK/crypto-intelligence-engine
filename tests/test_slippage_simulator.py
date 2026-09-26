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
from backend.app.paper_trading.slippage_simulator import (
    SlippageSimulator,
)


def test_buy_execution_price_applies_slippage_upward():
    execution_price = (
        SlippageSimulator.calculate_execution_price(
            price=100.0,
            slippage_rate=0.001,
            is_buy=True,
        )
    )

    assert execution_price == pytest.approx(100.1)


def test_sell_execution_price_applies_slippage_downward():
    execution_price = (
        SlippageSimulator.calculate_execution_price(
            price=100.0,
            slippage_rate=0.001,
            is_buy=False,
        )
    )

    assert execution_price == pytest.approx(99.9)


def test_zero_slippage_preserves_price():
    buy_price = (
        SlippageSimulator.calculate_execution_price(
            price=100.0,
            slippage_rate=0.0,
            is_buy=True,
        )
    )
    sell_price = (
        SlippageSimulator.calculate_execution_price(
            price=100.0,
            slippage_rate=0.0,
            is_buy=False,
        )
    )

    assert buy_price == pytest.approx(100.0)
    assert sell_price == pytest.approx(100.0)


@pytest.mark.parametrize(
    "price",
    [
        "100",
        None,
        True,
    ],
)
def test_execution_price_requires_numeric_price(
    price,
):
    with pytest.raises(
        TypeError,
        match="price must be a number",
    ):
        SlippageSimulator.calculate_execution_price(
            price=price,
            slippage_rate=0.001,
            is_buy=True,
        )


@pytest.mark.parametrize(
    "price",
    [
        0.0,
        -1.0,
        math.inf,
        -math.inf,
        math.nan,
    ],
)
def test_execution_price_requires_positive_finite_price(
    price,
):
    with pytest.raises(
        ValueError,
        match=(
            "price must be finite "
            "and greater than zero"
        ),
    ):
        SlippageSimulator.calculate_execution_price(
            price=price,
            slippage_rate=0.001,
            is_buy=True,
        )


@pytest.mark.parametrize(
    "slippage_rate",
    [
        "0.001",
        None,
        True,
    ],
)
def test_execution_price_requires_numeric_slippage_rate(
    slippage_rate,
):
    with pytest.raises(
        TypeError,
        match="slippage_rate must be a number",
    ):
        SlippageSimulator.calculate_execution_price(
            price=100.0,
            slippage_rate=slippage_rate,
            is_buy=True,
        )


@pytest.mark.parametrize(
    "slippage_rate",
    [
        -0.001,
        1.0,
        1.1,
        math.inf,
        -math.inf,
        math.nan,
    ],
)
def test_execution_price_requires_valid_slippage_rate(
    slippage_rate,
):
    with pytest.raises(
        ValueError,
        match=(
            "slippage_rate must be finite "
            "and between zero and one"
        ),
    ):
        SlippageSimulator.calculate_execution_price(
            price=100.0,
            slippage_rate=slippage_rate,
            is_buy=True,
        )


@pytest.mark.parametrize(
    "is_buy",
    [
        1,
        0,
        "true",
        None,
    ],
)
def test_execution_price_requires_boolean_execution_side(
    is_buy,
):
    with pytest.raises(
        TypeError,
        match="is_buy must be a bool",
    ):
        SlippageSimulator.calculate_execution_price(
            price=100.0,
            slippage_rate=0.001,
            is_buy=is_buy,
        )


@pytest.mark.parametrize(
    (
        "side",
        "expected_price",
    ),
    [
        (
            PositionSide.LONG,
            100.1,
        ),
        (
            PositionSide.SHORT,
            99.9,
        ),
    ],
)
def test_entry_execution_price_respects_position_side(
    side,
    expected_price,
):
    position = SimulatedPosition(
        symbol="BTCUSDT",
        side=side,
        quantity=0.5,
        entry_price=100.0,
        entry_timestamp=1_700_000_000_000,
    )

    execution_price = (
        SlippageSimulator.calculate_entry_price(
            position=position,
            slippage_rate=0.001,
        )
    )

    assert execution_price == pytest.approx(
        expected_price
    )


@pytest.mark.parametrize(
    (
        "side",
        "expected_price",
    ),
    [
        (
            PositionSide.LONG,
            109.89,
        ),
        (
            PositionSide.SHORT,
            110.11,
        ),
    ],
)
def test_exit_execution_price_reverses_execution_side(
    side,
    expected_price,
):
    position = SimulatedPosition(
        symbol="BTCUSDT",
        side=side,
        quantity=0.5,
        entry_price=100.0,
        entry_timestamp=1_700_000_000_000,
    )

    simulated_exit = SimulatedExit(
        position=position,
        exit_price=110.0,
        exit_timestamp=1_700_000_060_000,
    )

    execution_price = (
        SlippageSimulator.calculate_exit_price(
            simulated_exit=simulated_exit,
            slippage_rate=0.001,
        )
    )

    assert execution_price == pytest.approx(
        expected_price
    )


def test_entry_price_requires_simulated_position():
    with pytest.raises(
        TypeError,
        match="position must be a SimulatedPosition",
    ):
        SlippageSimulator.calculate_entry_price(
            position="BTCUSDT",
            slippage_rate=0.001,
        )


def test_exit_price_requires_simulated_exit():
    with pytest.raises(
        TypeError,
        match=(
            "simulated_exit must be a SimulatedExit"
        ),
    ):
        SlippageSimulator.calculate_exit_price(
            simulated_exit="BTCUSDT",
            slippage_rate=0.001,
        )
