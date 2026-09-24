class SupportResistanceLevelBreakDetector:
    def detect(
        self,
        zones: list[dict],
        closes: list[float],
    ) -> list[dict]:
        break_events = []

        for zone in zones:
            zone_type = zone["type"]
            price = zone["price"]
            confirmation_index = zone["confirmation_index"]

            if zone_type not in {
                "support",
                "resistance",
            }:
                raise ValueError(
                    "zone type must be support or resistance"
                )

            if price <= 0:
                raise ValueError(
                    "zone price must be greater than zero"
                )

            if confirmation_index < 0:
                raise ValueError(
                    "confirmation index cannot be negative"
                )

            if confirmation_index >= len(closes):
                raise ValueError(
                    "confirmation index must reference "
                    "an existing close"
                )

            start_index = confirmation_index + 1

            for index in range(
                start_index,
                len(closes),
            ):
                close = closes[index]

                if (
                    zone_type == "resistance"
                    and close > price
                ):
                    break_events.append(
                        {
                            "index": index,
                            "type": zone_type,
                            "price": price,
                            "close": close,
                            "zone_confirmation_index": (
                                confirmation_index
                            ),
                        }
                    )
                    break

                if (
                    zone_type == "support"
                    and close < price
                ):
                    break_events.append(
                        {
                            "index": index,
                            "type": zone_type,
                            "price": price,
                            "close": close,
                            "zone_confirmation_index": (
                                confirmation_index
                            ),
                        }
                    )
                    break

        return sorted(
            break_events,
            key=lambda event: event["index"],
        )
