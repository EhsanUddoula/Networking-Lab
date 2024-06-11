import socket

HOST=socket.gethostbyname(socket.gethostname())
PORT=12345
ENCODER="utf-8"


server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((HOST,PORT))

server_socket.listen(2)

print("Server is connected...")

client,addr=server_socket.accept()
client.send("You are connected...".encode(ENCODER))

while True:

    message=client.recv(1024).decode(ENCODER)
    if message=="quit":
        print("\nEnding...")
        break
    else:
        print("Converting to lower case: "+message.lower())
        client.send(message.lower().encode(ENCODER))

server_socket.close()