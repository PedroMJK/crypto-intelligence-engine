import httpx
import pytest

from backend.app.data.market_data_client import MarketDataClient


def test_market_data_client_uses_configured_base_url():
    client = MarketDataClient(base_url="https://fapi.binance.com")

    assert client.base_url == "https://fapi.binance.com"


@pytest.mark.asyncio
async def test_get_server_time_returns_response_data():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/fapi/v1/time"

        return httpx.Response(
            status_code=200,
            json={"serverTime": 1750000000000},
        )

    transport = httpx.MockTransport(mock_handler)

    client = MarketDataClient(
        base_url="https://fapi.binance.com",
        transport=transport,
    )

    result = await client.get_server_time()

    assert result == {"serverTime": 1750000000000}