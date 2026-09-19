import httpx


class MarketDataClient:
    def __init__(
        self,
        base_url: str,
        transport: httpx.AsyncBaseTransport | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.transport = transport

    async def get_server_time(self) -> dict:
        async with httpx.AsyncClient(
            base_url=self.base_url,
            transport=self.transport,
        ) as client:
            response = await client.get("/fapi/v1/time")
            response.raise_for_status()

            return response.json()

    async def get_exchange_info(self) -> dict:
        async with httpx.AsyncClient(
            base_url=self.base_url,
            transport=self.transport,
        ) as client:
            response = await client.get("/fapi/v1/exchangeInfo")
            response.raise_for_status()

            return response.json()
