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