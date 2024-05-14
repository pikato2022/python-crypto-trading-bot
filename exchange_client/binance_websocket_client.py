from typing import Callable, NoReturn
from websocket import WebSocket, create_connection
import time
import json


class BinanceWebSocketClient:
    def __init__(self, uri: str):
        self.ws = create_connection(uri)
        self.on_message_callbacks: Callable[..., None] | None = None

    async def process_message_forever(self) -> NoReturn:
        while True:
            msg = self.ws.recv()
            self.on_message(msg)

    def subscribe(self, stream: list[str], id: int | None = None):
        if not id:
            id = int(time.time() * 1000)
        message = json.dumps(
            {"method": "SUBSCRIBE", "params": stream, "id": id}
        )
        self.ws.send(message)

    def on_ping(self):
        self.ws.ping()

    def on_pong(self):
        self.ws.pong()

    def unsubscribe(self, stream: str, id: int | None = None):
        if not id:
            id = int(time.time() * 1000)
        message = json.dumps(
            {"method": "UNSUBSCRIBE", "params": stream, "id": id}
        )
        self.ws.send(message)

    def on_message(self, msg: str | bytes):
        if self.on_message_callbacks:
            self.on_message_callbacks(msg)
