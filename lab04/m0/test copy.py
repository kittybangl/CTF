
from enum import unique
from tracemalloc import start
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import secrets
import time
import binascii
# key = secrets.token_bytes(4)
# print(key)
# print(bytes.fromhex(key.hex()))
key = b'\x19\x8d\xdb\x94'
lkey = SHA256.new(key[:2]).digest()
rkey = SHA256.new(key[2:]).digest()
lcipher = AES.new(lkey, AES.MODE_ECB)
rcipher = AES.new(rkey, AES.MODE_ECB)
msg = b'1' * 32
ctxt = lcipher.encrypt(msg)
# print(ctxt)
ans = rcipher.encrypt(ctxt)
print(len(ans))
# print(ans.decode())
print(len(bytes.fromhex(ans.hex())))
ans2 = rcipher.decrypt(bytes.fromhex(ans.hex()))
print(ans2)
# tmp = b'\xb0\xb0\xb6\x0c.\xc1~\x8d\xf4R\xd0\x14^\x0b\x92U'
# ans2 = rcipher.decrypt(tmp)
l = []
for lkey in range(0x10000):
    lkey = bytes.fromhex('{:04x}'.format(lkey))
    # key = bytes.fromhex(str(key[2:]))
    # print(lkey)
    lkey = SHA256.new(lkey).digest()
    lcipher = AES.new(lkey, AES.MODE_ECB)
    msg = b'1' * 32
    ctxt = lcipher.encrypt(msg)
    # print(ctxt)
    l.append(ctxt)
print(ans2 in l)
