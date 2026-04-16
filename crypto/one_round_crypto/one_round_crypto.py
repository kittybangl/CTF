#!/usr/bin/env python3

import os
from core import DIM, enc

flag = os.getenv('FLAG', 'ECSC{testflag}')
key = bytes.fromhex(os.getenv('KEY_HEX')) if os.getenv('KEY_HEX') else os.urandom(16)

m = input('> ')
print(enc(m, key))

print('=' * 50)

for _ in range(100):
    m = os.urandom(DIM - 1).hex()
    e = enc(m, key)
    print(e)
    guess = input('> ')
    if guess != m:
        print('Wrong!')
        exit()

print(flag)
