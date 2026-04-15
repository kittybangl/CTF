def pkcs7_padding(data, block_size):
    pad_size = block_size - len(data) % block_size
    padding = bytes([pad_size] * pad_size)
    return data + padding
print(pkcs7_padding("hello world".encode(), 16).hex())