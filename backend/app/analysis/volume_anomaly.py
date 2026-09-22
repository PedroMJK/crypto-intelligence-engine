class VolumeAnomaly:
    def calculate(
        self,
        current_volume: float,
        baseline_volume: float,
    ) -> float:
        if current_volume < 0:
            raise ValueError("current_volume cannot be negative")

        if baseline_volume <= 0:
            raise ValueError("baseline_volume must be greater than zero")

        return current_volume / baseline_volume
