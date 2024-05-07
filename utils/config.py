import json


class Config:
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        future_api_key: str,
        future_api_secret: str,
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.future_api_key = future_api_key
        self.future_api_secret = future_api_secret

    @classmethod
    def read_from_file(cls, file_name: str) -> "Config":
        f = open(file_name)
        secret = json.load(f)
        return Config(
            secret["BINANCE_API_KEY"],
            secret["BINANCE_API_SECRET"],
            secret["BINANCE_FUTURE_API_KEY"],
            secret["BINANCE_FUTURE_API_KEY"],
        )
