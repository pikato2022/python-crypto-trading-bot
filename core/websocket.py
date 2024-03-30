import websockets
import asyncio
import logging
import time
import json


def on_message(ws, message):
    print(f"Received message: {message}")


def on_error(ws, message):
    print(f"Error in WS: {message}")


def on_close(ws):
    print(f"Close WS")


def create_heartbeat_request(id):
    request = {
        "id": f"{id}",
        "method": "public/respond-heartbeat"
    }
    request_str = json.dumps(request)

    return request_str


async def connect_websocket(uri, channel):
    sample_request = {
        "method": "subscribe",
        "params": {
            "channels": [channel]
        },
    }
    heartbeat_id = None
    while True:
        try:
            async with websockets.connect(uri) as ws:
                # Avoid rate limit

                await ws.send(json.dumps(sample_request))

                while True:
                    res = await ws.recv()
                    # await asyncio.sleep(1)
                    res = json.loads(res)
                    if res['method'] == "public/heartbeat":
                        heartbeat_id = res['id']
                        print(
                            f"Sending heart beat response with id {heartbeat_id}")
                        heartbeat_request = create_heartbeat_request(
                            heartbeat_id)
                        await ws.send(heartbeat_request)
                        print("Sent heart beat response")
                    print(f"Receive message {res}")
        except Exception as e:
            print(f"Error when connect : {e}")
            await asyncio.sleep(1)


# async def handler(ws):
#     sample_request = {
#     "method": "subscribe",
#     "params": {
#     "channels": ["book.BTCUSD-PERP.10"]
#     },
#     }

#     while True:
#         ws.send(json.dumps(sample_request))
#         asyncio.sleep(1)
#         res = await ws.recv()
#         print(f"Receive message {json.loads(res)}")
