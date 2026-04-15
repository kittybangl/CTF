import secrets
# from boilerplate import CommandServer, on_command, on_startup

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
a = secrets.token_bytes(1)
b = a + b'\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f'
print(b)
print(len(b))
import secrets
from Crypto.Util.strxor import strxor
print(strxor('9999'.encode(), '9999'.encode()))
# result_set = set()
# data = b''
# for key in range(0x100):
#     key = bytes.fromhex('{:02x}'.format(key))
#     result_set.add(key + b'\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f')
#     data += (key + b'\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f')
# # print(result_set)
# # print(b)
# # print(len(b))
# b += b'111'
# b = b.hex()
# print(len(b))
