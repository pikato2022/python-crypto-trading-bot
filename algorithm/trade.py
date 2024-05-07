from exchange_client.binance_future_api_client import BinanceFutureAPIClient
from trading_bot.utils.config import Config
from utils.binance_connector import BinanceConnector
from utils.kafka_core import init_consumer
import pandas as pd
import asyncio
import numpy as np
from collections import deque
import logging
from utils.my_log import config_logging
import utils.constant as constant

config_logging(logging, logging.INFO)


async def moving_average_5_strategy(df, in_position):
    last_price = df.tail(1).price.values[0]

    sma5 = df.price.rolling(5).mean().tail(1).values[0]
    # print(f"Type of last_price {type(last_price)}, type of sma5: {sma5}")
    if not in_position and last_price < sma5:
        # create buy order
        print(f"bought for {last_price}")
        in_position = True
    if in_position and sma5 < last_price:
        # create sell position
        print(f"SELL for {last_price}")
        in_position = False
    return in_position


async def moving_average_5_strategy_bn(queue, binanceConnector):
    last_price = queue.back()

    sma5 = np.mean(queue)


def buy_order(price):
    pass


def sell_order(price):
    pass


def to_type(df, dtype):
    df = df.astype(dtype=dtype)
    return df


async def main_cryptocom():
    dtypes = {"price": float, "quantity": float, "num_of_order": int}
    consumer = init_consumer("get-price")
    asks_all_df = to_type(
        pd.DataFrame(columns=["price", "quantity", "num_of_order"]), dtypes
    )
    bid_all_df = to_type(
        pd.DataFrame(columns=["price", "quantity", "num_of_order"]), dtypes
    )
    in_position = False
    while next(consumer):
        msg = next(consumer)
        # print(f"Get price from market feed {msg}")
        asks = msg.value["data"][0]["asks"]
        bids = msg.value["data"][0]["bids"]

        # Bids array: [0] = Price, [1] = Quantity, [2] = Number of Orders

        asks_df = pd.DataFrame(
            asks, columns=["price", "quantity", "num_of_order"]
        )
        asks_df.price = asks_df.price.astype(float)
        asks_df.quantity = asks_df.quantity.astype(float)
        bid_df = pd.DataFrame(
            bids, columns=["price", "quantity", "num_of_order"]
        )
        bid_df.price = asks_df.price.astype(float)
        bid_df.quantity = asks_df.quantity.astype(float)
        asks_all_df = pd.concat([asks_all_df, asks_df], axis=0)
        # print(asks_all_df.dtypes)
        bid_all_df = pd.concat([bid_all_df, bid_df], axis=0)
        asks_all_df = asks_all_df.tail(20)
        if asks_all_df.shape[0] > 10:
            in_position = await moving_average_5_strategy(
                asks_all_df, in_position
            )


async def main_binance():
    consumer = init_consumer("binance-get-price")
    symbol = "btcusdt"
    config = Config.read_from_file("test.json")
    apiClient = BinanceFutureAPIClient(
        config,
        base_url=constant.DEV_BINANCE_API_FUTURE_ENDPOINT,
        # show_header=True,
    )
    binanceConnector = BinanceConnector(None, apiClient)
    price_queue = deque()
    while next(consumer):
        msg = next(consumer)
        logging.info(f"Message is {msg}")
        price_queue.append(msg["p"])


if __name__ == "__main__":
    asyncio.run(main_binance())
