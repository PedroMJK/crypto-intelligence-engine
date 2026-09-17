from collections.abc import Callable
from typing import Any

import websockets


class MarketWebSocketClient:
    def __init__(
        self,
        base_url: str,
        connector: Callable[..., Any] = websockets.connect,
    ):
        self.base_url = base_url.rstrip("/")
        self.connector = connector

    async def connect(self):
        return await self.connector(self.base_url)

    async def receive_trade(self, symbol: str):
        stream_name = f"{symbol.lower()}@aggTrade"
        connection = await self.connector(
            f"{self.base_url}/ws/{stream_name}"
        )

        return await connection.recv()

    async def receive_ticker(self, symbol: str):
        stream_name = f"{symbol.lower()}@miniTicker"
        connection = await self.connector(
            f"{self.base_url}/ws/{stream_name}"
        )

        return await connection.recv()

    async def receive_candle(self, symbol: str, interval: str):
        stream_name = f"{symbol.lower()}@kline_{interval}"
        connection = await self.connector(
            f"{self.base_url}/ws/{stream_name}"
        )

        return await connection.recv()