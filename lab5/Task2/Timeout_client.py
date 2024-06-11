import socket
import os
import random
import time

HOST="localhost"
PORT=8000
ENCODER="utf-8"


def extract(packet):
    packet=packet.decode(ENCODER)
    seq_num=packet[12:18]
    recv_window=packet[24:30]

    return (int(seq_num),int(recv_window))

def main():
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((HOST,PORT))
    print("Connected with sever...")

    try:
        with open("recieve_file.txt","wb") as file:
            seq_num=0
            while True:
                
                try:
                    packet=client_socket.recv(1024)
                except:
                    print("Did not revieve file")
                    break
                

                if packet.decode(ENCODER)=="<END>":
                    break
                recv_seq_num,recv_win_num=extract(packet)
                payload=packet[30:]

                rd=random.randint(1,10)

                if rd<3:
                    print("Creating time out...")
                    time.sleep(1.1)
                    client_socket.send(ack.encode(ENCODER))
                
                elif recv_seq_num==seq_num :
                    print(f"sequence number-{recv_seq_num}, recieved window-{recv_win_num}, payload-{len(payload)}")
                    file.write(payload)
                    seq_num=seq_num+len(payload)
                    ack=str(seq_num)
                    client_socket.send(ack.encode(ENCODER))
                else:
                    print("Out of order...")
                    ack=str(seq_num)
                    client_socket.send(ack.encode(ENCODER))
        client_socket.close()
        print("Done...")
            

    except:
        client_socket.close()
        print("Exception...")
    
        


if __name__=="__main__":
    main()