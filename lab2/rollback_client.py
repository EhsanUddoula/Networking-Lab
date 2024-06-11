import socket
import random as rd 
import time


HOST=socket.gethostbyname(socket.gethostname())
PORT=12543
ENCODER="utf-8"
SUCCESSFUL="200"
money="5"

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
    
        

print("Type the following for:-\n1: To debit")
pack=0
start_time=time.time()
while True:
    if pack==100:
        break
    messNdmon=f"{"1"}:{money}"
    client_socket.send(messNdmon.encode(ENCODER))
    client_socket.recv(1024).decode(ENCODER)
    num=rd.randint(1,10)
    if num<=3 :
        client_socket.send("404".encode(ENCODER))
        print("Couldn't withdraw...")
        time.sleep(0.01)
    else:
        client_socket.send(SUCCESSFUL.encode(ENCODER))
        pack+=1
        print("Successfully withdrawn...")

messNdmon=f"{"quit"}:{"0"}"
client_socket.send(messNdmon.encode(ENCODER))
end_time=time.time()
print("Time ",end_time-start_time)

client_socket.close()
