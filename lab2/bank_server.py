import socket
import random as rd 

HOST = socket.gethostbyname(socket.gethostname())
PORT = 12555
ENCODER = "utf-8"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen(2)

print("Server is connected...")

client, addr = server_socket.accept()
client.send("You are connected...".encode(ENCODER))

ID = "a"
PASSWORD = "123"
balance = "100"
SUCCESSFUL="200"



while True:
    id_and_password = client.recv(1024).decode(ENCODER)
    id, password = id_and_password.split(':')
    if id != ID or password != PASSWORD:
        client.send("i".encode(ENCODER))
    else: 
        client.send("s".encode(ENCODER))
        print("You are logged in successfully\n")
        break

while True:
    message=client.recv(1024).decode(ENCODER)
    if message=="4":
        print("Ending...")
        break

    if message == '1':
        print(message)
        print("Checking balance")
        client.send(balance.encode(ENCODER))
    elif message == '2':
        print(message)
        money = client.recv(1024).decode(ENCODER)
        print("Credit success...")
        b = int(balance) + int(money)
        balance = str(b)
        client.send(f"Credit success...\nYOUR CURRENT BALANCE- {balance}".encode(ENCODER))
    elif message =='3':
        print(message)
        money = client.recv(1024).decode(ENCODER)
        if int(money) > int(balance):
            client.send(("Insufficient balance: " + balance).encode(ENCODER))
        else:
            b = int(balance) - int(money)
            balance = str(b)
            print("Debit success...")
            client.send(f"Debit success...\nYOUR CURRENT BALANCE- {balance}".encode(ENCODER))




# Close the server socket outside the loop
server_socket.close()
