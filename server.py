import socket
import select

"""   AF_INET ≡ IPV4 and SOCK_STREAM ≡ TCP  """
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

IP = "127.0.0.1"
PORT = 1234
headerSize = 10

""" Bind the socket to address. The socket must not already be bound. 
(The format of address depends on the address family)  """
server.bind((IP, PORT))


 #    AllOW us the reconnect 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Anable a server to accept connections the argument is the maximum of connections 
server.listen()


socketsList = [server]

#  a client dictionnary with the client socket as key and the data as value 
clients = {}

def recieveMessage(clientSocket):
    try:
        messageHeader = clientSocket.recv(headerSize)
        # if whe didn't recieve a message header
        if not len(messageHeader):
            return False
        
        messageLength = int(messageHeader.decode("utf-8").strip())
        return {"header": messageHeader, "data": clientSocket.recv(messageLength) }
    
    except:
        return False


while True:
    # we want readSockets -the sockets we recieve data from
    readSockets, _, exceptionSockets = select.select(socketsList, [], socketsList)
    
    for notifiedSocket in readSockets:

        """ If someone connect"""
        if notifiedSocket == server:

            clientSocket, clientAddress = server.accept()
            user = recieveMessage(clientSocket)

            # if the user disconnect the server keep running
            if user is False:
                continue
            
            socketsList.append(clientSocket)
            clients[clientSocket] = user
            print(f"Accepted new connection from {clientAddress[0]}:{clientAddress[1]}, username: {user['data'].decode('utf-8')}")

        # If someone disconnect 
        else:
            message = recieveMessage(notifiedSocket)

            if message is False:
                print(f"Closed connection from {clients[notifiedSocket]['data'].decode('utf-8')}")
                socketsList.remove(notifiedSocket)
                del clients[notifiedSocket]
                continue
            
            user = clients[notifiedSocket]
            print(f"Recieved message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

           #  Sharing the message with everyone 
            for clientSocket in clients:
                if clientSocket is not notifiedSocket:
                    clientSocket.send(user['header'] + user['data'] + message['header'] + message['data'])


            for notifiedSocket in exceptionSockets:
                socketsList.remove(notifiedSocket)
                del clients[notifiedSocket]
             