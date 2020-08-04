import socket
import time
from message import *

class Client():
    def __init__(self, port):
        self.port = port

    def __send(self, socket, data):
        socket.send(data.encode('utf-8'))

    def __recieve(self, socket):
        responseText = socket.recv(1024)
        if responseText.decode() == '':
            return ''
        else:
            return deserializeMsg(responseText)

    def sendMsg(self, msg):
        s = socket.socket()
        host = socket.gethostname()
        s.connect((host, self.port))
        self.__send(s, msg.serialize())
        respond = self.__recieve(s)
        s.close()
        return respond

    def sendHeartBeat(self, isRunning):

        if isRunning:
            content = HeartBeatContent(time.time(), EtcdState.EtcdOK)
        else:
            content = HeartBeatContent(time.time(), EtcdState.EtcdDown)

        heartBeatMsg = Message(MessageType.HeartBeat, content)
        self.sendMsg(heartBeatMsg)

    def sentReady(self):
        msg = Message(MessageType.Ready)
        response = self.sendMsg(msg)
        return response