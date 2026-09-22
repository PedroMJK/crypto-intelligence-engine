class PressureTransition:
    def calculate(
        self,
        previous_score: float,
        current_score: float,
    ) -> float:
        scores = {
            "previous_score": previous_score,
            "current_score": current_score,
        }

        for score_name, score_value in scores.items():
            if not -1.0 <= score_value <= 1.0:
                raise ValueError(
                    f"{score_name} must be between -1.0 and 1.0"
                )

        return current_score - previous_score
