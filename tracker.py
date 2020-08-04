import message
import time
from threading import Lock


class ProgressTracker():
    def __init__(self):
        self.lock = Lock()
        self.state = message.EtcdState.EtcdDown
        self.lastHeartBeatTime = time.time()
        self.firstEtcdDownMsgTime = time.time()
        self.etcdDownInterval = 0
        self.etcdNetworkErrorInterval = 0

    def update(self, msg):
        newState = msg.content["state"]
        newTime = msg.content["time"]

        self.lock.acquire()
        if self.state == message.EtcdState.EtcdOK.value:
            if newState == message.EtcdState.EtcdDown.value:
                self.firstEtcdDownMsgTime = newTime
            else:
                pass
        else:
            if newState == message.EtcdState.EtcdDown.value:
                self.etcdDownInterval = newTime - self.firstEtcdDownMsgTime
            else:
                self.etcdDownInterval = 0

        self.state = newState
        self.lastHeartBeatTime = newTime
        self.lock.release()

        print(self.state, "  ", self.lastHeartBeatTime)
