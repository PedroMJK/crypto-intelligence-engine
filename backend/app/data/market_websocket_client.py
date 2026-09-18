import asyncio
from collections.abc import Callable
from typing import Any

import websockets
from websockets.exceptions import ConnectionClosedError


class MarketWebSocketClient:
    def __init__(
        self,
        base_url: str,
        connector: Callable[..., Any] = websockets.connect,
        sleeper: Callable[..., Any] = asyncio.sleep,
        max_reconnect_attempts: int = 3,
        initial_backoff: float = 1.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.connector = connector
        self.sleeper = sleeper
        self.max_reconnect_attempts = max_reconnect_attempts
        self.initial_backoff = initial_backoff

    async def _connect_with_reconnection(self, url: str):
        backoff_delay = self.initial_backoff

        for attempt in range(self.max_reconnect_attempts + 1):
            try:
                return await self.connector(url)
            except ConnectionError:
                if attempt == self.max_reconnect_attempts:
                    raise

                await self.sleeper(backoff_delay)
                backoff_delay *= 2

    async def _receive_with_reconnection(self, url: str):
        connection = await self._connect_with_reconnection(url)

        try:
            return await connection.recv()
        except ConnectionClosedError:
            connection = await self._connect_with_reconnection(url)
            return await connection.recv()

    async def connect(self):
        return await self._connect_with_reconnection(self.base_url)

    async def receive_trade(self, symbol: str):
        stream_name = f"{symbol.lower()}@aggTrade"

        return await self._receive_with_reconnection(
            f"{self.base_url}/ws/{stream_name}"
        )

    async def receive_ticker(self, symbol: str):
        stream_name = f"{symbol.lower()}@miniTicker"

        return await self._receive_with_reconnection(
            f"{self.base_url}/ws/{stream_name}"
        )

    async def receive_candle(self, symbol: str, interval: str):
        stream_name = f"{symbol.lower()}@kline_{interval}"

        return await self._receive_with_reconnection(
            f"{self.base_url}/ws/{stream_name}"
        )

    async def receive_order_book(self, symbol: str):
        stream_name = f"{symbol.lower()}@depth"

        return await self._receive_with_reconnection(
            f"{self.base_url}/ws/{stream_name}"
        )