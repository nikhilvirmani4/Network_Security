import socket
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

# configure local ip and port numbers for UDP
localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024

#msgFromServer = "Hello UDP Client"
#bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")


# socket list, users names, username with ip mapping, username with status "idle" or "busy"
socket_list = []
users = {}
users_present_with_ip = {}
user_with_status = {}


# function to add username and ip
def add_user_ip(name, ip):
    users_present_with_ip[name] = ip

# function to add username and client status


def add_user_status(name, status):
    user_with_status[name] = status


# Listen for incoming datagrams

while (True):

    # 1. read the input from client
    rec_msg_from_client = UDPServerSocket.recvfrom(bufferSize)
    # user_name, public_key = bytesAddressPair[0].split(',')

    message = rec_msg_from_client[0]
    address = rec_msg_from_client[1]

    # if msg starts with#, means it's for username auth
    if message.decode().startswith("#"):
        msg_decoded = message.decode()
        user_name, public_key = msg_decoded.split(',')
        # user has sent his/her username and the path to public key file

        # debug
        print(user_name)
        print(public_key)

        # add username and ip in dictionary
        add_user_ip(user_name[1:], address)
        # add username and status, make it idle, when user logs-in
        add_user_status(user_name[1:], 'idle')

        print(users_present_with_ip)

        pub_key = RSA.import_key(open(public_key).read())
        nonce = get_random_bytes(16)

        print(f"randomly generated nonce {nonce}")
        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(pub_key)
        enc_nonce = cipher_rsa.encrypt(nonce)

        print(f" encrypted nonce {enc_nonce}")
        UDPServerSocket.sendto(enc_nonce, address)

        # Sending a reply to client, saying that we added your username, and send status dictionary
        # ! is the delimiter here
        
       

    elif message.decode().startswith("AUTH"):
        print('Authentication here') 
        print(message.decode()[5:])
        # at 0:48, checking ss
        #match rsa passwords rsa check
        if(str(message.decode()[5:])==str(nonce) ):
            print("match") #match added

        msg = "added your ip and username now find the list of users with status !" + \
        str(user_with_status)
        UDPServerSocket.sendto(msg.encode(), address)

    

    elif message.decode().startswith("@"):
        # @ starting message is for the username which client wants to talk to
        msg_decoded = message.decode()

        # make the client and the requested user as busy
        add_user_status(msg_decoded[1:], 'busy')
        add_user_status(user_name[1:], 'busy')

        # send status dictionary again, post updating the busy status for both
        msg = str(user_with_status)
        UDPServerSocket.sendto(msg.encode(), address)

        # find the ip of requested client, send back
        msg2 = str(users_present_with_ip.get(msg_decoded[1:]))
        print(msg2)
        UDPServerSocket.sendto(msg2.encode(), address)