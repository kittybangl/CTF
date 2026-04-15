#!/usr/bin/env python3
# from https://cryptohack.org/challenges/introduction/

import telnetlib
import json
# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True
import math
# Remember to change the port if you are re-using this client for other challenges
PORT = 51000
from Crypto.Hash import MD5, HMAC, SHA256
from typing import Tuple
if REMOTE:
    host = "aclabs.ethz.ch"
else:
    host = "localhost"

tn = telnetlib.Telnet(host, PORT)
def readline():
    return tn.read_until(b"\n")

def json_recv():
    line = readline()
    return json.loads(line.decode())

def json_send(req):
    request = json.dumps(req).encode()
    tn.write(request + b"\n")

def get_nonce(msg: bytes, sign_key: int, g: int, p: int, q: int) -> Tuple[int, int]:
    # Because we don't trust our server, we will be hedging against randomness failures by derandomising

    h = MD5.new(msg).digest()

    # We begin by deterministically deriving a nonce
    # as specified in https://datatracker.ietf.org/doc/html/rfc6979#section-3.2
    l = 8 * MD5.digest_size
    rlen = math.ceil(q.bit_length() / 8)
    V = bytes([1] * l)
    K = bytes([0] * l)

    K = HMAC.new(K, V + b'\x00' + sign_key.to_bytes(rlen, "big") + h).digest()
    V = HMAC.new(K, V).digest()
    K = HMAC.new(K, V + b'\x01' + sign_key.to_bytes(rlen, "big") + h).digest()
    V = HMAC.new(K, V).digest()

    while True:
        T = b''
        tlen = 0

        while tlen < q.bit_length():
            V = HMAC.new(K, V).digest()
            T += V
            tlen += len(V) * 8

        # Apply bits2int and bring down k to the length of q
        k = int.from_bytes(T, "big")
        k >>= k.bit_length() - q.bit_length()

        r = pow(g, k, p) % q

        if 1 <= k <= q-1 and r != 0:
            break

        K = HMAC.new(K, V + b'\x00').digest()
        V = HMAC.new(K, V).digest()

    return k, r

def DSA_sign(msg: bytes, sign_key: int, g: int, p: int, q: int):
    # Get k and r = (g^k mod p) mod q
    k, r = get_nonce(msg, sign_key, g, p, q)
    # Compute the signature
    h = int.from_bytes(SHA256.new(msg).digest(), "big")
    s = (pow(k, -1, q) * (h + sign_key * r)) % q
    return r, s

def find_b(s: int, a: int, q: int) -> int:
    gcd, x, _ = extended_gcd(a, q)
    if gcd != 1:
        raise ValueError("No answer")
    return (s * gcd) % q

def find_x(a, b, q):
    gcd, x, _ = extended_gcd(b, q)
    if gcd != 1:
        raise ValueError("No answer")
    b_inv = x % q
    x = (a * b_inv) % q
    return x

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return d, x, y
request = {
    "command": "get_params"
}
    # print(request['m'])
json_send(request)
response = json_recv()
# print(response)
q = response['q']
sign_key = response['vfy_key']
g = response['g']
p = response['p']
msg1 = "d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f8955ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5bd8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70"
msg2 = "d131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f8955ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5bd8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70"
request = {
    "command": "sign",
    "message": msg1
}
    # print(request['m'])
json_send(request)
response = json_recv()
# print(response)
s1 = response['s']
r = response['r']

request = {
    "command": "sign",
    "message": msg2
}
json_send(request)
response = json_recv()
# print(response)
s2 = response['s']
h1 = int.from_bytes(SHA256.new(bytes.fromhex(msg1)).digest(), "big")
h2 = int.from_bytes(SHA256.new(bytes.fromhex(msg2)).digest(), "big")
pow1 = ((s1 - s2 + q) * pow(h1 - h2, q - 2, q) % q)
sign_key = find_x(s1 - ((pow1*h1) % q), pow1 * r, q)
# print(sign_key)

msg = b'Give me a flag!'
r, s = DSA_sign(msg, sign_key, g, p, q)
request = {
    "command": "flag",
    "r": r,
    "s": s
}
json_send(request)
response = json_recv()
print(response['flag'])