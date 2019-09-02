import socket
import select
import time
import player
import sys
import game
import ttt        # Import games from subdirectories like this

player_list = []       # Contains player objects, including one for this server

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
    joined = False
    try:
        game_list[join].addPlayer(s)                        # Simply look it up
        s.state = join
        joined = True
        print("Success")
    except:                                                 # If not, try again
        print("Unsuccessful")
        s.sendUpdate('SERVER: Not a recognised game, !help for a list\n')

def cmdInterpereter(s: player.player, cmd: str):
    cmd = cmd.lower().split()       # Split up the string so that it's readable
    if cmd:

        if cmd[0] == '!quit':                # Player quits, say bye then purge
            s.sendUpdate("SERVER: Bye!\n")
            print(s.name, 'quit!')
            purge(s)

        elif cmd[0] == '!help':               # Sends the user the command list
            s.sendUpdate(cmdlist)
            print(s.name, 'requested help')

        elif cmd[0] == '!name':                       # Changes the user's name
            if len(cmd) > 1:
                print(s.name, 'changed their name to', cmd[1])
                s.name = cmd[1]
                s.sendUpdate('SERVER: Name changed to ' + s.name + '\n')
            else:
                s.sendUpdate('SERVER: Please use the format: "!name [name]"\n')

        elif cmd [0] == '!join':                                 # Join a lobby
            if len(cmd) > 1:
                print(s.name, 'attempting to join', cmd[1])
                gameJoiner(s, cmd[1])
            else:
                s.sendUpdate('SERVER: Please use the format: "!join [game]"\n')

        else:                                          # They fucked up, not us
            s.sendUpdate('SERVER: Command not recognized, type !help\n')

def main():

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