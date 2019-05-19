import socket

"""   AF_INET ≡ IPV4 and SOCK_STREAM ≡ TCP   """
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

""" BUFFER: Temporary storage spot for a chunk of data that is transfered to one place to another """
bufferSize = 8
fullMessage = ""

while True:
    messagePortion = s.recv(bufferSize)
    
    if len(messagePortion) <= 0:
        break

    fullMessage += messagePortion.decode("utf-8") 

print(fullMessage)




