import socket
import rsa

bytes_to_send = str.encode("Hello UDP Server")
HOST = socket.gethostbyname(socket.gethostname())
PORT = 4444
ADDR = (HOST, PORT)
bufferSize = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


def gen_rsa_key(id):
    (public_key, private_key) = rsa.newkeys(1024)
    with open(f'keys/{id}public.pem', 'wb') as p:
        p.write(public_key.save_pkcs1('PEM'))

    return (f'keys/{id}public.pem', private_key)

# Send to server using created UDP socket


# 1.    #send username to authenticate
username = input("Enter your user name:")
# generate rsa_key with and share the public key path with server
public_key, private_key = gen_rsa_key(username)


path_for_public_key_username = username + "," + public_key
# client_socket.send(send_msg.encode())
UDPClientSocket.sendto(path_for_public_key_username.encode(), ADDR)


##auth reply received back- has encrypted nonce 
msg_for_auth = UDPClientSocket.recvfrom(bufferSize)
# msg_for_auth_decoded = msg_for_auth


print(f" msg_for_auth {msg_for_auth}")




decrypted_nonce_auth = rsa.decrypt(msg_for_auth[0], private_key)
# print("Decrypted message: ", decrypted_nonce_auth)
decrypted_nonce_auth = 'AUTH,' + str(decrypted_nonce_auth)
print("Decrypted message: ", decrypted_nonce_auth)
UDPClientSocket.sendto(decrypted_nonce_auth.encode(), ADDR)



# msg received has list of clients with state
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg_status = "Message from Server {}".format(msgFromServer[0].decode())
print(msg_status)

#to check idle counts
# check if no one is idle, if yes then make the client in receiving mode
text,dict_status=msgFromServer[0].decode().split('!')
print(dict_status)



import json

json_acceptable_string = dict_status.replace("'", "\"")
d = json.loads(json_acceptable_string)




no_of_idle=0
for key, val in d.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
    if val =='idle':
        no_of_idle=no_of_idle+1

print(no_of_idle)




if(no_of_idle==1):
    #listen mode
    # for alice, return thing is none,
  
        while True:

            # 2. msg received from client
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            msg1 = "Message from other client {}".format(msgFromServer[0])
            print(msg1)

            # 1.#send welcome msg to other user
            send_msg = input("msg to send to requested user")
            print(send_msg)
            # client_socket.send(send_msg.encode())
            msg_sent = send_msg.encode()
            UDPClientSocket.sendto(msg_sent, msgFromServer[1])

            #send_msg = input("if you want to end type exit ")
            if (send_msg == 'exit'):
                break

        



else:
        # 2.    #send msg to server, username
    send_msg = input("enter user you want to talk to ")
    to_talk = send_msg.encode()
    UDPClientSocket.sendto(to_talk, ADDR)


    # 2msg received status + client ip and port
    msgFromServer_status = UDPClientSocket.recvfrom(bufferSize)
    msg2 = "Message from Server {}".format(msgFromServer_status[0].decode())
    msg_addr_server = msgFromServer_status[1]
    print("status=",msg2)


    # msg received has client ip and port
    msgFromServer_ip = UDPClientSocket.recvfrom(bufferSize)
    msg2 = "Message from Server {}".format(msgFromServer_ip[0].decode())
    msg_addr_server = msgFromServer_ip[1]
    print(msg2)
    # print(msg_addr_server)


    addr_client = msgFromServer_ip[0]
    print(addr_client)
    print(addr_client.decode())

    print(msg2)
    print(type(addr_client))
    print(type(addr_client.decode()))




    while True:

        udp_ip = socket.gethostbyname(socket.gethostname())
        addr_client_decoded = addr_client.decode()
        udp_port = addr_client_decoded[addr_client_decoded.index(',')+1:-1]
        print(udp_port)
        udp_port_int = int(udp_port)
    # 1.#send welcome msg to other user
        send_msg = input("msg to send to requested user")
        print(send_msg)
        # client_socket.send(send_msg.encode())
        msg_sent = send_msg.encode()
        UDPClientSocket.sendto(msg_sent, (udp_ip, udp_port_int))

    # 2. msg received from client
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg1 = "Message from Server {}".format(msgFromServer[0])
        print(msg1)

        #send_msg = input("if you want to end type exit ")
        if (send_msg == 'exit'):
            break

    UDPClientSocket.close()


# UDPClientSocket.close()
