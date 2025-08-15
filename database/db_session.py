from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import Config

# Create database engine
engine = create_engine(Config.DB_URL)
Session = sessionmaker(bind=engine)