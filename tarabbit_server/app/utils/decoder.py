from cryptography.fernet import Fernet

class Decoder:
    def __init__(self, secret_key, encrypted_message):
        self.secret_key = secret_key
        self.encrypted_message = encrypted_message
        
    def decrypt(self):
        cipher_suite = Fernet(self.secret_key)
        decrypted_message = cipher_suite.decrypt(self.encrypted_message)
        return decrypted_message.decode("utf-8")