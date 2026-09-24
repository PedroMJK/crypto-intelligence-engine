class VolatilityAnalyzer:
    def analyze(
        self,
        atr_values: list[float],
        lookback: int,
    ) -> dict:
        if not isinstance(lookback, int):
            raise TypeError(
                "lookback must be an integer"
            )

        if lookback <= 0:
            raise ValueError(
                "lookback must be greater than zero"
            )

        if len(atr_values) < lookback + 1:
            raise ValueError(
                "atr_values must contain the current ATR "
                "and at least lookback previous values"
            )

        if any(
            atr_value < 0
            for atr_value in atr_values
        ):
            raise ValueError(
                "ATR values cannot be negative"
            )

        current_atr = atr_values[-1]

        reference_values = atr_values[
            -(lookback + 1):-1
        ]

        reference_atr = (
            sum(reference_values) / lookback
        )

        if reference_atr <= 0:
            raise ValueError(
                "reference ATR must be greater than zero"
            )

        ratio = current_atr / reference_atr
        change = ratio - 1.0

        if ratio > 1.0:
            state = "expanding"
        elif ratio < 1.0:
            state = "contracting"
        else:
            state = "stable"

        return {
            "current_atr": current_atr,
            "reference_atr": reference_atr,
            "ratio": ratio,
            "change": change,
            "state": state,
        }
