#!/usr/bin/env python3

"""
This is a simple client implementation based on telnetlib that can help you connect to the remote server.

Taken from https://cryptohack.org/challenges/introduction/
"""

import telnetlib
import json
from string import printable
from string import ascii_letters, digits
ALPHABET = ascii_letters + digits
# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True

# Remember to change the port if you are re-using this client for other challenges
PORT = 50222

if REMOTE:
    host = "aclabs.ethz.ch"
else:
    host = "localhost"

tn = telnetlib.Telnet(host, PORT)
def pkcs7_padding(data, block_size):
    pad_size = block_size - len(data) % block_size
    padding = bytes([pad_size] * pad_size)
    return data + padding

def readline():
    return tn.read_until(b"\n")

def json_recv():
    line = readline()
    return json.loads(line.decode())

def json_send(req):
    request = json.dumps(req).encode()
    tn.write(request + b"\n")
final_ans = "3y_4n1_w0n't_y0u_m0s3y_0n_d0wn_fr0m_7h3_l1gh7?}"
# final_ans = ''
for i in range(6):
    request = {
                # "command": "intro"
                "command": "encrypt", "prepend_pad": '1'*(22+i*2)
            }
    json_send(request)
    response = json_recv()
    byte_str = response['res'][-128:-96]
    print(byte_str)
    print(response)
    ans = 0
    for j in printable:
        # print(pkcs7_padding((j+final_ans).encode(), 16).hex())
        request = {
                # "command": "intro"
                "command": "encrypt", "prepend_pad": pkcs7_padding((j+final_ans).encode(), 16).hex()
            }
        json_send(request)
        response = json_recv()
        if response['res'][:32] == byte_str:
            ans = j
        # print(response)
    print(ans)
    final_ans = ans + final_ans
    # request = {"command": "solve", "solve": ans}
    # json_send(request)
    # response = json_recv()
    # print(response)
print(final_ans)
# r0m_7h3_l1gh7?}