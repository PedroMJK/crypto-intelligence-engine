class StructuralTrendDetector:
    def detect(
        self,
        structural_points: list[dict],
    ) -> str:
        latest_high_classification = None
        latest_low_classification = None
        previous_index = None

        for point in structural_points:
            point_type = point["type"]
            point_index = point["index"]
            classification = point["classification"]

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

            if point_type == "high":
                if classification not in {None, "HH", "LH"}:
                    raise ValueError(
                        "invalid classification for high point"
                    )

                if classification is not None:
                    latest_high_classification = classification

            else:
                if classification not in {None, "HL", "LL"}:
                    raise ValueError(
                        "invalid classification for low point"
                    )

                if classification is not None:
                    latest_low_classification = classification

            previous_index = point_index

        if (
            latest_high_classification == "HH"
            and latest_low_classification == "HL"
        ):
            return "bullish"

        if (
            latest_high_classification == "LH"
            and latest_low_classification == "LL"
        ):
            return "bearish"

        return "indeterminate"
