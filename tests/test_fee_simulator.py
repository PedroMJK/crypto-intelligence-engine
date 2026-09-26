import math

import pytest

from backend.app.paper_trading.fee_simulator import (
    FeeSimulator,
)
from backend.app.paper_trading.position_side import (
    PositionSide,
)
from backend.app.paper_trading.simulated_exit import (
    SimulatedExit,
)
from backend.app.paper_trading.simulated_position import (
    SimulatedPosition,
)


def test_fee_simulator_calculates_fee_from_notional():
    fee = FeeSimulator.calculate(
        price=50_000.0,
        quantity=0.5,
        fee_rate=0.0004,
    )

    assert fee == pytest.approx(10.0)


def test_fee_simulator_supports_different_fee_rates():
    fee = FeeSimulator.calculate(
        price=3_000.0,
        quantity=2.0,
        fee_rate=0.001,
    )

    assert fee == pytest.approx(6.0)


def test_fee_simulator_allows_zero_fee_rate():
    fee = FeeSimulator.calculate(
        price=50_000.0,
        quantity=0.5,
        fee_rate=0.0,
    )

    assert fee == 0.0


def test_fee_simulator_does_not_depend_on_position_side():
    long_fee = FeeSimulator.calculate(
        price=50_000.0,
        quantity=0.5,
        fee_rate=0.0004,
    )

    short_fee = FeeSimulator.calculate(
        price=50_000.0,
        quantity=0.5,
        fee_rate=0.0004,
    )

    assert long_fee == pytest.approx(short_fee)


@pytest.mark.parametrize(
    "price",
    [
        "50000",
        None,
        True,
    ],
)
def test_fee_simulator_requires_numeric_price(
    price,
):
    with pytest.raises(
        TypeError,
        match="price must be a number",
    ):
        FeeSimulator.calculate(
            price=price,
            quantity=0.5,
            fee_rate=0.0004,
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
def test_fee_simulator_requires_positive_finite_price(
    price,
):
    with pytest.raises(
        ValueError,
        match=(
            "price must be finite "
            "and greater than zero"
        ),
    ):
        FeeSimulator.calculate(
            price=price,
            quantity=0.5,
            fee_rate=0.0004,
        )


@pytest.mark.parametrize(
    "quantity",
    [
        "0.5",
        None,
        True,
    ],
)
def test_fee_simulator_requires_numeric_quantity(
    quantity,
):
    with pytest.raises(
        TypeError,
        match="quantity must be a number",
    ):
        FeeSimulator.calculate(
            price=50_000.0,
            quantity=quantity,
            fee_rate=0.0004,
        )


@pytest.mark.parametrize(
    "quantity",
    [
        0.0,
        -1.0,
        math.inf,
        -math.inf,
        math.nan,
    ],
)
def test_fee_simulator_requires_positive_finite_quantity(
    quantity,
):
    with pytest.raises(
        ValueError,
        match=(
            "quantity must be finite "
            "and greater than zero"
        ),
    ):
        FeeSimulator.calculate(
            price=50_000.0,
            quantity=quantity,
            fee_rate=0.0004,
        )


@pytest.mark.parametrize(
    "fee_rate",
    [
        "0.0004",
        None,
        True,
    ],
)
def test_fee_simulator_requires_numeric_fee_rate(
    fee_rate,
):
    with pytest.raises(
        TypeError,
        match="fee_rate must be a number",
    ):
        FeeSimulator.calculate(
            price=50_000.0,
            quantity=0.5,
            fee_rate=fee_rate,
        )


@pytest.mark.parametrize(
    "fee_rate",
    [
        -0.0001,
        math.inf,
        -math.inf,
        math.nan,
    ],
)
def test_fee_simulator_requires_non_negative_finite_fee_rate(
    fee_rate,
):
    with pytest.raises(
        ValueError,
        match=(
            "fee_rate must be finite "
            "and non-negative"
        ),
    ):
        FeeSimulator.calculate(
            price=50_000.0,
            quantity=0.5,
            fee_rate=fee_rate,
        )


def test_fee_simulator_calculates_position_entry_fee():
    position = SimulatedPosition(
        symbol="BTCUSDT",
        side=PositionSide.LONG,
        quantity=0.5,
        entry_price=50_000.0,
        entry_timestamp=1_700_000_000_000,
    )

    fee = FeeSimulator.calculate_entry_fee(
        position=position,
        fee_rate=0.0004,
    )

    assert fee == pytest.approx(10.0)


def test_fee_simulator_calculates_position_exit_fee():
    position = SimulatedPosition(
        symbol="BTCUSDT",
        side=PositionSide.LONG,
        quantity=0.5,
        entry_price=50_000.0,
        entry_timestamp=1_700_000_000_000,
    )

    simulated_exit = SimulatedExit(
        position=position,
        exit_price=51_000.0,
        exit_timestamp=1_700_000_060_000,
    )

    fee = FeeSimulator.calculate_exit_fee(
        simulated_exit=simulated_exit,
        fee_rate=0.0004,
    )

    assert fee == pytest.approx(10.2)


def test_entry_fee_uses_position_entry_price():
    position = SimulatedPosition(
        symbol="ETHUSDT",
        side=PositionSide.SHORT,
        quantity=2.0,
        entry_price=3_000.0,
        entry_timestamp=1_700_000_000_000,
    )

    fee = FeeSimulator.calculate_entry_fee(
        position=position,
        fee_rate=0.001,
    )

    assert fee == pytest.approx(6.0)


def test_exit_fee_uses_simulated_exit_price():
    position = SimulatedPosition(
        symbol="ETHUSDT",
        side=PositionSide.SHORT,
        quantity=2.0,
        entry_price=3_000.0,
        entry_timestamp=1_700_000_000_000,
    )

    simulated_exit = SimulatedExit(
        position=position,
        exit_price=2_900.0,
        exit_timestamp=1_700_000_060_000,
    )

    fee = FeeSimulator.calculate_exit_fee(
        simulated_exit=simulated_exit,
        fee_rate=0.001,
    )

    assert fee == pytest.approx(5.8)


def test_entry_fee_requires_simulated_position():
    with pytest.raises(
        TypeError,
        match="position must be a SimulatedPosition",
    ):
        FeeSimulator.calculate_entry_fee(
            position="BTCUSDT",
            fee_rate=0.0004,
        )


def test_exit_fee_requires_simulated_exit():
    with pytest.raises(
        TypeError,
        match="simulated_exit must be a SimulatedExit",
    ):
        FeeSimulator.calculate_exit_fee(
            simulated_exit="BTCUSDT",
            fee_rate=0.0004,
        )
