import os
from socket import *

def receiveSingleFile(fileName):
    f = open(fileName, 'wb')
    while True:
        data, addr = clientUDPSocket.recvfrom(1024)
        if str(data) != "b'end'":
            f.write(data)
        else:
            break
        clientUDPSocket.sendto('ok'.encode('utf-8'), addr)
    f.close()

def receiveFolder(fileName):
    while True:
        folderOrFileName, addr = clientUDPSocket.recvfrom(1024)
        # print(folderOrFileName.decode())
        name = folderOrFileName.decode().replace('\\', '/')
        if str(folderOrFileName) == "b'end'":
            break
        elif "." in name.split('/')[-1]:
            # have suffix, means this is a file
            f = open(name, 'wb')
            receiveSingleFile(name)
        else:
            # no suffix, means this is a folder
            # if not make sure the folder is exist, there will be error
            if os.path.exists(name):
                continue
            else:
                os.makedirs(name)

serverName = '127.0.0.1'
serverTCPPort = 8081
serverUDPPort = 8083

# TCP connection for text message with server
clientTCPSocket = socket(AF_INET, SOCK_STREAM)
clientTCPSocket.connect((serverName, int(serverTCPPort)))

# UDP connection for receiving files from server.py
# work as UDP server work to get file transferred from UDP client
clientUDPSocket = socket(AF_INET, SOCK_DGRAM)
clientUDPSocket.bind(('', serverUDPPort))

# get list of file first in order to help judge if the file exist
clientTCPSocket.send("listallfiles".encode())
list = clientTCPSocket.recv(1024)

while True:
    sentence = input('> ')
    if sentence == "exit":
        print("Exitting")
        clientTCPSocket.close()
        break
    # download send commands for download by TCP and get file back by UDP
    elif sentence.startswith("download "):
        clientTCPSocket.send(sentence.encode())
        fileName = sentence[9:]
        if fileName == "all":
            receiveFolder(fileName)
            # print("Downloaded " + fileName)
        elif fileName in list.decode().split(' '):
            if "." in fileName:
                receiveSingleFile(fileName)
                # print("Downloaded " + fileName)
            else:
                receiveFolder(fileName)
                # print("Downloaded " + fileName)
        modifiedSentence = clientTCPSocket.recv(1024)
        print(modifiedSentence.decode())
    elif sentence == "listallfiles":
        # listallfiles or other commands that are not correct
        clientTCPSocket.send(sentence.encode())
        fileList = clientTCPSocket.recv(1024)
        list = fileList
        print(fileList.decode())
    else:
        print("please enter the correct command")