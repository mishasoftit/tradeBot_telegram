import unittest
from unittest.mock import patch
from database.encryption import EncryptionManager, encrypt_api_key, decrypt_api_key

class TestEncryptionManager(unittest.TestCase):

    @patch('database.encryption.Config')
    def setUp(self, mock_config):
        # Setup mock configuration with a fixed key
        mock_config.ENCRYPTION_KEY = 'test_key_32_characters_long!'
        self.manager = EncryptionManager()

    def test_singleton_pattern(self):
        """Test that only one instance exists"""
        second_manager = EncryptionManager()
        self.assertIs(self.manager, second_manager)

    def test_encrypt_decrypt_string(self):
        """Test encrypt/decrypt cycle with string data"""
        original = "sensitive_data"
        encrypted = self.manager.encrypt(original)
        decrypted = self.manager.decrypt(encrypted)
        self.assertEqual(original, decrypted)

    def test_encrypt_decrypt_bytes(self):
        """Test encrypt/decrypt cycle with bytes data"""
        original = b"binary_data"
        encrypted = self.manager.encrypt(original)
        decrypted = self.manager.decrypt(encrypted)
        self.assertEqual(original, decrypted)

    def test_encrypt_api_key(self):
        """Test API key encryption helper function"""
        api_key = "api_key_123"
        encrypted = encrypt_api_key(api_key)
        self.assertIsInstance(encrypted, str)
        self.assertNotEqual(api_key, encrypted)

    def test_decrypt_api_key(self):
        """Test API key decryption helper function"""
        api_key = "api_key_123"
        encrypted = encrypt_api_key(api_key)
        decrypted = decrypt_api_key(encrypted)
        self.assertEqual(api_key, decrypted)

    @patch('database.encryption.Fernet')
    def test_invalid_key_length(self, mock_fernet):
        """Test handling of invalid key length"""
        with self.assertRaises(ValueError):
            self.manager.cipher  # Force initialization with bad key

    def test_tampered_data(self):
        """Test decryption fails with tampered data"""
        original = "sensitive_data"
        encrypted = self.manager.encrypt(original)
        # Tamper with the encrypted data
        tampered = encrypted[:-1] + ('a' if encrypted[-1] != 'a' else 'b')
        with self.assertRaises(Exception):
            self.manager.decrypt(tampered)

if __name__ == '__main__':
    unittest.main()