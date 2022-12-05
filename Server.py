import socket,select,sys

port = 12345
socket_list = []
users = {}
users_status_dictionary={"dummy":"idle"}
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

 

server_socket.bind(('',port)) # chekc
server_socket.listen(5)
socket_list.append(server_socket)


while True:
    ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0)

    for sock in ready_to_read:
        if sock == server_socket:
            connect, addr = server_socket.accept()
            socket_list.append(connect)
            str1="You are connected to server:" + str(addr) +"pls enter the username and authenticate"
            connect.send(str1.encode())
        else:
            try:
                print("server_else_block")
                data = sock.recv(2048).decode()
                print(data)

                if data.startswith("#"):

                    ## let's put the auth protocol patch here, if it's authenticated send below msg, else send failed

                    auth=1 #for now assume auth is 1

                    if auth==1:
                        users[data[1:].lower()]=connect
                        users_status_dictionary[data[1:].lower()]='idle'

                        print(users) 
                        print(users_status_dictionary)
                        print ("User " + data[1:] +" added.")

                        #read from dictionary
                        str_dict=" "
                        print(str_dict)
                        for key, value in users_status_dictionary.items() :
                            str_dict=str_dict + key + ":" +value
                        print(str_dict)

                        str_list= "List of users with status" + str_dict
                        
                        
                        str2="Your user detail saved as : "+str(data[1:] + "list of user online with status" +str_list +"now send client you want to talk to")
                        connect.send(str2.encode())


                elif data.startswith("t"):
                    users_status_dictionary[data[1:].lower()]='busy'
                    print(socket_list)
                    
                    #broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)

                    str3=data[data.index(':')+1:]
                    print("str3=",str3)

                    test=users.get(str3)
                    print(test)
                    peer_name=str(test.getpeername())
                    print(peer_name)
                    data_to_send=users.get(str3)
                    print("data_h=",data_to_send)


                    #str3 has name of client the sender of socket data wants to speak to
                    #send back the port id, so that client1 can talk to requested client
                    #connect.send(data_to_send.encode())
                    connect.send(peer_name.encode())
                    


                    #users[data[1:data.index(':')].lower()].send(str3.encode())
            except:
                continue


server_socket.close()

 



'''
print(users)
            print(type(users))

            str_set="names:"
            for key, value in users.items() :
                str_set+=key
             
            print(str_set)

            str2= "List of users" + str_set
            str3=str1+str2

        # for communication
            elif data.startswith("@"):
                    str3=data[data.index(':')+1:]
                    users[data[1:data.index(':')].lower()].send(str3.encode())
           
'''

# check github
# agin tried new add
#this time 7:22
##7:24
#7.25 ti
#7:32
#7:34