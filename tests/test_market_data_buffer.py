import asyncio

import pytest

from backend.app.data.market_data_buffer import MarketDataBuffer


@pytest.mark.asyncio
async def test_market_data_buffer_stores_and_returns_message():
    buffer = MarketDataBuffer(max_size=2)

    message = {"e": "aggTrade", "s": "BTCUSDT"}

    await buffer.put(message)

    assert await buffer.get() == message


@pytest.mark.asyncio
async def test_market_data_buffer_waits_when_full():
    buffer = MarketDataBuffer(max_size=1)

    first_message = {"e": "aggTrade", "s": "BTCUSDT"}
    second_message = {"e": "aggTrade", "s": "ETHUSDT"}

    await buffer.put(first_message)

    put_task = asyncio.create_task(buffer.put(second_message))

    await asyncio.sleep(0)

    assert not put_task.done()

    assert await buffer.get() == first_message

    await put_task

    assert await buffer.get() == second_message


@pytest.mark.parametrize("max_size", [0, -1])
def test_market_data_buffer_rejects_non_positive_max_size(max_size):
    with pytest.raises(
        ValueError,
        match="max_size must be greater than zero",
    ):
        MarketDataBuffer(max_size=max_size)
