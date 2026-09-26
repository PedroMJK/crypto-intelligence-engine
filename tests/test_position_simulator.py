import pytest

from backend.app.paper_trading.position_side import PositionSide
from backend.app.paper_trading.position_simulator import (
    PositionSimulator,
)
from backend.app.paper_trading.simulated_position import (
    SimulatedPosition,
)


def test_position_side_defines_long_and_short():
    assert PositionSide.LONG.value == "long"
    assert PositionSide.SHORT.value == "short"


def test_simulated_position_preserves_position_data():
    position = SimulatedPosition(
        symbol="BTCUSDT",
        side=PositionSide.LONG,
        quantity=0.5,
        entry_price=50_000.0,
        entry_timestamp=1_700_000_000_000,
    )

    assert position.symbol == "BTCUSDT"
    assert position.side is PositionSide.LONG
    assert position.quantity == 0.5
    assert position.entry_price == 50_000.0
    assert position.entry_timestamp == 1_700_000_000_000


def test_simulated_position_is_immutable():
    position = SimulatedPosition(
        symbol="BTCUSDT",
        side=PositionSide.LONG,
        quantity=0.5,
        entry_price=50_000.0,
        entry_timestamp=1_700_000_000_000,
    )

    with pytest.raises(AttributeError):
        position.quantity = 1.0


@pytest.mark.parametrize(
    "symbol",
    [
        None,
        123,
        True,
    ],
)
def test_simulated_position_rejects_invalid_symbol_type(
    symbol,
):
    with pytest.raises(
        TypeError,
        match="symbol must be a string",
    ):
        SimulatedPosition(
            symbol=symbol,
            side=PositionSide.LONG,
            quantity=0.5,
            entry_price=50_000.0,
            entry_timestamp=1_700_000_000_000,
        )


@pytest.mark.parametrize(
    "symbol",
    [
        "",
        " ",
        "   ",
    ],
)
def test_simulated_position_rejects_empty_symbol(
    symbol,
):
    with pytest.raises(
        ValueError,
        match="symbol must not be empty",
    ):
        SimulatedPosition(
            symbol=symbol,
            side=PositionSide.LONG,
            quantity=0.5,
            entry_price=50_000.0,
            entry_timestamp=1_700_000_000_000,
        )


@pytest.mark.parametrize(
    "side",
    [
        None,
        "long",
        "short",
        1,
        True,
    ],
)
def test_simulated_position_rejects_invalid_side(
    side,
):
    with pytest.raises(
        TypeError,
        match="side must be a PositionSide",
    ):
        SimulatedPosition(
            symbol="BTCUSDT",
            side=side,
            quantity=0.5,
            entry_price=50_000.0,
            entry_timestamp=1_700_000_000_000,
        )


@pytest.mark.parametrize(
    "quantity",
    [
        None,
        "0.5",
        True,
    ],
)
def test_simulated_position_rejects_invalid_quantity_type(
    quantity,
):
    with pytest.raises(
        TypeError,
        match="quantity must be a number",
    ):
        SimulatedPosition(
            symbol="BTCUSDT",
            side=PositionSide.LONG,
            quantity=quantity,
            entry_price=50_000.0,
            entry_timestamp=1_700_000_000_000,
        )


@pytest.mark.parametrize(
    "quantity",
    [
        0.0,
        -0.1,
        float("nan"),
        float("inf"),
        float("-inf"),
    ],
)
def test_simulated_position_rejects_invalid_quantity_value(
    quantity,
):
    with pytest.raises(
        ValueError,
        match="quantity must be finite and greater than zero",
    ):
        SimulatedPosition(
            symbol="BTCUSDT",
            side=PositionSide.LONG,
            quantity=quantity,
            entry_price=50_000.0,
            entry_timestamp=1_700_000_000_000,
        )


@pytest.mark.parametrize(
    "entry_price",
    [
        None,
        "50000",
        True,
    ],
)
def test_simulated_position_rejects_invalid_entry_price_type(
    entry_price,
):
    with pytest.raises(
        TypeError,
        match="entry_price must be a number",
    ):
        SimulatedPosition(
            symbol="BTCUSDT",
            side=PositionSide.LONG,
            quantity=0.5,
            entry_price=entry_price,
            entry_timestamp=1_700_000_000_000,
        )


@pytest.mark.parametrize(
    "entry_price",
    [
        0.0,
        -1.0,
        float("nan"),
        float("inf"),
        float("-inf"),
    ],
)
def test_simulated_position_rejects_invalid_entry_price_value(
    entry_price,
):
    with pytest.raises(
        ValueError,
        match="entry_price must be finite and greater than zero",
    ):
        SimulatedPosition(
            symbol="BTCUSDT",
            side=PositionSide.LONG,
            quantity=0.5,
            entry_price=entry_price,
            entry_timestamp=1_700_000_000_000,
        )


@pytest.mark.parametrize(
    "entry_timestamp",
    [
        None,
        1.5,
        "1700000000000",
        True,
    ],
)
def test_simulated_position_rejects_invalid_entry_timestamp_type(
    entry_timestamp,
):
    with pytest.raises(
        TypeError,
        match="entry_timestamp must be an int",
    ):
        SimulatedPosition(
            symbol="BTCUSDT",
            side=PositionSide.LONG,
            quantity=0.5,
            entry_price=50_000.0,
            entry_timestamp=entry_timestamp,
        )


