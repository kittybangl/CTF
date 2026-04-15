

from binascii import unhexlify

def xor(X, Y):
    return bytes(x ^ y for (x, y) in zip(X, Y))

c1 = "One time pad is perfectly secure, what can go wroNg?"
c2 = "flag{One time pad is perfectly secure, what can go wroNg?}"
otp1 = b'9b51325d75a7701a3d7060af62086776d66a91f46ec8d426c04483d48e187d9005a4919a6d58a68514a075769c97093e29523ba0'
otp2 = b'b253361a7a81731a3d7468a627416437c22f8ae12bdbc538df0193c581142f864ce793806900a6911daf213190d6106c21537ce8760265dd83e4'
c1_b = c1.encode()
otp1_b = unhexlify(otp1)
plaintext = xor(c1_b, otp1_b)

print(len(c1))
print(len(otp1))
print(plaintext)
print(plaintext.hex())

c2_b = c2.encode()
otp2_b = unhexlify(otp2)
plaintext = xor(c2_b, otp2_b)
print(plaintext)
print(plaintext.hex())