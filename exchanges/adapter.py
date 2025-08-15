import abc
import ccxt
from config.settings import Config
from database.encryption import decrypt_api_key

class ExchangeAdapter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def buy(self, symbol, amount, price=None):
        pass

    @abc.abstractmethod
    def sell(self, symbol, amount, price=None):
        pass

    @abc.abstractmethod
    def get_balance(self):
        pass

    @abc.abstractmethod
    def get_order_book(self, symbol, limit=5):
        pass

class ExchangeBase(ExchangeAdapter):
    def __init__(self, exchange_id):
        self.exchange = getattr(ccxt, exchange_id)({
            'apiKey': decrypt_api_key(Config.EXCHANGE_API_KEY),
            'secret': decrypt_api_key(Config.EXCHANGE_API_SECRET),
            'enableRateLimit': True
        })
        
    def buy(self, symbol, amount, price=None):
        return self.exchange.create_market_buy_order(symbol, amount) if not price \
            else self.exchange.create_limit_buy_order(symbol, amount, price)
            
    def sell(self, symbol, amount, price=None):
        return self.exchange.create_market_sell_order(symbol, amount) if not price \
            else self.exchange.create_limit_sell_order(symbol, amount, price)
            
    def get_balance(self):
        return self.exchange.fetch_balance()
        
    def get_order_book(self, symbol, limit=5):
        return self.exchange.fetch_order_book(symbol, limit)