@pytest.mark.parametrize(
    "entry_timestamp",
    [
        -1,
        -1000,
    ],
)
def test_simulated_position_rejects_negative_entry_timestamp(
    entry_timestamp,
):
    with pytest.raises(
        ValueError,
        match="entry_timestamp must not be negative",
    ):
        SimulatedPosition(
            symbol="BTCUSDT",
            side=PositionSide.LONG,
            quantity=0.5,
            entry_price=50_000.0,
            entry_timestamp=entry_timestamp,
        )


def test_position_simulator_starts_without_open_position():
    simulator = PositionSimulator()

    assert simulator.current_position is None


def test_position_simulator_reports_no_open_position_initially():
    simulator = PositionSimulator()

    assert simulator.has_open_position is False


def test_position_simulator_registers_simulated_entry():
    simulator = PositionSimulator()

    position = simulator.register_entry(
        symbol="BTCUSDT",
        side=PositionSide.LONG,
        quantity=0.5,
        entry_price=50_000.0,
        entry_timestamp=1_700_000_000_000,
    )

    assert isinstance(
        position,
        SimulatedPosition,
    )

    assert position.symbol == "BTCUSDT"
    assert position.side is PositionSide.LONG
    assert position.quantity == 0.5
    assert position.entry_price == 50_000.0
    assert (
        position.entry_timestamp
        == 1_700_000_000_000
    )


def test_registered_entry_becomes_current_position():
    simulator = PositionSimulator()

    position = simulator.register_entry(
        symbol="ETHUSDT",
        side=PositionSide.SHORT,
        quantity=2.0,
        entry_price=3_000.0,
        entry_timestamp=1_700_000_000_000,
    )

    assert simulator.current_position is position


def test_position_simulator_reports_open_position_after_entry():
    simulator = PositionSimulator()

    simulator.register_entry(
        symbol="BTCUSDT",
        side=PositionSide.LONG,
        quantity=0.5,
        entry_price=50_000.0,
        entry_timestamp=1_700_000_000_000,
    )

    assert simulator.has_open_position is True


def test_position_simulator_rejects_second_open_position():
    simulator = PositionSimulator()

    first_position = simulator.register_entry(
        symbol="BTCUSDT",
        side=PositionSide.LONG,
        quantity=0.5,
        entry_price=50_000.0,
        entry_timestamp=1_700_000_000_000,
    )

    with pytest.raises(
        RuntimeError,
        match="an open position already exists",
    ):
        simulator.register_entry(
            symbol="ETHUSDT",
            side=PositionSide.SHORT,
            quantity=2.0,
            entry_price=3_000.0,
            entry_timestamp=1_700_000_060_000,
        )

    assert simulator.current_position is first_position


def test_failed_second_entry_preserves_existing_position():
    simulator = PositionSimulator()

    first_position = simulator.register_entry(
        symbol="BTCUSDT",
        side=PositionSide.LONG,
        quantity=0.5,
        entry_price=50_000.0,
        entry_timestamp=1_700_000_000_000,
    )

    try:
        simulator.register_entry(
            symbol="ETHUSDT",
            side=PositionSide.SHORT,
            quantity=2.0,
            entry_price=3_000.0,
            entry_timestamp=1_700_000_060_000,
        )
    except RuntimeError:
        pass

    assert simulator.current_position is first_position
    assert simulator.has_open_position is True


@pytest.mark.parametrize(
    (
        "symbol",
        "side",
        "quantity",
        "entry_price",
        "entry_timestamp",
        "expected_exception",
        "expected_message",
    ),
    [
        (
            "",
            PositionSide.LONG,
            0.5,
            50_000.0,
            1_700_000_000_000,
            ValueError,
            "symbol must not be empty",
        ),
        (
            "BTCUSDT",
            "long",
            0.5,
            50_000.0,
            1_700_000_000_000,
            TypeError,
            "side must be a PositionSide",
        ),
        (
            "BTCUSDT",
            PositionSide.LONG,
            0.0,
            50_000.0,
            1_700_000_000_000,
            ValueError,
            "quantity must be finite and greater than zero",
        ),
        (
            "BTCUSDT",
            PositionSide.LONG,
            0.5,
            0.0,
            1_700_000_000_000,
            ValueError,
            "entry_price must be finite and greater than zero",
        ),
        (
            "BTCUSDT",
            PositionSide.LONG,
            0.5,
            50_000.0,
            -1,
            ValueError,
            "entry_timestamp must not be negative",
        ),
    ],
)
def test_position_simulator_reuses_position_validation_for_entries(
    symbol,
    side,
    quantity,
    entry_price,
    entry_timestamp,
    expected_exception,
    expected_message,
):
    simulator = PositionSimulator()

    with pytest.raises(
        expected_exception,
        match=expected_message,
    ):
        simulator.register_entry(
            symbol=symbol,
            side=side,
            quantity=quantity,
            entry_price=entry_price,
            entry_timestamp=entry_timestamp,
        )

    assert simulator.current_position is None
    assert simulator.has_open_position is False
