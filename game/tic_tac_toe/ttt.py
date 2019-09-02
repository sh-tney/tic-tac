import game
import player

cmdlist = '\n!leave   - Leaves tic-tac-toe, returning to the main menu\n' + \
          '!help    - Displays this exact list\n' + \
          '!users   - Displys a list of users in the room\n' + \
          '!play    - Queues you up for a game against an opponent\n' + \
          '\nNon-flagged inputs are considered game commands, if they are\n' + \
          'a number between 1 and 9\n'

class tictactoe(game.game):

    def __init__(self):
        self.players = []
        self.name = 'ttt'
        self.count = 0
        self.games = []

    def addPlayer(self, p: player.player):        # Append, Increment, Announce
        self.players.append(p)
        self.count  = self.count + 1
        p.sendUpdate('\nWelcome to tic-tac-toe!' + cmdlist)
        print(p.name, 'joined ttt')
        self.updatePlayers(self.players, str(p.name)  + ' joined!\n')

    def removePlayer(self, p: player.player):         # Remove, State, Accounce
        self.players.remove(p)
        self.count = self.count - 1
        p.state = None
        print(p.name, 'left chat')
        self.updatePlayers(self.players, str(p.name) + ' left!\n')

    def updatePlayers(self, targets: [player.player], msg: str):
        pass

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

        else:                                         # Try to make a game move
            s.sendUpdate('Type !play to join a game, or !help for help\n')

    