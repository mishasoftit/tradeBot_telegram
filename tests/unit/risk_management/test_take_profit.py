import unittest
from unittest.mock import AsyncMock, MagicMock
from risk_management.take_profit import TakeProfitManager

class TestTakeProfitManager(unittest.TestCase):
    def setUp(self):
        self.strategy = MagicMock()
        self.strategy.exchange = AsyncMock()
        self.manager = TakeProfitManager(self.strategy)

    async def test_set_take_profit(self):
        """Test setting take-profit order"""
        self.strategy.exchange.sell.return_value = {'id': 'tp123'}
        order = await self.manager.set_take_profit('BTC/USDT', 50000, 0.5, 5.0)
        
        self.assertEqual(order['id'], 'tp123')
        self.strategy.exchange.sell.assert_awaited_once_with(
            'BTC/USDT', 0.5, 52500.0, params={'takeProfit': {'type': 'limit'}}
        )

    async def test_update_take_profit(self):
        """Test updating existing take-profit order"""
        # First set a take-profit
        self.manager.active_take_profits['BTC/USDT'] = 'tp123'
        self.strategy.exchange.cancel_order.return_value = True
        self.strategy.exchange.sell.return_value = {'id': 'tp456'}
        
        # Mock position size
        self.manager._get_position_size = AsyncMock(return_value=0.6)
        
        order = await self.manager.update_take_profit('BTC/USDT', 53000)
        
        self.assertEqual(order['id'], 'tp456')
        self.strategy.exchange.cancel_order.assert_awaited_once_with('tp123')
        self.strategy.exchange.sell.assert_awaited_once_with(
            'BTC/USDT', 0.6, 53000, params={'takeProfit': {'type': 'limit'}}
        )

    async def test_update_missing_take_profit(self):
        """Test updating non-existent take-profit order"""
        result = await self.manager.update_take_profit('ETH/USDT', 3500)
        self.assertIsNone(result)

    async def test_get_position_size(self):
        """Test position size retrieval"""
        self.strategy.exchange.get_balance.return_value = {'BTC': 1.5, 'ETH': 5.0}
        size = await self.manager._get_position_size('BTC')
        self.assertEqual(size, 1.5)

if __name__ == '__main__':
    unittest.main()