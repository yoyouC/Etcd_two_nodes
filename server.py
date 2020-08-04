from message import *
import socket
from util import recieve

def handleReq(conn, data):
    response = ""
    msg = deserializeMsg(data)

    print(msg)
    if msg.type == MessageType.Ready.value:
        response = Message(MessageType.ReadyResp).serialize()
    elif msg.type == MessageType.HeartBeat.value:
        pass
    
    if response != "":
        conn.send(response.encode())


def startServer(port):
    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, port))

    s.listen(5)
    while True:
        c, addr = s.accept()
        data = recieve(c)
        handleReq(c, data)
        c.close()