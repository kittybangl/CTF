#!/usr/bin/env python3
# from https://cryptohack.org/challenges/introduction/

import telnetlib
import json
from typing import Tuple
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA256
import time
# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True
# Remember to change the port if you are re-using this client for other challenges
PORT = 51003
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

for i in range(256):
    request = {
        "command": "get_params"
    }
    json_send(request)
    response = json_recv()

    N = response['N']
    e = response['e']

    request = {
        "command": "get_challenge"
    }
    json_send(request)
    response = json_recv()
    # print(response)
    challenge = response['challenge']
    # print(challenge)
    challenge = int(challenge, 16)

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

request = {
        "command": "flag"
}
json_send(request)
response = json_recv()
print(response['flag'])