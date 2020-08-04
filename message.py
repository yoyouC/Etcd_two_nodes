import enum
import json

def deserializeMsg(msg):
    return Message().deserialize(msg)


class EtcdState(enum.Enum):
    EtcdOK = 0
    EtcdDown = 1


class MessageType(enum.Enum):
    Ready = 0
    ReadyResp = 1
    HeartBeat = 2


class HeartBeatContent():
    def __init__(self, time, state):
        self.time = time
        self.state = state


class Message():
    def __init__(self, type=None, content=None):
        self.type = type
        self.content = content
    def serialize(self):
        return json.dumps(self, cls=MessageEncoder)
    def deserialize(self, jsonString):
        self.__dict__ = json.loads(jsonString)
        return self
    

class MessageEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, MessageType):
            return o.value
        elif isinstance(o, EtcdState):
            return o.value
        else:
            return o.__dict__


if __name__ == "__main__":
    msg = Message(MessageType.ReadyResp, HeartBeatContent(1, EtcdState.EtcdOK))
    print(msg.serialize())
    msg.deserialize(msg.serialize())
    print(type(msg))