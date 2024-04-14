import asyncio
from asyncio import constants
import time
import logging
from binance.lib.utils import config_logging
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient
from kafka import KafkaProducer
from binance.spot import Spot
import json
from model.order import BinanceOrder, BinanceTimeInForce, OrderType
import utils.constant as constant
from utils.kafka_core import broadcast_kafka, init_producer

config_logging(logging, logging.INFO)


class BinanceConnector:
    def __init__(self, producer: KafkaProducer, apiClient: Spot) -> None:

        self.producer = producer
        self.socketClient = SpotWebsocketStreamClient(
            on_message=self.message_handler
        )
        self.apiClient = apiClient

    def message_handler(self, _, message):
        # print(message)
        res = json.loads(message)
        logging.debug(
            f"Sending price to Kafka queue topic get_price type : {type(res)}"
        )

        broadcast_kafka(self.producer, constant.KAFKA_TOPIC_BINANCE, res)
        logging.info(f"Sent price to Kafka queue topic get_price: {res}")

    async def get_binance_trade_stream(self, symbol):
        # Subscribe to a single symbol stream
        self.socketClient.trade(symbol=symbol)
        # time.sleep(100)
        # logging.info("closing ws connection")
        # my_client.stop()

    def create_order(self, price, isSell):
        logging.info(self.apiClient.time())
        order = BinanceOrder(
            price, isSell, 1, OrderType.LIMIT, BinanceTimeInForce.IOC, "BTCUSDT"
        )
        logging.info(f"Created order {order.to_exchange_dict()}")
        self.apiClient.new_order_test(
            "BTCUSDT", "SELL", OrderType.LIMIT, **order.to_exchange_dict()
        )


if __name__ == "__main__":
    symbol = "btcusdt"
    producer = init_producer()
    apiClient = Spot(
        constant.BINANCE_TEST_API_KEY,
        constant.BINANCE_TEST_API_SECRET,
        base_url=constant.DEV_BINANCE_API_ENDPOINT,
    )
    binanceConnector = BinanceConnector(producer, apiClient)
    binanceConnector.create_order(64000, True)
    # asyncio.run(binanceConnector.get_binance_trade_stream(symbol))
