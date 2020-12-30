import msvcrt
import socket
from threading import Thread


def main():

    while True:
        # UDP
        try:
            correctDate = b'\xfe\xed\xbe\xef\x02'
            ip = '127.0.0.1'
            port = 13117
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            client.bind(("", port))
            print("Client started, listening for offer requests...")
            data, address = client.recvfrom(1024)
            if data[0:4] != correctDate[0:4]:
                print("Wrong Message")
                # continue
            print("Received offer from " + ip + "," + " attempting to connect...")
        except:
            print("Oh NO!!!!")


        group_name = "Bits please, this is not a bug it's a feature\n"

        # TCP
        try:
            serverName = '127.0.0.1'
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((serverName, (int(hex(data[5])[2:]+hex(data[6])[2:], 16))))
            clientSocket.sendall(bytes(group_name, 'utf-8'))
            break
            # clientSocket.close()
        except:
            print("Oh NO TCP Problem!!!!")

    message = clientSocket.recv(1024)
    print(message.decode('utf-8'))

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            print("Key is {}".format(key))






if __name__ == '__main__':
    main()
