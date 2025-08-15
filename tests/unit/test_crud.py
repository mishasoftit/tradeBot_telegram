import unittest
from unittest.mock import patch, MagicMock
from database.crud import CrudOperations
from database.models import User, APIKey
from sqlalchemy.orm import Session

class TestCrudOperations(unittest.TestCase):

    @patch('database.crud.Session')
    def setUp(self, mock_session):
        self.mock_session = MagicMock(spec=Session)
        mock_session.return_value = self.mock_session

    def test_create_user(self):
        user_data = {'telegram_id': 123, 'username': 'test_user'}
        CrudOperations.create_user(**user_data)
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()

    @patch('database.encryption.encrypt_api_key')
    def test_store_api_key(self, mock_encrypt):
        mock_encrypt.side_effect = [b'enc_key', b'enc_secret']
        CrudOperations.store_api_key(123, 'binance', 'api_key', 'api_secret')
        
        # Verify encryption calls
        mock_encrypt.assert_any_call('api_key')
        mock_encrypt.assert_any_call('api_secret')
        
        # Verify database operations
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()

    @patch('database.encryption.decrypt_api_key')
    def test_get_decrypted_api_key(self, mock_decrypt):
        mock_decrypt.side_effect = ['dec_key', 'dec_secret']
        mock_key = MagicMock(spec=APIKey)
        mock_key.encrypted_key = b'enc_key'
        mock_key.encrypted_secret = b'enc_secret'
        
        self.mock_session.query.return_value.get.return_value = mock_key
        
        result = CrudOperations.get_decrypted_api_key(1)
        self.assertEqual(result, {'key': 'dec_key', 'secret': 'dec_secret'})
        mock_decrypt.assert_any_call(b'enc_key')
        mock_decrypt.assert_any_call(b'enc_secret')

if __name__ == '__main__':
    unittest.main()