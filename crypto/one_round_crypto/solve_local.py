#!/usr/bin/env python3

import os

from core import dec_block, enc, DIM


def main():
    key_hex = os.getenv('KEY_HEX', '00112233445566778899aabbccddeeff')
    key = bytes.fromhex(key_hex)

    # Equivalent to the first free oracle query.
    _ = enc('00', key)

    for _ in range(100):
        m = os.urandom(DIM - 1)
        c = bytes.fromhex(enc(m.hex(), key))
        recovered = dec_block(c, key)
        assert recovered[:-1] == m and recovered[-1] == 1

    print('local verification passed: solved 100/100 rounds')


if __name__ == '__main__':
    main()
