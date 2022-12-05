import socket

client_socket = socket.socket()
port = 12345
client_socket.connect(('127.0.0.1',port))



    #recieve connection message from server
recv_msg = client_socket.recv(1024)
print (recv_msg)
    ## server sends the prompt to authenticate


    #send user details to server
send_msg = input("Enter your user name(prefix with #):")
print(send_msg)
client_socket.send(send_msg.encode())




    #tell the user we want to talk to, check from idle list
while True:
    recv_msg = client_socket.recv(1024)

    msg_2=recv_msg.decode()
    print (msg_2) #list with idle and busy
    send_msg = input("enter user you want to talk to ")
    byt2=send_msg.encode()

    print(byt2)
    client_socket.send(byt2)
    recv_msg_user_with_id = client_socket.recv(10240)
    msg3=recv_msg_user_with_id.decode()
    print(msg3)

    ack="received port id of user"
    client_socket.send(ack.encode())



client_socket.close()

#receive and send message from/to different user/s
'''
while True:
    recv_msg = client_socket.recv(1024)
    msg_2=recv_msg.decode()
    print (msg_2)
    send_msg = input("Send your message in format [@user:message] ")
    byt2=send_msg.encode()
    #print(byt2)
    if send_msg == 'exit':
        break;
    else:
        client_socket.send(byt2)
'''

