class ScannerRanking:
    def rank(self, pairs: list[dict]) -> list[dict]:
        return sorted(
            pairs,
            key=lambda pair: (
                -pair["trade_count"],
                pair["symbol"],
            ),
        )
