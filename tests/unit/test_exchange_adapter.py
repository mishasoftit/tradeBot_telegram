import unittest
from unittest.mock import patch, MagicMock
from exchanges.adapter import ExchangeAdapter, ExchangeBase
import ccxt

class TestExchangeAdapter(unittest.TestCase):

    @patch('exchanges.adapter.Config')
    @patch('exchanges.adapter.decrypt_api_key')
    def setUp(self, mock_decrypt, mock_config):
        mock_decrypt.side_effect = ['decrypted_key', 'decrypted_secret']
        mock_config.EXCHANGE_API_KEY = 'encrypted_key'
        mock_config.EXCHANGE_API_SECRET = 'encrypted_secret'
        
        self.adapter = ExchangeAdapter('binance')
        self.adapter.exchange = MagicMock()

    def test_get_balance(self):
        self.adapter.exchange.fetch_balance.return_value = {'free': {'BTC': 1.5}}
        balance = self.adapter.get_balance()
        self.assertEqual(balance, 1.5)
        self.adapter.exchange.fetch_balance.assert_called_once()

    def test_get_balance_error(self):
        """Test error handling during balance fetch"""
        self.adapter.exchange.fetch_balance.side_effect = ccxt.NetworkError('Network issue')
        with self.assertRaises(ccxt.NetworkError):
            self.adapter.get_balance()

    def test_execute_trade_buy(self):
        self.adapter.exchange.create_market_buy_order.return_value = {'id': '123', 'status': 'filled'}
        result = self.adapter.execute_trade('BTC/USDT', 'buy', 0.01)
        self.assertEqual(result['status'], 'filled')
        self.adapter.exchange.create_market_buy_order.assert_called_once_with('BTC/USDT', 0.01)

    def test_execute_trade_sell(self):
        self.adapter.exchange.create_market_sell_order.return_value = {'id': '456', 'status': 'filled'}
        result = self.adapter.execute_trade('BTC/USDT', 'sell', 0.01)
        self.assertEqual(result['status'], 'filled')
        self.adapter.exchange.create_market_sell_order.assert_called_once_with('BTC/USDT', 0.01)

    def test_execute_trade_insufficient_balance(self):
        """Test trade execution with insufficient balance"""
        self.adapter.exchange.create_market_buy_order.side_effect = ccxt.InsufficientFunds('Not enough USDT')
        with self.assertRaises(ccxt.InsufficientFunds):
            self.adapter.execute_trade('BTC/USDT', 'buy', 10000)

    def test_execute_trade_invalid_symbol(self):
        """Test trade execution with invalid symbol format"""
        self.adapter.exchange.create_market_buy_order.side_effect = ccxt.BadSymbol('Invalid symbol')
        with self.assertRaises(ccxt.BadSymbol):
            self.adapter.execute_trade('INVALID_SYMBOL', 'buy', 0.01)

    @patch('exchanges.adapter.ExchangeBase._get_symbol_precision')
    def test_execute_trade_precision(self, mock_precision):
        mock_precision.return_value = 6
        self.adapter.execute_trade('BTC/USDT', 'buy', 0.01234567)
        self.adapter.exchange.create_market_buy_order.assert_called_once_with('BTC/USDT', 0.012346)

    def test_rate_limit_handling(self):
        """Test handling of rate limit errors"""
        self.adapter.exchange.fetch_balance.side_effect = ccxt.RateLimitExceeded('Too many requests')
        with self.assertRaises(ccxt.RateLimitExceeded):
            self.adapter.get_balance()

    def test_api_key_error(self):
        """Test error handling for invalid API keys"""
        with patch('exchanges.adapter.decrypt_api_key') as mock_decrypt:
            mock_decrypt.side_effect = Exception('Decryption failed')
            with self.assertRaises(Exception):
                ExchangeAdapter('binance')

    def test_connection_error(self):
        """Test handling of connection errors"""
        self.adapter.exchange.fetch_balance.side_effect = ccxt.ExchangeNotAvailable('Exchange down')
        with self.assertRaises(ccxt.ExchangeNotAvailable):
            self.adapter.get_balance()

if __name__ == '__main__':
    unittest.main()