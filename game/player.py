import socket

class player:
    # Default initializers
    def __init__(self, 
        sock: socket.socket, 
        addr=None, 
        name: str=None, 
        state: str=None):

        if name is None:
            self.name = addr
        else:
            self.name = name
        self.addr = addr
        self.sock = sock
        self.state = state

    def sendUpdate(self, update='Updated, No Message\n'):
        self.sock.send((update + '\n').encode())

    def getResponse(self):
        data = self.sock.recv(1024)
        if data:
            return data.decode()
        else: 
            return False
        
