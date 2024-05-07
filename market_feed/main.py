from typing import Any
from exchange_client.binance_websocket_client import (
    BinanceWebSocketClient,
)
from utils.kafka_core import broadcast_kafka, init_producer
from utils.config import Config
from utils.websocket_utils import connect_websocket
import utils.constant as constant
import asyncio


async def main():
    # SETUP
    # config = Config.read_from_file("test.json")
    websocketClient = BinanceWebSocketClient(
        constant.DEV_BINANCE_WEBSOCKET_ENDPOINT
    )
    # kafka_producer = init_producer()
    websocketClient.on_message_callbacks = lambda msg: print(f"receive {msg}")
    # broadcast_kafka(
    #     kafka_producer, "price", msg
    # )

    # RUN
    websocketClient.subscribe(["btcusdt@aggTrade"])
    await websocketClient.process_message_forever()


if __name__ == "__main__":
    asyncio.run(main())
