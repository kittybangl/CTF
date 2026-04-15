


from binascii import unhexlify

def xor(X, Y):
    return bytes(x ^ y for (x, y) in zip(X, Y))

c = "Pay no mind to the distant thunder, Beauty fills his head with wonder, boy"
otp = b"bca914890bc40728b3cf7d6b5298292d369745a2592ad06ffac1f03f04b671538fdbcff6bd9fe1f086863851d2a31a69743b0452fd87a993f489f3454bbe1cab4510ccb979013277a7bf"

c1_b = c.encode()
otp_b = unhexlify(otp)
plaintext = xor(c1_b, otp_b)
print(plaintext.hex())