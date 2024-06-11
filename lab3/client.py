import socket
import os

HOST="localhost"
PORT=12356
ENCODER="utf-8"


client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))

print("Available file list...")
listed=client_socket.recv(1024).decode(ENCODER).split("\n")

for lis in listed:
    print(lis)
while True:
    file=input("What file do you want?\n")
    client_socket.send(file.encode(ENCODER))
    fl=client_socket.recv(1024).decode()

    if fl=="ERROR":
        print("File name Error...")
        print("Type again...")
    else :
        break

file= open("img.jpg","wb")
file_bytes=b""


while True:
    message=client_socket.recv(1024)

    if file_bytes[-5:]==b"<END>":
        print("\nEnding...")
        break
    else:
        file_bytes+=message

file.write(file_bytes)
file.close()

print("File Recieved Successfully...")

client_socket.close()
