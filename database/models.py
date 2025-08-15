from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(50), unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    strategies = relationship('Strategy', back_populates='user')
    api_keys = relationship('APIKey', back_populates='user')
    trades = relationship('Trade', back_populates='user')

class Strategy(Base):
    __tablename__ = 'strategies'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(50), nullable=False)  # starter, basic, etc.
    config = Column(JSON)  # Strategy-specific parameters
    capital = Column(Float, default=0.0)
    is_active = Column(Integer, default=0)  # 0=inactive, 1=active
    
    user = relationship('User', back_populates='strategies')
    trades = relationship('Trade', back_populates='strategy')

class Trade(Base):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    strategy_id = Column(Integer, ForeignKey('strategies.id'), nullable=False)
    symbol = Column(String(20), nullable=False)
    type = Column(String(10))  # buy/sell
    amount = Column(Float)
    price = Column(Float)
    fee = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20))  # open, closed, cancelled
    
    user = relationship('User', back_populates='trades')
    strategy = relationship('Strategy', back_populates='trades')

class APIKey(Base):
    __tablename__ = 'api_keys'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    exchange = Column(String(20), nullable=False)  # binance, bybit, etc.
    encrypted_key = Column(String(255), nullable=False)
    encrypted_secret = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='api_keys')
