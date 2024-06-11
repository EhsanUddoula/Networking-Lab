import socket

def main():
    HOST=socket.gethostbyname(socket.gethostname())
    PORT=12345
    ENCODER="utf-8"


    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))

    server_socket.listen(2)

    print("Server is connected...")

    client,addr=server_socket.accept()
    client.send("You are connected...".encode(ENCODER))

    while True:

        message=client.recv(1024).decode(ENCODER)
        if message=="quit":
            print("\nEnding...")
            break
        if(message=='1'):
            msg=client.recv(1024).decode(ENCODER)
            flag=prime(int(msg))
            if flag:
                print("Given Number",msg)
                print("YES prime...")
                client.send("YES prime...".encode(ENCODER))
            else:
                print("Given Number",msg)
                print("NOT prime...")
                client.send("NOT prime...".encode(ENCODER))
        
        else:
            msg=client.recv(1024).decode(ENCODER)
            flag=check_palin(msg)
            if flag:
                print("Given Text",msg)
                print("YES palindrome...")
                client.send("YES palindrome...".encode(ENCODER))
            else:
                print("Given Text",msg)
                print("NOT palindrome...")
                client.send("NOT palindrome...".encode(ENCODER))

    server_socket.close()

def check_palin(st):
    if(st==st[::-1]):
        return True
    else:
        return False
    
def prime(num):
    i=2
    while( i*i<=num):
        if num%i==0:
            return False
        i+=1
        
    return True

main()