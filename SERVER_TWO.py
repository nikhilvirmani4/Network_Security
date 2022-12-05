import os
import socket
import rsa


HOST = socket.gethostbyname(socket.gethostname())
PORT = 4444
ADDR = (HOST, PORT)
buffer_size = 1024
bytes_to_send = str.encode("Hello Client")

# UDP Datagram Socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind(ADDR)
print("Server is up and running")

socket_list = []
users = {}
client_address_dict = {}
user_with_status={}

def add_user_status(name, status):
    user_with_status[name] = status

   
def add_client(name, addr):
    client_address_dict[name] = addr


def encrypt_nonce(name):
    with open(f'keys/{name}public.pem') as filereader:
        pkeydata = filereader.read()

    pubkey = rsa.PublicKey.load_pkcs1(pkeydata)
    nonce = os.urandom(10)

    # msg = random_text.encode('utf8')
    print("Random encoded text: ", nonce)

    encrypt_msg = rsa.encrypt(nonce, pubkey)
    print("encrypted message: ", encrypt_msg)

    return nonce, encrypt_msg


# Listen for incoming datagrams
while (True):

    # read the input from client
    message_address_pair = UDPServerSocket.recvfrom(buffer_size)

    message = message_address_pair[0].decode()

    # address of the client
    address = message_address_pair[1]

    if message.startswith("#"):
        username, public_key = message.split(',')

        # print(username)
        # print(public_key)

        # client_msg = "Message from Client:{}".format(message)
        client_addr = "Client IP Address:{}".format(address)

        # print(client_msg)
        print(client_addr)

        # add username and ip in dictionary
        add_client(username[1:], address)
        add_user_status(username[1:], 'idle')


        print(client_address_dict)

        nonce, encrypt_msg = encrypt_nonce(username)
        #msg_having_nonce=str(encrypt_msg)+"!" +str(user_with_status)


        print(encrypt_msg)
        #print(msg_having_nonce)
        # send encrypt_msg to client for auth
        UDPServerSocket.sendto(encrypt_msg, address)

        # print all clients
        print(client_address_dict)

    elif message.startswith("AUTH"):
        print('Authentication condition')
        print(message)

        #post successfull auth, send list of clients
        msg = "added your ip and username, now find the list of users with status !" + str(user_with_status)
        UDPServerSocket.sendto(msg.encode(), address)



    elif message.startswith("@"):
        # 2. listen for the username
        #bytesAddressPair2 = UDPServerSocket.recvfrom(bufferSize)
        #message = bytesAddressPair2[0]
        #address = bytesAddressPair2[1]

        clientMsg = "Message from Client:{}".format(message)
        clientIP = "Client IP Address:{}".format(address)

        msg_decoded = message_address_pair[0].decode()
        print(clientMsg)
        print(clientIP)



        add_user_status(msg_decoded[1:], 'busy')
        add_user_status(username[1:], 'busy')

        msg = str(user_with_status)
        UDPServerSocket.sendto(msg.encode(), address)


        msg2 = str(client_address_dict.get(msg_decoded[1:]))
        print(msg2)
        UDPServerSocket.sendto(msg2.encode(), address)
