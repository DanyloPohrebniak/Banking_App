import os
import random
import hashlib


# def check_login(current_user):
#     if current_user is None:
#         print("You have to log in or create new account!")
#         return False
#     return True


def generate_mfa_code():
    '''Generate the MFA code'''
    return str(random.randint(100000, 999999))


def hash_password(password: str, salt: bytes = None) -> str:
    '''Hash user password'''
    if not salt:
        salt = os.urandom(16)
    hash_ = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return salt.hex() + ":" + hash_.hex()


def check_password(password: str, stored: str) -> bool:
    '''Password check'''
    try:
        salt_hex, hash_hex = stored.split(":")
        salt = bytes.fromhex(salt_hex)
        new_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000).hex()
        return new_hash == hash_hex
    except(ValueError, TypeError):
        return False
