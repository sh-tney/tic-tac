import player

cmdlist = '\n!exit    - Exits the chat, returning to the main menu\n' + \
          '!help    - Displays this exact list\n' + \
          'Anything else will be broadcast to the chatroom\n'

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
            p.sendUpdate('Welcome to Chat!' + cmdlist)
            print(p.name, 'joined chat')
            return True
        else:
            return False

    def removePlayer(self, p: player) -> int:
        self.players.remove(p)
        p.state = None
        return len(self.players)

    def updateGame(self, sender: player, cmd: str):
        if cmd.split()[0] == '!exit':
            sender.sendUpdate('Bye!')
            self.removePlayer(sender)
        elif cmd.split()[0] == '!help':
            sender.sendUpdate(cmdlist)
            print(sender.addr, 'requested help')
        else:
            print(sender.addr, 'sent in chatrooom', cmd)