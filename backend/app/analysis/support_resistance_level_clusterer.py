class SupportResistanceLevelClusterer:
    def __init__(
        self,
        tolerance_ratio: float,
    ) -> None:
        if tolerance_ratio < 0:
            raise ValueError(
                "tolerance ratio cannot be negative"
            )

        self.tolerance_ratio = tolerance_ratio

    def cluster(
        self,
        levels: list[dict],
    ) -> list[dict]:
        clusters = []
        previous_index = None
        previous_confirmation_index = None

        for level in levels:
            if level["type"] not in {"support", "resistance"}:
                raise ValueError(
                    "level type must be support or resistance"
                )

            if level["price"] <= 0:
                raise ValueError(
                    "level price must be greater than zero"
                )

            if (
                previous_index is not None
                and level["index"] <= previous_index
            ):
                raise ValueError(
                    "levels must be in chronological order"
                )

            confirmation_index = level[
                "confirmation_index"
            ]

            if confirmation_index < level["index"]:
                raise ValueError(
                    "confirmation index cannot be lower "
                    "than level index"
                )

            if (
                previous_confirmation_index is not None
                and confirmation_index
                < previous_confirmation_index
            ):
                raise ValueError(
                    "level confirmations must be in "
                    "chronological order"
                )

            matching_cluster = None

            for cluster in clusters:
                if cluster["type"] != level["type"]:
                    continue

                distance_ratio = abs(
                    level["price"] - cluster["price"]
                ) / cluster["price"]

                if distance_ratio <= self.tolerance_ratio:
                    matching_cluster = cluster
                    break

            if matching_cluster is None:
                clusters.append(
                    {
                        "type": level["type"],
                        "price": level["price"],
                        "level_count": 1,
                        "level_indices": [level["index"]],
                        "confirmation_index": confirmation_index,
                    }
                )

                previous_index = level["index"]
                previous_confirmation_index = (
                    confirmation_index
                )
                continue

            previous_count = matching_cluster[
                "level_count"
            ]
            new_count = previous_count + 1

            matching_cluster["price"] = (
                (
                    matching_cluster["price"]
                    * previous_count
                )
                + level["price"]
            ) / new_count

            matching_cluster["level_count"] = new_count
            matching_cluster["level_indices"].append(
                level["index"]
            )
            matching_cluster["confirmation_index"] = (
                confirmation_index
            )

            previous_index = level["index"]
            previous_confirmation_index = (
                confirmation_index
            )

        return clusters
