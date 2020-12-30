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


# TODO - make remove
def sendMessageToGroups(players, message):
    for playerSock in players.values():
        playerSock.sendall(bytes(message, 'utf-8'))


def startGame(groupCount, playerSocket, message):
    playerSocket.sendall(bytes(message, 'utf-8'))

    nowTCP = time.time()
    futureTCP = nowTCP + 10
    while time.time() < futureTCP:
        # connectionSocket, address = playerSocket.accept()
        sentence = playerSocket.recv(1024)
        print(sentence.decode('utf-8'))  # TODO - Remove
        if sentence.decode('utf-8') not in groupCount:
            groupCount[sentence.decode('utf-8')] = 1
        else:
            groupCount[sentence.decode('utf-8')] += 1




def main():
    players = {}

    _thread.start_new_thread(brodcast, ())
    _thread.start_new_thread(receiveTCP, (players, ))
    sleep(10.1)

    lst = divedToGroups(players)
    group1 = lst[0]
    group2 = lst[1]

    group1Count = {}
    group2Count = {}
    message = makeMessageToGroups(group1, group2)
    # sendMessageToGroups(players, message)  # TODO - maybe in thread?

    for teamName, playerSocket in players.items():
        if teamName in group1:
            _thread.start_new_thread(startGame, (group1Count, playerSocket, message, ))
        else:
            _thread.start_new_thread(startGame, (group2Count, playerSocket, message, ))

    sleep(10.1)

    print(sum(group1Count.values()))
    print(sum(group2Count.values()))





if __name__ == '__main__':
    main()

