class PriceVelocity:
    def calculate(
        self,
        previous_price: float,
        current_price: float,
        window_seconds: float,
    ) -> float:
        if previous_price <= 0:
            raise ValueError("previous_price must be greater than zero")

        if current_price <= 0:
            raise ValueError("current_price must be greater than zero")

        if window_seconds <= 0:
            raise ValueError("window_seconds must be greater than zero")

        price_change_ratio = (
            current_price - previous_price
        ) / previous_price

        return price_change_ratio / window_seconds
