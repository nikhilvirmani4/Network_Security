import socket
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

# function to generate rsa public, pvt pair
# store the pvt key in client side only, and add the public key to the keys folder, send path of public key


def public_private_key(id):
    key = RSA.generate(1024)
    private_key = key.export_key()
    # print(private_key)
    # file_out = open("private.pem", "wb")
    # file_out.write(private_key)
    # file_out.close()

    public_key = key.publickey().export_key()
    # print(public_key)
    public_key_file_path = f'keys/{id}public.pem'
    file_out = open(public_key_file_path, "wb")
    file_out.write(public_key)
    file_out.close()

    return public_key_file_path, private_key, key
  ##or main onlt

def get_count(dict_status):
    import json

    json_acceptable_string = dict_status.replace("'", "\"")
    d = json.loads(json_acceptable_string)
    no_of_idle = 0
    for key, val in d.items():  
        if val == 'idle':
            no_of_idle = no_of_idle+1

    print(no_of_idle)
    return (no_of_idle)


# server address is stored here
serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


# Client is on, enter username after #
username = input("Enter your user name:")
# generate rsa_key with and share the public key path with server
public_key, private_key, key = public_private_key(username)


path_for_public_key = username + "," + public_key
UDPClientSocket.sendto(path_for_public_key.encode(), serverAddressPort)


nonce_for_auth = UDPClientSocket.recvfrom(bufferSize)
nonce_for_auth = nonce_for_auth[0]
print(f"nonce for auth {nonce_for_auth}")
cipher_rsa = PKCS1_OAEP.new(key)

# print(f"cipher_rsa {cipher_rsa}")
decrypted_nonce = cipher_rsa.decrypt(nonce_for_auth)
print(f"decrypted_nonce for auth {decrypted_nonce}")

#send auth checking auth

decrypted_nonce_auth = 'AUTH,' + str(decrypted_nonce)
print("Decrypted message: ", decrypted_nonce)
UDPClientSocket.sendto(decrypted_nonce_auth.encode(), serverAddressPort)


# msg received has list of clients with state, idle or busy
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg1 = "Message from Server {}".format(msgFromServer[0].decode())
print(msg1)


# split received input and extract the dictionary
text, dict_from_server = msgFromServer[0].decode().split('!')
print(dict_from_server)

# get number of idle counts from get_count function
no_of_idle_count = get_count(dict_from_server)


# if only the user who entered is idle, means no one is available to talk
# go to listen mode, wait for msg from other user
if (no_of_idle_count == 1):
    while True:
        #  msg received from client
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg1 = "Message from {} - {}".format(
            msgFromServer[1], msgFromServer[0].decode())
        print("\n", msg1)

        # send reply msg to other user
        print("\n")
        send_msg = input("msg to reply to {} -".format(msgFromServer[1]))
        # print(send_msg)

        UDPClientSocket.sendto(send_msg.encode(), msgFromServer[1])

        # wait for exit key word, if yes then break the communication
        if (send_msg == 'exit'):
            break


# dont go to listen mode, send the username we want to talk to from the list
else:

    #  #send msg to server, username
    send_msg = input("enter user you want to talk to ")
    UDPClientSocket.sendto(send_msg.encode(), serverAddressPort)

    # msg received status and client ip and port
    msgFromServer_status = UDPClientSocket.recvfrom(bufferSize)
    msg2 = "Message from Server {}".format(msgFromServer_status[0].decode())
    msg_addr_server = msgFromServer_status[1]
    print("status=", msg2)

    msgFromServer_ip = UDPClientSocket.recvfrom(bufferSize)
    msg2 = "Message from Server {}".format(msgFromServer_ip[0].decode())
    msg_addr_server = msgFromServer_ip[1]
    print(msg2)

    addr_client = msgFromServer_ip[0]
    # print(addr_client)
    print(addr_client.decode())

    # talk to the client on the port and ip received
    while True:

        # all are on localhost, so ip is same as below
        udp_ip = "127.0.0.1"
        addr_client_decoded = addr_client.decode()
        # extract port number from address ('127.0.0.1',port)
        udp_port = addr_client_decoded[addr_client_decoded.index(',')+1:-1]
        # print(udp_port)
        udp_port_int = int(udp_port)

    #  send first msg to other user
        print("\n")
        send_msg = input(
            "msg to send to requested user {} port {} - ".format(udp_ip, udp_port_int))
        UDPClientSocket.sendto(send_msg.encode(), (udp_ip, udp_port_int))

    # 2. reply received from other client
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg1 = "Message from {} - {} ".format(
            msgFromServer[1], msgFromServer[0].decode())
        print("\n", msg1)

        #send_msg = input("if you want to end type exit ")
        if (send_msg == 'exit'):
            break

    UDPClientSocket.close()
