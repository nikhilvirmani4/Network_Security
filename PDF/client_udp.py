import socket
import rsa

# check


msgFromClient = "Hello UDP Server"
bytesToSend = str.encode(msgFromClient)
serverAddressPort = ("127.0.0.1", 20001)
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
print(username + " -> ")
print(private_key)
path_for_public_key = username + "," + public_key
# client_socket.send(send_msg.encode())
UDPClientSocket.sendto(path_for_public_key.encode(), serverAddressPort)


# msg received has list of clients with state
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg1 = "Message from Server {}".format(msgFromServer[0].decode())
print(msg1)


# 2.    #send msg to server, username
send_msg = input("enter user you want to talk to ")
to_talk = send_msg.encode()
UDPClientSocket.sendto(to_talk, serverAddressPort)


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


if addr_client.decode() != "None":
    while True:

        udp_ip = "127.0.0.1"
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


# for alice, return thing is none,
if addr_client.decode() == "None":
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

    UDPClientSocket.close()


# UDPClientSocket.close()
