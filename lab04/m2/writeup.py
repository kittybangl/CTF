
import telnetlib
import json
from Crypto.Util.strxor import strxor
import time
# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True

# Remember to change the port if you are re-using this client for other challenges
PORT = 50402

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

# request = {
#         "command": "flag"
# }
def attack_block(m0, c0, c):
    ans = b''
    for i in range(15, -1, -1):
        s = bytes([16 - i] * (16 - i))
        for b in range(256):
            c0_ = bytes(i) + strxor(s, bytes([b]) + ans)
            if padding_oracle(m0, c0_, c):
                ans = bytes([b]) + ans
                break
        else:
            raise ValueError(f"Unable to find decryption for {s}, {m0}, {c0}, and {c}")
    return strxor(c0, ans)

def padding_oracle(m0, c0, ctxt):
    # print(type(m0))
    # if isinstance(m0, bytes):
    #     m0 = m0.hex()
    ctxt = ctxt.hex()
    request = {
        "command": "decrypt",
        "m0": m0.hex(),
        "c0": c0.hex(),
        "ctxt": ctxt
    }
    # print(request)
    # print(ctxt.decode())
    json_send(request)
    response = json_recv()
    # print(response)
    if "res" in response:
        return True
    else:
        return False

if __name__ == "__main__":
    start_time = time.time()
    request = {
            "command": "flag"
    }
    json_send(request)
    response = json_recv()
    # print(response)
    m0 = bytes.fromhex(response['m0'])
    c0 = bytes.fromhex(response['c0'])
    ctxt = bytes.fromhex(response['ctxt'])
    p = attack_block(m0, c0, ctxt[0:16])
    for i in range(16, len(ctxt), 16):
        print(i)
        p += attack_block(p[i - 16:i], ctxt[i - 16:i], ctxt[i:i + 16])
    print(unpad(p.decode()))
    end_time = time.time()
    print(end_time-start_time)
    # print(attack(padding_oracle, bytes.fromhex(response['m0']), bytes.fromhex(response['c0']), bytes.fromhex(response['ctxt'])))

# b'\xe7\x1f\xe1\x1c\xca\x93\xa4x#\x1e\xbe*\x1c_j\xd3\x03\xe4\xe2\xfc\x8bB\xdeL\xf9\x02\xeaQ_\x1fP`\x0c\xf3u\xa9\xa7V\x08$C\xf0\x98\x9a\x8f\x83\x14(\xce\x01\xc5\xa5v\xd4`\xd5",d\x10,\t\x1b\x01\x85RJ\xd0\xedFo\x86\xc6\x1b|\x0cs\x83\xa6~'