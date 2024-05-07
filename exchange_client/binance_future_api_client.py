import time
import requests
from utils.config import Config
from utils import constant, time_utils
from utils.string_utils import (
    check_required_parameters,
    encoded_string,
    cleanNoneValue,
)
from binance.lib.authentication import (
    hmac_hashing,
    rsa_signature,
    ed25519_signature,
)
import logging
from utils.my_log import config_logging

config_logging(logging, logging.DEBUG)


class BinanceAPIPublicAPIClient:
    def __init__(
        self,
        base_url: str,
        timeout: int | None = None,
    ):
        self.base_url = base_url
        self.timeout = timeout


# class Binance
class BinanceFutureAPIClient(BinanceAPIPublicAPIClient):
    # base_url = constant.DEV_BINANCE_API_FUTURE_ENDPOINT

    def __init__(
        self,
        config: Config,
        base_url: str,
        timeout: int | None = None,
        private_key: str | None = None,
        private_key_pass: str | None = None,
    ):
        super().__init__(base_url, timeout)
        self.api_key = config.future_api_key
        self.api_secret = config.future_api_secret
        self.base_url = base_url
        self.timeout = timeout
        self.private_key = private_key
        self.private_key_pass = private_key_pass
        self.headers = {
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/json",
        }

    def sign_request(
        self, http_method: str, url_path: str, payload=None
    ) -> dict:
        if payload is None:
            payload = {}
        payload["timestamp"] = time_utils.get_current_timestamp()
        query_string = self._prepare_params(payload)
        payload["signature"] = self._get_sign(query_string)
        return self.send_request(http_method, url_path, payload)

    def _prepare_params(self, params: dict):
        return encoded_string(cleanNoneValue(params))

    def _get_sign(self, payload):
        if self.private_key is not None:
            try:
                return ed25519_signature(
                    self.private_key, payload, self.private_key_pass
                )
            except ValueError:
                return rsa_signature(
                    self.private_key, payload, self.private_key_pass
                )
        else:
            return hmac_hashing(self.api_secret, payload)

    def send_request(self, http_method: str, url_path: str, payload={}) -> dict:

        url = self.base_url + url_path
        logging.debug("url: " + url)
        params = cleanNoneValue(
            {
                "url": url,
                "params": self._prepare_params(payload),
                "timeout": self.timeout,
                # "proxies": self.proxies,
                "headers": self.headers,
            }
        )
        match http_method:
            case "GET":
                response = requests.get(**params)
            case "POST":
                response = requests.post(**params)
            case "PUT":
                response = requests.put(**params)
            case "DELETE":
                response: requests.Response = requests.delete(**params)
            case _:
                raise ValueError(f"Invalid HTTP Method {http_method}")
        logging.debug("raw response from server:" + response.text)
        if response.status_code >= 400:
            raise Exception(
                f"Error when calling api: return status {response.status_code}: {response.text}"
            )

        data = response.json()

        return data

    def new_order(self, symbol, side, type, **kwargs) -> dict:
        check_required_parameters(
            [[symbol, "symbol"], [side, "side"], [type, "type"]]
        )
        params = {"symbol": symbol, "side": side, "type": type, **kwargs}
        url_path = "/fapi/v1/order"
        return self.sign_request("POST", url_path, params)

    def account(self, **kwargs) -> dict:
        url_path = "/fapi/v2/account"
        return self.sign_request("GET", url_path, kwargs)
