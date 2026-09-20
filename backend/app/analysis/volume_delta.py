class VolumeDelta:
    def calculate(
        self,
        buy_volume: float,
        sell_volume: float,
    ) -> float:
        if buy_volume < 0:
            raise ValueError("buy_volume cannot be negative")

        if sell_volume < 0:
            raise ValueError("sell_volume cannot be negative")

        return buy_volume - sell_volume
