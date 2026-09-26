from dataclasses import dataclass

from backend.app.paper_trading.fee_simulator import (
    FeeSimulator,
)
from backend.app.paper_trading.position_side import (
    PositionSide,
)
from backend.app.paper_trading.simulated_exit import (
    SimulatedExit,
)
from backend.app.paper_trading.slippage_simulator import (
    SlippageSimulator,
)


@dataclass(frozen=True)
class TradePerformance:
    entry_execution_price: float
    exit_execution_price: float
    gross_pnl: float
    entry_fee: float
    exit_fee: float
    total_fees: float
    net_pnl: float
    return_rate: float

    @classmethod
    def calculate(
        cls,
        simulated_exit: SimulatedExit,
        entry_fee_rate: float,
        exit_fee_rate: float,
        slippage_rate: float,
    ) -> "TradePerformance":
        cls._validate_simulated_exit(
            simulated_exit
        )

        entry_execution_price = (
            SlippageSimulator.calculate_entry_price(
                position=simulated_exit.position,
                slippage_rate=slippage_rate,
            )
        )

        exit_execution_price = (
            SlippageSimulator.calculate_exit_price(
                simulated_exit=simulated_exit,
                slippage_rate=slippage_rate,
            )
        )

        quantity = simulated_exit.position.quantity

        entry_fee = FeeSimulator.calculate(
            price=entry_execution_price,
            quantity=quantity,
            fee_rate=entry_fee_rate,
        )

        exit_fee = FeeSimulator.calculate(
            price=exit_execution_price,
            quantity=quantity,
            fee_rate=exit_fee_rate,
        )

        gross_pnl = cls._calculate_gross_pnl(
            side=simulated_exit.position.side,
            quantity=quantity,
            entry_execution_price=(
                entry_execution_price
            ),
            exit_execution_price=(
                exit_execution_price
            ),
        )

        total_fees = entry_fee + exit_fee
        net_pnl = gross_pnl - total_fees

        entry_notional = (
            entry_execution_price * quantity
        )
        return_rate = net_pnl / entry_notional

        return cls(
            entry_execution_price=(
                entry_execution_price
            ),
            exit_execution_price=(
                exit_execution_price
            ),
            gross_pnl=gross_pnl,
            entry_fee=entry_fee,
            exit_fee=exit_fee,
            total_fees=total_fees,
            net_pnl=net_pnl,
            return_rate=return_rate,
        )

    @staticmethod
    def _calculate_gross_pnl(
        side: PositionSide,
        quantity: float,
        entry_execution_price: float,
        exit_execution_price: float,
    ) -> float:
        if side is PositionSide.LONG:
            price_difference = (
                exit_execution_price
                - entry_execution_price
            )
        else:
            price_difference = (
                entry_execution_price
                - exit_execution_price
            )

        return price_difference * quantity

    @staticmethod
    def _validate_simulated_exit(
        simulated_exit: SimulatedExit,
    ) -> None:
        if not isinstance(
            simulated_exit,
            SimulatedExit,
        ):
            raise TypeError(
                "simulated_exit must be a SimulatedExit"
            )
