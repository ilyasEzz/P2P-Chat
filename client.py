import socket
import select
import errno
import sys

IP = "127.0.0.1"
PORT = 1234
headerSize = 10
myUsername = input("My user name: ")


#   Connection config     
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(( IP, PORT))
clientSocket.setblocking(False)

# Sending user information to the server 
userName = myUsername.encode("utf-8")
usernameHeader = f"{len(userName):>{headerSize}}".encode("utf-8")
clientSocket.send(usernameHeader + userName)


while True:
    message = input(f"{myUsername} > ")
#     Sending messages    """
    if message:
        message = message.encode("utf-8")
        messageHeader = f"{len(message):>{headerSize}}".encode("utf-8")
        clientSocket.send(messageHeader + message)



#     Recieving messages          
    try:
        while True:
            usernameHeader = clientSocket.recv(headerSize)
            if not len(usernameHeader):
                print("Connection closed by the server")
                sys.exit()
            
            """ Decoding the username and the message """
            usernameLength = int(usernameHeader.decode("utf-8").strip())
            username = clientSocket.recv(usernameLength).decode("utf-8")

            messageHeader = clientSocket.recv(headerSize)
            messageLength = int(messageHeader.decode("utf-8").strip())
            message = clientSocket.recv(messageLength).decode("utf-8")

            print(f"{username}> {message} ")


    #     if there is no more message to be recieved  (it's not an error)      
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error: ", str(e))
            sys.exit()
        continue
    

    except Exception as e:
        print("General Error: ", str(e))
        sys.exit()
    