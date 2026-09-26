from dataclasses import dataclass


@dataclass(frozen=True)
class RegressionMetrics:
    mae: float
    mse: float
    rmse: float
