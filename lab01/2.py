from binascii import unhexlify

def xor(X, Y):
    return bytes(x ^ y for (x, y) in zip(X, Y))

c = b"210e09060b0b1e4b4714080a02080902470b0213470a0247081213470801470a1e4704060002"
c_b = unhexlify(c)
print(c_b)
key = 0
for i in range(256):
    plaintext = xor(c_b, [i]*len(c_b))
    print(i, plaintext)
    # print(xor(c, [i]))
        