import socket

HOST=socket.gethostbyname(socket.gethostname())
PORT=12345
ENCODER="utf-8"

client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))

message=client_socket.recv(1024).decode(ENCODER)

print(message)

while True:
    print("1.Check Prime\n2.Check Palindrome")
    message=input("Enter option : 1 or 2\n Type quit to quit ")
    if message=="quit":
        client_socket.send("quit".encode(ENCODER))
        print("\nEnding...")
        break
    else:
        client_socket.send(message.encode(ENCODER))
        if message=='1':
            msg=input("Input your number: ")
            if msg=="quit":
                client_socket.send("quit".encode(ENCODER))
                print("\nEnding...")
                break
            client_socket.send(msg.encode(ENCODER))
            print("\nPrime check : "+client_socket.recv(1024).decode(ENCODER))
            print()
            print("........")

        elif message=='2':
            msg=input("Input your text: ")
            if msg=="quit":
                client_socket.send("quit".encode(ENCODER))
                print("\nEnding...")
                break
            client_socket.send(msg.encode(ENCODER))
            print("\nPalindrome check : "+client_socket.recv(1024).decode(ENCODER))
            print()
            print("........")

client_socket.close()