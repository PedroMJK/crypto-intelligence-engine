class SupportResistanceLevelDetector:
    def detect(
        self,
        swing_points: list[dict],
    ) -> list[dict]:
        previous_index = None
        levels = []

        for point in swing_points:
            point_type = point["type"]
            point_index = point["index"]

            if point_type not in {"high", "low"}:
                raise ValueError(
                    "point type must be high or low"
                )

            if (
                previous_index is not None
                and point_index <= previous_index
            ):
                raise ValueError(
                    "points must be in chronological order"
                )

            confirmation_index = point.get(
                "confirmation_index"
            )

            if confirmation_index is None:
                previous_index = point_index
                continue

            if confirmation_index < point_index:
                raise ValueError(
                    "confirmation index cannot be lower "
                    "than point index"
                )

            level_type = (
                "resistance"
                if point_type == "high"
                else "support"
            )

            levels.append(
                {
                    "index": point_index,
                    "confirmation_index": confirmation_index,
                    "price": point["price"],
                    "type": level_type,
                }
            )

            previous_index = point_index

        return levels
