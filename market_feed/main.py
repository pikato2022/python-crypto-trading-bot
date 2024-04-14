from utils.websocket_utils import connect_websocket
import utils.constant as constant
import asyncio


async def main():
    try:
        # get orders
        channel = "book.BTCUSD-PERP.10"
        sample_request = {
            "method": "subscribe",
            "params": {
                "channels": [channel]
            },
        }
        await connect_websocket(constant.DEV_WEBSOCKET_ROOT_ENDPOINT_MARKET, sample_request)
        # strategy
        #
    except Exception as e:
        print(f"Error {e}")

if __name__ == '__main__':
    asyncio.run(main())
