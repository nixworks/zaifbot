import json
import threading
from websocket import create_connection
from zaifapi.impl import ZaifPublicApi, ZaifPrivateApi
from zaifbot.bot_common.config import load_config


class _ZaifWebSocket:
    _WEB_SOCKET_API_URI = 'ws://{}:{}/stream?currency_pair={}'
    _instance = None
    _lock = threading.Lock()
    _ws = None
    _config = None

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._config = load_config()
                cls._ws = cls._get_connection()
        return cls._instance

    def __del__(self):
        self._ws.close()

    @property
    def last_price(self):
        for count in range(self._config.system.retry_count):
            try:
                result = self._ws.recv()
                json_obj = json.loads(result)
                return json_obj['last_price']['price']
            except:
                self._ws = self._get_connection()
        api = ZaifPublicApi()
        return api.last_price(self._config.system.currency_pair)['last_price']

    @classmethod
    def _get_connection(cls):
        return create_connection(cls._WEB_SOCKET_API_URI.format(cls._config.system.api_domain,
                                                                cls._config.system.socket.port,
                                                                cls._config.system.currency_pair))


def get_current_last_price():
    api = _ZaifWebSocket()
    return api.last_price


class ZaifOrder:
    def __init__(self):
        self._config = load_config()
        self._private_api = ZaifPrivateApi(self._config.api_keys.key, self._config.api_keys.secret)

    def get_active_orders(self):
        return self._private_api.active_orders(currency_pair=self._config.system.currency_pair)

    def trade(self, action, price, amount):
        return self._private_api.trade(currency_pair=self._config.system.currency_pair, action=action, price=price, amount=amount)

    def cancel_order(order_id):
        self._private_api.cancel_order(order_id)
