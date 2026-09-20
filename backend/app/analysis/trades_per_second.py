class TradesPerSecond:
    def calculate(
        self,
        trade_count: int,
        window_seconds: float,
    ) -> float:
        if trade_count < 0:
            raise ValueError("trade_count cannot be negative")

        if window_seconds <= 0:
            raise ValueError("window_seconds must be greater than zero")

        return trade_count / window_seconds
