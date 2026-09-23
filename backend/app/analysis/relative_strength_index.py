class RelativeStrengthIndex:
    def calculate(
        self,
        values: list[float],
        period: int,
    ) -> float:
        if not isinstance(period, int):
            raise TypeError("period must be an integer")

        if period <= 0:
            raise ValueError("period must be greater than zero")

        if len(values) < period + 1:
            raise ValueError(
                "values must contain at least period plus one elements"
            )

        changes = [
            current_value - previous_value
            for previous_value, current_value in zip(
                values,
                values[1:],
            )
        ]

        initial_changes = changes[:period]

        average_gain = (
            sum(max(change, 0.0) for change in initial_changes)
            / period
        )
        average_loss = (
            sum(max(-change, 0.0) for change in initial_changes)
            / period
        )

        for change in changes[period:]:
            gain = max(change, 0.0)
            loss = max(-change, 0.0)

            average_gain = (
                (average_gain * (period - 1)) + gain
            ) / period
            average_loss = (
                (average_loss * (period - 1)) + loss
            ) / period

        if average_gain == 0 and average_loss == 0:
            return 50.0

        if average_loss == 0:
            return 100.0

        if average_gain == 0:
            return 0.0

        relative_strength = average_gain / average_loss

        return 100 - (100 / (1 + relative_strength))
