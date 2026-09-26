import math

from backend.app.paper_trading.simulated_exit import (
    SimulatedExit,
)
from backend.app.paper_trading.simulated_position import (
    SimulatedPosition,
)


class FeeSimulator:
    @staticmethod
    def calculate(
        price: float,
        quantity: float,
        fee_rate: float,
    ) -> float:
        FeeSimulator._validate_price(price)
        FeeSimulator._validate_quantity(quantity)
        FeeSimulator._validate_fee_rate(fee_rate)

        notional = price * quantity

        return notional * fee_rate

    @staticmethod
    def calculate_entry_fee(
        position: SimulatedPosition,
        fee_rate: float,
    ) -> float:
        if not isinstance(
            position,
            SimulatedPosition,
        ):
            raise TypeError(
                "position must be a SimulatedPosition"
            )

        return FeeSimulator.calculate(
            price=position.entry_price,
            quantity=position.quantity,
            fee_rate=fee_rate,
        )

    @staticmethod
    def calculate_exit_fee(
        simulated_exit: SimulatedExit,
        fee_rate: float,
    ) -> float:
        if not isinstance(
            simulated_exit,
            SimulatedExit,
        ):
            raise TypeError(
                "simulated_exit must be a SimulatedExit"
            )

        return FeeSimulator.calculate(
            price=simulated_exit.exit_price,
            quantity=simulated_exit.position.quantity,
            fee_rate=fee_rate,
        )

    @staticmethod
    def _validate_price(
        price: float,
    ) -> None:
        if (
            isinstance(price, bool)
            or not isinstance(
                price,
                (int, float),
            )
        ):
            raise TypeError(
                "price must be a number"
            )

        if (
            not math.isfinite(price)
            or price <= 0
        ):
            raise ValueError(
                "price must be finite "
                "and greater than zero"
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
    def _validate_fee_rate(
        fee_rate: float,
    ) -> None:
        if (
            isinstance(fee_rate, bool)
            or not isinstance(
                fee_rate,
                (int, float),
            )
        ):
            raise TypeError(
                "fee_rate must be a number"
            )

        if (
            not math.isfinite(fee_rate)
            or fee_rate < 0
        ):
            raise ValueError(
                "fee_rate must be finite "
                "and non-negative"
            )
