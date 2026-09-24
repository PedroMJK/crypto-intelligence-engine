class SupportResistanceTouchDetector:
    def detect(
        self,
        zones: list[dict],
        highs: list[float],
        lows: list[float],
    ) -> list[dict]:
        if len(highs) != len(lows):
            raise ValueError(
                "highs and lows must have the same length"
            )

        for high, low in zip(highs, lows):
            if high < low:
                raise ValueError(
                    "high cannot be lower than low"
                )

        touch_events = []

        for zone in zones:
            if zone["type"] not in {"support", "resistance"}:
                raise ValueError(
                    "zone type must be support or resistance"
                )

            if zone["price"] <= 0:
                raise ValueError(
                    "zone price must be greater than zero"
                )

            confirmation_index = zone["confirmation_index"]

            if confirmation_index < 0:
                raise ValueError(
                    "confirmation index cannot be negative"
                )

            if confirmation_index >= len(highs):
                raise ValueError(
                    "confirmation index must reference "
                    "an existing candle"
                )

            start_index = confirmation_index + 1

            for index in range(start_index, len(highs)):
                if lows[index] <= zone["price"] <= highs[index]:
                    touch_events.append(
                        {
                            "index": index,
                            "type": zone["type"],
                            "price": zone["price"],
                            "zone_confirmation_index": (
                                confirmation_index
                            ),
                        }
                    )

        return sorted(
            touch_events,
            key=lambda event: event["index"],
        )
