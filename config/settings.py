import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram settings
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS', '').split(',') if x]
    
    # Database settings
    DB_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/dbname')
    
    # Exchange settings
    EXCHANGE_API_KEY = os.getenv('EXCHANGE_API_KEY')
    EXCHANGE_API_SECRET = os.getenv('EXCHANGE_API_SECRET')
    
    # Encryption
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
    
    # Strategy defaults
    DEFAULT_STRATEGY = os.getenv('DEFAULT_STRATEGY', 'starter')
    RISK_PERCENT = float(os.getenv('RISK_PERCENT', 1.0))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Validate essential configuration"""
        if not cls.TELEGRAM_TOKEN:
            raise ValueError('TELEGRAM_TOKEN is not set')
        if not cls.EXCHANGE_API_KEY or not cls.EXCHANGE_API_SECRET:
            raise ValueError('Exchange API credentials are not set')
        if not cls.ENCRYPTION_KEY:
            raise ValueError('ENCRYPTION_KEY is not set')