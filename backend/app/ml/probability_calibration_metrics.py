from dataclasses import dataclass


@dataclass(frozen=True)
class ProbabilityCalibrationMetrics:
    brier_score: float
    log_loss: float
