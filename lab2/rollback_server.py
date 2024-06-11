import socket
import random as rd 

HOST = socket.gethostbyname(socket.gethostname())
PORT = 12543
ENCODER = "utf-8"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen(2)

print("Server is connected...")

client, addr = server_socket.accept()
client.send("You are connected...".encode(ENCODER))

ID = "a"
PASSWORD = "123"
balance = "10000"
SUCCESSFUL="200"



while True:
    id_and_password = client.recv(1024).decode(ENCODER)
    id, password = id_and_password.split(':')
    if id != ID or password != PASSWORD:
        client.send("i".encode(ENCODER))
    else: 
        client.send("s".encode(ENCODER))
        print("You are logged in successfully")
        break
Error=0
while True:
    messageAndMoney=client.recv(1024).decode(ENCODER)
    message,money=messageAndMoney.split(':')
    if message=="quit":
        print("Ending...")
        break
    
    elif message =='1':
        if int(money) > int(balance):
            client.send(("Insufficient balance: " + balance).encode(ENCODER))
        else:
            client.send("Debit success in server...".encode(ENCODER))
            b = int(balance) - int(money)
            balance = str(b)
        check=client.recv(1024).decode(ENCODER)
        if check==SUCCESSFUL :
            print("succeed...")
        else:
            b=int(balance)+ int(money)
            balance=str(b)
            Error+=1
            print("Rollback success...")

print(Error)


# Close the server socket outside the loop
server_socket.close()
