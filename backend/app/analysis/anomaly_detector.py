import math


class AnomalyDetector:
    def analyze(
        self,
        historical_values: list[float],
        current_value: float,
    ) -> dict:
        if not isinstance(historical_values, list):
            raise TypeError(
                "historical values must be a list"
            )

        if not historical_values:
            raise ValueError(
                "historical values must not be empty"
            )

        if not all(
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            for value in historical_values
        ):
            raise TypeError(
                "historical values must contain only numbers"
            )

        if (
            not isinstance(current_value, (int, float))
            or isinstance(current_value, bool)
        ):
            raise TypeError(
                "current value must be a number"
            )

        mean = sum(historical_values) / len(
            historical_values
        )

        variance = sum(
            (value - mean) ** 2
            for value in historical_values
        ) / len(historical_values)

        standard_deviation = math.sqrt(variance)

        if standard_deviation == 0:
            raise ValueError(
                "historical standard deviation must be greater than zero"
            )

        deviation = current_value - mean
        z_score = deviation / standard_deviation

        return {
            "current_value": current_value,
            "mean": mean,
            "standard_deviation": standard_deviation,
            "deviation": deviation,
            "z_score": z_score,
        }
