import socket
import os
import threading
import time

HOST="localhost"
PORT=8000
ENCODER="utf-8"

def make_packet(src_port,dest_port,seq_num,ack,payload,recv_window):
    header=f"{src_port:06d}{dest_port:06d}{seq_num:06d}{ack:06d}{recv_window:06d}"
    header=header.encode(ENCODER)
    packet=header+payload
    return packet

def extract():
    pass

def threaded(client,addr):
    recv_window=900
    seq_num=0
    src_port=PORT
    dest_port=addr[1]
    acki=0
    file=open("sent_file.txt","rb")
    file_size=os.path.getsize("sent_file.txt")
    print("file size-",file_size)
    rec=0
    file.seek(0)
    payload =file.read(900)
    packet=make_packet(src_port,dest_port,seq_num,acki,payload,recv_window)
    client.send(packet)
    st=time.time()
    print("file sent from bytes...",rec)

    while True:
        ack=client.recv(1024).decode(ENCODER)
        print("Acknowledgement-",ack)
        rec=int(ack)
        
        if int(ack)==seq_num+recv_window:
            file.seek(rec)
            payload =file.read(900)
            seq_num=seq_num+recv_window
            packet=make_packet(src_port,dest_port,seq_num,acki,payload,recv_window)
            if not payload:
                break
            
            client.send(packet)
            print("file sent from bytes...",rec)
        else:
            print("Out of order acknowledgement recieved...",rec)
            file.seek(rec)
            payload =file.read(900)
            seq_num=rec
            packet=make_packet(src_port,dest_port,seq_num,acki,payload,recv_window)
            if not payload:
                break
            
            client.send(packet)
            print("file sent from bytes...",rec)
        
    client.send(b"<END>")

    file.close()

    print(f"Disconnecting from {addr[0]} : {addr[1]}")
    ed=time.time()
    Throughput=file_size/(ed-st)
    print("Throughput-",Throughput,"B/s")

def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))

    server_socket.listen()

    print("Server has started...")

    try:
        while True:
            client, addr = server_socket.accept()
            print(f"Server is connected to {addr[0]} : {addr[1]}")
        
            t = threading.Thread(target=threaded, args=(client,addr))
            t.start()
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
        
    
    server_socket.close()
    print("Server closed...")

if __name__=="__main__":
    main()