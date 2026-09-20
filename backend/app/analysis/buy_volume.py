class BuyVolume:
    def calculate(self, trade: dict) -> float:
        quantity = float(trade["q"])

        if quantity < 0:
            raise ValueError("trade quantity cannot be negative")

        if trade["m"]:
            return 0.0

        return quantity
