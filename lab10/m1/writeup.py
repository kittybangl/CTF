#!/usr/bin/env python3
# from https://cryptohack.org/challenges/introduction/

import telnetlib
import json
# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True
# Remember to change the port if you are re-using this client for other challenges
PORT = 51001
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

def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        d, x, y = extended_gcd(b, a % b)
        return (d, y, x - (a // b) * y)
    
p = 2**127 - 1
TAG_LEN = 16

msg1 = "Give me a flah "
msg2 = "Give me a flah!"

nonce = '1' * 16
request = {
    "command": "encrypt",
    "message": msg1,
    "nonce": nonce
}
json_send(request)
response = json_recv()
# print(response)
tag1 = response['tag']
tag1 = bytes.fromhex(tag1)
tag1 = int.from_bytes(tag1, byteorder='big')
c1 = response['ciphertext']
c1: int = int.from_bytes(bytes.fromhex(c1), "big") % p
# print(tag1)

request = {
    "command": "encrypt",
    "message": msg2,
    "nonce": nonce
}
json_send(request)
response = json_recv()
# print(response)
tag2 = response['tag']
tag2 = bytes.fromhex(tag2)
tag2 = int.from_bytes(tag2, byteorder='big')
c2 = response['ciphertext']
c2: int = int.from_bytes(bytes.fromhex(c2), "big") % p
# print(tag2)

a = tag1 - tag2
b = c1 - c2
_, b_inv, _ = extended_gcd(b, p)
K_pow_2 = (a * b_inv) % p
# print(K_pow_2)


msg = "Give me a flag "
request = {
    "command": "encrypt",
    "message": msg,
    "nonce": nonce
}
json_send(request)
response = json_recv()
# print(response)
tag = response['tag']
ciphertext = int(response['ciphertext'], 16)
if ciphertext % 2:
    ciphertext -= 1
else:
    ciphertext += 1
# print(ciphertext)
# c: int = int.from_bytes(ciphertext.to_bytes(16, "big"), "big") % p
# print(c)
# print(c1)
tag = (tag1 + (ciphertext - c1) * K_pow_2) % p
# print(hex(tag))
# print(hex(ciphertext))
request = {
    "command": "decrypt",
    "ciphertext": hex(ciphertext)[2:].zfill(30),
    "tag": hex(tag)[2:].zfill(32),
    "nonce": nonce
}
json_send(request)
response = json_recv()
print(response['res'].split("That's illegal. ")[1])