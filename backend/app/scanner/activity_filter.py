class ActivityFilter:
    def __init__(self, min_trade_count: int):
        if min_trade_count < 0:
            raise ValueError("min_trade_count cannot be negative")

        self.min_trade_count = min_trade_count

    def filter(self, pairs: list[dict]) -> list[dict]:
        filtered_pairs = []

        for pair in pairs:
            trade_count = pair["trade_count"]

            if trade_count < 0:
                raise ValueError("trade_count cannot be negative")

            if trade_count >= self.min_trade_count:
                filtered_pairs.append(pair)

        return filtered_pairs
