class StructuralPointClassifier:
    def classify(
        self,
        swing_points: list[dict],
    ) -> list[dict]:
        previous_high = None
        previous_low = None
        previous_index = None
        classified_points = []

        for point in swing_points:
            point_type = point["type"]
            point_index = point["index"]
            point_price = point["price"]

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

            classification = None

            if point_type == "high":
                if previous_high is not None:
                    if point_price > previous_high:
                        classification = "HH"
                    elif point_price < previous_high:
                        classification = "LH"

                previous_high = point_price

            else:
                if previous_low is not None:
                    if point_price > previous_low:
                        classification = "HL"
                    elif point_price < previous_low:
                        classification = "LL"

                previous_low = point_price

            classified_points.append(
                {
                    "index": point_index,
                    "price": point_price,
                    "type": point_type,
                    "classification": classification,
                }
            )

            previous_index = point_index

        return classified_points
