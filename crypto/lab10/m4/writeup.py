#!/usr/bin/env python3
# from https://cryptohack.org/challenges/introduction/

import telnetlib
import json
from typing import Tuple
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA256
import time
from Crypto.PublicKey import RSA
from Crypto.Hash import SHAKE256
# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True
# Remember to change the port if you are re-using this client for other challenges
PORT = 51004
if REMOTE:
    host = "aclabs.ethz.ch"
else:
    host = "localhost"
RSA_KEYLEN = 1024 # 1024-bit modulus
RAND_LEN = 256 # 256-bit of randomness for masking
P_LEN = (RSA_KEYLEN - RAND_LEN - 8) // 8
tn = telnetlib.Telnet(host, PORT)
def readline():
    return tn.read_until(b"\n")

def json_recv():
    line = readline()
    return json.loads(line.decode())

def json_send(req):
    request = json.dumps(req).encode()
    tn.write(request + b"\n")

def xor(a: bytes, b: bytes) -> bytes:
    # assert len(a) == len(b), f"{len(a)}, {len(b)}"
    return bytes(x ^ y for x, y in zip(a, b))

def find_len(challenge, e, N):
    ans = 1016
    while True:
        challenge *= pow(2, e, N)
        challenge %= N
        request = {
            "command": "decrypt",
            "ctxt": hex(challenge)[2:].zfill(256)
        }
        json_send(request)
        response = json_recv()
        # print(response)
        if 'res' in response:
            # print(response)
            ans -= 1
            continue
        error = response['error']
        if 'Error:' in error:
            break
        ans -= 1
    # print(ans)
    request = {
        "command": "solve",
        "i": ans
    }
    json_send(request)
    response = json_recv()
    # print(response)
    return ans

def is_above_N(mid, challenge, e, N):
    # print(challenge)
    # print(tmp)
    # print(tmp.bit_length())
    challenge *= pow(mid, e, N)
    challenge %= N
    # print(hex(challenge)[2:].zfill(256))
    request = {
        "command": "decrypt",
        "ctxt": hex(challenge)[2:].zfill(256)
    }
    json_send(request)
    response = json_recv()
    if 'res' in response:
        return True
    error = response['error']
    # print(response)
    if 'Eror:' in error:
        # print(1)
        return True
    return False

def find_a0(challenge, len, e, N):
    min = pow(2, 1024-len-1)
    max = pow(2, 1024-len+1)
    ans = 0
    for i in range(min, max):
        if is_above_N(i, challenge, e, N) == True:
            ans = i
            print(i)
            break
    return ans

def ceil (a: int , b: int ) -> int : 
# Necessary because of floating point precision loss
    return a // b + (1 if a % b != 0 else 0)
def get_multiplier ( m_max : int , m_min : int , N: int , B: int) -> int : 
    tmp = ceil (2 * B , m_max - m_min)
    r = tmp * m_min // N 
    alpha = ceil (r * N , m_min)
    return alpha

if __name__ == '__main__':
    flag = False
    start_time = time.time()
    while True:
        if flag:
            break
        request = {
            "command": "get_params"
        }
        json_send(request)
        response = json_recv()

        N = response['N']
        e = response['e']

        request = {
            "command": "flag"
        }
        json_send(request)
        response = json_recv()
        challenge = response['flag']
        challenge = int(challenge, 16)

        # Step 1
        len = find_len(challenge, e, N)
        print("len", len)
        if len < 1011:
            break
        # Step 2
        a0 = find_a0(challenge, len, e, N)
        print("a0", a0)
        m_min = N // a0 - 10
        m_max = N // (a0-1) + 10
        print(m_max, m_min)


        B = 2<<1015
        alpha = get_multiplier(m_max, m_min, N, B)
        # α · mmin > rN
        r = alpha * m_min // N
        B_plus_rN = B + r*N
        # print(B_plus_rN//alpha)
        # print(is_above_N(alpha-1, challenge, e, N))
        cnt = 0
        while True:
            cnt += 1
            print(cnt)
            if cnt > 2000:
                break
            if (m_max - m_min <= 1):
                print(m_max)
                break
            alpha = get_multiplier(m_max, m_min, N, B)
            # print(alpha.bit_length())
            # print((alpha*(m_max-m_min)) - 2 * B)
            # α · mmin > rN
            r = alpha * m_min // N
            B_plus_rN = B + r*N
            if is_above_N(alpha, challenge, e, N):
                m_max = B_plus_rN//alpha
            else:
                m_min = B_plus_rN//alpha
        m_max = m_max.to_bytes(RSA_KEYLEN // 8, 'big')
        rand = m_max[1:1+RAND_LEN//8]
        ptxt_masked = m_max[1+RAND_LEN//8:]
        rand_hashed = SHAKE256.new(rand).read(P_LEN)
        # print(type(ptxt_masked))
        # print(type(rand_hashed))
        ptxt_padded = xor(ptxt_masked, rand_hashed)
        final_flag = ''
        for i, b in enumerate(ptxt_padded):
            if b == 1 and all(ch == 0 for ch in ptxt_padded[:i]):
                final_flag = ptxt_padded[i+1:]
                flag = True
        if b'flag{' and b'}' not in final_flag:
            flag = False
    end_time = time.time()
    print(final_flag.decode())
    print(end_time-start_time)