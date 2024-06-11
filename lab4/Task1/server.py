import socket
import threading
import os

ENCODER='utf-8'

def handle_client(data,addr,server_socket):
    print(data)
    file= open('dns.txt','r')
    flag="$$$"
    for line in file:
        line= line.split()
        name=line[0]
        value=line[1]
        typ= line[2]
        ttl= line[3]

        if name==data and (typ=='A' or typ=='AAAA') :
            response=data+' '+value+' '+ttl
            flag='1'
            server_socket.sendto(response.encode(ENCODER),addr)
            break
    if flag=="$$$":
        server_socket.sendto(flag.encode(ENCODER),addr)
    print(f"Disconnecting with {addr[0]}: {addr[1]}")

def main():
    HOST='192.168.0.104'
    PORT=8001
    ADDR=(HOST,PORT)
    server_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(ADDR)
    print("Server is starting...")
    print(f"Server is listening on {HOST} : {PORT}")

    try:
        while True:
            data, addr= server_socket.recvfrom(1024)
            data=data.decode(ENCODER)
            print(f"Connecting with {addr[0]}: {addr[1]}")
            t=threading.Thread(target=handle_client, args=(data,addr,server_socket))
            t.start()
            #handle_client(data,addr,server_socket)
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")

if __name__== '__main__':
    main()