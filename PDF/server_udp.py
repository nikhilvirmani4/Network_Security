import socket
import rsa

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024
msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

socket_list = []
users = {}
users_present_with_ip = {}


def add_user_ip(name, ip):
    users_present_with_ip[name] = ip


# Listen for incoming datagrams

while (True):

    # 1. read the input from client
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    # user_name, public_key = bytesAddressPair[0].split(',')

    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    
    if message.decode().startswith("#"):

        msg_decoded = message.decode()
        user_name, public_key = msg_decoded.split(',')
        print(user_name)
        print(public_key)
        clientMsg = "Message from Client:{}".format(message)
        clientIP = "Client IP Address:{}".format(address)

        print(clientMsg)
        print(clientIP)
        # add username and ip in dictionary
        add_user_ip(message.decode(), address)

        print(users_present_with_ip)
        # Sending a reply to client, saying that we added your username
        msg = "added your ip and username"
        UDPServerSocket.sendto(msg.encode(), address)


# 2. listen for the username
    bytesAddressPair2 = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair2[0]
    address = bytesAddressPair2[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)
    msg2 = str(users_present_with_ip.get(message.decode()))
    print(msg2)
    UDPServerSocket.sendto(msg2.encode(), address)
