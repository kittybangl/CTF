#!/usr/bin/env python3
# from https://cryptohack.org/challenges/introduction/

import telnetlib
import json
from typing import Tuple
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA256
# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True
# Remember to change the port if you are re-using this client for other challenges
PORT = 51002
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

def DHIES_encrypt(sk: int, g: int, p: int, pk_other: int, ciphertext: int, tag: int, nonce: int) -> Tuple[int, bytes, bytes, bytes]:
    # Generate our ephemeral private key
    # sk = secrets.randbelow((p-1)//2) + 1
    pk = pow(g, sk, p)

    pk_bytes = pk.to_bytes(512, "big")

    # Compute shared Diffie-Hellman value
    shared = pow(pk_other, sk, p)
    shared_bytes = shared.to_bytes(512, "big")

    pk_other_bytes = pk_other.to_bytes(512, "big")

    # Compute symmetric key
    K: bytes = HKDF(shared_bytes + pk_bytes + pk_other_bytes, 32, salt=b"", num_keys=1, context=b"dhies-enc", hashmod=SHA256) #type: ignore
    cipher = AES.new(K, AES.MODE_GCM, nonce)
    try:
        data = cipher.decrypt_and_verify(ciphertext, tag)
        print(data.decode())
        # return data
    except:
        # print("error")
        pass

p = 2**1279-1	
prime_set = []
for i in range(1279): 
    prime_set.append(pow(2, i, p))
# print(prime_set)
# print(len(prime_set))

p = 2**1279-1
g = 2
request = {
    "command": "set_params",
    "p": p,
    "g": g
}
json_send(request)
response = json_recv()
# print(response)
bob_pubkey =  response['bob_pubkey']

for i in range(len(prime_set)):
    if prime_set[i] == bob_pubkey:
        bob_privkey = i
        break

request = {
    "command": "encrypt"
}
json_send(request)
response = json_recv()
# print(response)
pk = response['pk']
ciphertext = bytes.fromhex(response['ciphertext'])
tag = bytes.fromhex(response['tag'])
nonce = bytes.fromhex(response['nonce'])
# print(ciphertext, tag, nonce)
for i in range(1279):
    DHIES_encrypt(i, g, p, bob_pubkey, ciphertext, tag, nonce)
