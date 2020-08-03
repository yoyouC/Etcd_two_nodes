import socket
import threading
import server
from message import *


def send(socket, data):
    socket.send(data.encode('utf-8'))

def recieve(conn):
    data = conn.recv(1024)
    return data.decode()
    
def startServer(port):
    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, port))        

    s.listen(5)                 
    while True:
        c, addr = s.accept()     
        data = recieve(c)
        server.handleReq(c, data)
        c.close()                
    
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

     

def startHA(selfport, otherport):
    serverT = threading.Thread(target=startServer, args=(selfport,))
    MonitorT = threading.Thread(target=startMonitor, args=(otherport,))
    serverT.start()
    MonitorT.start()


if __name__ == "__main__":
    startHA(12345, 12345)
