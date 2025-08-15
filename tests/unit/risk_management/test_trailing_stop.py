import unittest
from unittest.mock import AsyncMock, MagicMock
from risk_management.trailing_stop import TrailingStopManager

class TestTrailingStopManager(unittest.TestCase):
    def setUp(self):
        self.strategy = MagicMock()
        self.strategy.exchange = AsyncMock()
        self.manager = TrailingStopManager(self.strategy, 1.0, 0.5)

    async def test_set_trailing_stop(self):
        """Test setting trailing stop order"""
        self.strategy.exchange.sell.return_value = {'id': 'ts123'}
        order = await self.manager.set_trailing_stop('BTC/USDT', 50000, 0.5)
        
        self.assertEqual(order['id'], 'ts123')
        self.strategy.exchange.sell.assert_awaited_once_with(
            'BTC/USDT', 0.5, None, 
            params={
                'trailingStop': True,
                'trailingActivationPrice': 50500.0,
                'trailingDistance': 0.5
            }
        )

    async def test_update_trailing_stop_activation(self):
        """Test updating trailing stop when activation price is reached"""
        # First set a trailing stop
        await self.manager.set_trailing_stop('BTC/USDT', 50000, 0.5)
        self.manager.active_trails['BTC/USDT'] = {
            'id': 'ts123',
            'entry_price': 50000
        }
        
        # Current price moves to 51000 (above activation price)
        self.strategy.exchange.cancel_order.return_value = True
        self.strategy.exchange.sell.return_value = {'id': 'ts456'}
        self.manager._get_position_size = AsyncMock(return_value=0.5)
        
        result = await self.manager.update_trailing_stop('BTC/USDT', 51000)
        
        self.assertIsNotNone(result)
        self.strategy.exchange.cancel_order.assert_awaited_once_with('ts123')
        self.strategy.exchange.sell.assert_awaited_once()

    async def test_update_trailing_stop_no_activation(self):
        """Test updating trailing stop when not at activation price"""
        # First set a trailing stop
        await self.manager.set_trailing_stop('BTC/USDT', 50000, 0.5)
        self.manager.active_trails['BTC/USDT'] = {
            'id': 'ts123',
            'entry_price': 50000
        }
        
        # Current price at 50200 (below activation price)
        result = await self.manager.update_trailing_stop('BTC/USDT', 50200)
        
        self.assertIsNone(result)
        self.strategy.exchange.cancel_order.assert_not_called()
        self.strategy.exchange.sell.assert_not_called()

    async def test_update_missing_trailing_stop(self):
        """Test updating non-existent trailing stop order"""
        result = await self.manager.update_trailing_stop('ETH/USDT', 3000)
        self.assertIsNone(result)

    async def test_get_position_size(self):
        """Test position size retrieval"""
        self.strategy.exchange.get_balance.return_value = {'BTC': 1.5, 'ETH': 5.0}
        size = await self.manager._get_position_size('BTC')
        self.assertEqual(size, 1.5)

if __name__ == '__main__':
    unittest.main()