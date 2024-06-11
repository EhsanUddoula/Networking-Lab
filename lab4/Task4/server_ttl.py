import socket
import threading
import os
import time
import csv
from csv import DictReader

ENCODER='utf-8'
TLD=("localhost",8002)

fieldname=["name","value","type","ttl"]


def handle_client(data,addr,server_socket):
    print(data)
    flag=0
    for line in domain:
        if line['name']==data :
            if line['type']=='A' or line['type']=='AAAA':
                response='1 '+data+' '+line['value']+' '+str(line['ttl'])
                flag=1
                server_socket.sendto(response.encode(ENCODER),addr)
                break
            else:
                
                break
    if flag==0:
        response='0 '+TLD[0]+' '+str(TLD[1])
        server_socket.sendto(response.encode(ENCODER),addr)
    print(f"Disconnected with {addr[0]}: {addr[1]}")

def checkcache(st):
    with open("cache.csv", "r") as file:
        dict_read=DictReader(file)
        csvFile=list(dict_read)
    for i in csvFile:
        ed=time.time()
        if ed-st >= float(i["ttl"]):
            print("time is",ed-st)
            csvFile.remove(i)
    with open ("cache.csv", "w") as file:
        writer=csv.DictWriter(file, fieldnames=fieldname)
        writer.writeheader()
        writer.writerows(csvFile)
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
    st=time.time()
    try:
        while True:
            response=input("Enter 'data' to see cached data\n")
            if response=='data':
                checkcache(st)
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")

if __name__== '__main__':
    main()