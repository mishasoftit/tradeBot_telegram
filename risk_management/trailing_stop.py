class TrailingStopManager:
    def __init__(self, strategy, activation_percent=1.0, trail_percent=0.5):
        self.strategy = strategy
        self.activation_percent = activation_percent
        self.trail_percent = trail_percent
        self.active_trails = {}

    async def set_trailing_stop(self, symbol, entry_price, position_size):
        """Set trailing stop order"""
        activation_price = entry_price * (1 + self.activation_percent / 100)
        params = {
            'trailingStop': True,
            'trailingActivationPrice': activation_price,
            'trailingDistance': self.trail_percent
        }
        order = await self.strategy.exchange.sell(
            symbol, 
            position_size, 
            None,  # Market order
            params=params
        )
        self.active_trails[symbol] = {
            'id': order['id'],
            'entry_price': entry_price
        }
        return order

    async def update_trailing_stop(self, symbol, current_price):
        """Update trailing stop based on price movement"""
        if symbol not in self.active_trails:
            return None
            
        entry = self.active_trails[symbol]['entry_price']
        new_activation = current_price * (1 - self.activation_percent / 100)
        
        if new_activation > entry:
            await self.strategy.exchange.cancel_order(self.active_trails[symbol]['id'])
            return await self.set_trailing_stop(symbol, current_price, 
                                             await self._get_position_size(symbol))

    async def _get_position_size(self, symbol):
        """Get current position size for a symbol"""
        balance = await self.strategy.exchange.get_balance()
        return balance.get(symbol, 0)