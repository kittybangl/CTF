from Crypto.Cipher import AES
from Crypto.Hash import SHA256

CIPHERTEXT = "79b04593c08cb44da3ed9393e3cbb094ad1ea5b7af8a40457ce87f2c3095e29980a28da9b2180061e56f61cd3ee023ebb08e8607bc44ae37682b1a4a39ca7eaf285b32f575a8bfb630ccd1548c6a7c6d78ceec8e1f45866a0f17bf5216c29ca3"
CONST_IV = "e764ea639dc187d058554645ed1714d8"

def aes_cbc_decryption(ciphertext: bytes, key: bytes, iv: bytes):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

def generate_aes_key_from_int(integer: int, key_length: int):
    seed = (integer).to_bytes(2, byteorder='big')
    hash_object = SHA256.new(seed)
    aes_key = hash_object.digest()
    trunc_key = aes_key[:key_length]
    return trunc_key

def check_meaningful(plaintext: bytes):
    return plaintext.isascii()

def main():
    ciphertext = bytes.fromhex(CIPHERTEXT)
    iv = bytes.fromhex(CONST_IV)

    for i in range(0x10000):
        key = generate_aes_key_from_int(i, 16)
        plaintext = aes_cbc_decryption(ciphertext, key, iv)
        if check_meaningful(plaintext):
            print(plaintext)


if __name__ == '__main__':
    main()