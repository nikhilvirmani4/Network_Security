import socket
import uuid
from datetime import datetime

def get_SessionKey():
    return uuid.uuid4().hex;

def get_Timestamp():
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    print(type(ts))
    return ts

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
msgFromServer       = "Hello  Client"
#bytesToSend= str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 # Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams

bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
message = bytesAddressPair[0]
address = bytesAddressPair[1]


data = str(message).split("#")
for i in range(len(data)):
    print(type(data[i]))

new_tsmp = float("1669590957.116429")
time_diff = get_Timestamp() - new_tsmp
print(time_diff)


if message == "END OF TRANSMISSION":
    socket.close()
clientMsg = "Message from Client:{}".format(message)
clientIP  = "Client IP Address:{}".format(address)

    
#print(clientMsg)
#print(clientIP)

    # Sending a reply to client
msgFromServer = msgFromServer + get_SessionKey()
print(msgFromServer)
bytesToSend = str.encode(msgFromServer)
UDPServerSocket.sendto(bytesToSend, address)


UDPServerSocket.close()
