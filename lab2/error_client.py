import socket
import random as rd 
import time


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
pack=0
start_time=time.time()
while True:
    if pack==100:
        break
    queryType=rd.randint(1,3)
    print("query type",queryType)
    client_socket.send(str(queryType).encode(ENCODER))
    check=client_socket.recv(1024).decode(ENCODER)
    if check==SUCCESSFUL:
        pack+=1
        if queryType==1:
            print("Balance :"+client_socket.recv(1024).decode(ENCODER))
        elif queryType==2:
            money='5'
            client_socket.send(money.encode(ENCODER))
            chk=client_socket.recv(1024).decode(ENCODER)
            print(chk)
        elif queryType==3:
            money='5'
            client_socket.send(money.encode(ENCODER))
            chk=client_socket.recv(1024).decode(ENCODER)
            print(chk)
    else :
        time.sleep(0.01)
        continue


client_socket.send("quit".encode(ENCODER))
end_time=time.time()
print(end_time-start_time)

client_socket.close()
