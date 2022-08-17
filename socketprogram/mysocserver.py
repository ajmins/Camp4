import socket #socket module
def server_program():
    host = socket.gethostname() #get the hostname
    port = 5000 #initiate port no above 1024 till 65535
    #HOST = "127.0.0.1" #statndard loopback interface address ( or localhost)
    #PORT = 65432 #port to listen on (non-priveleged ports are > 1024)

    server_socket = socket.socket() #get instance of socket

    server_socket.bind((host,port))
    #bind host address and port together to our instance
    #the bind() function takes  host and port as a tuple as argument
    #configure how many client the server can listen simultaneously, here it's 2
    server_socket.listen(2)
    #the accept method will give back the connection object and ip address of the incoming connection request
    conn, address = server_socket.accept() #accept new connection
    print("Connection from: " + str(address))

    #now we can receive the messages
    #using while loop, keep the connection active and receive msgs until there is none
    #the bind() function takes tuple as argument
    while True:
        #infinite while loop to receive data stream
        #it won't accept the data packet greater than 1024 bytes
        #decode the received data
        data = conn.recv(1024).decode()
        if not data:
            #if data is not received, then break the while loop
            break
            #if valid data we can print the data received
        print("Message from client " + str(address) + " : " + str(data))
        #give provision to send reply back to the clinet
        data = input('Send Reply to client:')
        conn.send(data.encode()) #encode the data and send data to the client
    
    conn.close() #close the connection once the while loop breaks

#this is a convention in python is intended to allow you to write code that can be run directly, or imported
#if our prgrm is imported, the just be there as an imported code and do not run until the user calls the function(default behaviour)
#if we directly running it using the command python [prog.py] then sart the function server_program() automatically
if __name__ == '__main__': 
    server_program()


#output server
"""
python .\mysocserver.py
Connection from: ('192.168.5.172', 62309)
message from client ('192.168.5.172', 62309) : hello server
Send Reply:hsi clint
message from client ('192.168.5.172', 62309) : hello
Send Reply:hows the day?
message from client ('192.168.5.172', 62309) : it's fine here
Send Reply:that's good
message from client ('192.168.5.172', 62309) : how is for u
Send Reply:good and exit
PS C:\Users\Ajmi\Camp4\socketprogram>


"""