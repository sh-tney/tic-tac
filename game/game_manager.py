import socket
import select

import player
import game

# Establish the server's socket, accepting from any client, and also sets
#   up the dictionary of sockets & player objects, which the server's socket
#   is also on, with a None player object; such that the server's socket can
#   be checked alongside other recieving sockets
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '0.0.0.0'
port = 6969
addr = (host, port)
playerList = { server_sock: player.player(server_sock, addr) }

gameList = []
gameList.append(game.game())

cmdlist = '\n!help        - Displays this exact list\n' + \
          '!quit        - Exits and closes your connection safely\n' + \
          '!name [xxxx] - Changes your username to [xxxx]\n' + \
          '!join [game] - Attempts to join a game from the following list\n' + \
          '                 if one exists, or creates a new lobby and waits\n' + \
          '                 for opponents\n' + '\n' + \
          '     GAME OPTIONS:\n' + \
          '     chat    - not actually a game, just a simple multi-user chat\n\n'

def gameJoiner(sender: player.player, join: str):
    joined = False
    for g in gameList:
        if join == g.name:
            sender.state = g.name
            g.addPlayer(sender)
            joined = True
            break
    if not joined:
        sender.sendUpdate('SERVER: Not a recognised game, !help for a list')

def cmdInterpereter(sender: player.player, cmd: str):
    cmd = cmd.lower().split()
    if cmd:
        if cmd[0] == '!quit':
            sender.sendUpdate('Bye!')
            playerList.pop(sender.sock)
            sender.sock.close()
            print(sender.name, 'quit!')
        elif cmd[0] == '!help':
            sender.sendUpdate(cmdlist)
            print(sender.name, 'requested help')
        elif cmd[0] == '!name':
            if len(cmd) > 1:
                print(sender.name, 'changed their name to', cmd[1])
                sender.name = cmd[1]
                sender.sendUpdate('SERVER: Name changed to ' + cmd[1])
            else:
                sender.sendUpdate('SERVER: Please use the format: "!name [name]"')
        elif cmd [0] == '!join':
            if len(cmd) > 1:
                print(sender.name, 'attempting to join', cmd[1])
                gameJoiner(sender, cmd[1])
            else:
                sender.sendUpdate('SERVER: Please use the format: "!join [game]"')
        else:
            sender.sendUpdate('SERVER: Command not recognized, type !help')

def killPlayer(p: player.player, e: Exception=None):
    print('Terminating player:', p.name)
    print('Error:', e)
    try:
        for g in gameList:
            if g.name == p.state:
                g.removePlayer(p)
    except Exception as ex1:
        print('Error while removing player from game:\n', ex1)
    try:
        playerList.pop(p.sock)
    except Exception as ex2:
        print('Error while removing player from list:\n', ex2)
    try: 
        p.sock.close()
    except Exception as ex3:
        print('Error while closing player socket:\n', ex3)

# Loops through the list of active sockets, including the server itself;
# On the server socket, the server will accept any incoming connection
# On active players, they will simply be skipped, as they are 
#   assumed to be handled by the relevant activity they are in.
# On other inactive players, checks for incoming requests, upon which
#   users can attempt to assign themselves a name, or join an activity.
#   Users who atempt a non-recognized action here will be prompted with
#   a the list of commands they were shown on connection. 
def readTraffic():
    while True:
        readySockets = select.select(playerList.keys(), [], [])[0]
        for sock in readySockets:
            if sock == server_sock:
                s, a = sock.accept()
                playerList[s] = player.player(s, a)
                print('Connection from', a)
                playerList[s].sendUpdate('SERVER: Welcome to tic-tac, type !help for a list of commands, or !quit to quit')

            else:
                try:
                    data = (playerList[sock].getResponse())
                    if data:

                        if playerList[sock].state is None:
                            cmdInterpereter(playerList[sock], data)
                        else:
                            for g in gameList:
                                if g.name == playerList[sock].state:
                                    g.updateGame(playerList[sock], data)
                except Exception as e:
                    killPlayer(playerList[sock], e)
                    continue

server_sock.bind(addr)
server_sock.listen()
print('Now listening on port', addr)
readTraffic()