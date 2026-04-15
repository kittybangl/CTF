from Crypto.Random import get_random_bytes

def xor(X, Y):
    return bytes(x ^ y for (x, y) in zip(X, Y))

ptxt1 = b" REDACTED "
ptxt2 = b"flag{" + ptxt1 + b"}"

key = get_random_bytes(len(ptxt1))
print(key.hex())
print(get_random_bytes(len(ptxt2) - len(ptxt1)).hex())
ctxt1 = xor(ptxt1, key)
ctxt2 = xor(ptxt2, key + get_random_bytes(len(ptxt2) - len(ptxt1)))

print(ctxt1.hex(), ctxt2.hex())
# d43f577d01
# d43f577d01ce1d7f
# d43f577d01ce1d7f1d0001cb42