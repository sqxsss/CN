from socket import *
import os
import os.path

# tranfer single file like file1.txt
def transferSignleFile(fileCommand):
    f = open(fileCommand, 'rb')
    while True:
        data = f.read(1024)
        if str(data) != "b''":
            serverUDPSocket.sendto(data, (serverName, serverUDPPort))
        else:
            serverUDPSocket.sendto('end'.encode('utf-8'), (serverName, serverUDPPort))
            break
        data, server_addr = serverUDPSocket.recvfrom(1024)

# tranfer folder like file2
def transferFolder(fileCommand):
    if fileCommand != "":
        serverUDPSocket.sendto(fileCommand.encode(), (serverName, serverUDPPort))
    for root, dirs, files in os.walk('./' + fileCommand):
        for dir in dirs:
            dirPath = root + '/' + dir
            serverUDPSocket.sendto(dirPath.encode(), (serverName, serverUDPPort))
        for file in files:
            filePath = root + '/' + file
            serverUDPSocket.sendto(filePath.encode(), (serverName, serverUDPPort))
            transferSignleFile(root + '/' + file)
    serverUDPSocket.sendto('end'.encode('utf-8'), (serverName, serverUDPPort))

serverName = "127.0.0.1"
# TCP connection, work as server
serverTCPPort = 8081
serverTCPSocket = socket(AF_INET, SOCK_STREAM)
serverTCPSocket.bind(('', serverTCPPort))
serverTCPSocket.listen(1)

# UDP connection, work as client
serverUDPPort = 8083
serverUDPSocket = socket(AF_INET, SOCK_DGRAM)

print("Server Running")

# get file list under /server/
allFiles = ""
for root, dirs, files in os.walk('./'):
    allFiles = allFiles + ' '.join(dirs) + ' ' + ' '.join(files)
    break

while True:
    connectionSocket, addr = serverTCPSocket.accept()
    while True:
        try:
            requestCommand = connectionSocket.recv(1024).decode()
            if requestCommand == "listallfiles":
                list = ""
                for root, dirs, files in os.walk('./'):
                    list = list + ' '.join(dirs) + ' ' + ' '.join(files)
                    break
                allFiles = list
                connectionSocket.send(allFiles.encode())
            # elif requestCommand == "exit":
            #     connectionSocket.close()
            #     break
            elif requestCommand.startswith("download "):
                fileCommand = requestCommand[9:]
                # print(fileCommand)
                if fileCommand == "all":
                    # download all files under './'
                    transferFolder('')
                elif fileCommand in allFiles.split(' '):
                    if os.path.isfile(fileCommand):
                        # suffix, single file
                        transferSignleFile(fileCommand)
                    elif os.path.isdir(fileCommand):
                        # folder
                        transferFolder(fileCommand)
                else:
                    fileCommand = "fail, file not exist"
                    # connectionSocket.send(fileErrMessage.encode())
                sendMessage = "Downloaded " + fileCommand
                connectionSocket.send(sendMessage.encode())
            else:
                print("client disconnected")
                break
                # commandErrMessage = "please enter the correct command"
                # connectionSocket.send(commandErrMessage.encode())
        except ConnectionAbortedError:
            print("client disconnected")
            break
    connectionSocket.close()



