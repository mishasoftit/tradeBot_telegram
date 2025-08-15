class StopLossManager:
    def __init__(self, strategy):
        self.strategy = strategy
        self.active_stops = {}

    async def set_stop_loss(self, symbol, entry_price, position_size, stop_percent=2.0):
        """Set stop-loss order for a position"""
        stop_price = entry_price * (1 - stop_percent / 100)
        order = await self.strategy.exchange.sell(
            symbol, 
            position_size, 
            stop_price,
            params={'stopLoss': {'type': 'stop'}}
        )
        self.active_stops[symbol] = order['id']
        return order

    async def update_stop_loss(self, symbol, new_stop_price):
        """Update existing stop-loss order"""
        if symbol not in self.active_stops:
            return None
            
        await self.strategy.exchange.cancel_order(self.active_stops[symbol])
        position_size = await self._get_position_size(symbol)
        return await self.set_stop_loss(symbol, new_stop_price, position_size)

    async def _get_position_size(self, symbol):
        """Get current position size for a symbol"""
        balance = await self.strategy.exchange.get_balance()
        return balance.get(symbol, 0)