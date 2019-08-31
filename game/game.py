import player

cmdlist = '\n!exit    - Exits the chat, returning to the main menu\n' + \
          '!help    - Displays this exact list\n' + \
          '!users   - Displys a list of users in the room' + \
          'Anything else will be broadcast to the chatroom\n'

class game:
    def __init__(self, name='chatroom'):
        self.players = []
        self.name = name
        self.limit = 0
        self.count = 0

    def addPlayer(self, p: player) -> bool:
        if (self.count < self.limit) or (self.limit == 0):
            self.players.append(p)
            self.count  = self.count + 1
            p.sendUpdate('Welcome to Chat!' + cmdlist)
            print(p.name, 'joined chat')
            return True
        else:
            return False

    def removePlayer(self, p: player.player) -> int:
        self.players.remove(p)
        self.count = self.count - 1
        p.state = None
        return len(self.players)

    def updatePlayers(self, targets: [player.player], msg: str):
        print(targets)
        for p in targets:
            print(p.name)
            p.sendUpdate(msg)

    def updateGame(self, sender: player.player, cmd: str):
        if cmd.split()[0] == '!exit':
            sender.sendUpdate('Bye, sending you back to the main menu!')
            self.removePlayer(sender)
        elif cmd.split()[0] == '!help':
            sender.sendUpdate(cmdlist)
            print(sender.name, 'requested help')
        elif cmd.split()[0] == '!users':
            for p in self.players:
                sender.sendUpdate(str(p.name))
            print(sender.name, 'requested chatroom list')
        else:
            self.updatePlayers(self.players, str(sender.name) + ': ' + cmd)