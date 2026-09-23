class MovingAverageConvergenceDivergence:
    def calculate(
        self,
        values: list[float],
        fast_period: int,
        slow_period: int,
        signal_period: int,
    ) -> dict[str, float]:
        periods = {
            "fast_period": fast_period,
            "slow_period": slow_period,
            "signal_period": signal_period,
        }

        for period_name, period_value in periods.items():
            if not isinstance(period_value, int):
                raise TypeError(
                    f"{period_name} must be an integer"
                )

            if period_value <= 0:
                raise ValueError(
                    f"{period_name} must be greater than zero"
                )

        if fast_period >= slow_period:
            raise ValueError(
                "fast_period must be less than slow_period"
            )

        minimum_values = slow_period + signal_period - 1

        if len(values) < minimum_values:
            raise ValueError(
                "values do not contain enough elements"
            )

        fast_ema_series = self._calculate_ema_series(
            values=values,
            period=fast_period,
        )
        slow_ema_series = self._calculate_ema_series(
            values=values,
            period=slow_period,
        )

        fast_offset = slow_period - fast_period
        aligned_fast_ema_series = fast_ema_series[fast_offset:]

        macd_series = [
            fast_ema - slow_ema
            for fast_ema, slow_ema in zip(
                aligned_fast_ema_series,
                slow_ema_series,
            )
        ]

        signal_series = self._calculate_ema_series(
            values=macd_series,
            period=signal_period,
        )

        macd_value = macd_series[-1]
        signal_value = signal_series[-1]
        histogram = macd_value - signal_value

        return {
            "macd": macd_value,
            "signal": signal_value,
            "histogram": histogram,
        }

    def _calculate_ema_series(
        self,
        values: list[float],
        period: int,
    ) -> list[float]:
        initial_values = values[:period]
        exponential_average = sum(initial_values) / period
        multiplier = 2 / (period + 1)

        exponential_averages = [exponential_average]

        for value in values[period:]:
            exponential_average = (
                (value - exponential_average) * multiplier
                + exponential_average
            )
            exponential_averages.append(exponential_average)

        return exponential_averages
