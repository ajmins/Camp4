import socket #socket module

def client_program():
    host = socket.gethostname() #get the hostname
    #since both server and client are in the same machine we can get the loopback address as the server addres
    port = 5000 #initiate port no above 1024 till 65535
    #HOST = "127.0.0.1" #statndard loopback interface address ( or localhost)
    #PORT = 65432 #port to listen on (non-priveleged ports are > 1024)
    
    #get instance of socket
    client_socket = socket.socket() 

    #instead of binding, client we are connecting to server
    client_socket.connect((host,port)) #host & port as tuple
    
    #getting the msg to send to the server
    message = input("Enter the msg to send to server: ")

    while message.lower().strip() != 'exit':
        #if the msg is not 'exit', encode and send it to server
        client_socket.send(message.encode())
        #receive any reply from the server
        data = client_socket.recv(1024).decode()
        #printing the received data as text
        print("Received from server: "+data)
        #getting the msg to send to the server
        message = input("Enter the msg as reply to server: ")

    #close the socket connection once the while loop is exited
    client_socket.close()

if __name__ == '__main__': 
    client_program()   


#output client
"""
 python .\mysocclient.py
Enter the msg to send to server: hello server
Receeived from server: hsi clint
Enter the msg as reply to server: hello
Receeived from server: hows the day?
Enter the msg as reply to server: it's fine here
Receeived from server: that's good
Enter the msg as reply to server: how is for u
Receeived from server: good and exit
Enter the msg as reply to server: exit
PS C:\Users\Ajmi\Camp4\socketprogram>
"""