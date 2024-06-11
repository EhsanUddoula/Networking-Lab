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
duplicate_ack=0

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
    global duplicate_ack

    seq_num=0
    recv_window=200
    src_port=PORT
    dest_port=addr[1]
    acki=0
    mss=1
    ssthresh=8 #Threshold selected to 8 initially
    threshold_flag=0
    file=open("sent_file.txt","rb")
    file_size=os.path.getsize("sent_file.txt")
    print("file size-",file_size)
    rec=0
    #Timeout is 2 second
    timeout=2
    Transmission_Round=1

    base=0
    size=(int)(file_size/recv_window)
    cwnd=min(mss,size)*recv_window
    packet_loss=0

    #Creating receiving thread
    newthread=threading.Thread(target=recieve,args=(client,))
    newthread.start()
    st=time.time()
    while True:
        if base>=file_size:
            break

        #Always seek from acknowledgement number
        file.seek(rec)
        while seq_num<cwnd:
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
            if not stack:
                continue
            if stack[-1]==seq_num:
                break
            elif duplicate_ack>=3:
                ssthresh=mss//2
                mss=ssthresh-1
                threshold_flag=1
                duplicate_ack=0
                break
        
        if time.time()-start > timeout:
            print("TIMEOUT!")
            ssthresh=mss//2
            mss=1
            threshold_flag=0

        elif threshold_flag==1:
            mss+=1
            print("Three duplicate received...First Retransmit...")
        
        elif threshold_flag==0 and mss >= ssthresh:
            print("Exceeded Threshold value...")
            mss+=1

        else:
            mss=mss*2
    
        print("Recieved Cumulative Acknowledgement-",stack[-1])

        #Getting acknowledgement number and window size for flow control
        rec=stack[-1]
        recv_window=rwnd
        print("Window size", recv_window)
        cwnd=rec+mss*recv_window
        packet_loss+=seq_num-rec
        print(f"Congestion window size- {cwnd} mss- {mss} Time taken- {time.time()-st} packet loss- {packet_loss}")
        Transmission_Round+=1
        print("Transmission Round",Transmission_Round)
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
    global duplicate_ack

    last=0

    try:
        while True:
            if stop_thread==True:
                break
            message=client.recv(1024).decode(ENCODER)
            ack,rwnd=extract(message)
            if ack==last:
                duplicate_ack+=1
            else:
                duplicate_ack=0
            last=ack
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