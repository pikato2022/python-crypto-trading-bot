# Crypto.com
DEV_WEBSOCKET_ROOT_ENDPOINT_USER = "wss://uat-stream.3ona.co/exchange/v1/user"
DEV_WEBSOCKET_ROOT_ENDPOINT_MARKET = (
    "wss://uat-stream.3ona.co/exchange/v1/market"
)


PROD_WEBSOCKET_ROOT_ENDPOINT_USER = "wss://stream.crypto.com/exchange/v1/user"
PROD_WEBSOCKET_ROOT_ENDPOINT_MARKET = (
    "wss://stream.crypto.com/exchange/v1/market"
)


DEV_REST_API_ROOT_ENDPOINT = "https://uat-api.3ona.co/exchange/v1/{method}"


PROD_RES_API_ROOT_ENDPOINT = "https://api.crypto.com/exchange/v1/{method}"


# BINANCE
PROD_BINANCE_API_ENDPOINT = "https://api.binance.com/api"
DEV_BINANCE_API_ENDPOINT = "https://testnet.binance.vision"
DEV_BINANCE_API_FUTURE_ENDPOINT = "https://testnet.binancefuture.com"
PROD_BINANCE_FUTURE_STREAM = "wss://fstream.binance.com/ws"
DEV_BINANCE_FUTURE_STREAM = "wss://fstream.binancefuture.com/ws"
DEV_BINANCE_WEBSOCKET_ENDPOINT = "wss://stream.binancefuture.com/ws"
PROD_BINANCE_FUTURE_WEBSOCKET_ENDPOINT = "wss://fstream.binance.com/ws"
CREATE_ORDER_URI = "private/create-order"
CANCEL_ORDER_URI = "private/cancel-order"

KAFKA_TOPIC_CRYPTO_COM = "get-price"
KAFKA_TOPIC_BINANCE = "binance-get-price"
