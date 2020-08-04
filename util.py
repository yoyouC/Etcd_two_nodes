

def send(socket, data):
    socket.send(data.encode('utf-8'))

def recieve(conn):
    data = conn.recv(1024)
    return data.decode()