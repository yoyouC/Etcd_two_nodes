from message import *

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