from message import *


def send(socket, data):
    socket.send(data.encode('utf-8'))


def recieve(conn):
    data = conn.recv(1024)
    return data.decode()



class MsgHandler():
    def __init__(self, tracker):
        self.tracker = tracker


    def handleReq(self, conn, data):
        response = ""
        msg = deserializeMsg(data)

        print(msg)
        if msg.type == MessageType.Ready.value:
            response = Message(MessageType.ReadyResp).serialize()
        elif msg.type == MessageType.HeartBeat.value:
            self.tracker.update(msg)

        if response != "":
            conn.send(response.encode())