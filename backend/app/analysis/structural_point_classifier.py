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
            confirmation_index = point.get("confirmation_index")

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

            classified_point = {
                "index": point_index,
                "price": point_price,
                "type": point_type,
                "classification": classification,
            }

            if confirmation_index is not None:
                classified_point["confirmation_index"] = (
                    confirmation_index
                )

            classified_points.append(classified_point)

            previous_index = point_index

        return classified_points
