import socket
import select
import player

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_addr = ('0.0.0.0', 6969)
server_sock.bind(server_addr)
server_sock.listen()
print("Listening")

def purge(p: player.player):
    print('Purging player', p)
    try:
        player_list.pop(p)
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
        del p
    except:
        print("Couldn't delete")

player_list = [ player.player(server_sock, server_addr) ]
while True:
    for p in player_list:
        read = select.select([p.sock], [], [], 0)[0]

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