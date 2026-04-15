#!/usr/bin/env python3
# from https://cryptohack.org/challenges/introduction/

import telnetlib
import json
from Crypto.Util.strxor import strxor
# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True

# Remember to change the port if you are re-using this client for other challenges
PORT = 50403

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

def blockify(a):
    return [bytes.fromhex(a[i : i + 32]) for i in range(0, len(a), 32)]

request = {
        "command": "flag"
}

json_send(request)
response = json_recv()
print(response)
result_set = set()
data = b''
for key in range(0x100):
    key = bytes.fromhex('{:02x}'.format(key))
    result_set.add(key + b'\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f')
    data += (key + b'\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f')
# print(result_set)
# print(b)
# print(len(b))
data += b'111'
data = data.hex()
file_name = "f"
file_name = file_name.encode()
data_fromhex = bytes.fromhex(data)

ctxt = (
    b"filename="
    + file_name
    + b"&data="
    + data_fromhex
    + b"&secret_byte="
).hex()
ctxt = blockify(ctxt)
for cnt in range(10):
    request = {
            "command": "encrypt",
            "file_name": "f",
            "data": data
    }
    json_send(request)
    response = json_recv()
    # print(response)
    iv = response['iv']
    ptxt = response['ctxt']

    ptxt = blockify(ptxt)
    print(len(ptxt))
    # print(ptxt)
    tmp = []
    for i in range(len(ptxt)):
        if i == 0:
            tmp.append(strxor(bytes.fromhex(iv), ptxt[i]).hex())
        else:
            # print(i)
            # print(ctxt[i-1])
            # print(len(ctxt[i-1]))
            # print(ptxt[i])
            # print(len(ptxt[i]))
            tmp.append(strxor(ctxt[i-1], ptxt[i]).hex())
    ans = b''
    for i in range(1, 257):
        if tmp[i] == tmp[258]:
            ans = bytes.fromhex('{:02x}'.format(i-1))
    print(ans.hex())
    request = {
            "command": "solve",
            "solve": ans.hex()
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