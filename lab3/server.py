import socket
import os
from _thread import *
import threading
import time

ENCODER="utf-8"

def threaded(c,addr):
    file_list= os.listdir()
    send=""
    if len(file_list)==0:
        send += "The server directory is empty"
    else:
        send += "\n".join(f for f in file_list)
    

    c.send(send.encode(ENCODER))

    while True:
    
        file_name=c.recv(1024).decode(ENCODER)
        try:
            file= open(file_name,"rb")
            file_size=os.path.getsize(file_name)
            c.send(f"{str(file_size)}".encode(ENCODER))

            st=time.time()
            data=file.read()
            c.sendall(data)
            c.send(b"<END>")

            file.close()
            stop=time.time()
            print("Finished")
            print("Elapsed:", stop-st)
            print("Disconnected with-",addr[0])
            break
        except:
            c.send("ERROR".encode(ENCODER))
            print("File Not found.")
            continue
    c.close()
    

def main():
    HOST="localhost"
    PORT=12356
    
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))
    server_socket.listen()

    print("Server is running...")

    try:
        while True:
            client,addr=server_socket.accept()
            
            print("Connected to :",addr[0],":",addr[1])
            t = threading.Thread(target=threaded, args=(client,addr))
            t.start()
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
        
    server_socket.close()
    
if __name__ == '__main__':
    main()