import socket

class player:
    # Default initializers
    def __init__(self, 
        sock: socket.socket, 
        addr=None, 
        name: str=None, 
        state: str=None):

        self.name = name
        self.addr = addr
        self.sock = sock
        self.state = state

    def sendUpdate(self, update='Updated, No Message\n'):
        self.sock.send(update.encode())

    def getReponse(self, buff=4096):
        return self.sock.recv(buff)