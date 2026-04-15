#!/usr/bin/env python3
# from https://cryptohack.org/challenges/introduction/

import telnetlib
import json
import datetime
from Crypto.Util.strxor import strxor
# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True

# Remember to change the port if you are re-using this client for other challenges
PORT = 50406

if REMOTE:
    host = "aclabs.ethz.ch"
else:
    host = "localhost"

tn = telnetlib.Telnet(host, PORT)

def unpad(string):
    # source from https://gist.github.com/olooney/1498025
		if not string: return string
		if len(string) % 16:
			raise TypeError('string is not a multiple of the block size.')
		padding_number = ord(string[-1])
		if padding_number >= 16:
			return string
		else:
			if all(padding_number == ord(c) for c in string[-padding_number:]):
				return string[0:-padding_number]
			else:
				return string

def readline():
    return tn.read_until(b"\n")

def json_recv():
    line = readline()
    return json.loads(line.decode())

def json_send(req):
    request = json.dumps(req).encode()
    tn.write(request + b"\n")

def blockify(a):
    return [a[i : i + 16] for i in range(0, len(a), 16)]

request = {
                "command": "flag"
            }
# print(request)
json_send(request)
response = json_recv()
# print(response)

ctxt = response['ctxt']
m0 = response['m0']
c0 = response['c0']
request = {
                "command": "metadata_leak",
                "m0": response['m0'],
                "c0": response['c0'],
                "ctxt": response['ctxt']
            }
# print(request)
json_send(request)
response = json_recv()
# print(response)
dt = datetime.datetime.fromisoformat(response['metadata'][59:84])
time_bytes = int(dt.timestamp()).to_bytes(4, "little")
fixed_1 = b'MONTONE-PROTOCOL9\x05\x00\x00\xc1\x06\x00\x00'
fixed_2 = b'\x01\x00\x00\x03message_type=flag&lab=4&graded=True\r\r\r\r\r\r\r\r\r\r\r\r\rThank you for using Montone messaging services. Here is a flag that you will not be able to obtain:'
m = fixed_1 + time_bytes + fixed_2
# print(m)
# print(len(m))
m = blockify(m)[:-1]
# m3 = b'message_type=fla'
# print(m2)
# print(len(m2))
c = blockify(bytes.fromhex(ctxt))
# c1 = bytes.fromhex(ctxt[:32])
# c2 = bytes.fromhex(ctxt[32:64])
# c3 = bytes.fromhex(ctxt[64:96])
# c4 = bytes.fromhex(ctxt[96:128])
block = 11
# print(len(c))
for block in range(11, len(c)):
    new_c2 = strxor(strxor(c[block], m[0]), m[block-1])

    left = 0
    right = 256
    additional_metadata_len = left
    while left <= right:
        mid = int((left+right)/2)
        # print(mid)
        # print(left)
        # print(right)
        new_ctxt = c[0].hex()+new_c2.hex()+'1'*32*mid
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
        # print(response)
        if 'metadata' in response:
            additional_metadata_len = mid
            right = mid - 1
        else:
            left = mid + 1
    new_ctxt = c[0].hex()+new_c2.hex()+'1'*32*additional_metadata_len
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

    # print(additional_metadata_len)
    additional_metadata_len = additional_metadata_len.to_bytes(1, 'little')
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
    ans = strxor(strxor(ans, c[0]), c[block-1])
    m.append(ans)
    # print("m", m)
# print(b''.join(m))
flag = ((b''.join(m)).split(b": ")[1].split(b"}")[0] + b"}").decode()
print(flag)
# request = {
#                 "command": "flag",
#                 "solve": ans.decode()
#             }
# # print(request)
# json_send(request)
# response = json_recv()
# print(response['flag'])


# b'MONTONE-PROTOCOL9\x05\x00\x00\xc1\x06\x00\x00\x07\xdf\x18d\x01\x00\x00\x03messag
# b'MONTONE-PROTOCOL9\x05\x00\x00\xc1\x06\x00\x00\x07\xdf\x18d\x01\x00\x00\x03message