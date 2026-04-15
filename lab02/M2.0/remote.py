#!/usr/bin/env python3

"""
This is a simple client implementation based on telnetlib that can help you connect to the remote server.

Taken from https://cryptohack.org/challenges/introduction/
"""

import telnetlib
import json

# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True

# Remember to change the port if you are re-using this client for other challenges
PORT = 50220

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

for i in range(20, 22, 2):
    request = {
        # "command": "intro"
        "command": "encrypt", "prepend_pad": '666c61672c20706c6561736521030303'
    }
    json_send(request)

    response = json_recv()
    print(i)
    print(response)

request = {"command": "solve", "ciphertext": "ff7837b501ffd7f49d895d83dad0344f"}

json_send(request)
response = json_recv()
print(response)
# f1156d2ff22bda815da1c3852b0f3ce555e284c0288ee604bd1ed578b0ee13e619987e8b127e7ee60d5b70007e16207a
# 35d14e6d3e3a279cf01e343e34e7ded