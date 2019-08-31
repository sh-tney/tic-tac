import socket
import select

import player

# Establish the server's socket, accepting from any client, and also sets
#   up the dictionary of sockets & player objects, which the server's socket
#   is also on, with a None player object; such that the server's socket can
#   be checked alongside other recieving sockets
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '0.0.0.0'
port = 6969
addr = (host, port)
playerList:{socket.socket: player.player} = { server_sock: player.player(server_sock, addr) }
cmdlist = '!quit    - Exits and closes your connection safely\n' + \
          '!help    - Displays this exact list'

# A simple broadcasting method, which will send msg to every member
# of the list of sockets, except for the server's own socket
def broadcast(targets: [player.player], msg: str):
    for s in targets:
        if s.addr != addr:
            try:
                s.sendUpdate(msg)
            except:
                print('Terminating connection from (broadcasting)', s.addr)
                s.sock.close()
                playerList.pop(s.sock)
                #continue

def cmdInterpereter(sender: player.player, cmd: str):
    cmd = cmd.lower().split()
    if cmd:
        if cmd[0] == '!quit':
            sender.sendUpdate('Bye!')
            playerList.pop(sender.sock)
            sender.sock.close()
            print(sender.addr, 'quit!')
        elif cmd[0] == '!help':
            sender.sendUpdate(cmdlist)
            print(sender.addr, 'requested help')
        else:
            sender.sendUpdate('Command not recognized, type !help')


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
                playerList[s].sendUpdate('Welcome to tic-tac, type !help for a list of commands, or !quit to quit')

            else:
                try:
                    data = (playerList[sock].getResponse())
                    if data:
                        print(data)
                        if playerList[sock].state is None:
                            cmdInterpereter(playerList[sock], data)
                except:
                    print('Terminating connection from (recieving)', playerList[sock].addr)
                    sock.close()
                    playerList.pop(sock)
                    #continue

server_sock.bind(addr)
server_sock.listen()
print('Now listening on port', addr)
readTraffic()