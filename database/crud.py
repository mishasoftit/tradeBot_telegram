from .db_session import Session
from .models import User, Strategy, Trade, APIKey
from .encryption import encrypt_api_key, decrypt_api_key

class CRUD:
    @staticmethod
    def create_user(telegram_id, username, first_name, last_name):
        session = Session()
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        session.add(user)
        session.commit()
        return user

    @staticmethod
    def get_user_by_telegram_id(telegram_id):
        session = Session()
        return session.query(User).filter_by(telegram_id=telegram_id).first()

    @staticmethod
    def create_strategy(user_id, name, config, capital=0.0):
        session = Session()
        strategy = Strategy(
            user_id=user_id,
            name=name,
            config=config,
            capital=capital
        )
        session.add(strategy)
        session.commit()
        return strategy

    @staticmethod
    def get_active_strategy(user_id):
        session = Session()
        return session.query(Strategy).filter_by(
            user_id=user_id,
            is_active=1
        ).first()

    @staticmethod
    def create_trade(user_id, strategy_id, symbol, trade_type, amount, price, fee=0.0, status='open'):
        session = Session()
        trade = Trade(
            user_id=user_id,
            strategy_id=strategy_id,
            symbol=symbol,
            type=trade_type,
            amount=amount,
            price=price,
            fee=fee,
            status=status
        )
        session.add(trade)
        session.commit()
        return trade

    @staticmethod
    def update_trade_status(trade_id, status):
        session = Session()
        trade = session.query(Trade).get(trade_id)
        if trade:
            trade.status = status
            session.commit()
        return trade

    @staticmethod
    def store_api_key(user_id, exchange, api_key, api_secret):
        session = Session()
        encrypted_key = encrypt_api_key(api_key)
        encrypted_secret = encrypt_api_key(api_secret)
        api_key = APIKey(
            user_id=user_id,
            exchange=exchange,
            encrypted_key=encrypted_key,
            encrypted_secret=encrypted_secret
        )
        session.add(api_key)
        session.commit()
        return api_key

    @staticmethod
    def get_api_keys(user_id):
        session = Session()
        return session.query(APIKey).filter_by(user_id=user_id).all()

    @staticmethod
    def get_decrypted_api_key(api_key_id):
        session = Session()
        api_key = session.query(APIKey).get(api_key_id)
        if api_key:
            return {
                'key': decrypt_api_key(api_key.encrypted_key),
                'secret': decrypt_api_key(api_key.encrypted_secret)
            }
        return None