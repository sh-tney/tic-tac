import socket

class player:
    # Default initializers
    def __init__(self, sock=None, name=None, stat=None):
        self.name = name
        self.sock = sock
        self.stat = stat

    def sendUpdate(self, update='Updated, No Message'):
        self.sock.send(update.encode())

    def getReponse(self, buff=1024):
        data = self.sock.recv(buff)
        if data:
            self.sock.send(data.decode().encode())