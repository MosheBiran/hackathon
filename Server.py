import _thread
import socket
import time
from time import sleep
from scapy.all import get_if_addr


def broadcastUDP(UDP_server_Socket):
    """
    This function broadcast for 10 seconds UDP sockets to anyone who listens and want play
    :param UDP_server_Socket: The UDP Server Socket initialized
    """
    message_structure = b'\xfe\xed\xbe\xef\x02\x19\xA5'

    # Linux
    # ip = get_if_addr('eth1')

    # Windows
    ip = '127.0.0.1'
    print("Server started, listening on IP address " + ip)

    now = time.time()
    future = now + 10
    while time.time() < future:
        UDP_server_Socket.sendto(message_structure, ('255.255.255.255', 13117))
        sleep(1)


def receiveTCP(players, TCP_Server_Socket):
    """
    This function receiving for 10 seconds TCP connections from players that what to play
    :param players: empty dictionary of players that will be fulled - {key = player name : Value = Connection socket}
    :param TCP_Server_Socket: The TCP Server Socket initialized
    """
    nowTCP = time.time()
    futureTCP = nowTCP + 10
    while time.time() < futureTCP:

        connectionSocket, address = TCP_Server_Socket.accept()
        received_data = connectionSocket.recv(1024)
        players[received_data.decode('utf-8')] = connectionSocket


def divedToGroups(players):
    """
    This function dived the players into 2 groups.
    :param players: dictionary of players - {key = player name : Value = Connection socket}
    :return: list of groups - [group 1 dictionary, group 2 dictionary]
    """
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
    """
    This function makes the Start game message of the players.
    :param group1: dictionary of group 1 - {key = player name : Value = Connection socket}
    :param group2: dictionary of group 2 - {key = player name : Value = Connection socket}
    :return: String - The Start Game Message
    """
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

    message += "\n\nStart pressing keys on your keyboard as fast as you can!!\n"

    return message


def startGame(groupCount, playerSocket, message, playerName):
    """
    This function sends the start game message to the player
    and starting to listen with TCP server socket to the typing of the player for 10 seconds
    :param playerName: String - Player Name
    :param groupCount: dictionary of the characters that group 1 typed -  {key = character : Value = number it typed}
    :param playerSocket: the TCP Socket of the player
    :param message: String - the start game message
    """
    try:
        playerSocket.sendall(bytes(message, 'utf-8'))
    except:
        print("player Disconnected  : " + playerName + "\n")
        return

    nowTCP = time.time()
    futureTCP = nowTCP + 10
    while time.time() < futureTCP:
        try:
            received_data = playerSocket.recv(1024)
        except:
            print("player Disconnected  : " + playerName + "\n")
            return

        if received_data.decode('utf-8') not in groupCount:
            groupCount[received_data.decode('utf-8')] = 1

        else:
            groupCount[received_data.decode('utf-8')] += 1


def gameSummaryMessage(group1, group2, group1Count, group2Count):
    """
    This function summarize the game into a message
    :param group1: dictionary of group 1 - {key = player name : Value = Connection socket}
    :param group2: dictionary of group 2 - {key = player name : Value = Connection socket}
    :param group1Count: dictionary of the characters that group 1 typed -  {key = character : Value = number it typed}
    :param group2Count: dictionary of the characters that group 2 typed -  {key = character : Value = number it typed}
    :return: message: String - the summary message
    """
    winners = {}
    winners_char = {}
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
        winners_char = group1Count

    elif sumOfGroup1 < sumOfGroup2:
        message += "******  Group 2 wins!  ******\n\n"
        winners = group2
        winners_char = group2Count

    elif sumOfGroup1 == sumOfGroup2:
        message += "******* Its a TIE!!!!! Good Job! *******\n\n"
        winners = {**group1, **group2}
        winners_char = {**group1Count, **group2Count}


    message += "\n **********  Statistics  ********** \n"

    if len(winners_char) > 0:

        Sorted_By_Count = dict(sorted(winners_char.items(), key=lambda e: e[1]))

        message += "\nThe Most  Typed Character is :  '" + list(Sorted_By_Count.keys())[len(Sorted_By_Count) - 1] + "'\n"
        message += "\nThe Least Typed Character is :  '" + list(Sorted_By_Count.keys())[0] + "'\n"
        message += "\nThe Number of Unique Character is :  '" + str(len(Sorted_By_Count.keys())) + "'\n"



    message += "\nCongratulations to the winners:\n"
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
        if len(players) == 0:
            print("\n**** There Are No players Connected .... No game .... ****\n")
            continue

        """--------------------------------- Deviation Of The Players Into 2 Groups ------------------------------------"""

        lst_of_groups = divedToGroups(players)

        if len(lst_of_groups) == 0:
            print("\nFailed To Devised Into Groups ....\n")
            continue

        group1 = lst_of_groups[0]
        group2 = lst_of_groups[1]


        group1_count = {}
        group_2_Count = {}

        """--------------------------------- Create The Start Message To The Players ------------------------------------"""

        StartMessage = makeMessageToGroups(group1, group2)

        """--------------------------------- Send To The Players To Begin The Game By Threads ------------------------------------"""

        for PlayerName, playerSocket in players.items():
            if PlayerName in group1:
                _thread.start_new_thread(startGame, (group1_count, playerSocket, StartMessage, PlayerName,))
            else:
                _thread.start_new_thread(startGame, (group_2_Count, playerSocket, StartMessage, PlayerName,))

        sleep(10.1)

        """--------------------------------- Make + Send The Game Summary To The Players  ------------------------------------"""

        SummaryMessage = gameSummaryMessage(group1, group2, group1_count, group_2_Count)

        for playerName, playerSocket in players.items():
            try:
                playerSocket.sendall(bytes(SummaryMessage, 'utf-8'))
            except:
                print("\nPlayer Disconnected : " + playerName + "\n")
                continue

        players.clear()

        print("\n****** Game over *********\n")
        print("sending out offer requests...\n")



if __name__ == '__main__':
    main()

