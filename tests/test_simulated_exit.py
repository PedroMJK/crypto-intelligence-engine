import math

import pytest

from backend.app.paper_trading.position_side import PositionSide
from backend.app.paper_trading.simulated_exit import SimulatedExit
from backend.app.paper_trading.simulated_position import (
    SimulatedPosition,
)


def create_position() -> SimulatedPosition:
    return SimulatedPosition(
        symbol="BTCUSDT",
        side=PositionSide.LONG,
        quantity=0.5,
        entry_price=50_000.0,
        entry_timestamp=1_700_000_000_000,
    )


def test_simulated_exit_preserves_closed_position():
    position = create_position()

    simulated_exit = SimulatedExit(
        position=position,
        exit_price=51_000.0,
        exit_timestamp=1_700_000_060_000,
    )

    assert simulated_exit.position is position


def test_simulated_exit_preserves_exit_data():
    simulated_exit = SimulatedExit(
        position=create_position(),
        exit_price=51_000.0,
        exit_timestamp=1_700_000_060_000,
    )

    assert simulated_exit.exit_price == 51_000.0
    assert (
        simulated_exit.exit_timestamp
        == 1_700_000_060_000
    )


def test_simulated_exit_is_immutable():
    simulated_exit = SimulatedExit(
        position=create_position(),
        exit_price=51_000.0,
        exit_timestamp=1_700_000_060_000,
    )

    with pytest.raises(AttributeError):
        simulated_exit.exit_price = 52_000.0


def test_simulated_exit_requires_simulated_position():
    with pytest.raises(
        TypeError,
        match="position must be a SimulatedPosition",
    ):
        SimulatedExit(
            position="BTCUSDT",
            exit_price=51_000.0,
            exit_timestamp=1_700_000_060_000,
        )


@pytest.mark.parametrize(
    "exit_price",
    [
        "51000",
        None,
        True,
    ],
)
def test_simulated_exit_requires_numeric_exit_price(
    exit_price,
):
    with pytest.raises(
        TypeError,
        match="exit_price must be a number",
    ):
        SimulatedExit(
            position=create_position(),
            exit_price=exit_price,
            exit_timestamp=1_700_000_060_000,
        )


@pytest.mark.parametrize(
    "exit_price",
    [
        0.0,
        -1.0,
        math.inf,
        -math.inf,
        math.nan,
    ],
)
def test_simulated_exit_requires_positive_finite_exit_price(
    exit_price,
):
    with pytest.raises(
        ValueError,
        match=(
            "exit_price must be finite "
            "and greater than zero"
        ),
    ):
        SimulatedExit(
            position=create_position(),
            exit_price=exit_price,
            exit_timestamp=1_700_000_060_000,
        )


@pytest.mark.parametrize(
    "exit_timestamp",
    [
        1.5,
        "1700000060000",
        None,
        True,
    ],
)
def test_simulated_exit_requires_integer_exit_timestamp(
    exit_timestamp,
):
    with pytest.raises(
        TypeError,
        match="exit_timestamp must be an int",
    ):
        SimulatedExit(
            position=create_position(),
            exit_price=51_000.0,
            exit_timestamp=exit_timestamp,
        )


def test_simulated_exit_rejects_exit_before_entry():
    position = create_position()

    with pytest.raises(
        ValueError,
        match=(
            "exit_timestamp must not be "
            "before entry_timestamp"
        ),
    ):
        SimulatedExit(
            position=position,
            exit_price=51_000.0,
            exit_timestamp=(
                position.entry_timestamp - 1
            ),
        )


def test_simulated_exit_allows_exit_at_entry_timestamp():
    position = create_position()

    simulated_exit = SimulatedExit(
        position=position,
        exit_price=51_000.0,
        exit_timestamp=position.entry_timestamp,
    )

    assert (
        simulated_exit.exit_timestamp
        == position.entry_timestamp
    )
