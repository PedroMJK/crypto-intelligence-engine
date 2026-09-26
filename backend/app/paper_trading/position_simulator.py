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
