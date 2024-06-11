import socket



HOST=socket.gethostbyname(socket.gethostname())
PORT=12555
ENCODER="utf-8"
SUCCESSFUL="200"

client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))

message=client_socket.recv(1024).decode(ENCODER)
print(message)

while True:
    name = input("Type name:")
    password = input("Type password :")


    credentials = f"{name}:{password}"
    client_socket.send(credentials.encode(ENCODER))
    flag = 0

    check = client_socket.recv(1024).decode(ENCODER)
    print(check)
    if check == "i":
        print("Invalid name and password type again!")
    else:
        break
    
        

print("Type the following for:-\n1: check acc balance \n2: to Credit amount \n3: to Debit amount \n4 : to quit")

while True:
    queryType = input("\nQuery- ")
    client_socket.send(queryType.encode(ENCODER))
    if queryType=="4":
        print("Ending")
        break
    if queryType=="1":
        print("Balance :"+client_socket.recv(1024).decode(ENCODER))
    elif queryType=="2":
        money=input("Give the money you want to deposit- ")
        client_socket.send(money.encode(ENCODER))
        chk=client_socket.recv(1024).decode(ENCODER)
        print(chk)
    elif queryType=="3":
        money=input("Give the money you want to withdraw- ")
        client_socket.send(money.encode(ENCODER))
        chk=client_socket.recv(1024).decode(ENCODER)
        print(chk)




client_socket.close()
