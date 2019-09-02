import socket
import game
import player
import tttai

cmdlist = '\n' + \
'!leave   - Leaves tic-tac-toe, returning to the main menu\n' + \
'!help    - Displays this exact list\n' + \
'!users   - Displys a list of users in the room\n' + \
'!playai  - Puts you up against an "unbeatable" bot\n\n' + \
"   Non-flagged input is considered a game command, if it's a number from 1-9" + \
'\n\n'

aiBot = tttai.tttai(name='aiBot');

class tictactoe(game.game):

    def __init__(self):
        self.players = []
        self.name = 'ttt'
        self.count = 0
        self.games = {}

    def addPlayer(self, p: player.player):        # Append, Increment, Announce
        self.players.append(p)
        self.count  = self.count + 1
        p.sendUpdate('\n   Welcome to tic-tac-toe!\n' + cmdlist)
        print(p.name, 'joined ttt')
        self.updatePlayers(self.players, str(p.name)  + ' joined!\n')

    def removePlayer(self, p: player.player):         # Remove, State, Accounce
        if x = self.findGame(p):
            self.games.pop(x)
            x = list(x)
            x.remove(p)
            self.updatePlayers(x[0], str(x[0].name) + 'forfeits!\n')
        self.players.remove(p)
        self.count = self.count - 1
        p.state = None
        print(p.name, 'left ttt')
        self.updatePlayers(self.players, str(p.name) + ' left!\n')

    def updatePlayers(self, targets: [player.player], msg: str):
        for p in targets:
            try:
                p.sendUpdate(msg)
            except:    # Don't worry if someone's dead, manager will pick it up
                print("Error updating", p.name)
                continue

    def createGame(self, p: player.player, p2: player.player):
        x = (p, p2)
        self.games[x] = ['\n    1 2 3\n    4 5 6\n    7 8 9\n\n', 0]
        self.updatePlayers(x, str(p.name) +" (O) v " + str(p2.name) +" (X)!\n")

    def findGame(self, p: player.player) -> (player.player, player.player):
        for g in self.games.keys():
            if g[0] == p:
                return g
            if g[1] == p:
                return g
        return None

    def gameEnd(self, x, result: int):
        print(self.games[x][0])
        self.updatePlayers(x, self.games[x][0])
        if result == 2:
            self.updatePlayers(x, "DRAW!\n")
            #Draw Script
        if result == 1:
            self.updatePlayers(x, str(x[result].name) + "WINS!\n")
            #p2 Win script
        if result == 0:
            self.updatePlayers(x, str(x[result].name) + "WINS\n")
            #p1 win Script
        self.games.pop(x)

    def checkWins(self, x) -> bool:
        grid = (self.games[x][0].split())
        if grid[0] == grid[1] and grid[1] == grid[2]:              # Horizontal
            return True
        if grid[3] == grid[4] and grid[4] == grid[5]:
            return True
        if grid[6] == grid[7] and grid[7] == grid[8]:
            return True

        if grid[0] == grid[3] and grid[3] == grid[6]:                # Vertical
            return True
        if grid[1] == grid[4] and grid[4] == grid[7]:
            return True
        if grid[2] == grid[5] and grid[5] == grid[8]:
            return True

        if grid[0] == grid[4] and grid[4] == grid[8]:                # Diagonal
            return True
        if grid[2] == grid[4] and grid[4] == grid[6]:
            return True

        return False                                            # Continue Game

    def checkState(self, p, x):

        q = True
        for i in self.games[x][0].split():   # This loop just checks for spaces
            if i.isdigit():
                q = False                               # If there is, carry on

        if q:                   
            self.gameEnd(x, 2)                         # If not, it's a draw

        else:
            if self.checkWins(x):                    # If someone won this turn
                self.gameEnd(x, x.index(p))           # They must be the winner
            else:
                newP = x[self.games[x][1]]  
                cmd = newP.sendUpdate(self.games[x][0]) 
                if cmd is not None:
                    self.playerMove(newP, x, cmd)

    def playerMove(self, p, x: (player.player, player.player), cmd: str):
        q = None
        if self.games[x][1] == x.index(p):          # If it's this players turn

            i = cmd.split()[0][0]
            if i.isdigit() and i != '0':            # If it's a number from 1-9

                if i in self.games[x][0]:          # If it's not a taken number

                    if self.games[x][1] == 0: 
                        self.games[x][0] = self.games[x][0].replace(i, 'O')
                        self.games[x][1] = 1

                    else:                             # Flip the current player
                        self.games[x][0] = self.games[x][0].replace(i, 'X')
                        self.games[x][1] = 0
                    self.checkState(p, x)

                else:
                    q = p.sendUpdate("Pick a number that isn't taken\n")
            else:
                q = p.sendUpdate('Enter a number between 1 and 9\n')
        else:
            p.sendUpdate('Wait your turn!\n')
        if q is not None:                # This makes sure AI make a valid turn
            self.playerMove(p, x, q)

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

            elif cmd.split()[0] == '!playai': # Start a game, show p1 the board
                self.createGame(s, aiBot)
                print(s.name, 'started a ttt vs ai game')
                s.sendUpdate(self.games[(s, aiBot)][0])

            else:  # We're assuming anything starting with "!" is a cmd attempt
                s.sendUpdate('SERVER: Command not recognized, try !help\n')

        else:                                         # Try to make a game move
            x = self.findGame(s)
            if x is None:
                s.sendUpdate('Type !play to join a game, or !help for help\n')
            else:
                self.playerMove(s, x, cmd)

    