import socket
import uuid 
from datetime import datetime 

# nikhil
#added at 17:56
# naga

def get_Timestamp():
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    print(type(ts))
    return str(ts)
     

def get_SessionKey():
    return str(uuid.uuid4().hex);


msgFromClient       = '#'.join(["Hello from Client", get_SessionKey(), get_Timestamp()])
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)

msg = "Message from Server {}".format(msgFromServer[0])
print(msg)
