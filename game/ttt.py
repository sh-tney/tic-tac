import socket
import game
import player
import tttai
import tttsql

cmdlist = '\n' +\
'!leave   - Leaves tic-tac-toe, returning to the main menu\n' +\
'!help    - Displays this exact list\n' +\
'!users   - Displys a list of users in the room\n' +\
'!playai  - Puts you up against an "unbeatable" bot\n' +\
'!playpvp - Matches up against a person in the lobby, or waits for one\n\n' +\
"   Once in game, enter a number (1-9) to choose the coorresponding square" +\
'\n\n'

aiBot = tttai.tttai(name='aiBot');

class tictactoe(game.game):
    """An implementation of game, serving as a tictactoe lobby"""

    def __init__(self):
        """Houses neccesary initialization

        Also creates the waiter object, to house players who are waiting for
        someone else to play a pvp game, and a dictionary setup to store info
        on all the active games.
        """

        self.players = []
        self.name = 'ttt'
        self.games = {}
        self.waiter = None

    def addPlayer(self, p: player.player):        # Append, Increment, Announce
        """Adds a player to the lobby, with personalized messages"""

        self.players.append(p)
        p.sendUpdate('\n   Welcome to tic-tac-toe!\n' + cmdlist)
        print(p.name, 'joined ttt')
        self.updatePlayers(self.players, str(p.name)  + ' joined!\n')

    def removePlayer(self, p: player.player):         # Remove, State, Accounce
        """Removes a player from the lobby, checking active games

        Important that we check the active games and remove BOTH players, so
        that in the event of a disconnect mid-game, the other player isn't just
        stuck in limbo.
        """

        x = self.findGame(p)
        if x is not None:
            self.games.pop(x)
            x = list(x)
            x.remove(p)
        self.players.remove(p)
        p.state = None
        print(p.name, 'left ttt')
        self.updatePlayers(self.players, str(p.name) + ' left!\n')

    def updatePlayers(self, targets: [player.player], msg: str):
        """Updates all the players on the target list with the msg"""

        for p in targets:
            try:
                p.sendUpdate(msg)
            except:    # Don't worry if someone's dead, manager will pick it up
                print("Error updating", p.name)
                continue

    def createGame(self, p: player.player, p2: player.player):
        """Initializes a game with two players, adding it to the dictionary"""

        x = (p, p2)
        self.games[x] = ['\n    1 2 3\n    4 5 6\n    7 8 9\n\n', 0]
        self.updatePlayers(x, str(p.name) +" (O) v " + str(p2.name) +" (X)!\n")

    def findGame(self, p: player.player) -> (player.player, player.player):
        """A handy function to search for the game a player is in, if any

        Returns the two-player tuple that references the game state on the
        dictionary. Makes sure to check both the p1 and p2 positions, but 
        doesn't tell which position the player is.
        """

        for g in self.games.keys():
            if g[0] == p:
                return g
            if g[1] == p:
                return g
        return None

    def gameEnd(self, x, result: int):
        """Handles the ending of a game, passing on messages & SQL requests"""

        print(self.games[x][0])
        self.updatePlayers(x, self.games[x][0])

        if result == 2:
            self.updatePlayers(x, "DRAW!\n")
            tttsql.updateDraw(x[0])
            tttsql.updateDraw(x[1])
        else:
            self.updatePlayers(x, str(x[result].name) + " WINS!\n")
            tttsql.updateWin(x[result])
            tttsql.updateLoss(x[(result-1)*(-1)])

        self.games.pop(x)
        self.updatePlayers(x, 'SERVER: Returned to the ttt lobby\n')

    def checkWins(self, x) -> bool:
        """Checks the gamestate for a win between the two players

        Checking the hard way, if there are three in a row of either side.
        This assumes that it runs every time a command is fulfilled, and 
        therefore just returns True (win) or false (not win), assuming that 
        the returning function understands the most recent player probably
        won.
        """

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
        """Sanitizes game inputs, the main handler for active games

        Goes through the process of actually checking if the game has ended
        in a draw, or a win, and if not delegates the result to endGame. Also
        tells the other player it's their turn if not, or in the case of bot
        opponents, makes the bot move and then passes right back.
        """

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
                if cmd is not None:            # AI Opponents respond instantly
                    self.playerMove(newP, x, cmd)
                else:                    # Human opponents take slightly longer
                    newP.sendUpdate('SERVER: Your turn!\n')
                    p.sendUpdate('SERVER: Waiting for your opponent...\n')

    def playerMove(self, p, x: (player.player, player.player), cmd: str):
        """Handles the move checking & sanitizing, before checkState

        Indicates back to the player if they have made an invalid move, and
        in the case of bots, allows them to recalculate & submit.
        """

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
        """The entry point of all commands to the ttt lobby

        Handles any relevant commands, and passes on to an active game if
        applicable.
        """

        if cmd[0] == '!':                     # Check if there's a command flag
            cmd = cmd.lower()

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
            
            elif cmd.split()[0] == '!playpvp':          # Start a game, or wait
                if self.waiter is not None:    # We could add some kind of ELO?
                    self.createGame(self.waiter, s)
                    print('Match betweeen', s.name, 'and', self.waiter.name)
                    self.waiter.sendUpdate(self.games[(self.waiter, s)][0])
                    self.waiter.sendUpdate('You first!\n')
                    s.sendUpdate('Waiting for the opponents turn...\n')
                    self.waiter = None
                else:
                    self.waiter = s                  # This is the waiting part
                    s.sendUpdate('Waiting for another player to play...\n')

            else:  # We're assuming anything starting with "!" is a cmd attempt
                s.sendUpdate('SERVER: Command not recognized, try !help\n')

        else:                                         # Try to make a game move
            x = self.findGame(s)
            if x is None:
                s.sendUpdate('Type !play to join a game, or !help for help\n')
            else:
                self.playerMove(s, x, cmd)

def main():
    """100 ai v ai games, only for demonstration purposes

    If you don't want this clogging up the database, don't run this.
    """

    t = tictactoe()
    chad = tttai.tttai(name='DEMO_chad')
    virgil = tttai.tttai(name='DEMO_virgil')

    for i in range(100):
        t.createGame(chad, virgil)
        t.updateGame(chad, str(chad.sendUpdate('Start')))
        

if __name__ == '__main__':
    main()