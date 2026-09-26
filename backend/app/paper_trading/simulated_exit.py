import math
from dataclasses import dataclass

from backend.app.paper_trading.simulated_position import (
    SimulatedPosition,
)


@dataclass(frozen=True)
class SimulatedExit:
    position: SimulatedPosition
    exit_price: float
    exit_timestamp: int

    def __post_init__(self) -> None:
        self._validate_position(self.position)
        self._validate_exit_price(self.exit_price)
        self._validate_exit_timestamp(
            self.exit_timestamp,
            self.position,
        )

    @staticmethod
    def _validate_position(
        position: SimulatedPosition,
    ) -> None:
        if not isinstance(
            position,
            SimulatedPosition,
        ):
            raise TypeError(
                "position must be a SimulatedPosition"
            )

    @staticmethod
    def _validate_exit_price(
        exit_price: float,
    ) -> None:
        if (
            isinstance(exit_price, bool)
            or not isinstance(
                exit_price,
                (int, float),
            )
        ):
            raise TypeError(
                "exit_price must be a number"
            )

        if (
            not math.isfinite(exit_price)
            or exit_price <= 0
        ):
            raise ValueError(
                "exit_price must be finite "
                "and greater than zero"
            )

    @staticmethod
    def _validate_exit_timestamp(
        exit_timestamp: int,
        position: SimulatedPosition,
    ) -> None:
        if (
            isinstance(exit_timestamp, bool)
            or not isinstance(
                exit_timestamp,
                int,
            )
        ):
            raise TypeError(
                "exit_timestamp must be an int"
            )

        if (
            exit_timestamp
            < position.entry_timestamp
        ):
            raise ValueError(
                "exit_timestamp must not be "
                "before entry_timestamp"
            )
