# pip install pycryptodome

from Crypto.Hash import SHA256
import hashlib
import os


def hash(key, iv):
    # key = b'z$B&E)H@McQfTjWnZr4u7x!A%D*F-JaN'
    # iv = os.urandom(16) 
    hash = key+iv   
    hashed_data = hashlib.sha256(hash).hexdigest()
    return hashed_data

