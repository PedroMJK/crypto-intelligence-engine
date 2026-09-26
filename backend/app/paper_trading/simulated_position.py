import math
from dataclasses import dataclass

from backend.app.paper_trading.position_side import PositionSide


@dataclass(frozen=True)
class SimulatedPosition:
    symbol: str
    side: PositionSide
    quantity: float
    entry_price: float
    entry_timestamp: int

    def __post_init__(self) -> None:
        self._validate_symbol(self.symbol)
        self._validate_side(self.side)
        self._validate_quantity(self.quantity)
        self._validate_entry_price(self.entry_price)
        self._validate_entry_timestamp(
            self.entry_timestamp
        )

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        if not isinstance(symbol, str):
            raise TypeError(
                "symbol must be a string"
            )

        if not symbol.strip():
            raise ValueError(
                "symbol must not be empty"
            )

    @staticmethod
    def _validate_side(
        side: PositionSide,
    ) -> None:
        if not isinstance(
            side,
            PositionSide,
        ):
            raise TypeError(
                "side must be a PositionSide"
            )

    @staticmethod
    def _validate_quantity(
        quantity: float,
    ) -> None:
        if (
            isinstance(quantity, bool)
            or not isinstance(
                quantity,
                (int, float),
            )
        ):
            raise TypeError(
                "quantity must be a number"
            )

        if (
            not math.isfinite(quantity)
            or quantity <= 0
        ):
            raise ValueError(
                "quantity must be finite "
                "and greater than zero"
            )

    @staticmethod
    def _validate_entry_price(
        entry_price: float,
    ) -> None:
        if (
            isinstance(entry_price, bool)
            or not isinstance(
                entry_price,
                (int, float),
            )
        ):
            raise TypeError(
                "entry_price must be a number"
            )

        if (
            not math.isfinite(entry_price)
            or entry_price <= 0
        ):
            raise ValueError(
                "entry_price must be finite "
                "and greater than zero"
            )

    @staticmethod
    def _validate_entry_timestamp(
        entry_timestamp: int,
    ) -> None:
        if (
            isinstance(entry_timestamp, bool)
            or not isinstance(
                entry_timestamp,
                int,
            )
        ):
            raise TypeError(
                "entry_timestamp must be an int"
            )

        if entry_timestamp < 0:
            raise ValueError(
                "entry_timestamp must not be negative"
            )
