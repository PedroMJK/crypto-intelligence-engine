from backend.app.scanner.scanner_ranking import ScannerRanking


def test_ranking_orders_pairs_by_trade_count_descending():
    ranking = ScannerRanking()

    pairs = [
        {
            "symbol": "LOWACTIVITYUSDT",
            "trade_count": 1_000,
        },
        {
            "symbol": "HIGHACTIVITYUSDT",
            "trade_count": 5_000,
        },
        {
            "symbol": "MIDACTIVITYUSDT",
            "trade_count": 2_500,
        },
    ]

    result = ranking.rank(pairs)

    assert result == [
        {
            "symbol": "HIGHACTIVITYUSDT",
            "trade_count": 5_000,
        },
        {
            "symbol": "MIDACTIVITYUSDT",
            "trade_count": 2_500,
        },
        {
            "symbol": "LOWACTIVITYUSDT",
            "trade_count": 1_000,
        },
    ]


def test_ranking_orders_equal_trade_counts_by_symbol():
    ranking = ScannerRanking()

    pairs = [
        {
            "symbol": "BETAUSDT",
            "trade_count": 5_000,
        },
        {
            "symbol": "ALPHAUSDT",
            "trade_count": 5_000,
        },
    ]

    result = ranking.rank(pairs)

    assert result == [
        {
            "symbol": "ALPHAUSDT",
            "trade_count": 5_000,
        },
        {
            "symbol": "BETAUSDT",
            "trade_count": 5_000,
        },
    ]
