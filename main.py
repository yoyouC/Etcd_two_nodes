import socket
import threading
import server
from message import *
import sys, os
import subprocess
import time
import tracker

class EtcdHA():
    def __init__(self, serverPort, sendPort):
        self.sendPort = sendPort
        self.serverPort = serverPort
        self.tracker = tracker.ProgressTracker()
        self.msgHandler = server.MsgHandler(self.tracker)

    def sendMsg(self, msg):
        s = socket.socket()
        host = socket.gethostname()
        s.connect((host, self.sendPort))
        server.send(s, msg.serialize())
        return s

    def startEtcd(self):
        return subprocess.Popen(["C:\\Users\\c50014277\\Documents\\etcd-release-3.4\\bin\\etcd"])

    def sendHeartBeat(self, isRunning):

        if isRunning:
            content = HeartBeatContent(EtcdState.EtcdOK, time.time())
        else:
            content = HeartBeatContent(EtcdState.EtcdDown, time.time())

        heartBeatMsg = Message(MessageType.HeartBeat, content)
        self.sendMsg(heartBeatMsg)

    def startMonitoring(self, process):
        while True:
            isRunning = False
            if process.poll() == None:
                isRunning = True

            self.sendHeartBeat(isRunning)
            time.sleep(1)

    def waitForTheOther(self):
        while True:
            try:
                s = socket.socket()
                host = socket.gethostname()
                s.connect((host, self.sendPort))

                msg = Message(MessageType.Ready)
                server.send(s, msg.serialize())

                responseText = s.recv(1024)
                response = deserializeMsg(responseText)
                if response.type == MessageType.ReadyResp.value:
                    s.close()
                    break
            except ConnectionRefusedError:
                print("Connection refused by", host, self.sendPort)

    def startServer(self):
        s = socket.socket()
        host = socket.gethostname()
        s.bind((host, self.serverPort))

        s.listen(5)
        while True:
            c, addr = s.accept()
            data = server.recieve(c)
            self.msgHandler.handleReq(c, data)
            c.close()

    def startMonitor(self):
        self.waitForTheOther()
        process = self.startEtcd()
        self.startMonitoring(process)

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