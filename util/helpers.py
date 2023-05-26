import jwt
from cryptography.fernet import Fernet
from django.conf import settings

def encrypt(message):
    if is_encrypted(message):
        return message
    if message is None:
        return message
    f = Fernet(settings.FERNET_KEY.encode())  # no
    encrypted = f.encrypt(message.encode())
    return encrypted.decode("utf-8")


def decrypt(encrypted):
    try:
        f = Fernet(settings.FERNET_KEY.encode())
        decrypted = f.decrypt(encrypted.encode())
        return decrypted.decode("utf-8")
    except Exception:
        return encrypted


def is_encrypted(message):
    try:
        f = Fernet(settings.FERNET_KEY.encode())
        f.decrypt(message.encode())
        return True
    except Exception:
        return False


