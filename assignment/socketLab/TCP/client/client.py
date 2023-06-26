from socket import *

serverName = "127.0.0.1"
serverPort = 8090
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

def transferSignleFile(fileCommand):
    f = open(fileCommand, 'rb')
    while True:
        data = f.read(1024)
        if str(data) != "b''":
            clientSocket.send(data)
        else:
            clientSocket.send('end'.encode('utf-8'))
            break
        data = clientSocket.recv(1024)
    clientSocket.close()

transferSignleFile("file1.pdf")
