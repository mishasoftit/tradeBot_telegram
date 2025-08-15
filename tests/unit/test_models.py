import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, User, Strategy, Trade, APIKey

class TestModels(unittest.TestCase):
    def setUp(self):
        # Create in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_user_creation(self):
        """Test user model creation with valid data"""
        user = User(
            telegram_id="123456789",
            username="test_user",
            first_name="Test",
            last_name="User"
        )
        self.session.add(user)
        self.session.commit()
        
        self.assertIsNotNone(user.id)
        self.assertEqual(user.telegram_id, "123456789")
        self.assertIsInstance(user.created_at, datetime)

    def test_user_required_fields(self):
        """Test user model requires telegram_id"""
        with self.assertRaises(Exception):
            user = User(username="incomplete_user")
            self.session.add(user)
            self.session.commit()

    def test_strategy_creation(self):
        """Test strategy model creation with valid data"""
        user = User(telegram_id="123")
        self.session.add(user)
        self.session.commit()
        
        strategy = Strategy(
            user_id=user.id,
            name="basic",
            config={"param1": "value1"},
            capital=1000.0,
            is_active=1
        )
        self.session.add(strategy)
        self.session.commit()
        
        self.assertIsNotNone(strategy.id)
        self.assertEqual(strategy.name, "basic")
        self.assertEqual(strategy.config, {"param1": "value1"})

    def test_strategy_defaults(self):
        """Test strategy model default values"""
        user = User(telegram_id="123")
        self.session.add(user)
        self.session.commit()
        
        strategy = Strategy(user_id=user.id, name="starter")
        self.session.add(strategy)
        self.session.commit()
        
        self.assertEqual(strategy.capital, 0.0)
        self.assertEqual(strategy.is_active, 0)

    def test_trade_relationships(self):
        """Test trade relationships with user and strategy"""
        user = User(telegram_id="trader")
        strategy = Strategy(user_id=user.id, name="advanced")
        trade = Trade(
            user_id=user.id,
            strategy_id=strategy.id,
            symbol="BTC/USDT",
            type="buy",
            amount=0.1,
            price=50000.0
        )
        
        self.session.add_all([user, strategy, trade])
        self.session.commit()
        
        self.assertEqual(trade.user, user)
        self.assertEqual(trade.strategy, strategy)
        self.assertIn(trade, user.trades)
        self.assertIn(trade, strategy.trades)

    def test_api_key_encryption_fields(self):
        """Test API key model has required encryption fields"""
        user = User(telegram_id="apiuser")
        api_key = APIKey(
            user_id=user.id,
            exchange="binance",
            encrypted_key="encrypted_key_data",
            encrypted_secret="encrypted_secret_data"
        )
        self.session.add_all([user, api_key])
        self.session.commit()
        
        self.assertIsNotNone(api_key.id)
        self.assertEqual(api_key.exchange, "binance")
        self.assertEqual(api_key.encrypted_key, "encrypted_key_data")

    def test_api_key_required_fields(self):
        """Test API key model requires all fields"""
        with self.assertRaises(Exception):
            api_key = APIKey(exchange="binance")
            self.session.add(api_key)
            self.session.commit()

if __name__ == '__main__':
    unittest.main()