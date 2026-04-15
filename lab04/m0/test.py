import secrets
import os
import time
import json
# from boilerplate import CommandServer, on_command, on_startup

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
rkey = secrets.token_bytes(4)
key = set()
start_time = time.time()
for i in range(0x10000):
    rkey = bytes.fromhex('{:04x}'.format(i))
    # print(rkey)
    rkey = SHA256.new(rkey).digest()
    rcipher = AES.new(rkey, AES.MODE_ECB)
    key.add(rcipher)
end_time = time.time()
print(end_time-start_time)
msg = b'1'*16
start_time = time.time()
for k in key:
    tmp = k.decrypt(msg)
end_time = time.time()

print(end_time-start_time)
start_time = time.time()
for k in key:
    a = k in key
end_time = time.time()
print(end_time-start_time)