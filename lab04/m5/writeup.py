#!/usr/bin/env python3
# from https://cryptohack.org/challenges/introduction/

import telnetlib
import json
import datetime
from Crypto.Util.strxor import strxor
# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True

# Remember to change the port if you are re-using this client for other challenges
PORT = 50405

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

request = {
                "command": "init"
            }
# print(request)
json_send(request)
response = json_recv()
print(response)

ctxt = response['ctxt']
m0 = response['m0']
c0 = response['c0']
request = {
                "command": "metadata_leak",
                "m0": response['m0'],
                "c0": response['c0'],
                "ctxt": response['ctxt'][:64]+'1'*64
            }
# print(request)
json_send(request)
response = json_recv()
dt = datetime.datetime.fromisoformat(response['metadata'][59:84])
time_bytes = int(dt.timestamp()).to_bytes(4, "little")
m1 = b'MONTONE-PROTOCOL'
m2 = b'9\x05\x00\x00\xc1\x06\x00\x00' + time_bytes + b'\x01\x00\x00\x02'
# print(m2)
# print(len(m2))
c1 = bytes.fromhex(ctxt[:32])
c2 = bytes.fromhex(ctxt[32:64])
c3 = bytes.fromhex(ctxt[64:96])
new_c2 = strxor(strxor(c3, m1), m2)
# print(new_c2)

left = 0
right = 256
additional_metadata_len = left
while left <= right:
    mid = int((left+right)/2)
    # print(mid)
    # print(left)
    # print(right)
    new_ctxt = c1.hex()+new_c2.hex()+'1'*32*mid
    # print(new_ctxt)
    # print(len(new_ctxt))
    # print(i)
    request = {
                    "command": "metadata_leak",
                    "m0": m0,
                    "c0": c0,
                    "ctxt": new_ctxt
                }
    # print(request)
    json_send(request)
    response = json_recv()
    print(response)
    if 'metadata' in response:
        additional_metadata_len = mid
        right = mid - 1
    else:
        left = mid + 1
new_ctxt = c1.hex()+new_c2.hex()+'1'*32*additional_metadata_len
    # print(new_ctxt)
    # print(len(new_ctxt))
    # print(i)
request = {
                "command": "metadata_leak",
                "m0": m0,
                "c0": c0,
                "ctxt": new_ctxt
            }
# print(request)
json_send(request)
response = json_recv()
metadata = response['metadata']

additional_metadata_len = additional_metadata_len.to_bytes(1, 'little')
print(additional_metadata_len)
sender = metadata.split('from ')[1].split(' to')[0]
sender = int(sender).to_bytes(4, 'little')
print('sender', sender)
receiver = metadata.split('to ')[1].split(',')[0]
receiver = int(receiver).to_bytes(4, 'little')
print("receiver", receiver)
timestamp =  metadata.split('on ')[1].split('.')[0]
dt = datetime.datetime.fromisoformat(timestamp)
time_bytes = int(dt.timestamp()).to_bytes(4, "little")
print("timestamp", time_bytes)
protocol_maj_version = metadata.split('v')[1].split('.')[0]
protocol_maj_version = int(protocol_maj_version).to_bytes(2, "little")
print("protocol_maj_version", protocol_maj_version)
protocol_min_version = metadata.split('.')[1].split(')')[0]
protocol_min_version = int(protocol_min_version).to_bytes(1, "little")
print("protocol_min_version", protocol_min_version)
ans = sender + receiver + time_bytes + protocol_maj_version + protocol_min_version + additional_metadata_len
ans = strxor(strxor(ans, c1), c2)
print(ans)
request = {
                "command": "flag",
                "solve": ans.decode()
            }
# print(request)
json_send(request)
response = json_recv()
print(response['flag'])
