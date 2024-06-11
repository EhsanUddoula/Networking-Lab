import socket
import os
import random

HOST="localhost"
PORT=8000
ENCODER="utf-8"


def extract(packet):
    packet=packet.decode(ENCODER)
    seq_num=packet[12:18]
    recv_window=packet[24:30]
    return (int(seq_num),int(recv_window))

def make_packet(ack,rwnd):
    header=f"{ack:06d}{rwnd:06d}"
    header=header.encode(ENCODER)
    return header

def main():
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((HOST,PORT))
    print("Connected with sever...")

    file = open("recieve_file.txt","wb")
    seq_num=0
    rwnd=900
    while True: 
        try:
            packet=client_socket.recv(1024)
        except:
            print("Did not revieve file")
            break
        

        if packet.decode(ENCODER)=="<END>":
            break
        else:
            recv_seq_num,recv_win_num=extract(packet)
            payload=packet[30:]

        rd=random.randint(1,10)

        if rd<3:
            print("Out of order...")
            ack=seq_num
            header=make_packet(ack,rwnd)
            client_socket.send(header)
        
        elif recv_seq_num==seq_num :
            print(f"sequence number-{recv_seq_num}, recieved window-{recv_win_num}, payload-{len(payload)}")
            #print(payload)
            file.write(payload)
            seq_num=seq_num+len(payload)
            rd=random.randint(1,6)
            if rd==1:
                rwnd=500
            elif rd==2:
                rwnd=600
            elif rd==3:
                rwnd=300
            else:
                rwnd=900
            ack=seq_num
            header=make_packet(ack,rwnd)
            client_socket.send(header)
        else:
            print("Out of order...")
            ack=seq_num
            header=make_packet(ack,rwnd)
            client_socket.send(header)

    file.close()
    client_socket.close()
    print("Done...")
            

    


if __name__=="__main__":
    main()