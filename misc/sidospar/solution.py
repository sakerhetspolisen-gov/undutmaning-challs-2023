import socket
import time
import string

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# now connect to the web server on port 80 - the normal http port
s.connect(("!IP HERE!", 2323))
s.recv(1024)


def get_length(s: socket.socket):
    length = 0
    while True:
        length += 1
        s.sendall(b"a" * length + b"\n")
        time.sleep(0.1)
        feedback = s.recv(1024)
        if b"Wrong length" in feedback:
            print(feedback)
            continue
        else:
            break
    return length


def get_password(s: socket.socket, length):
    remaining_length = length
    solved = ""
    while True:
        remaining_length += -1
        for tested_char in string.printable:
            string_to_send = solved + tested_char + remaining_length * "ö" + "\n"
            s.sendall(string_to_send.encode())
            time.sleep(0.05)
            feedback = s.recv(1024)
            print(string_to_send)
            print(feedback)
            if b"ascii" in feedback.lower():
                solved += tested_char
                break
            elif b"unlocked" in feedback.lower():
                return solved + tested_char


length = get_length(s)
print(f"Length is: {length}")
password = get_password(s, length)
print(password.encode())