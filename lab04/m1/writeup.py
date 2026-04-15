#!/usr/bin/env python3
# from https://cryptohack.org/challenges/introduction/

import telnetlib
import json
# Change this to REMOTE = False if you are running against a local instance of the server
REMOTE = True

# Remember to change the port if you are re-using this client for other challenges
PORT = 50401

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
    "command":"register", 
    "username": "1&role=admin", 
    "role": "user", 
    "favourite_coffee": "2"
}
    # print(request['m'])
json_send(request)
response = json_recv()
print(response)
token = response['token']
request = {
    "command":"login", 
    "token":token
}
    # print(request['m'])
json_send(request)
response = json_recv()
print(response)

request = {
    "command": "change_settings", 
    "good_coffee": "true"
}
    # print(request['m'])
json_send(request)
response = json_recv()
print(response)

request = {
    "command": "get_coffee"
}
    # print(request['m'])
json_send(request)
response = json_recv()
print(response['res'].split(': ')[1])