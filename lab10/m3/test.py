import secrets
from typing import Tuple
# from boilerplate import CommandServer, on_command, on_startup

from Crypto.PublicKey import RSA
from Crypto.Hash import SHAKE256

TARGET = 256

RSA_KEYLEN = 1024 # 1024-bit modulus
RAND_LEN = 256 # 256-bit of randomness for masking
P_LEN = (RSA_KEYLEN - RAND_LEN - 8) // 8

def xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def RSA_pad_encrypt(e: int, N: int, ptxt: bytes) -> Tuple[bytes, int]:
    if len(ptxt) >= P_LEN:
        raise ValueError("Message too long to encrypt")

    rand = secrets.token_bytes(RAND_LEN // 8)
    # We use SHAKE256 in order to implement a hash function with output size of our liking
    rand_hashed = SHAKE256.new(rand).read(P_LEN)
    ptxt_padded = b"\x00" * (P_LEN - len(ptxt) - 1) + b"\x01" + ptxt
    # print(P_LEN - len(ptxt) - 1)
    assert len(ptxt_padded) == P_LEN

    ptxt_masked = xor(rand_hashed, ptxt_padded)
    m = int.from_bytes(b'\x00' + rand + ptxt_masked, "big")
    
    print(m)
    return pow(m, e, N).to_bytes(RSA_KEYLEN // 8, 'big'), m.bit_length()

e = 65537
N = 139263993471996573487073263511964263045993090905484562495399825723906416016491233177740440995894874169086343587108635922472940160541048157807089474364146009830615805884002967770587275737970410852971104643384036039284038040911840625904109370860028751515771425235626746163307832040532868838037314559186456998309
message = b"If you use textbook RSA I will find you and hunt you down (cit.)"
challenge, length = RSA_pad_encrypt(e, N, message)
i = int.from_bytes(challenge, byteorder='big')
print(i.bit_length())
print(length)
# RSA_pad_encrypt()
print(xor(b'\x01', b'\x03'))
rand = b'\xba\xfb\xa0m\x08\xb1\xdf\x9d 36!\xcf\x17lQ\x89\x9b\xd3+|;\\\x9a\xd6p\xdf\xb2Z\x1d\x9b\xd1'
print(rand)
    # We use SHAKE256 in order to implement a hash function with output size of our liking
rand_hashed = SHAKE256.new(rand).read(P_LEN)
print(rand_hashed)
rand = b'\xba\xfb\xa0m\x08\xb1\xdf\x9d 36!\xcf\x17lQ\x89\x9b\xd3+|;\\\x9a\xd6p\xdf\xb2Z\x1d\x9b\xd2'
rand_hashed = SHAKE256.new(rand).read(P_LEN)
print(rand_hashed)
from Crypto.Util.number import long_to_bytes, bytes_to_long

a1 = 1<<15
a2 = 1<<2
p1 = pow(a1, e, N) % N
p2 = pow(a2, e, N) % N
p = pow((a1+a2)%N, e, N) % N
print(long_to_bytes(p1+p2))
print(long_to_bytes(p))
print(p1+p2 == p)