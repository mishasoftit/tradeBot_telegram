from cryptography.fernet import Fernet
from config.settings import Config
import base64
import os

class EncryptionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EncryptionManager, cls).__new__(cls)
            # Generate key from environment variable
            key = base64.urlsafe_b64encode(Config.ENCRYPTION_KEY.encode()[:32].ljust(32, b'\0'))
            cls._instance.cipher = Fernet(key)
        return cls._instance

    def encrypt(self, data):
        if isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data).decode()

    def decrypt(self, encrypted_data):
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        return self.cipher.decrypt(encrypted_data).decode()

# Convenience functions
def encrypt_api_key(api_key):
    return EncryptionManager().encrypt(api_key)

def decrypt_api_key(encrypted_key):
    return EncryptionManager().decrypt(encrypted_key)