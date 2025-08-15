import abc
from typing import Dict, Any
from exchanges.adapter import ExchangeAdapter

class BaseStrategy(metaclass=abc.ABCMeta):
    def __init__(self, exchange: ExchangeAdapter, config: Dict[str, Any]):
        self.exchange = exchange
        self.config = config
        self.min_capital = config.get('min_capital', 0)
        self.max_capital = config.get('max_capital', float('inf'))
        self.risk_percent = config.get('risk_percent', 1.0)

    @abc.abstractmethod
    async def analyze_market(self, symbol: str):
        """Analyze market conditions for trading opportunity"""
        pass

    @abc.abstractmethod
    async def execute_trade(self, symbol: str, capital: float):
        """Execute trade based on strategy rules"""
        pass

    @abc.abstractmethod
    def should_switch(self, current_capital: float) -> bool:
        """Determine if strategy should switch based on capital"""
        return current_capital < self.min_capital or current_capital >= self.max_capital

    def get_trade_amount(self, capital: float) -> float:
        """Calculate trade amount based on risk percentage"""
        return capital * (self.risk_percent / 100)