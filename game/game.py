import player

cmdlist = '\n' + \
'!leave   - Leaves the chat, returning to the main menu\n' + \
'!help    - Displays this exact list\n' + \
'!users   - Displys a list of users in the room\n\n' + \
'   Anything else will be broadcast to the chatroom\n\n'

class game:
    """An abstract of a game class, functioning independently as a chatroom"""

    def __init__(self):
        """All game objects must have a players list, and a name string."""

        self.players = []
        self.name = 'chat'

    def addPlayer(self, p: player.player):        # Append, Increment, Announce
        """Adds a player to the this game's player list
        
        Also welcomes the player to the chatroom, and announces their arrival
        to the other players.   
        """

        self.players.append(p)
        p.sendUpdate('\n   Welcome to chat!\n' + cmdlist)
        print(p.name, 'joined chat')
        self.updatePlayers(self.players, 'SERVER: '+ str(p.name) +' joined!\n')

    def removePlayer(self, p: player.player):         # Remove, State, Accounce
        """Removes a given player from this game's list

        Absolutely imperative that the player's state is set to None during
        this, to allow the manager to resume handling commands from that user.
        Also announces the player's leaving to the chat room.
        """

        self.players.remove(p)
        p.state = None
        print(p.name, 'left chat')
        self.updatePlayers(self.players, str(p.name) + ' left!\n')

    def updatePlayers(self, targets: [player.player], msg: str): # Tell targets
        """Sends msg to all players in the targets list
        
        If a user can't recieve from here, we simply contniue and assume the
        manager will pick it up and close the connection normally.
        """

        for p in targets:
            try:
                p.sendUpdate(msg)
            except:    # Don't worry if someone's dead, manager will pick it up
                print("Error updating", p.name)
                continue


    def updateGame(self, s: player.player, cmd: str):
        """Handles the processing of whatever command the user sends

        This method should handle the brunt of processing for the game object's
        lobby, and is only called upon user responses (which is why this is best
        suited to turn based games). Also needs to handle lobby commands if
        needed. This implementation simply takes users' commands, and if not a 
        command detected by the !, will simply relay the message to th.e chat
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

            else:  # We're assuming anything starting with "!" is a cmd attempt
                s.sendUpdate('SERVER: Command not recognized, try !help\n')

        else:                         # Send everyone (including you) a message
            self.updatePlayers(self.players, str(s.name) + ': ' + cmd + '\n')