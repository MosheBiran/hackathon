import msvcrt
import socket
import time
from threading import Thread
from scapy.all import get_if_addr

# Linux
# import sys
# import select
# import tty
# import termios
#
#
# def isData():
#     return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


def main():
    while True:
        while True:
            # UDP
            try:
                correctDate = b'\xfe\xed\xbe\xef\x02'
                ip = '127.0.0.1'
                # ip = get_if_addr('eth1')
                port = 13117
                client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                client.bind(("", port))
                print("Client started, listening for offer requests...")
                data, address = client.recvfrom(1024)
                if data[0:4] != correctDate[0:4]:
                    print("Wrong Message")  # TODO - Remove
                    # continue
                print("Received offer from " + ip + "," + " attempting to connect...")
                client.close()
            except:
                print("Oh NO!!!!")


            group_name = "Bits please, this is not a bug it's a feature\n"

            # TCP
            try:
                serverName = '127.0.0.1'
                # serverName = get_if_addr('eth1')

                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientSocket.connect((serverName, (int(hex(data[5])[2:]+hex(data[6])[2:], 16))))
                clientSocket.sendall(bytes(group_name, 'utf-8'))
                break
                # clientSocket.close()
            except:
                print("Oh NO TCP Problem!!!!")

        message = clientSocket.recv(1024)
        print(message.decode('utf-8'))

        #  Windows
        now = time.time()
        futureTCP = now + 10
        while time.time() < futureTCP:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                clientSocket.send(key)
                print("Key is {}".format(key))


        # #  Linux!
        # old_settings = termios.tcgetattr(sys.stdin)
        # try:
        #     tty.setcbreak(sys.stdin.fileno())
        #     now = time.time()
        #     futureTCP = now + 10
        #     while time.time() < futureTCP:
        #         if isData():
        #           key = sys.stdin.read(1)
        #             clientSocket.send(key)
        #             print("Key is {}".format(key))
        #
        #
        #
        # finally:
        #     termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

        message = clientSocket.recv(1024)
        print(message.decode('utf-8'))
        clientSocket.close()





if __name__ == '__main__':
    main()
