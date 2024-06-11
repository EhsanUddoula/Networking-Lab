import socket
import threading
import time
import os
import csv
from csv import DictReader

ENCODER='utf-8'
TLD=("localhost",8002)

fieldname=["name","value","type","ttl"]

domain=[
    {
        "name":"www.google.com",
        "value":"201.123.21.12",
        "type": "A",
        "ttl": "86400"
    },
    {
        "name":"www.facebook.com",
        "value":"102.65.28.9",
        "type": "A",
        "ttl": "86400"
    },
    {
        "name":"www.cs.du.ac.bd",
        "value":"100.100.100.100",
        "type": "A",
        "ttl": "86400"
    }
]

def handle_client(data,addr,server_socket):
    print(data)
    dict={
        "name":data,
        "value":"101.100.100.100",
        "type": "A",
        "ttl": "86400"
    }
    domain.append(dict)
    with open ("cache.csv", "w") as file:
        writer=csv.DictWriter(file, fieldnames=fieldname)
        writer.writeheader()
        writer.writerows(domain)
    flag=0
    with open("cache.csv", "r") as file:
        dict_read=DictReader(file)
        csvFile=list(dict_read)
    for line in csvFile:
        if line['name']==data :
            if line['type']=='A' or line['type']=='AAAA':
                response='1 '+data+' '+line['value']+' '+line['ttl']
                flag=1
                server_socket.sendto(response.encode(ENCODER),addr)
                break
            else:
                
                break
    if flag==0:
        response='0 '+TLD[0]+' '+str(TLD[1])
        server_socket.sendto(response.encode(ENCODER),addr)
    print(f"Disconnected with {addr[0]}: {addr[1]}")

def checkcache():
   
    with open("cache.csv", "r") as file:
        csvFile=csv.reader(file)
        for line in csvFile:
            print(line)


def main():
    HOST='localhost'
    PORT=8001
    ADDR=(HOST,PORT)
    server_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(ADDR)
    print("Server is starting...")
    print(f"Server is listening on {HOST} : {PORT}")
    print("Cached data-")
    for i in domain:
        print(f"Name- {i['name']}  Value- {i['value']}")

    try:
        while True:
            data, addr= server_socket.recvfrom(1024)
            data=data.decode(ENCODER)
            print(f"Connecting with {addr[0]}: {addr[1]}")
            t=threading.Thread(target=handle_client, args=(data,addr,server_socket))
            t.start()
            response=input("Enter 'data' to see cached data\n")
            if response=='data':
                checkcache()
            #handle_client(data,addr,server_socket)
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")

if __name__== '__main__':
    main()