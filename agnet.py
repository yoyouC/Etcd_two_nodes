import subprocess
import time
from message import *
from client import Client


class Agnet():
    def __init__(self, port, tracker):
        self.port = port
        self.tracker = tracker
        self.client = Client(self.port)

    def startEtcd(self):
        return subprocess.Popen(["C:\\Users\\c50014277\\Documents\\etcd-release-3.4\\bin\\etcd"])

    def startMonitoring(self, process):
        while True:
            isRunning = False
            if process.poll() == None:
                isRunning = True

            self.client.sendHeartBeat(isRunning)
            time.sleep(1)

    def waitForTheOther(self):
        while True:
            try:
                response = self.client.sentReady()
                if response.type == MessageType.ReadyResp.value:
                    break
            except ConnectionRefusedError:
                print("Connection refused by", self.sendPort)

    def start(self):
        self.waitForTheOther()
        process = self.startEtcd()
        self.startMonitoring(process)
