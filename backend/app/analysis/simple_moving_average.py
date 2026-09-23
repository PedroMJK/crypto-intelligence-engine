class SimpleMovingAverage:
    def calculate(
        self,
        values: list[float],
        period: int,
    ) -> float:
        if not isinstance(period, int):
            raise TypeError("period must be an integer")

        if period <= 0:
            raise ValueError("period must be greater than zero")

        if len(values) < period:
            raise ValueError(
                "values must contain at least period elements"
            )

        period_values = values[-period:]

        return sum(period_values) / period
