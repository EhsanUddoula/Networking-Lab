import socket

HOST='192.168.0.104'
PORT=8001
ADDR=(HOST,PORT)
ENCODER='utf-8'

def main():
    client_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message= input("Enter domain name:\n")

    client_socket.sendto(message.encode(ENCODER),ADDR)

    response,addr= client_socket.recvfrom(1024)
    print("Response from the server...")
    print(response.decode(ENCODER))

if __name__== '__main__':
    main()
