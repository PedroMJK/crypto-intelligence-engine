class ContradictionEngine:
    def calculate(
        self,
        signals: list[float],
    ) -> float:
        if not isinstance(signals, list):
            raise TypeError(
                "signals must be a list"
            )

        if not signals:
            raise ValueError(
                "signals must not be empty"
            )

        if not all(
            isinstance(signal, (int, float))
            and not isinstance(signal, bool)
            for signal in signals
        ):
            raise TypeError(
                "signals must contain only numbers"
            )

        if not all(
            -1.0 <= signal <= 1.0
            for signal in signals
        ):
            raise ValueError(
                "signals must be between -1.0 and 1.0"
            )

        bullish_strength = sum(
            signal
            for signal in signals
            if signal > 0.0
        ) / len(signals)

        bearish_strength = sum(
            abs(signal)
            for signal in signals
            if signal < 0.0
        ) / len(signals)

        return 2.0 * min(
            bullish_strength,
            bearish_strength,
        )
