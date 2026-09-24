class AverageTrueRange:
    def calculate(
        self,
        highs: list[float],
        lows: list[float],
        closes: list[float],
        period: int,
    ) -> float:
        if not isinstance(period, int):
            raise TypeError("period must be an integer")

        if period <= 0:
            raise ValueError("period must be greater than zero")

        if not (
            len(highs) == len(lows) == len(closes)
        ):
            raise ValueError(
                "highs, lows, and closes must have the same length"
            )

        if len(highs) < period:
            raise ValueError(
                "price series must contain at least period elements"
            )

        true_ranges = []

        for index, (high, low) in enumerate(zip(highs, lows)):
            if high < low:
                raise ValueError("high cannot be lower than low")

            if index == 0:
                true_range = high - low
            else:
                previous_close = closes[index - 1]
                true_range = max(
                    high - low,
                    abs(high - previous_close),
                    abs(low - previous_close),
                )

            true_ranges.append(true_range)

        initial_true_ranges = true_ranges[:period]
        average_true_range = (
            sum(initial_true_ranges) / period
        )

        for true_range in true_ranges[period:]:
            average_true_range = (
                (
                    average_true_range * (period - 1)
                )
                + true_range
            ) / period

        return average_true_range

    def calculate_series(
        self,
        highs: list[float],
        lows: list[float],
        closes: list[float],
        period: int,
    ) -> list[float]:
        if not isinstance(period, int):
            raise TypeError("period must be an integer")

        if period <= 0:
            raise ValueError("period must be greater than zero")

        if not (
            len(highs) == len(lows) == len(closes)
        ):
            raise ValueError(
                "highs, lows, and closes must have the same length"
            )

        if len(highs) < period:
            raise ValueError(
                "price series must contain at least period elements"
            )

        true_ranges = []

        for index, (high, low) in enumerate(
            zip(highs, lows)
        ):
            if high < low:
                raise ValueError(
                    "high cannot be lower than low"
                )

            if index == 0:
                true_range = high - low
            else:
                previous_close = closes[index - 1]
                true_range = max(
                    high - low,
                    abs(high - previous_close),
                    abs(low - previous_close),
                )

            true_ranges.append(true_range)

        initial_true_ranges = true_ranges[:period]
        average_true_range = (
            sum(initial_true_ranges) / period
        )

        atr_values = [average_true_range]

        for true_range in true_ranges[period:]:
            average_true_range = (
                (
                    average_true_range * (period - 1)
                )
                + true_range
            ) / period

            atr_values.append(average_true_range)

        return atr_values
