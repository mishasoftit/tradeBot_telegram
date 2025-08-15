from strategies.base import BaseStrategy
from typing import Dict, Any

class StarterStrategy(BaseStrategy):
    def __init__(self, exchange, config: Dict[str, Any]):
        super().__init__(exchange, config)
        self.min_capital = 100
        self.max_capital = 1000
        self.risk_percent = 2.0  # Higher risk for aggressive growth
        self.target_profit_percent = 5.0

    async def analyze_market(self, symbol: str):
        # Simple strategy: look for coins with high volatility
        # and recent price drops for quick rebounds
        order_book = await self.exchange.get_order_book(symbol)
        spread = order_book['asks'][0][0] - order_book['bids'][0][0]
        spread_percent = (spread / order_book['asks'][0][0]) * 100
        
        # Look for high spread indicating volatility opportunity
        return spread_percent > 1.0

    async def execute_trade(self, symbol: str, capital: float):
        trade_amount = self.get_trade_amount(capital)
        current_price = (await self.exchange.get_order_book(symbol))['asks'][0][0]
        
        # Place buy order at current market price
        buy_order = await self.exchange.buy(symbol, trade_amount / current_price)
        
        # Set profit target at 5% above purchase price
        target_price = current_price * 1.05
        await self.exchange.sell(symbol, trade_amount / current_price, target_price)

    def should_switch(self, current_capital: float) -> bool:
        return current_capital >= self.max_capital