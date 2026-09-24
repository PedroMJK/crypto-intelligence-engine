class OrderBookImbalanceAnalyzer:
    def analyze(
        self,
        bids: list[tuple[float, float]],
        asks: list[tuple[float, float]],
        depth: int,
    ) -> dict:
        if not isinstance(depth, int):
            raise TypeError("depth must be an integer")

        if depth <= 0:
            raise ValueError(
                "depth must be greater than zero"
            )

        if not bids or not asks:
            raise ValueError(
                "bids and asks must not be empty"
            )

        selected_bids = bids[:depth]
        selected_asks = asks[:depth]

        for price, quantity in selected_bids:
            if price <= 0:
                raise ValueError(
                    "bid price must be greater than zero"
                )

            if quantity < 0:
                raise ValueError(
                    "bid quantity cannot be negative"
                )

        for price, quantity in selected_asks:
            if price <= 0:
                raise ValueError(
                    "ask price must be greater than zero"
                )

            if quantity < 0:
                raise ValueError(
                    "ask quantity cannot be negative"
                )

        bid_volume = sum(
            quantity
            for _, quantity in selected_bids
        )

        ask_volume = sum(
            quantity
            for _, quantity in selected_asks
        )

        total_volume = bid_volume + ask_volume

        if total_volume <= 0:
            raise ValueError(
                "total order book volume must be greater than zero"
            )

        imbalance = (
            (bid_volume - ask_volume)
            / total_volume
        )

        if imbalance > 0:
            state = "bid_dominant"
        elif imbalance < 0:
            state = "ask_dominant"
        else:
            state = "balanced"

        return {
            "bid_volume": bid_volume,
            "ask_volume": ask_volume,
            "total_volume": total_volume,
            "imbalance": imbalance,
            "state": state,
        }
