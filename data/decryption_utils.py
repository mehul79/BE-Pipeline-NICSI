import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import logging

def decrypt_java_api(encrypted_text, key):
    try:
        secret_key = key.encode('utf-8')
        if len(secret_key) not in [16, 24, 32]:
            raise ValueError("Invalid key length.")
        iv = b'\x00' * 16
        cipher = Cipher(algorithms.AES(secret_key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_bytes = decryptor.update(base64.b64decode(encrypted_text)) + decryptor.finalize()
        padding_length = decrypted_bytes[-1]
        return decrypted_bytes[:-padding_length].decode('utf-8')
    except Exception as e:
        logging.error(f"Decryption error: {str(e)}")
        return encrypted_text

def decrypt_asp_dot_net_api(encrypted_text, key):
    try:
        secret_key = key.encode('utf-8')
        if len(secret_key) not in [16, 24, 32]:
            raise ValueError("Invalid key length.")
        iv = b'\x00' * 16
        cipher = Cipher(algorithms.AES(secret_key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_bytes = decryptor.update(base64.b64decode(encrypted_text)) + decryptor.finalize()
        padding_length = decrypted_bytes[-1]
        return decrypted_bytes[:-padding_length].decode('utf-8')
    except Exception as e:
        logging.error(f"Decryption error: {str(e)}")
        return encrypted_text

def decrypt_php_data(encrypted_text, key):
    try:
        combined_bytes = base64.b64decode(encrypted_text)
        iv = combined_bytes[:16]
        encrypted_bytes = combined_bytes[16:]
        secret_key = key.encode('utf-8')
        cipher = Cipher(algorithms.AES(secret_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_bytes = decryptor.update(encrypted_bytes) + decryptor.finalize()
        padding_length = decrypted_bytes[-1]
        return decrypted_bytes[:-padding_length].decode('utf-8')
    except Exception as e:
        logging.error(f"Decryption Error: {str(e)}")
        return encrypted_text
