class SupportResistanceLevelStrengthCalculator:
    def calculate(
        self,
        zones: list[dict],
        touch_events: list[dict],
    ) -> list[dict]:
        for zone in zones:
            if zone["type"] not in {
                "support",
                "resistance",
            }:
                raise ValueError(
                    "zone type must be support or resistance"
                )

            if zone["price"] <= 0:
                raise ValueError(
                    "zone price must be greater than zero"
                )

            if (
                not isinstance(zone["level_count"], int)
                or isinstance(zone["level_count"], bool)
                or zone["level_count"] <= 0
            ):
                raise ValueError(
                    "level count must be a positive integer"
                )

            if zone["confirmation_index"] < 0:
                raise ValueError(
                    "confirmation index cannot be negative"
                )

        for touch in touch_events:
            if touch["type"] not in {
                "support",
                "resistance",
            }:
                raise ValueError(
                    "touch type must be support or resistance"
                )

            if touch["price"] <= 0:
                raise ValueError(
                    "touch price must be greater than zero"
                )

            matching_zone = next(
                (
                    zone
                    for zone in zones
                    if (
                        zone["type"] == touch["type"]
                        and zone["price"] == touch["price"]
                        and zone["confirmation_index"]
                        == touch["zone_confirmation_index"]
                    )
                ),
                None,
            )

            if matching_zone is None:
                raise ValueError(
                    "touch event must reference "
                    "an existing zone"
                )

            if (
                touch["index"]
                <= matching_zone["confirmation_index"]
            ):
                raise ValueError(
                    "touch index must be greater than "
                    "zone confirmation index"
                )

        strength_events = []

        for zone in zones:
            touch_count = 0

            strength_events.append(
                {
                    "index": zone["confirmation_index"],
                    "type": zone["type"],
                    "price": zone["price"],
                    "level_count": zone["level_count"],
                    "touch_count": touch_count,
                    "strength": zone["level_count"],
                    "zone_confirmation_index": (
                        zone["confirmation_index"]
                    ),
                }
            )

            matching_touches = [
                touch
                for touch in touch_events
                if (
                    touch["type"] == zone["type"]
                    and touch["price"] == zone["price"]
                    and touch["zone_confirmation_index"]
                    == zone["confirmation_index"]
                )
            ]

            matching_touches = sorted(
                matching_touches,
                key=lambda touch: touch["index"],
            )

            for touch in matching_touches:
                touch_count += 1

                strength_events.append(
                    {
                        "index": touch["index"],
                        "type": zone["type"],
                        "price": zone["price"],
                        "level_count": zone["level_count"],
                        "touch_count": touch_count,
                        "strength": (
                            zone["level_count"]
                            + touch_count
                        ),
                        "zone_confirmation_index": (
                            zone["confirmation_index"]
                        ),
                    }
                )

        return sorted(
            strength_events,
            key=lambda event: event["index"],
        )
