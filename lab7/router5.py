import socket
import os
import threading
import time
import heapq as heap
from collections import defaultdict
import math
import sys

HOST="localhost"
PORT=8004
ENCODER="utf-8"

curr_node='E'
Graph={}
neighbour=set()
portmap={'A':8000,'B':8001,'C':8002, 'D': 8003, 'E':8004, 'F':8005}
current_nodes=set()
size=6

lock=threading.Lock()
t1=time.time()
msg_ct=0

def start():
    with open('nodes.txt', 'r') as file:
        for line in file:
            src,dest,cost= line.split()

            if src==curr_node or dest==curr_node:
                if src not in Graph:
                    Graph[src]={}
                if dest not in Graph:
                    Graph[dest]={}
                Graph[src][dest]=cost
                Graph[dest][src]=cost
                if dest != curr_node:
                    neighbour.add(dest)
                else:
                    neighbour.add(src)

    print(Graph)
    print(neighbour)
    message=make_packet()
    broadcast(message)
    dijkstra()

def dijkstra():
    parents={}
    visited=set()
    priority_q=[]
    cost=defaultdict(lambda: math.inf)
    cost[curr_node]=0
    heap.heappush(priority_q,(0,curr_node))

    while priority_q:
        pq, node= heap.heappop(priority_q)
        visited.add(node)

        for adj, weight in Graph[node].items():
            if adj in visited:
                continue
            
            newcost=cost[node]+ int(weight)

            if newcost< cost[adj]:
                parents[adj]=node
                cost[adj]= newcost
                heap.heappush(priority_q,(newcost,adj))
    
    print(f"\nCurrent costs to go all routers from this router- {curr_node}\n")

    for i in cost:
        print(f"{i} {cost.get(i)}")

    print("\npath")

    for node in parents:
        path=[]
        dest=node
        while dest != curr_node:
            if dest not in parents:
                print(f"No path from {curr_node} to {dest}")
                break
            path.append(dest)
            dest=parents[dest]
        path.append(curr_node)

        print(f"Shortest path from {curr_node} to {node}: {' -> '.join(reversed(path))}")

    print("Size of memory: " + str(sys.getsizeof(cost)) + "bytes")

def make_packet():
    id= curr_node
    ttl="60"
    #msg=id+" "+ttl+"\n"
    msg=id+"\n"
     
    for adjNode, weight in Graph[curr_node].items():
        msg+=curr_node+" "+str(adjNode)+" "+str(weight)+"%"
    return msg

def extract_packet(message):
    global current_nodes
    global msg_ct

    lock.acquire()
    msg=message
    message=message.split('\n')
    #id, ttl= message[0].split(" ")
    id=message[0]
    #print(id)
    
    if id== curr_node or (id in current_nodes):
        lock.release()
        return
    else:
        broadcast(msg)
        data=message[1].split("%")
        msg_ct+=1

        for line in data:
            try:
                src, dest, weight=line.split()
            except:
                break

            if src not in Graph:
                Graph[src]={}
            if dest not in Graph:
                Graph[dest]={}
            
            Graph[src][dest]=weight
            Graph[dest][src]=weight

        print("\nGraph Updated\n")
        dijkstra()
        current_nodes.add(id)
        if len(current_nodes)==size:
            print('finish')
            print("Time-",time.time()-t1)
            print("Exchanged messeges-",msg_ct)

        lock.release()

def broadcast(message):

    for _ in neighbour:
        ip=HOST
        port=portmap[_]
        neibr=socket.socket()
        try:
            neibr.connect((ip,port))
            neibr.send(message.encode(ENCODER))
        except:
            print(f"{curr_node} couldn't connect with neibour {_} on port {port}")
        neibr.close()

def update_graph():
    global current_nodes
    global t1
    while True:
        lock.acquire()
        current_nodes.clear()
        current_nodes.add(curr_node)
        t1=time.time()
        start()
        lock.release()
        time.sleep(30)


def threaded_client(client,addr):
    data= client.recv(1024).decode(ENCODER)
    extract_packet(data)


def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))

    server_socket.listen()

    print("Server has started...")
    time.sleep(20)

    update_thread=threading.Thread(target=update_graph)
    update_thread.start()
    try:
       while True:
            client, addr = server_socket.accept()
            print(f"Server is connected to {addr[0]} : {addr[1]}")
        
            t = threading.Thread(target=threaded_client, args=(client,addr))
            t.start()
        
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
        
    
    server_socket.close()
    print("Server closed...")

if __name__=="__main__":
    main()