import threading
import sys
import tracker
from agnet import Agnet
from server import Server


class EtcdHA:
    def __init__(self, serverPort, sendPort):
        self.tracker = tracker.ProgressTracker()
        self.agent = Agnet(sendPort, self.tracker)
        self.server = Server(serverPort, self.tracker)

    def startServer(self):
        self.server.startServer()

    def startMonitor(self):
        self.agent.start()

    def start(self):
        serverT = threading.Thread(target=self.startServer)
        MonitorT = threading.Thread(target=self.startMonitor)
        serverT.start()
        MonitorT.start()


if __name__ == "__main__":
    etcdHA = None

    if len(sys.argv) > 1:
        serverPort = sys.argv[1]
        otherPort = sys.argv[2]
        etcdHA = EtcdHA(serverPort, otherPort)
    else:
        etcdHA = EtcdHA(12345, 12345)

    etcdHA.start()
