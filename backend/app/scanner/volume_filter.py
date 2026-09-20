class VolumeFilter:
    def __init__(self, min_quote_volume: float):
        if min_quote_volume < 0:
            raise ValueError("min_quote_volume cannot be negative")

        self.min_quote_volume = min_quote_volume

    def filter(self, pairs: list[dict]) -> list[dict]:
        filtered_pairs = []

        for pair in pairs:
            quote_volume = pair["quote_volume"]

            if quote_volume < 0:
                raise ValueError("quote_volume cannot be negative")

            if quote_volume >= self.min_quote_volume:
                filtered_pairs.append(pair)

        return filtered_pairs
