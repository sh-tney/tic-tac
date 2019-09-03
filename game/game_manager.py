import socket
import select
import time
import re
import player
import sys
import game
import ttt                         # Import games from subdirectories like this

player_list = []       # Contains player objects, including one for this server

""" 

Developers wanting to expand the game library should do so by adding their game
objects here, either as a single instance like in the two shown, or potentially
multiple if one wanted multiple lobbies for any reason. As long as something in
the list implements all the functions in the game.py file, it should work here.
Also probably a good idea to add tooltips to the cmdList here too.
"""

game_list = {       # Add game object inits here, with the appropriate name tag
            'chat': game.game(), 
            'ttt': ttt.tictactoe() 
            }
                               # Also worth adding the game info to the tooltip
cmdlist = '\n' + \
'!help        - Displays this exact list\n' + \
'!quit        - Exits and closes your connection safely\n' + \
'!name [xxxx] - Changes your username to [xxxx]\n' + \
'!join [game] - Attempts to join a game from the following list:\n\n' + \
'   GAME OPTIONS:\n' + \
'   chat - not actually a game, just a simple multi-user chat\n' + \
'   ttt  - tic-tac-toe\n\n'

def purge(p: player.player):
    """A method to erase this player & their connection

    This removes all the players' known object references, and also closes
    their connection safely (or at least attempts to). This passes down to
    the game lobby they are currently housed in, if any, and lets the game's
    library decide on how best to deal with it, and if needed complete game
    state calcuations to preserve the game state if needed.
    """

    print('Purging player', p.name) 
    try: 
        game_list[p.state].removePlayer(p)  # Removes p from current game lobby
    except:
        print("Player couldn't be removed from", p.state)
    try:
        player_list.remove(p)                  # Removes p from the player list
    except:
        print('Player not on list')
    try:
        p.sock.shutdown() # Shutdown fails often, but it's nice when it doesn't
    except:
        print('Sock shutdown fail')
    try:
        p.sock.close()      # Closing the socket, so the player is disconnected 
    except:
        print('Sock close fail')
    try:
        del p.sock           # Deleting the socket, no wierd reference buggging
    except:
        print("Couldn't delete socket")
    try: 
        del p                                                   # Kills em dead
    except:
        print("Couldn't delete player")

def gameJoiner(s: player.player, join: str):
    """A method that tries to scan the available games for a player to join

    This method simply checks the gameList dictionary for games matching the
    player's request (always converted to lower-case), and joins the lobby,
    matching up their state so that commands are passed correctly. On an
    unsuccessful search, the player is notified."
    """

    joined = False
    try:
        game_list[join].addPlayer(s)                        # Simply look it up
        s.state = join
        joined = True
        print("Success")
    except:                                                 # If not, try again
        print("Unsuccessful")
        s.sendUpdate('SERVER: Not a recognised game, !help for a list\n')

def cmdInterpereter(s: player.player, msg: str):
    """A method for handling the users' input when not in any game lobby

    When the game manager recieves a message from a player, and that player
    isn't in any active lobby, they are assumed to be sendinig a command to
    here, which it handles. Commands are assumed to always start with a !
    and are converted to lower case. One can also code in arguments if needed
    In this implementations, players are required to enter a username before
    joining any lobbies.
    """

    cmd = msg.split()[0].lower()    # Split up the string so that it's readable
    if cmd:
        if cmd == '!quit':                   # Player quits, say bye then purge
            s.sendUpdate("SERVER: Bye!\n")
            print(s.name, 'quit!')
            purge(s)

        elif cmd == '!help':                  # Sends the user the command list
            s.sendUpdate(cmdlist)
            print(s.name, 'requested help')

        elif cmd == '!name':                          # Changes the user's name

            n = ''                        
            for x in msg.split()[1:]:                       # Name sanitization
                n = n + '_' + x              # Replaces spaces with underscores
            n = re.sub(r'\W+', '', n[1:])           # Remvoes non-alphanumerics

            if len(n) > 0:
                print(s.name, 'changed their name to', n)
                s.name = n
                s.sendUpdate('SERVER: Name changed to ' + s.name + '\n')
            else:
                s.sendUpdate('SERVER: Please use the format: "!name [name]"\n')

        elif cmd == '!join':                                     # Join a lobby
            if len(msg.split()) > 1: 
                if s.name == s.addr:    # Force to Choose a name before joining
                    s.sendUpdate('SERVER: Please choose a !name first\n')
                else:
                    print(s.name, 'attempting to join', msg.split()[1].lower())
                    gameJoiner(s, msg.split()[1].lower())
            else:
                s.sendUpdate('SERVER: Please use the format: "!join [game]"\n')

        else:                                          # They fucked up, not us
            s.sendUpdate('SERVER: Command not recognized, type !help\n')

def main():
    """Main executable for a gameserver

    This program establishes an open recieving socket at the indicated host 
    initialized at 0.0.0.0:6969 here. It then enters an infinite loop. 
    This loop checks for readable sockets every loop, and removes connections
    that it finds to be closed or otherwise disconnected. Otherwise, hands
    down the recieved message to the players' current game lobby object, 
    in the dictionary at the record accorind to their player.state string,
    or if the player doesn't have a state, it passes on to cmdInterpreter.
    Also outputs everything here to stdout, and flushes every loop to allow
    for live log output.
    """

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_addr = ('0.0.0.0', 6969)
    server_sock.bind(server_addr)
    server_sock.listen()
    print("Listening on", server_addr)

    player_list.append(player.player(server_sock, server_addr))

    while True:

        for p in player_list:    # Loop through sockets, selecting individually

            read = select.select([p.sock], [], [], 0)[0]

            #print(p.name, len(read))        # Some nice diagnostics to look at
            #time.sleep(3)

            for r in read:  # Searching one socket at a time, we know the owner

                if r == server_sock:              # Accept incoming connections
                    s, a = server_sock.accept()
                    p = player.player(s, a)
                    print('Connection from', a)
                    player_list.append(p)
                    p.sendUpdate('\n    Welcome!\n' + cmdlist)

                else:                       # Otherwise, recieve client message

                    try:
                        dat = r.recv(8192).decode()
                        if dat == "":              # Check if connection closed
                            print(p.name, "connection closed")
                            purge(p)
                        else:                      # Otherwise, handle normally
                            if p.state is None:
                                cmdInterpereter(p, dat)
                            else:
                                game_list[p.state].updateGame(p, dat)
                                
                    except:                             # Connection died, kill
                        print(p.name, "connection died")
                        purge(p)
                        continue
        
        sys.stdout.flush()   # Flushing every loop, so we can live view the log

if __name__ == '__main__':
    main()