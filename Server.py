import _thread
import socket
import time
from threading import Thread
from time import sleep
from scapy.all import get_if_addr


def brodcast(socky):
    try:
        message = b'\xfe\xed\xbe\xef\x02\x19\xA5'

        ip = '127.0.0.1'
        print("Server started, listening on IP address " + ip)
        # our message is "offer" to every client who is listening
        now = time.time()
        future = now + 10
        while time.time() < future:
            socky.sendto(message, ('255.255.255.255', 13117))
            sleep(1)

    except:
        print("Oh NO!!!!")


def receiveTCP(players, serverSocket):


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


def startGame(groupCount, playerSocket, message):
    playerSocket.sendall(bytes(message, 'utf-8'))

    nowTCP = time.time()
    futureTCP = nowTCP + 10
    while time.time() < futureTCP:
        # connectionSocket, address = playerSocket.accept()
        sentence = playerSocket.recv(1024)
        # print(sentence.decode('utf-8'))  # TODO - Remove
        if sentence.decode('utf-8') not in groupCount:
            groupCount[sentence.decode('utf-8')] = 1
        else:
            groupCount[sentence.decode('utf-8')] += 1


def gameSummaryMessage(group1, group2, group1Count, group2Count):
    winners = {}
    message = ""
    sumOfGroup1 = sum(group1Count.values())
    sumOfGroup2 = sum(group2Count.values())
    message += "**************\n"
    message += "* Game over! *\n"
    message += "**************\n"
    message += "Group 1 typed in " + str(sumOfGroup1) + " characters.\n"
    message += "Group 2 typed in " + str(sumOfGroup2) + " characters.\n"
    if sumOfGroup1 > sumOfGroup2:
        message += "Group 1 wins!\n\n"
        winners = group1
    elif sumOfGroup1 < sumOfGroup2:
        message += "Group 2 wins!\n\n"
        winners = group2
    elif sumOfGroup1 == sumOfGroup2:
        message += "Its a TIE!!!!! Good Job!\n\n"
        winners = {**group1, **group2}

    message += "Congratulations to the winners:\n\n"
    message += "==\n\n"
    for name in winners.keys():
        message += name + "\n\n"

    return message


def main():
    # TCP SOCKET
    # ip = get_if_addr('eth1')

    ip = '127.0.0.1'
    serverPort = 6565
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((ip, serverPort))
    serverSocket.listen()

    # UDP
    # UDP SOCKET
    ip = '127.0.0.1'
    port = 13117
    socky = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socky.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socky.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    socky.bind((ip, port))

    players = {}
    while True:


        _thread.start_new_thread(brodcast, (socky, ))
        _thread.start_new_thread(receiveTCP, (players, serverSocket, ))
        sleep(10.1)

        if len(players) == 0:
            continue

        lst = divedToGroups(players)
        group1 = lst[0]
        group2 = lst[1]

        group1Count = {}
        group2Count = {}
        message = makeMessageToGroups(group1, group2)

        for teamName, playerSocket in players.items():
            if teamName in group1:
                _thread.start_new_thread(startGame, (group1Count, playerSocket, message, ))
            else:
                _thread.start_new_thread(startGame, (group2Count, playerSocket, message, ))

        sleep(10.1)

        message = gameSummaryMessage(group1, group2, group1Count, group2Count)

        for playerSocket in players.values():
            playerSocket.sendall(bytes(message, 'utf-8'))

        players.clear()






if __name__ == '__main__':
    main()

