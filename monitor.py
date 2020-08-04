import socket
from message import *
from util import send

def startMonitor(port):
    while True:
        try:
            s = socket.socket()
            host = socket.gethostname()
            s.connect((host, port))

            msg = Message(MessageType.Ready)
            send(s, msg.serialize())

            response = s.recv(1024)
            print(response.decode())

            s.close()
            break
        except ConnectionRefusedError:
            print("Connection refused by", host, port)