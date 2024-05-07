import asyncio
from asyncio import constants
import time
import logging
from my_log import config_logging
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient
from kafka import KafkaProducer
import json
from model.order import BinanceOrder, BinanceTimeInForce, OrderType, Side
from exchange_client.binance_future_api_client import (
    BinanceFutureAPIClient,
)
import utils.constant as constant
from utils.kafka_core import broadcast_kafka, init_producer

config_logging(logging, logging.INFO)


class BinanceConnector:
    def __init__(
        self, producer: KafkaProducer | None, apiClient: BinanceFutureAPIClient
    ) -> None:

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

    def create_order(self, price, side: Side, quantity: float):
        # logging.info(self.apiClient.time())
        order = BinanceOrder(
            price,
            side,
            quantity,
            OrderType.LIMIT,
            BinanceTimeInForce.IOC,
            "BTCUSDT",
        )
        logging.info(f"Created order {order.to_exchange_dict}")
        response = self.apiClient.new_order(
            "BTCUSDT",
            order.side,
            OrderType.LIMIT,
            **order.to_exchange_dict(),
        )
        logging.info(f"Response from order request: {response}")

    def get_balance(self):
        balance_json = self.apiClient.account()
        # logging.INFO(f"Current balance is {balance_json['balances']}")
        for asset in balance_json["assets"]:
            if asset.get("asset") == "BTC":
                logging.info(f"Current asset balance is {asset}")
        return balance_json["positions"]


if __name__ == "__main__":
    symbol = "btcusdt"
    producer = init_producer()
    apiClient = BinanceFutureAPIClient(
        constant.BINANCE_TEST_FUTURE_API_KEY,
        constant.BINANCE_TEST_FUTURE_API_SECRET,
        base_url=constant.DEV_BINANCE_API_FUTURE_ENDPOINT,
        # show_header=True,
    )
    binanceConnector = BinanceConnector(producer, apiClient)
    # binanceConnector.create_order(64950, Side.BUY, 0.004)
    # # binanceConnector.create_order(64500, Side.SELL, 0.004)
    # # balances = binanceConnector.get_balance()
    # for balance in balances:
    #     if balance.get("symbol") == "BTCUSDT":
    #         logging.info(f"Current balance is {balance}")
    #         break
    asyncio.run(binanceConnector.get_binance_trade_stream(symbol))
