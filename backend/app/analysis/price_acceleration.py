class PriceAcceleration:
    def calculate(
        self,
        previous_velocity: float,
        current_velocity: float,
        window_seconds: float,
    ) -> float:
        if window_seconds <= 0:
            raise ValueError("window_seconds must be greater than zero")

        velocity_change = current_velocity - previous_velocity

        return velocity_change / window_seconds
