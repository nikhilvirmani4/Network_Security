#pip install pycryptodomex
#pip install pycryptodome

from Crypto.Hash import SHA256
import hashlib
from Cryptodome.Cipher import AES
from Crypto.Random import get_random_bytes
import re

session_key = b'zMDEyMzQ1Njc4OTAxT8G0PHUg00CQ5QY'
IV = get_random_bytes(32) 
MD = session_key+IV  #computing hash with the key and initial vector  
hash = bytes(hashlib.sha256(MD).hexdigest(), 'utf')
print(hash)
#b'0172ed7087445e22793ea97a7acc6cfe3fc24739dbcbdd5ff20b9c9873444841'

plaintext = b'This is the plaintext,'
block = plaintext + hash
cipher = AES.new(session_key, AES.MODE_OFB)
iv = cipher.iv
encypted_data= cipher.encrypt(block)

try:
  cipher = AES.new(session_key, AES.MODE_OFB, iv=iv)
  decrypted_data = cipher.decrypt(encypted_data).decode()
  print(re.split(',', decrypted_data))
  # 'This is the plaintext', '0172ed7087445e22793ea97a7acc6cfe3fc24739dbcbdd5ff20b9c9873444841'
  

except ValueError:
    print('Decryption failed')
