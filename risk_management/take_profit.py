class TakeProfitManager:
    def __init__(self, strategy):
        self.strategy = strategy
        self.active_take_profits = {}

    async def set_take_profit(self, symbol, entry_price, position_size, profit_percent=5.0):
        """Set take-profit order for a position"""
        target_price = entry_price * (1 + profit_percent / 100)
        order = await self.strategy.exchange.sell(
            symbol, 
            position_size, 
            target_price,
            params={'takeProfit': {'type': 'limit'}}
        )
        self.active_take_profits[symbol] = order['id']
        return order

    async def update_take_profit(self, symbol, new_target_price):
        """Update existing take-profit order"""
        if symbol not in self.active_take_profits:
            return None
            
        await self.strategy.exchange.cancel_order(self.active_take_profits[symbol])
        position_size = await self._get_position_size(symbol)
        return await self.set_take_profit(symbol, new_target_price, position_size)

    async def _get_position_size(self, symbol):
        """Get current position size for a symbol"""
        balance = await self.strategy.exchange.get_balance()
        return balance.get(symbol, 0)