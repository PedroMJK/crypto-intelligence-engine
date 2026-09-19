import asyncio


class MarketDataBuffer:
    def __init__(self, max_size: int):
        if max_size <= 0:
            raise ValueError("max_size must be greater than zero")

        self.queue = asyncio.Queue(maxsize=max_size)
        self.dropped_messages = 0

    async def put(self, message: dict) -> None:
        await self.queue.put(message)

    def try_put(self, message: dict) -> bool:
        try:
            self.queue.put_nowait(message)
        except asyncio.QueueFull:
            self.dropped_messages += 1
            return False

        return True

    async def get(self) -> dict:
        return await self.queue.get()
