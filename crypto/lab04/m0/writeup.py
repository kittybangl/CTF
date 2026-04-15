#!/usr/bin/env python3
# from https://cryptohack.org/challenges/introduction/

import telnetlib
import json
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True

# Remember to change the port if you are re-using this client for other challenges
PORT = 50400

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
l = set()
for lkey in range(0x10000):
    lkey = bytes.fromhex('{:04x}'.format(lkey))
    # key = bytes.fromhex(str(key[2:]))
    # print(lkey)
    lkey = SHA256.new(lkey).digest()
    lcipher = AES.new(lkey, AES.MODE_ECB)
    msg = b'0' * 16
    ctxt = lcipher.encrypt(msg)
    # print(ctxt)
    l.add(ctxt)

key = set()
for rkey in range(0x10000):
    rkey = bytes.fromhex('{:04x}'.format(rkey))
    # print(rkey)
    rkey = SHA256.new(rkey).digest()
    rcipher = AES.new(rkey, AES.MODE_ECB)
    key.add(rcipher)
# print(key)
for i in range(64):
    request = {
                    "command": "query",
                    "m": "30303030303030303030303030303030"
                }
    # print(request)
    json_send(request)
    response = json_recv()
    # print(response)
    msg = bytes.fromhex(response['res'])
    # print(len(msg))
    flag = 1
    for k in key:
        tmp = k.decrypt(msg)
        if tmp in l:
            flag = 0
            break
    print(flag)
    request = { 
                    "command": "guess",
                    "b": flag
                }
    json_send(request)
    response = json_recv()
    print(response)

request = {
                "command": "flag"
            }
json_send(request)
response = json_recv()
print(response['flag'])
