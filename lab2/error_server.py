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
        print("You are logged in successfully")
        break

Error=0
while True:
    message=client.recv(1024).decode(ENCODER)
    num=rd.randint(1,10)
    if message=="quit":
        print("Ending...")
        break
    if num<=2:
        Error+=1
        print("Package Dropped")
        client.send("404".encode(ENCODER))
    else:
        client.send(SUCCESSFUL.encode(ENCODER))
        print("Successful")
        print(message)
        if message == '1':
            client.send(balance.encode(ENCODER))
        elif message == '2':
            money = client.recv(1024).decode(ENCODER)
            client.send("Credit success...".encode(ENCODER))
            b = int(balance) + int(money)
            balance = str(b)
        elif message =='3':
            money = client.recv(1024).decode(ENCODER)
            if int(money) > int(balance):
                client.send(("Insufficient balance: " + balance).encode(ENCODER))
            else:
                client.send("Debit success...".encode(ENCODER))
                b = int(balance) - int(money)
                balance = str(b)

print(Error)



# Close the server socket outside the loop
server_socket.close()
