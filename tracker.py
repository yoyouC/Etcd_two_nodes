import message
import time

class ProgressTracker():
    def __init__(self):
        self.status = message.EtcdState.EtcdDown
        self.lastHeartBeatTime = time.time()

    def update(self, msg):
        print(msg)

