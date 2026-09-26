from dataclasses import dataclass

from backend.app.paper_trading.trade_performance import (
    TradePerformance,
)


@dataclass(frozen=True)
class PerformanceMetrics:
    total_trades: int
    winning_trades: int
    losing_trades: int
    breakeven_trades: int
    win_rate: float
    gross_pnl: float
    total_fees: float
    net_pnl: float

    @classmethod
    def calculate(
        cls,
        trades: list[TradePerformance]
        | tuple[TradePerformance, ...],
    ) -> "PerformanceMetrics":
        cls._validate_trades(trades)

        total_trades = len(trades)

        winning_trades = sum(
            trade.net_pnl > 0
            for trade in trades
        )
        losing_trades = sum(
            trade.net_pnl < 0
            for trade in trades
        )
        breakeven_trades = sum(
            trade.net_pnl == 0
            for trade in trades
        )

        if total_trades == 0:
            win_rate = 0.0
        else:
            win_rate = (
                winning_trades / total_trades
            )

        gross_pnl = sum(
            trade.gross_pnl
            for trade in trades
        )
        total_fees = sum(
            trade.total_fees
            for trade in trades
        )
        net_pnl = sum(
            trade.net_pnl
            for trade in trades
        )

        return cls(
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            breakeven_trades=breakeven_trades,
            win_rate=win_rate,
            gross_pnl=gross_pnl,
            total_fees=total_fees,
            net_pnl=net_pnl,
        )

    @staticmethod
    def _validate_trades(
        trades: list[TradePerformance]
        | tuple[TradePerformance, ...],
    ) -> None:
        if not isinstance(
            trades,
            (list, tuple),
        ):
            raise TypeError(
                "trades must be a list or tuple"
            )

        if not all(
            isinstance(
                trade,
                TradePerformance,
            )
            for trade in trades
        ):
            raise TypeError(
                "all trades must be "
                "TradePerformance instances"
            )
