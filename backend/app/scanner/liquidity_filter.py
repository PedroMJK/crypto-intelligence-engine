class LiquidityFilter:
    def __init__(self, max_spread_ratio: float):
        if max_spread_ratio < 0:
            raise ValueError("max_spread_ratio cannot be negative")

        self.max_spread_ratio = max_spread_ratio

    def filter(self, pairs: list[dict]) -> list[dict]:
        filtered_pairs = []

        for pair in pairs:
            bid_price = pair["bid_price"]
            ask_price = pair["ask_price"]

            if bid_price <= 0 or ask_price <= 0:
                raise ValueError(
                    "bid_price and ask_price must be greater than zero"
                )

            if ask_price < bid_price:
                raise ValueError(
                    "ask_price cannot be lower than bid_price"
                )

            mid_price = (bid_price + ask_price) / 2
            spread_ratio = (ask_price - bid_price) / mid_price

            if spread_ratio <= self.max_spread_ratio:
                filtered_pairs.append(pair)

        return filtered_pairs
