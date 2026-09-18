import asyncio


class MarketDataBuffer:
    def __init__(self, max_size: int):
        if max_size <= 0:
            raise ValueError("max_size must be greater than zero")

        self.queue = asyncio.Queue(maxsize=max_size)

    async def put(self, message: dict) -> None:
        await self.queue.put(message)

    async def get(self) -> dict:
        return await self.queue.get()
