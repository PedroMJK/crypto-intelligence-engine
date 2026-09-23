class ExponentialMovingAverage:
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

        initial_values = values[:period]
        exponential_average = sum(initial_values) / period
        multiplier = 2 / (period + 1)

        for value in values[period:]:
            exponential_average = (
                (value - exponential_average) * multiplier
                + exponential_average
            )

        return exponential_average
