import logging
import sys
from config.settings import Config

def setup_logging():
    """Configure logging with file and console handlers"""
    logger = logging.getLogger()
    logger.setLevel(Config.LOG_LEVEL)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # File handler
    fh = logging.FileHandler('trading_bot.log')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    return logger