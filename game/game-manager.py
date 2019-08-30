import socket
import player

# Establish the server's socket, accepting from any client
server_sock = socket.socket() 
host = '0.0.0.0'
port = 6969
playerList = []

server_sock.bind((host, port))
print('Socket bound on', port)
server_sock.listen()
print('Listening')
playerList.append(player.player(server_sock))

# Loops through the list of player sockets, including this server's own;
    # On encountering our own socket, we check for new incoming connections
    #   and add them to the playerList
    # On other sockets (players), checks for incoming requests, upon which
    #   users can attempt to assign themselves a name, or join an activity.
    #   Users who atempt a non-recognized action here will be prompted with
    #   a the list of commands they were shown on connection.
try:
    while True:   
        for currentPlayer in playerList:
            if currentPlayer.sock == server_sock:
                s, addr = server_sock.accept()
                playerList.append(player.player(s))
                print('Someone connected on', addr)
                playerList[-1].sendUpdate(update='Welcome!')
except:
    server_sock.close()
    print('\nSocket closed correctly before exit')