import socket

class player:
    def __init__(self, 
        sock: socket.socket=None, 
        addr=None, 
        name: str=None, 
        state: str=None):
        """The quintesential player object

        This simple object houses the baseline neccesary information that the
        game manager requires to facilitate a player, and any class that 
        extends this should have these essentials: a name (String), an address,
        a socket, and a state. For server-hosted bot players, these are not 
        neccesary however, as long as they never enter the game manager's list
        of players.
        """

        if name is None:
            self.name = addr
        else:
            self.name = name
        self.addr = addr
        self.sock = sock
        self.state = state

    def sendUpdate(self, update: str) -> str:
        """Handles logic for when the player recieves updates

        In this case, it dooes just send the string to the player's socket,
        encoded and ready to go, however other implementations like bots may
        want to handle differently, and the return string is also convenient,
        for hosting server-side logic if needed, but otherwise should be left
        as returning None.
        """

        self.sock.send((update).encode())
        return None
        
