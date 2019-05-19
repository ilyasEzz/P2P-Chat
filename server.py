import socket


"""   AF_INET ≡ IPV4 and SOCK_STREAM ≡ TCP  """
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

IP = socket.gethostname()
PORT = 1234

""" Bind the socket to address. The socket must not already be bound. 
(The format of address depends on the address family)  """
s.bind((IP, PORT))

s.listen(5)


headerSize = 10

while True:
    clientSocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    message = "Welcome to the server!"
    message = f'{len(message):< 10}' + message
    clientSocket.send( bytes("Welcome to the server!", "utf-8") )
    clientSocket.close()
 