import socket
import select
import player
import time

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_addr = ('0.0.0.0', 6969)
server_sock.bind(server_addr)
server_sock.listen()
print("Listening")

def purge(p: player.player):
    print('Purging player', p.name)
    try:
        player_list.remove(p)
    except:
        print('Player not on list')
    try:
        p.sock.shutdown()
    except:
        print('Sock shutdown fail')
    try:
        p.sock.close()
    except:
        print('Sock close fail')
    try:
        del p.sock
    except:
        print("Couldn't delete socket")
    try: 
        del p
    except:
        print("Couldn't delete player")

player_list = [ player.player(server_sock, server_addr) ]
while True:

    for p in player_list:   # Loop through sockets, checking reads individually
        read = select.select([p.sock], [], [], 0)[0]

        print(p.name, len(read))            # Some nice diagnostics to look at
        time.sleep(3)

        for r in read:  # Searching one socket max, therefore we know the owner

            if r == server_sock:                  # Accept incoming connections
                s, a = server_sock.accept()
                print('Connection from', a)
                player_list.append(player.player(s, a))
                s.send('Hello from Server\n'.encode())

            else:                           # Otherwise, recieve client message
                data = r.recv(8192)
                try:
                    if data.decode() == "":# Recieveing null, connection closed
                        print(p.name, "connection closed")
                        purge(p)
                    else:                          # Otherwise, handle normally
                        print(data.decode())
                except:                                 # Connection died, kill
                    print(p.name, "connection died")
                    purge(p)
                    continue
                    

    """    
    for r in read:
        if r == server_sock:
            s, a = server_sock.accept()
            print('Connection from', a)
            player_list.append(s)
            s.send('Hello from Server\n'.encode())
        else:
            print("hi")
            data = r.recv(8192)
            print(data)
            try:
                if data.decode() == "":
                    print(r, "dead")
                    purge(r)
            except:
                purge(r)
"""