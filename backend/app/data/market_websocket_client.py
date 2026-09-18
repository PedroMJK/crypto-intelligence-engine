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

    async def _connect_with_reconnection(self, url: str):
        try:
            return await self.connector(url)
        except ConnectionError:
            return await self.connector(url)

    async def connect(self):
        return await self._connect_with_reconnection(self.base_url)

    async def receive_trade(self, symbol: str):
        stream_name = f"{symbol.lower()}@aggTrade"
        connection = await self._connect_with_reconnection(
            f"{self.base_url}/ws/{stream_name}"
        )

        return await connection.recv()

    async def receive_ticker(self, symbol: str):
        stream_name = f"{symbol.lower()}@miniTicker"
        connection = await self._connect_with_reconnection(
            f"{self.base_url}/ws/{stream_name}"
        )

        return await connection.recv()

    async def receive_candle(self, symbol: str, interval: str):
        stream_name = f"{symbol.lower()}@kline_{interval}"
        connection = await self._connect_with_reconnection(
            f"{self.base_url}/ws/{stream_name}"
        )

        return await connection.recv()

    async def receive_order_book(self, symbol: str):
        stream_name = f"{symbol.lower()}@depth"
        connection = await self._connect_with_reconnection(
            f"{self.base_url}/ws/{stream_name}"
        )

        return await connection.recv()