import pytest
from unittest.mock import AsyncMock, MagicMock
from strategies.starter import StarterStrategy
from strategies.basic import BasicStrategy
from strategies.intermediate import IntermediateStrategy
from strategies.institutional import InstitutionalStrategy
from strategies.base import BaseStrategy

# BaseStrategy tests
def test_base_strategy_trade_amount():
    """Test risk-based trade amount calculation"""
    strategy = BaseStrategy(MagicMock(), {'risk_percent': 2.0})
    assert strategy.get_trade_amount(1000) == 20.0

def test_base_strategy_should_switch():
    """Test capital-based strategy switching logic"""
    strategy = BaseStrategy(MagicMock(), {'min_capital': 100, 'max_capital': 1000})
    assert strategy.should_switch(50) is True
    assert strategy.should_switch(500) is False
    assert strategy.should_switch(2000) is True

# StarterStrategy tests
@pytest.mark.asyncio
async def test_starter_strategy_analyze_market():
    exchange = AsyncMock()
    exchange.get_order_book.return_value = {
        'asks': [[100, 1]],
        'bids': [[99, 1]]
    }
    
    strategy = StarterStrategy(exchange, {})
    result = await strategy.analyze_market('BTC/USDT')
    assert result is True  # Spread = 1% > threshold

@pytest.mark.asyncio
async def test_starter_strategy_execute_trade():
    exchange = AsyncMock()
    exchange.get_order_book.return_value = {'asks': [[100, 1]]}
    exchange.buy.return_value = {'id': 'buy_order'}
    exchange.sell.return_value = {'id': 'sell_order'}
    
    strategy = StarterStrategy(exchange, {})
    await strategy.execute_trade('BTC/USDT', 1000)
    
    exchange.buy.assert_awaited_once()
    exchange.sell.assert_awaited_once()

def test_starter_strategy_should_switch():
    strategy = StarterStrategy(MagicMock(), {})
    assert strategy.should_switch(999) is False
    assert strategy.should_switch(1000) is True

# BasicStrategy tests
def test_basic_strategy_config():
    """Test strategy-specific configuration"""
    strategy = BasicStrategy(MagicMock(), {'target_profit_percent': 5.0})
    assert strategy.target_profit_percent == 5.0

@pytest.mark.asyncio
async def test_basic_strategy_analyze_market():
    """Placeholder test for future implementation"""
    strategy = BasicStrategy(AsyncMock(), {})
    result = await strategy.analyze_market('BTC/USDT')
    assert result is True  # Current placeholder returns True

def test_basic_strategy_should_switch():
    strategy = BasicStrategy(MagicMock(), {})
    assert strategy.should_switch(4999) is False
    assert strategy.should_switch(5000) is True

# IntermediateStrategy tests
def test_intermediate_strategy_risk():
    """Test intermediate strategy risk parameters"""
    strategy = IntermediateStrategy(MagicMock(), {})
    assert strategy.risk_percent == 1.0
    assert strategy.min_capital == 5000

@pytest.mark.asyncio
async def test_intermediate_strategy_execute_trade():
    """Placeholder test for future implementation"""
    strategy = IntermediateStrategy(AsyncMock(), {})
    await strategy.execute_trade('ETH/USDT', 6000)
    # Verify no exceptions

def test_intermediate_strategy_should_switch():
    strategy = IntermediateStrategy(MagicMock(), {})
    assert strategy.should_switch(9999) is False
    assert strategy.should_switch(10000) is True

# InstitutionalStrategy tests
def test_institutional_strategy_config():
    """Test institutional strategy parameters"""
    strategy = InstitutionalStrategy(MagicMock(), {})
    assert strategy.risk_percent == 0.2
    assert strategy.min_capital == 100000

def test_institutional_strategy_should_switch():
    strategy = InstitutionalStrategy(MagicMock(), {})
    assert strategy.should_switch(50000) is False
    assert strategy.should_switch(1000000) is False  # Never switches out