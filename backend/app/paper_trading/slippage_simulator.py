import math

from backend.app.paper_trading.position_side import (
    PositionSide,
)
from backend.app.paper_trading.simulated_exit import (
    SimulatedExit,
)
from backend.app.paper_trading.simulated_position import (
    SimulatedPosition,
)


class SlippageSimulator:
    @staticmethod
    def calculate_execution_price(
        price: float,
        slippage_rate: float,
        is_buy: bool,
    ) -> float:
        SlippageSimulator._validate_price(price)
        SlippageSimulator._validate_slippage_rate(
            slippage_rate
        )
        SlippageSimulator._validate_is_buy(is_buy)

        if is_buy:
            return price * (1 + slippage_rate)

        return price * (1 - slippage_rate)

    @staticmethod
    def calculate_entry_price(
        position: SimulatedPosition,
        slippage_rate: float,
    ) -> float:
        if not isinstance(
            position,
            SimulatedPosition,
        ):
            raise TypeError(
                "position must be a SimulatedPosition"
            )

        is_buy = position.side is PositionSide.LONG

        return (
            SlippageSimulator.calculate_execution_price(
                price=position.entry_price,
                slippage_rate=slippage_rate,
                is_buy=is_buy,
            )
        )

    @staticmethod
    def calculate_exit_price(
        simulated_exit: SimulatedExit,
        slippage_rate: float,
    ) -> float:
        if not isinstance(
            simulated_exit,
            SimulatedExit,
        ):
            raise TypeError(
                "simulated_exit must be a SimulatedExit"
            )

        is_buy = (
            simulated_exit.position.side
            is PositionSide.SHORT
        )

        return (
            SlippageSimulator.calculate_execution_price(
                price=simulated_exit.exit_price,
                slippage_rate=slippage_rate,
                is_buy=is_buy,
            )
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
    def _validate_slippage_rate(
        slippage_rate: float,
    ) -> None:
        if (
            isinstance(slippage_rate, bool)
            or not isinstance(
                slippage_rate,
                (int, float),
            )
        ):
            raise TypeError(
                "slippage_rate must be a number"
            )

        if (
            not math.isfinite(slippage_rate)
            or slippage_rate < 0
            or slippage_rate >= 1
        ):
            raise ValueError(
                "slippage_rate must be finite "
                "and between zero and one"
            )

    @staticmethod
    def _validate_is_buy(
        is_buy: bool,
    ) -> None:
        if not isinstance(is_buy, bool):
            raise TypeError(
                "is_buy must be a bool"
            )
