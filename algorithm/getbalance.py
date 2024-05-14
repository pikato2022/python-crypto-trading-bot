from algorithm.trade import get_balance
from exchange_client.binance_future_api_client import (
    BinanceFutureAPIClient,
)
from utils.config import Config
from utils import constant


def main():
    config = Config.read_from_file("test.json")
    apiClient = BinanceFutureAPIClient(
        config,
        base_url=constant.DEV_BINANCE_API_FUTURE_ENDPOINT,
        # show_header=True,
    )
    balance, side = get_balance(apiClient)
    print(f"Current balance is {balance}")


main()
