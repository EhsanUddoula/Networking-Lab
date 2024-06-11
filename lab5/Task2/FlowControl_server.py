import socket
import os
import threading
import time

HOST="localhost"
PORT=8000
ENCODER="utf-8"
stack=[]
ack=0
stop_thread=False
rwnd=900

def make_packet(src_port,dest_port,seq_num,ack,payload,recv_window):
    header=f"{src_port:06d}{dest_port:06d}{seq_num:06d}{ack:06d}{recv_window:06d}"
    header=header.encode(ENCODER)
    packet=header+payload
    return packet

def extract(message):
    ack=message[0:6]
    rwnd=message[6:12]
    return(int(ack),int(rwnd))

def send(client,addr):
    global stack
    global ack
    global rwnd

    seq_num=0
    recv_window=900
    src_port=PORT
    dest_port=addr[1]
    acki=0
    file=open("sent_file.txt","rb")
    file_size=os.path.getsize("sent_file.txt")
    print("file size-",file_size)
    rec=0
    #Timeout is 2 second
    timeout=2

    base=0
    size=(int)(file_size/recv_window)
    win_size=min(5,size)*recv_window

    #Creating receiving thread
    newthread=threading.Thread(target=recieve,args=(client,))
    newthread.start()
    st=time.time()
    while True:
        if base>=file_size:
            break

        #Always seek from acknowledgement number
        file.seek(rec)
        while seq_num<win_size:
            payload=file.read(recv_window)
            if not payload:
                break
            print("file sent from bytes",seq_num)
            packet=make_packet(src_port,dest_port,seq_num,acki,payload,recv_window)
            client.send(packet)
            seq_num+=recv_window
            time.sleep(0.001)
        start=time.time()

        #Is it Timeout
        while time.time()-start<= timeout:
            if stack[-1]==seq_num:
                break
        
        if time.time()-start > timeout:
            print("TIMEOUT!")
    
        print("Recieved Cumulative Acknowledgement-",stack[-1])

        #Getting acknowledgement number and window size for flow control
        rec=stack[-1]
        recv_window=rwnd
        print("Window size", recv_window)
        win_size=rec+5*recv_window
        win_size=min(win_size,file_size)
        base=rec
        seq_num=base
        stack.clear()
        
    client.send(b"<END>")

    file.close()

    print(f"Disconnecting from {addr[0]} : {addr[1]}")
    ed=time.time()
    Throughput=file_size/(ed-st)
    print("Throughput-",Throughput,"B/s")
    stop_thread=True
    

def recieve(client):
    global stack
    global ack
    global rwnd

    try:
        while True:
            if stop_thread==True:
                break
            message=client.recv(1024).decode(ENCODER)
            ack,rwnd=extract(message)
            stack.append(ack)
    except:
        print("Recieve section closed...")


def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))

    server_socket.listen()

    print("Server has started...")

    try:
        client, addr = server_socket.accept()
        print(f"Server is connected to {addr[0]} : {addr[1]}")
        send(client,addr)
        
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
        
    
    server_socket.close()
    print("Server closed...")

if __name__=="__main__":
    main()