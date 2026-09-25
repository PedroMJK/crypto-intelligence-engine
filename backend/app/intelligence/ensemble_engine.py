import math
from dataclasses import dataclass


@dataclass(frozen=True)
class EnsembleResult:
    direction_score: float
    volume_score: float
    confidence: float
    contradiction: float


class EnsembleEngine:
    def calculate(
        self,
        technical_score: float,
        flow_score: float,
        momentum_score: float,
        structure_score: float,
        volume_score: float,
        confidence: float,
        contradiction: float,
    ) -> EnsembleResult:
        directional_scores = {
            "technical_score": technical_score,
            "flow_score": flow_score,
            "momentum_score": momentum_score,
            "structure_score": structure_score,
        }

        non_directional_scores = {
            "volume_score": volume_score,
            "confidence": confidence,
            "contradiction": contradiction,
        }

        all_scores = {
            **directional_scores,
            **non_directional_scores,
        }

        for score_name, score_value in all_scores.items():
            if (
                not isinstance(score_value, (int, float))
                or isinstance(score_value, bool)
            ):
                raise TypeError(
                    f"{score_name} must be a number"
                )

            if not math.isfinite(score_value):
                raise ValueError(
                    f"{score_name} must be finite"
                )

        for score_name, score_value in directional_scores.items():
            if not -1.0 <= score_value <= 1.0:
                raise ValueError(
                    f"{score_name} must be between -1.0 and 1.0"
                )

        for score_name, score_value in non_directional_scores.items():
            if not 0.0 <= score_value <= 1.0:
                raise ValueError(
                    f"{score_name} must be between 0.0 and 1.0"
                )

        direction_score = (
            sum(directional_scores.values())
            / len(directional_scores)
        )

        return EnsembleResult(
            direction_score=direction_score,
            volume_score=volume_score,
            confidence=confidence,
            contradiction=contradiction,
        )
