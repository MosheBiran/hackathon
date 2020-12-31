import msvcrt
import socket
import time
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

        """---------------------------------UDP Socket Init------------------------------------"""
        # UDP
        try:

            correctDate = b'\xfe\xed\xbe\xef\x02'

            # Linux
            # ip = get_if_addr('eth1')

            ip = '127.0.0.1'
            port = 13117

            UDP_Client_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            UDP_Client_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            UDP_Client_Socket.bind(("", port))

            print("Client started, listening for offer requests...")

            data, address = UDP_Client_Socket.recvfrom(1024)

            if data[0:4] != correctDate[0:4]:
                print("Wrong Message")  # TODO - Remove
                continue

            print("Received offer from " + ip + "," + " attempting to connect...")

        except:
            print("UDP Socket Exception")
            continue


        group_name = "BitS PleaSe\n"


        """---------------------------------TCP Socket Init------------------------------------"""

        # TCP
        try:
            # Linux
            # ip = get_if_addr('eth1')

            # Windows
            ip = '127.0.0.1'

            TCP_Client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            TCP_Client_Socket.connect((ip, (int(hex(data[5])[2:]+hex(data[6])[2:], 16))))
            TCP_Client_Socket.sendall(bytes(group_name, 'utf-8'))
        except:
            print("TCP Socket Exception")
            continue

        """---------------------------------Receive Game Start Message------------------------------------"""
        try:
            StartMessage = TCP_Client_Socket.recv(1024)
        except:
            print("Server Disconnected")
            continue
        print(StartMessage.decode('utf-8'))


        """---------------------------------Game Press Input 10 Sec------------------------------------"""

        #  Windows
        now = time.time()
        futureTCP = now + 10
        while time.time() < futureTCP:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                try:
                    TCP_Client_Socket.send(key)
                except:
                    print("Server Disconnected")
                    break

        # #  Linux!
        # old_settings = termios.tcgetattr(sys.stdin)
        # try:
        #     tty.setcbreak(sys.stdin.fileno())
        #     now = time.time()
        #         futureTCP = now + 10
        #         while time.time() < futureTCP:
        #         if isData():
        #             c = sys.stdin.read(1)
        #             if c == '\x1b':  # x1b is ESC
        #                 break
        #
        # finally:
        #     termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        """---------------------------------Summary Message------------------------------------"""
        try:
            SummaryMessage = TCP_Client_Socket.recv(1024)
            print(SummaryMessage.decode('utf-8'))
            print("\nServer disconnected, listening for offer requests...")
        except:
            print("Server Disconnected")






if __name__ == '__main__':
    main()
