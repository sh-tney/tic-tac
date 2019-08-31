import player

cmdlist = '!exit    - Exits and closes your connection safely\n' + \
          '!help    - Displays this exact list\n' + \
          'Anything else will be broadcast to the chatroom'

class game:
    def __init__(self, name='chatroom'):
        self.players = []
        self.name = name
        self.limit = 0
        self.count = 0

    def addPlayer(self, p: player) -> bool:
        if (self.count < self.limit) or (self.limit == 0):
            self.players = [self.players, p]
            self.count  = self.count + 1
            return True
        else:
            return False

    def removePlayer(self, p: player) -> int:
        self.players.remove(p)
        p.state = None
        return len(self.players)

    def sendUpdate(self, sender: player, cmd: str) -> bool:
        print(sender.addr, 'sent in chatrooom', cmd)
        cmd = cmd.lower().split()
        if cmd:
            if cmd[0] == '!exit':
                sender.sendUpdate('Bye!')
                self.removePlayer(sender)
            elif cmd[0] == '!help':
                sender.sendUpdate(cmdlist)
                print(sender.addr, 'requested help')
            #else:
                #nice