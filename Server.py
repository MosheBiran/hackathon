import _thread
import socket
import time
from threading import Thread
from time import sleep



def brodcast():
    try:
        message = b'\xfe\xed\xbe\xef\x02\x19\xA5'

        ip = '127.0.0.1'
        port = 13117
        # UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind((ip, port))
        # mode of listening
        print("Server started, listening on IP address " + ip)
        # our message is "offer" to every client who is listening
        now = time.time()
        future = now + 10
        while time.time() < future:
            sock.sendto(message, ('255.255.255.255', 13117))
            sleep(1)
    except:
        print("Oh NO!!!!")


def receiveTCP(players):
    ip = '127.0.0.1'
    serverPort = 6565
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((ip, serverPort))
    serverSocket.listen(20)

    nowTCP = time.time()
    futureTCP = nowTCP + 10
    while time.time() < futureTCP:
        connectionSocket, address = serverSocket.accept()
        sentence = connectionSocket.recv(1024)
        print(sentence.decode('utf-8'))  # TODO - Remove
        players[sentence.decode('utf-8')] = connectionSocket


def divedToGroups(players):
    group1 = {}
    group2 = {}
    count = 1
    for name, sock in players.items():
        if count % 2 == 0:
            group2[name] = sock
        else:
            group1[name] = sock

    return [group1, group2]


def makeMessageToGroups(group1, group2):
    message = "Welcome to Keyboard Spamming Battle Royal.\n"
    message += "Group 1:\n"
    message += "==\n"

    for player in group1.keys():
        message += player + "\n"

    message += "Group 2:\n"
    message += "==\n"

    for player in group2.keys():
        message += player + "\n"

    message += "\n"
    message += "Start pressing keys on your keyboard as fast as you can!!\n"

    return message


def sendMessageToGroups(players, message):
    for playerSock in players.values():
        playerSock.sendall(bytes(message, 'utf-8'))




def main():
    players = {}

    _thread.start_new_thread(brodcast, ())
    _thread.start_new_thread(receiveTCP, (players, ))
    sleep(10.1)

    lst = divedToGroups(players)
    group1 = lst[0]
    group2 = lst[1]

    message = makeMessageToGroups(group1, group2)
    sendMessageToGroups(players, message)  # TODO - maybe in thread?




if __name__ == '__main__':
    main()

