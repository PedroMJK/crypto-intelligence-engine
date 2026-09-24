class BreakOfStructureDetector:
    def detect(
        self,
        structural_points: list[dict],
        closes: list[float],
    ) -> list[dict]:
        previous_point_index = None
        break_events = []

        for point in structural_points:
            point_type = point["type"]
            point_index = point["index"]

            if point_type not in {"high", "low"}:
                raise ValueError(
                    "point type must be high or low"
                )

            if (
                previous_point_index is not None
                and point_index <= previous_point_index
            ):
                raise ValueError(
                    "points must be in chronological order"
                )

            confirmation_index = point.get(
                "confirmation_index"
            )

            if confirmation_index is None:
                previous_point_index = point_index
                continue

            if confirmation_index < point_index:
                raise ValueError(
                    "confirmation index cannot be lower "
                    "than point index"
                )

            if confirmation_index >= len(closes):
                raise ValueError(
                    "confirmation index must reference "
                    "an existing close"
                )

            level = point["price"]
            start_index = confirmation_index + 1

            for close_index in range(
                start_index,
                len(closes),
            ):
                close = closes[close_index]

                if (
                    point_type == "high"
                    and close > level
                ):
                    break_events.append(
                        {
                            "index": close_index,
                            "direction": "bullish",
                            "level": level,
                            "structural_point_index": point_index,
                            "structural_point_confirmation_index": (
                                confirmation_index
                            ),
                        }
                    )
                    break

                if (
                    point_type == "low"
                    and close < level
                ):
                    break_events.append(
                        {
                            "index": close_index,
                            "direction": "bearish",
                            "level": level,
                            "structural_point_index": point_index,
                            "structural_point_confirmation_index": (
                                confirmation_index
                            ),
                        }
                    )
                    break

            previous_point_index = point_index

        return sorted(
            break_events,
            key=lambda event: event["index"],
        )
