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
socketDict = { server_sock: player.player(server_sock) }

# A simple catch-all function to throw to, ensure that if all else goes
#   wrong, we at least close the port
def kill(e):
    server_sock.close()
    print('\nSocket closed on crash\n', e)

# A simple broadcasting method, which will send msg to every member
# of the list of sockets, except for the server's own socket
def broadcast(players: [player.player], msg: str):
    for p in players:
        if p.addr is not None:
            p.sendUpdate(msg)

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
        readySockets = select.select(socketDict.keys(), [], [])[0]
        for sock in readySockets:
            if sock == server_sock:
                s, a = sock.accept()
                p = player.player(s, a)
                socketDict[s] = p
                print('Connection from', a)
                p.sendUpdate()
            else:
                try:
                    data = sock.recv(1024)
                    if data:
                        broadcast(socketDict.values(), data.decode())
                except:
                    print('Connection lost by', sock)
                    sock.close()
                    socketDict.pop(sock)
                    continue

server_sock.bind((host, port))
server_sock.listen()
print('Now listening on port', port)
readTraffic()