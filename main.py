import socket
import threading
from server import startServer
from monitor import startMonitor

    

    


     

def startHA(selfport, otherport):
    serverT = threading.Thread(target=startServer, args=(selfport,))
    MonitorT = threading.Thread(target=startMonitor, args=(otherport,))
    serverT.start()
    MonitorT.start()


if __name__ == "__main__":
    startHA(12345, 12345)
