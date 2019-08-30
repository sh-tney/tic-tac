import socket

# Establish the server's socket
sock = socket.socket() 
host = ''
port = 6969
#sock.close()
sock.bind((host, port))
print('Socket Bound:', host, port)

def telnetListener():
    while True:
        client, addr = sock.accept()
        print(addr, ' connected.')
        client.send(('OwO').encode())

sock.listen()
print('Listening')
try:
    telnetListener()
except:
    sock.close()
    print('\nSocket closed correctly before exit')