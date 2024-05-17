import math
from algorithm.moving_average import MovingAverage, SimpleMovingAverage
from exchange_client.binance_future_api_client import BinanceFutureAPIClient
from model.order import BinanceOrder, BinanceTimeInForce, OrderType, Side
from utils.config import Config
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


async def moving_average_5_strategy_bn(
    apiClient: BinanceFutureAPIClient, movingAvg: MovingAverage
) -> None:
    last_price = movingAvg.current_price
    balance, side = get_balance(apiClient)
    logging.info(f"Current balance is {balance}")
    sma5 = movingAvg.cal_moving_average()
    if sma5 is None:
        return

    logging.info(f"last price: {last_price:.2f} average: {sma5:.2f}")
    if last_price > sma5 * 1.002:  # type: ignore
        if balance > -2:
            create_order(
                apiClient, round(last_price * 0.99, 1), Side.SELL, 0.004  # type: ignore
            )
    elif last_price < sma5 * 0.998:  # type: ignore
        if balance < 2:
            create_order(
                apiClient, round(last_price * 1.01, 1), Side.BUY, 0.004  # type: ignore
            )


def create_order(
    apiClient: BinanceFutureAPIClient, price: float, side: Side, quantity: float
):
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
    response = apiClient.new_order(
        "BTCUSDT",
        order.side,
        OrderType.LIMIT,
        **order.to_exchange_dict(),
    )
    logging.info(f"Response from order request: {response}")


def get_balance(apiClient: BinanceFutureAPIClient) -> tuple[float, str]:
    balance_json = apiClient.account()
    # logging.INFO(f"Current balance is {balance_json['balances']}")
    # for asset in balance_json["assets"]:
    #     if asset.get("asset") == "BTC":
    #         logging.info(f"Current asset balance is {asset}")
    for pos in balance_json["positions"]:
        if pos.get("symbol") == "BTCUSDT":
            logging.debug(f"Current position is {pos}")

            return float(pos["positionAmt"]), pos["positionSide"]
    return 0, "BOTH"


def to_type(df: pd.DataFrame, dtype: dict) -> pd.DataFrame:
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
    consumer = init_consumer(constant.KAFKA_TOPIC_BINANCE)
    symbol = "btcusdt"
    config = Config.read_from_file("test.json")
    apiClient = BinanceFutureAPIClient(
        config,
        base_url=constant.DEV_BINANCE_API_FUTURE_ENDPOINT,
        # show_header=True,
    )

    # price_queue = deque()
    movingAvg = SimpleMovingAverage()
    while next(consumer):
        msg = next(consumer)
        logging.info(f"Receive price :{msg.value['p']}")
        movingAvg.add_element(float(msg.value["p"]))
        if movingAvg.length >= 3:
            await moving_average_5_strategy_bn(apiClient, movingAvg)

        if movingAvg.length >= 50:
            movingAvg.remove_first()


if __name__ == "__main__":
    asyncio.run(main_binance())
