import player

cmdlist = '\n!leave   - Leaves the chat, returning to the main menu\n' + \
          '!help    - Displays this exact list\n' + \
          '!users   - Displys a list of users in the room\n' + \
          'Anything else will be broadcast to the chatroom\n\n'

class game:
    def __init__(self, name='chat'):
        self.players = []
        self.name = name
        self.count = 0

    def addPlayer(self, p: player):               # Append, Increment, Announce
        self.players.append(p)
        self.count  = self.count + 1
        p.sendUpdate('\nWelcome to chat!' + cmdlist)
        print(p.name, 'joined chat')
        self.updatePlayers(self.players, str(p.name)  + ' joined!\n')

    def removePlayer(self, p: player.player):         # Remove, State, Accounce
        self.players.remove(p)
        self.count = self.count - 1
        p.state = None
        print(p.name, 'left chat')
        self.updatePlayers(self.players, str(p.name) + ' left!\n')

    def updatePlayers(self, targets: [player.player], msg: str): # Tell targets
        for p in targets:
            try:
                p.sendUpdate(msg)
            except:    # Don't worry if someone's dead, manager will pick it up
                print("Error updating", p.name)
                continue


    def updateGame(self, s: player.player, cmd: str):
        if cmd[0] == '!':                     # Check if there's a command flag

            if cmd.split()[0] == '!leave':                    # Say bye, remove
                s.sendUpdate('SERVER: Sending you back to the main menu!\n')
                self.removePlayer(s)

            elif cmd.split()[0] == '!help':                      # Display list
                s.sendUpdate(cmdlist)
                print(s.name, 'requested help')

            elif cmd.split()[0] == '!users':    # Display list of users in chat
                for p in self.players:
                    s.sendUpdate('\n - ' + str(p.name))
                s.sendUpdate('\n\n')
                print(s.name, 'requested chat user list')

            else:  # We're assuming anything starting with "!" is a cmd attempt
                s.sendUpdate('SERVER: Command not recognized, try !help\n')

        else:                         # Send everyone (including you) a message
            self.updatePlayers(self.players, str(s.name) + ': ' + cmd + '\n')