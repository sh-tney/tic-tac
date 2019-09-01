import socket
import select
import time
import player

server_addr = ('0.0.0.0', 6969)
player_list = []
cmdlist = '\n!help        - Displays this exact list\n' +\
          '!quit        - Exits and closes your connection safely\n' +\
          '!name [xxxx] - Changes your username to [xxxx]\n' +\
          '!join [game] - Attempts to join a game from the following list\n' +\
          '               if one exists, or creates a new lobby and waits\n' +\
          '                 for opponents\n' + '\n' +\
          '   GAME OPTIONS:\n' +\
          '   chat    - not actually a game, just a simple multi-user chat\n\n'

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
                print(sender.name, 'attempting to join', cmd[1])
                gameJoiner(sender, cmd[1])
            else:
                s.sendUpdate('SERVER: Please use the format: "!join [game]"\n')

        else:                                          # They fucked up, not us
            s.sendUpdate('SERVER: Command not recognized, type !help\n')

def main():

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(server_addr)
    server_sock.listen()
    print("Listening on", server_addr)

    player_list.append(player.player(server_sock, server_addr))

    while True:

        for p in player_list:    # Loop through sockets, selecting individually

            try:
                read = select.select([p.sock], [], [], 1)[0]
            except:
                print("List ordering error", p.name)
                continue

            print(p.name, len(read))        # Some nice diagnostics to look at
            time.sleep(3)

            for r in read:  # Searching one socket at a time, we know the owner

                if r == server_sock:              # Accept incoming connections
                    s, a = server_sock.accept()
                    p = player.player(s, a)
                    print('Connection from', a)
                    player_list.append(p)
                    p.sendUpdate('Hello from Server\n')

                else:                       # Otherwise, recieve client message

                    try:
                        dat = r.recv(8192).decode()
                        print("decoded ok")
                        if dat == "":              # Check if connection closed
                            print(p.name, "connection closed")
                            purge(p)
                        else:                      # Otherwise, handle normally
                            if p.state is None:
                                print("print cmd")
                                cmdInterpereter(p, dat)
                            else:
                                #Game handle
                                print("Game handler")
                                
                    except:                             # Connection died, kill
                        print(p.name, "connection died")
                        purge(p)
                        continue

if __name__ == '__main__':
    main()