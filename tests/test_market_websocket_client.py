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
async def test_connect_reconnects_after_connection_failure():
    connection_attempts = []

    async def mock_connect(url: str):
        connection_attempts.append(url)

        if len(connection_attempts) == 1:
            raise ConnectionError("Connection failed")

        return "reconnected"

    async def mock_sleep(delay: float):
        pass

    client = MarketWebSocketClient(
        base_url="wss://fstream.binance.com",
        connector=mock_connect,
        sleeper=mock_sleep,
    )

    connection = await client.connect()

    assert connection_attempts == [
        "wss://fstream.binance.com",
        "wss://fstream.binance.com",
    ]
    assert connection == "reconnected"


@pytest.mark.asyncio
async def test_connect_waits_before_reconnection():
    connection_attempts = []
    sleep_delays = []

    async def mock_connect(url: str):
        connection_attempts.append(url)

        if len(connection_attempts) == 1:
            raise ConnectionError("Connection failed")

        return "reconnected"

    async def mock_sleep(delay: float):
        sleep_delays.append(delay)

    client = MarketWebSocketClient(
        base_url="wss://fstream.binance.com",
        connector=mock_connect,
        sleeper=mock_sleep,
    )

    connection = await client.connect()

    assert connection_attempts == [
        "wss://fstream.binance.com",
        "wss://fstream.binance.com",
    ]
    assert sleep_delays == [1.0]
    assert connection == "reconnected"


@pytest.mark.asyncio
async def test_connect_uses_exponential_backoff_between_reconnection_attempts():
    connection_attempts = []
    sleep_delays = []

    async def mock_connect(url: str):
        connection_attempts.append(url)

        if len(connection_attempts) < 4:
            raise ConnectionError("Connection failed")

        return "reconnected"

    async def mock_sleep(delay: float):
        sleep_delays.append(delay)

    client = MarketWebSocketClient(
        base_url="wss://fstream.binance.com",
        connector=mock_connect,
        sleeper=mock_sleep,
    )

    connection = await client.connect()

    assert connection_attempts == [
        "wss://fstream.binance.com",
        "wss://fstream.binance.com",
        "wss://fstream.binance.com",
        "wss://fstream.binance.com",
    ]
    assert sleep_delays == [1.0, 2.0, 4.0]
    assert connection == "reconnected"


@pytest.mark.asyncio
async def test_connect_raises_after_reconnection_failure():
    connection_attempts = []
    sleep_delays = []

    async def mock_connect(url: str):
        connection_attempts.append(url)
        raise ConnectionError("Connection failed")

    async def mock_sleep(delay: float):
        sleep_delays.append(delay)

    client = MarketWebSocketClient(
        base_url="wss://fstream.binance.com",
        connector=mock_connect,
        sleeper=mock_sleep,
    )

    with pytest.raises(ConnectionError, match="Connection failed"):
        await client.connect()

    assert connection_attempts == [
        "wss://fstream.binance.com",
        "wss://fstream.binance.com",
        "wss://fstream.binance.com",
        "wss://fstream.binance.com",
    ]
    assert sleep_delays == [1.0, 2.0, 4.0]


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


@pytest.mark.asyncio
async def test_receive_trade_reconnects_after_connection_failure():
    connection_attempts = []

    class MockConnection:
        async def recv(self):
            return '{"e":"aggTrade","s":"BTCUSDT"}'

    async def mock_connect(url: str):
        connection_attempts.append(url)

        if len(connection_attempts) == 1:
            raise ConnectionError("Connection failed")

        return MockConnection()

    async def mock_sleep(delay: float):
        pass

    client = MarketWebSocketClient(
        base_url="wss://fstream.binance.com",
        connector=mock_connect,
        sleeper=mock_sleep,
    )

    message = await client.receive_trade("BTCUSDT")

    assert connection_attempts == [
        "wss://fstream.binance.com/ws/btcusdt@aggTrade",
        "wss://fstream.binance.com/ws/btcusdt@aggTrade",
    ]
    assert message == '{"e":"aggTrade","s":"BTCUSDT"}'


@pytest.mark.asyncio
async def test_receive_ticker_returns_message_from_symbol_stream():
    received_urls = []

    class MockConnection:
        async def recv(self):
            return '{"e":"24hrMiniTicker","s":"BTCUSDT"}'

    async def mock_connect(url: str):
        received_urls.append(url)
        return MockConnection()

    client = MarketWebSocketClient(
        base_url="wss://fstream.binance.com",
        connector=mock_connect,
    )

    message = await client.receive_ticker("BTCUSDT")

    assert received_urls == [
        "wss://fstream.binance.com/ws/btcusdt@miniTicker"
    ]
    assert message == '{"e":"24hrMiniTicker","s":"BTCUSDT"}'


@pytest.mark.asyncio
async def test_receive_candle_returns_message_from_symbol_interval_stream():
    received_urls = []

    class MockConnection:
        async def recv(self):
            return '{"e":"kline","s":"BTCUSDT"}'

    async def mock_connect(url: str):
        received_urls.append(url)
        return MockConnection()

    client = MarketWebSocketClient(
        base_url="wss://fstream.binance.com",
        connector=mock_connect,
    )

    message = await client.receive_candle("BTCUSDT", "1m")

    assert received_urls == [
        "wss://fstream.binance.com/ws/btcusdt@kline_1m"
    ]
    assert message == '{"e":"kline","s":"BTCUSDT"}'


@pytest.mark.asyncio
async def test_receive_order_book_returns_message_from_symbol_stream():
    received_urls = []

    class MockConnection:
        async def recv(self):
            return '{"e":"depthUpdate","s":"BTCUSDT"}'

    async def mock_connect(url: str):
        received_urls.append(url)
        return MockConnection()

    client = MarketWebSocketClient(
        base_url="wss://fstream.binance.com",
        connector=mock_connect,
    )

    message = await client.receive_order_book("BTCUSDT")

    assert received_urls == [
        "wss://fstream.binance.com/ws/btcusdt@depth"
    ]
    assert message == '{"e":"depthUpdate","s":"BTCUSDT"}'
