import pytest

from backend.app.data.market_websocket_client import MarketWebSocketClient


def test_market_websocket_client_uses_configured_base_url():
    client = MarketWebSocketClient(
        base_url="wss://fstream.binance.com",
    )

    assert client.base_url == "wss://fstream.binance.com"


@pytest.mark.asyncio
async def test_connect_uses_configured_websocket_url():
    connected_urls = []

    async def mock_connect(url: str):
        connected_urls.append(url)
        return "mock-connection"

    client = MarketWebSocketClient(
        base_url="wss://fstream.binance.com",
        connector=mock_connect,
    )

    connection = await client.connect()

    assert connected_urls == ["wss://fstream.binance.com"]
    assert connection == "mock-connection"


@pytest.mark.asyncio
async def test_receive_trade_returns_message_from_symbol_stream():
    received_urls = []

    class MockConnection:
        async def recv(self):
            return '{"e":"aggTrade","s":"BTCUSDT"}'

    async def mock_connect(url: str):
        received_urls.append(url)
        return MockConnection()

    client = MarketWebSocketClient(
        base_url="wss://fstream.binance.com",
        connector=mock_connect,
    )

    message = await client.receive_trade("BTCUSDT")

    assert received_urls == [
        "wss://fstream.binance.com/ws/btcusdt@aggTrade"
    ]
    assert message == '{"e":"aggTrade","s":"BTCUSDT"}'
