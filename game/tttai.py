import socket
import player

class tttai(player.player):
    def __init__(self, 
        sock: socket.socket=None, 
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

    def sendUpdate(self, update: str) -> str:
        #self.sock.send((update).encode())
        return None
        
