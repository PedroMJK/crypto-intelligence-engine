from backend.app.paper_trading.position_side import PositionSide
from backend.app.paper_trading.simulated_position import (
    SimulatedPosition,
)


class PositionSimulator:
    def __init__(self) -> None:
        self._current_position: (
            SimulatedPosition | None
        ) = None

    @property
    def current_position(
        self,
    ) -> SimulatedPosition | None:
        return self._current_position

    @property
    def has_open_position(self) -> bool:
        return self._current_position is not None

    def register_entry(
        self,
        symbol: str,
        side: PositionSide,
        quantity: float,
        entry_price: float,
        entry_timestamp: int,
    ) -> SimulatedPosition:
        if self.has_open_position:
            raise RuntimeError(
                "an open position already exists"
            )

        position = SimulatedPosition(
            symbol=symbol,
            side=side,
            quantity=quantity,
            entry_price=entry_price,
            entry_timestamp=entry_timestamp,
        )

        self._current_position = position

        return position
