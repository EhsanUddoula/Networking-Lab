import socket
import threading
import os

ENCODER='utf-8'
TLD=("192.168.0.104",8002)

domain=[
    {
        "name":"www.google.com",
        "value":"ns.google.com",
        "type": "NS",
        "ttl": "86400"
    },
    {
        "name":"www.facebook.com",
        "value":"102.65.28.9",
        "type": "A",
        "ttl": "86400"
    },
    {
        "name":"www.keil.com",
        "value":"ns.keil.com",
        "type": "NS",
        "ttl": "86400"
    },
    {
        "name":"www.cs.du.ac.bd",
        "value":"ns.cs.du.ac.com",
        "type": "MX",
        "ttl": "86400"
    }
]

def handle_client(data,addr,server_socket):
    print(data)
    flag=0
    for line in domain:
        if line['name']==data :
            if line['type']=='A' or line['type']=='AAAA':
                response=data+' '+line['value']+' '+line['ttl']
                flag=1
                server_socket.sendto(response.encode(ENCODER),addr)
            else:
                server_socket.sendto(data.encode(ENCODER),TLD)
                flag=1
                dat,cur=server_socket.recvfrom(1024)
                server_socket.sendto(dat,addr)
            
            break
    if flag==0:
        server_socket.sendto("Error Occured...Could not find data...".encode(ENCODER),addr)
    print(f"Disconnected with {addr[0]}: {addr[1]}")

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
            # t=threading.Thread(target=handle_client, args=(data,addr,server_socket))
            # t.start()
            handle_client(data,addr,server_socket)
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")

if __name__== '__main__':
    main()