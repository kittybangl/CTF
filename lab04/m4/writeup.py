#!/usr/bin/env python3
# from https://cryptohack.org/challenges/introduction/

import telnetlib
import json
import time
import secrets
import binascii
from Crypto.Util.strxor import strxor
# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True

# Remember to change the port if you are re-using this client for other challenges
PORT = 50404

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

# print(result_set)
# print(b)
# print(len(b))

# ans = b''
ans = b'000000000&flag='
for cnt in range(86):
    result_set = set()
    data_fixed = b''
    for key in range(0x100):
        key = bytes.fromhex('{:02x}'.format(key))
        result_set.add(ans[-15:] + key)
        data_fixed += (ans[-15:] + key)
    data = data_fixed + b'0'*(105-cnt)
    data = data.hex()
    file_name = "f"
    file_name = file_name.encode()
    data_fromhex = bytes.fromhex(data)
    # print(ans[16:])
    ctxt = (
        b"filename="
        + file_name
        + b"&data="
        + data_fromhex
        + b"&flag="
        + ans[15:]
    ).hex()
    ctxt = blockify(ctxt)[:-1]
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
    # print(ptxt)
    tmp = []
    for i in range(len(ctxt)+1):
        if i == 0:
            tmp.append(strxor(bytes.fromhex(iv), ptxt[i]).hex())
        else:
            # print(i)
            tmp.append(strxor(ctxt[i-1], ptxt[i]).hex())
    # # print(len(tmp))
    # print(int(263-(cnt-15)/16))
    for i in range(1, 257):
        if tmp[i] == tmp[263]:
            ans += bytes.fromhex('{:02x}'.format(i-1))
print(ans[15:].decode())
#     request = {
#             "command": "solve",
#             "solve": ans.hex()
#     }

#     json_send(request)
#     response = json_recv()
#     print(response)

# request = {
#         "command": "flag"
# }

# json_send(request)
# response = json_recv()
# print(response)