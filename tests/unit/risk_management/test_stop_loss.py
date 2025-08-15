import unittest
from unittest.mock import AsyncMock, MagicMock
from risk_management.stop_loss import StopLossManager

class TestStopLossManager(unittest.TestCase):
    def setUp(self):
        self.strategy = MagicMock()
        self.strategy.exchange = AsyncMock()
        self.manager = StopLossManager(self.strategy)

    async def test_set_stop_loss(self):
        """Test setting stop-loss order"""
        self.strategy.exchange.sell.return_value = {'id': 'stop123'}
        order = await self.manager.set_stop_loss('BTC/USDT', 50000, 0.5, 2.0)
        
        self.assertEqual(order['id'], 'stop123')
        self.strategy.exchange.sell.assert_awaited_once_with(
            'BTC/USDT', 0.5, 49000.0, params={'stopLoss': {'type': 'stop'}}
        )

    async def test_update_stop_loss(self):
        """Test updating existing stop-loss order"""
        # First set a stop-loss
        self.manager.active_stops['BTC/USDT'] = 'stop123'
        self.strategy.exchange.cancel_order.return_value = True
        self.strategy.exchange.sell.return_value = {'id': 'stop456'}
        
        # Mock position size
        self.manager._get_position_size = AsyncMock(return_value=0.6)
        
        order = await self.manager.update_stop_loss('BTC/USDT', 51000)
        
        self.assertEqual(order['id'], 'stop456')
        self.strategy.exchange.cancel_order.assert_awaited_once_with('stop123')
        self.strategy.exchange.sell.assert_awaited_once_with(
            'BTC/USDT', 0.6, 51000, params={'stopLoss': {'type': 'stop'}}
        )

    async def test_update_missing_stop_loss(self):
        """Test updating non-existent stop-loss order"""
        result = await self.manager.update_stop_loss('ETH/USDT', 3000)
        self.assertIsNone(result)

    async def test_get_position_size(self):
        """Test position size retrieval"""
        self.strategy.exchange.get_balance.return_value = {'BTC': 1.5, 'ETH': 5.0}
        size = await self.manager._get_position_size('BTC')
        self.assertEqual(size, 1.5)

if __name__ == '__main__':
    unittest.main()