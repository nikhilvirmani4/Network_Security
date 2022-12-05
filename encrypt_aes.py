# pip install pycryptodomex

from Cryptodome.Cipher import AES
from hash import *

def encrypt(plaintext, key, hashed_data):
    B = plaintext + hashed_data
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(B)
    return ciphertext, nonce, tag

