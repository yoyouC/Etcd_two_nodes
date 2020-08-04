# Server define how we handle messages from the other node
from message import *
import socket


class Server:
    def __init__(self, port, tracker):
        self.port = port
        self.tracker = tracker

    def startServer(self):
        s = socket.socket()
        host = socket.gethostname()
        s.bind((host, self.port))

        s.listen(5)
        while True:
            c, addr = s.accept()
            data = self.recieve(c)
            self.handleReq(c, data)
            c.close()

    def handleReq(self, conn, data):
        response = ""
        msg = deserializeMsg(data)

        if msg.type == MessageType.Ready.value:
            response = Message(MessageType.ReadyResp).serialize()
        elif msg.type == MessageType.HeartBeat.value:
            self.tracker.update(msg)

        if response != "":
            conn.send(response.encode())

    def recieve(conn):
        data = conn.recv(1024)
        return data.decode()
