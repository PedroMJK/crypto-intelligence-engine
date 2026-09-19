class PriceFilter:
    def __init__(self, min_price: float, max_price: float):
        if min_price > max_price:
            raise ValueError("min_price cannot be greater than max_price")

        self.min_price = min_price
        self.max_price = max_price

    def filter(self, pairs: list[dict]) -> list[dict]:
        return [
            pair
            for pair in pairs
            if self.min_price <= pair["price"] <= self.max_price
        ]
