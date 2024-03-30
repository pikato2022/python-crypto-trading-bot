from core.websocket import connect_websocket
import cf
import asyncio


async def main():
    try:
        # get orders
        await connect_websocket(cf.DEV_WEBSOCKET_ROOT_ENDPOINT_MARKET, "book.BTCUSD-PERP.10")
        # strategy
        #
    except Exception as e:
        print(f"Error {e}")

if __name__ == '__main__':
    asyncio.run(main())
