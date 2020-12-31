import _thread
import socket
import time
from time import sleep
from scapy.all import get_if_addr


def broadcastUDP(UDP_server_Socket):

    message_structure = b'\xfe\xed\xbe\xef\x02\x19\xA5'

    # Linux
    # ip = get_if_addr('eth1')

    ip = '127.0.0.1'
    print("Server started, listening on IP address " + ip)

    now = time.time()
    future = now + 10
    while time.time() < future:
        UDP_server_Socket.sendto(message_structure, ('255.255.255.255', 13117))
        sleep(1)


def receiveTCP(players, TCP_Server_Socket):


    nowTCP = time.time()
    futureTCP = nowTCP + 10
    while time.time() < futureTCP:

        connectionSocket, address = TCP_Server_Socket.accept()
        received_data = connectionSocket.recv(1024)
        players[received_data.decode('utf-8')] = connectionSocket


def divedToGroups(players):
    group1 = {}
    group2 = {}
    count = 1

    for PlayerName, PlayerSocket in players.items():
        if count % 2 == 0:
            group2[PlayerName] = PlayerSocket
        else:
            group1[PlayerName] = PlayerSocket

    return [group1, group2]


def makeMessageToGroups(group1, group2):

    message = "\nWelcome to Keyboard Spamming Battle Royal.\n"
    message += "\n*** Group 1: ***\n"
    message += "==\n"

    for player in group1.keys():
        message += player + "\n"

    message += "****************\n"
    message += "\n*** Group 2: ***\n"
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

        received_data = playerSocket.recv(1024)

        if received_data.decode('utf-8') not in groupCount:
            groupCount[received_data.decode('utf-8')] = 1

        else:
            groupCount[received_data.decode('utf-8')] += 1


def gameSummaryMessage(group1, group2, group1Count, group2Count):

    winners = {}
    message = ""
    sumOfGroup1 = sum(group1Count.values())
    sumOfGroup2 = sum(group2Count.values())

    message += "****************************\n"
    message += "******  Game over!  ********\n"
    message += "****************************\n\n"
    message += "Group 1 typed in " + str(sumOfGroup1) + " characters.\n"
    message += "Group 2 typed in " + str(sumOfGroup2) + " characters.\n\n"

    if sumOfGroup1 > sumOfGroup2:
        message += "******  Group 1 wins!  ******\n\n"
        winners = group1

    elif sumOfGroup1 < sumOfGroup2:
        message += "******  Group 2 wins!  ******\n\n"
        winners = group2

    elif sumOfGroup1 == sumOfGroup2:
        message += "******* Its a TIE!!!!! Good Job! *******\n\n"
        winners = {**group1, **group2}

    # Sorted_By_Count = dict(sorted(winners.items(), key=lambda e: e[1]))
    #
    # message += "\n The Most  Typed Character is :  " + list(Sorted_By_Count.keys())[0] + "\n"
    # message += "\n The Least Typed Character is :  " + list(Sorted_By_Count.keys())[len(Sorted_By_Count) - 1] + "\n"



    message += "Congratulations to the winners:\n"
    message += "==\n"

    for name in winners.keys():
        message += name + "\n"

    return message


def main():


    """---------------------------------TCP Socket Init------------------------------------"""
    # TCP SOCKET

    # ip = get_if_addr('eth1')
    ip = '127.0.0.1'
    TCP_ServerPort = 6565

    TCP_Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCP_Server_Socket.bind((ip, TCP_ServerPort))
    TCP_Server_Socket.listen()

    """---------------------------------UDP Socket Init------------------------------------"""
    # UDP SOCKET

    UDP_Server_Port = 13117

    UDP_server_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDP_server_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    UDP_server_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    UDP_server_Socket.bind((ip, UDP_Server_Port))

    # Key = Player Name  : Value = The Connection
    players = {}

    while True:

        """--------------------------------- UDP Broadcast + Tcp Receive + Timer 10 sec ------------------------------------"""
        _thread.start_new_thread(broadcastUDP, (UDP_server_Socket,))
        _thread.start_new_thread(receiveTCP, (players, TCP_Server_Socket, ))
        sleep(10.1)

        #  TODO - check if we need this
        # if len(players) == 0:
        #     continue

        """--------------------------------- Deviation Of The Players Into 2 Groups ------------------------------------"""

        lst_of_groups = divedToGroups(players)
        group1 = lst_of_groups[0]
        group2 = lst_of_groups[1]


        group1_count = {}
        group_2_Count = {}

        """--------------------------------- Create The Start Message To The Players ------------------------------------"""

        StartMessage = makeMessageToGroups(group1, group2)

        """--------------------------------- Send To The Players To Begin The Game By Threads ------------------------------------"""

        for PlayerName, playerSocket in players.items():
            if PlayerName in group1:
                _thread.start_new_thread(startGame, (group1_count, playerSocket, StartMessage, ))
            else:
                _thread.start_new_thread(startGame, (group_2_Count, playerSocket, StartMessage, ))

        sleep(10.1)

        """--------------------------------- Make + Send The Game Summary To The Players  ------------------------------------"""

        SummaryMessage = gameSummaryMessage(group1, group2, group1_count, group_2_Count)

        for playerSocket in players.values():
            playerSocket.sendall(bytes(SummaryMessage, 'utf-8'))


        players.clear()

        print("\n****** Game over *********\n")
        print("sending out offer requests...\n")



if __name__ == '__main__':
    main()

