import socket

HOST=socket.gethostbyname(socket.gethostname())
PORT=12345
ENCODER="utf-8"

client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))

message=client_socket.recv(1024).decode(ENCODER)

print(message)

while True:
    message=input("Type anything :")
    if message=="quit":
        client_socket.send("quit".encode(ENCODER))
        print("\nEnding...")
        break
    else:
        client_socket.send(message.encode(ENCODER))
        print("Converting to lower from server: "+client_socket.recv(1024).decode(ENCODER))

client_socket.close()