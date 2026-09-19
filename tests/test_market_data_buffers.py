import pytest

from backend.app.data.market_data_buffer import MarketDataBuffer
from backend.app.data.market_data_buffers import MarketDataBuffers


def test_market_data_buffers_creates_buffer_for_each_market_stream():
    buffers = MarketDataBuffers(max_size=100)

    assert isinstance(buffers.trade, MarketDataBuffer)
    assert isinstance(buffers.ticker, MarketDataBuffer)
    assert isinstance(buffers.candle, MarketDataBuffer)
    assert isinstance(buffers.order_book, MarketDataBuffer)


@pytest.mark.asyncio
async def test_market_data_buffers_are_independent():
    buffers = MarketDataBuffers(max_size=100)

    trade_message = {"e": "aggTrade", "s": "BTCUSDT"}
    ticker_message = {"e": "24hrMiniTicker", "s": "ETHUSDT"}

    await buffers.trade.put(trade_message)
    await buffers.ticker.put(ticker_message)

    assert await buffers.trade.get() == trade_message
    assert await buffers.ticker.get() == ticker_message
