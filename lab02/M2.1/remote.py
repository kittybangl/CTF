#!/usr/bin/env python3

"""
This is a simple client implementation based on telnetlib that can help you connect to the remote server.

Taken from https://cryptohack.org/challenges/introduction/
"""

import telnetlib
import json
from string import ascii_letters, digits
ALPHABET = ascii_letters + digits
# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True

# Remember to change the port if you are re-using this client for other challenges
PORT = 50221

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
for i in range(5):
    request = {
            # "command": "intro"
        "command": "encrypt", "prepend_pad": ''
    }
    json_send(request)

    response = json_recv()
    print(response)
    base = len(response['res'])
    random_len = 0
    byte_str = ""
    for i in range(2, 32, 2):
        request = {
            # "command": "intro"
            "command": "encrypt", "prepend_pad": '1'*i
        }
        json_send(request)

        response = json_recv()
        tmp = len(response['res'])
        # print(i)
        # print(response)
        if tmp > base:
            random_len = i
            request = {
                # "command": "intro"
                "command": "encrypt", "prepend_pad": '1'*(i+2)
            }
            json_send(request)

            response = json_recv()
            tmp = len(response['res'])
            byte_str = response['res'][-32:]
            print(i+2)
            print(response)
            break
    print(random_len, byte_str)
    ans = 0
    for i in ALPHABET:
        request = {
                # "command": "intro"
                "command": "encrypt", "prepend_pad": i.encode().hex() + '0f' * 15
            }
        json_send(request)
        response = json_recv()
        if response['res'][:32] == byte_str:
            ans = i
        # print(response)
    print(ans)
    request = {"command": "solve", "solve": ans}
    json_send(request)
    response = json_recv()
    print(response)
request = {"command": "solve", "solve": ans}
json_send(request)
response = json_recv()
print(response)
# padding = '1' * (random_len+2)
# request = {
#         # "command": "intro"
#     "command": "encrypt", "prepend_pad": padding
# }
# json_send(request)

# response = json_recv()
# print(response['res'])
# print(response['res'][-32:])
# for i in range(97, 123):
#     request = {"command": "solve", "solve": chr(i)}

# json_send(request)
# response = json_recv()
# print(response)
# f1156d2ff22bda815da1c3852b0f3ce555e284c0288ee604bd1ed578b0ee13e619987e8b127e7ee60d5b70007e16207a
# 35d14e6d3e3a279cf01e343e34e7ded