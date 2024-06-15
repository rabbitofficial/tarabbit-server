from cryptography.fernet import Fernet

class Decoder:
    def decrypt(secret_key, encrypted_message):
        cipher_suite = Fernet(secret_key)
        decrypted_message = cipher_suite.decrypt(encrypted_message)
        return decrypted_message.decode("utf-8")