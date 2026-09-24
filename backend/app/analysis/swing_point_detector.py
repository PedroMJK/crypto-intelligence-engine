class SwingPointDetector:
    def detect(
        self,
        highs: list[float],
        lows: list[float],
        window: int,
    ) -> list[dict]:
        if not isinstance(window, int):
            raise TypeError("window must be an integer")

        if window <= 0:
            raise ValueError("window must be greater than zero")

        if len(highs) != len(lows):
            raise ValueError(
                "highs and lows must have the same length"
            )

        minimum_length = (2 * window) + 1

        if len(highs) < minimum_length:
            raise ValueError(
                "price series must contain at least "
                "2 * window + 1 elements"
            )

        for high, low in zip(highs, lows):
            if high < low:
                raise ValueError("high cannot be lower than low")

        swing_points = []

        for index in range(window, len(highs) - window):
            current_high = highs[index]
            current_low = lows[index]

            neighboring_highs = (
                highs[index - window:index]
                + highs[index + 1:index + window + 1]
            )
            neighboring_lows = (
                lows[index - window:index]
                + lows[index + 1:index + window + 1]
            )

            is_swing_high = all(
                current_high > high
                for high in neighboring_highs
            )
            is_swing_low = all(
                current_low < low
                for low in neighboring_lows
            )

            if is_swing_high:
                swing_points.append(
                    {
                        "index": index,
                        "confirmation_index": index + window,
                        "price": current_high,
                        "type": "high",
                    }
                )

            if is_swing_low:
                swing_points.append(
                    {
                        "index": index,
                        "confirmation_index": index + window,
                        "price": current_low,
                        "type": "low",
                    }
                )

        return swing_points
