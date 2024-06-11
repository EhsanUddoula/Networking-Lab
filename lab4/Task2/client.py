import socket

ENCODER='utf-8'

def main():
    client_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message= input("Enter domain name:\n")
    flag=0
    HOST='192.168.0.104'
    PORT=8001
    ADDR=(HOST,PORT)
    while True:

        client_socket.sendto(message.encode(ENCODER),ADDR)

        response,addr= client_socket.recvfrom(1024)
        response=response.decode(ENCODER)
        # print(response)
        response=response.split(" ")
        flag=response[0]
        if flag=='0':
            HOST=response[1]
            PORT=int(response[2])
            ADDR=(HOST,PORT)
        elif flag=='1':
            name=response[1]
            value=response[2]
            ttl=response[3]
            print("Response from the server...")
            print(f"Domain- {name}\nIP- {value}\nttl-{ttl}")
            break
        else:
            print("Some error occured...")
            break

if __name__== '__main__':
    main()
