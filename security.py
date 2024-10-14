from cryptography.fernet import Fernet
import os

def get_or_create_key():
    key_file = 'encryption_key.key'
    if os.path.exists(key_file):
        with open(key_file, 'rb') as file:
            key = file.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, 'wb') as file:
            file.write(key)
    return key

def encrypt_data(data):
    key = get_or_create_key()
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data):
    key = get_or_create_key()
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode()