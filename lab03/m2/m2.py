#!/usr/bin/env python3
# from https://cryptohack.org/challenges/introduction/

from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import telnetlib
import json
from itertools import cycle

tn = telnetlib.Telnet("aclabs.ethz.ch", 50302)

def xor(a, b):
    if len(a) < len(b):
        a, b = b, a
    return bytes([i ^ j for i, j in zip(a, cycle(b))])

def readline():
    return tn.read_until(b"\n")

def json_recv():
    line = readline()
    return json.loads(line.decode())

def json_send(req):
    request = json.dumps(req).encode()
    tn.write(request + b"\n")

def main():
    cmd_encrypted = bytes(16)
    cmd = bytes(16)
    for i in range(256):
        cmd_encrypted = i.to_bytes(16, 'big')
        json_send({"command": "encrypted_command", "encrypted_command": cmd_encrypted.hex()})
        res = json_recv()
        if "Failed" not in res["res"]:
            cmd = pad(bytes.fromhex(res["res"][len("No such command: "):]), 16)
            break

    print("cmd_encrypted: " + cmd_encrypted.hex())
    print("cmd: " + cmd.hex())

    mask = xor(cmd, cmd_encrypted)

    print("mask: " + mask.hex())

    flag = pad(b"flag", 16)
    flag_encrypted = xor(flag, mask)

    print("flag: " + flag.hex())
    print("flag_encrypted: " + flag_encrypted.hex())

    request = {
        "command": "encrypted_command",
        "encrypted_command": flag_encrypted.hex()
    }
    json_send(request)

    response = json_recv()

    print(response)

if __name__ == "__main__":
    main()