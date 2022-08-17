import socket
import json

phoneBook = dict()

#to list contacts
def list():
    phoneDetails = {"ch":1, "args":None}

#to add a new contact
def add():
    details = dict()
    name = input("Enter the name of new contact: ")
    num = input("Enter the phone number: ")
    phoneDetails = {"ch":2, "args":{"name":name,"num":num}}
    return phoneDetails

#to remove a contact
def delete():
    name = input("Enter the name of contact to delete: ")
    phoneDetails = {"ch":3, "args":{"name":name}}
    return phoneDetails

#to search a contact by name
def searchName():
    name = input("Enter the name of contact to search: ")
    phoneDetails = {"ch":4, "args":{"name":name}}
    return phoneDetails

#to search a contact by number
def searchNo():
    num = int((input("Enter the phone number to search: ")))
    phoneDetails = {"ch":5, "args":{"num":num}}
    return phoneDetails

def get_userDetails(ch):
    global details
    details =""
    if ch == 1:
        details = list()
    elif ch == 2:
        details = add()
    elif ch == 3:
        details = delete()
    elif ch == 4:
        details = searchName()
    elif ch == 5:
        details = searchNo()
    elif ch == 6:
        exit()
    else:
        print("Wrong choice")
    return json.dumps(details)

def handleReply(detailsString):
    details = json.loads(detailsString)
    print(details['status'])
    if (details['value']):
        print(details['value'])

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
    

    while(True):
        ch =int(input("""
    1.List all contacts
    2.Add a new contact
    3.Delete a contact
    4.Search by name
    5.Search by number
    6.Exit & Disconnect

    Enter the choice: 
    """))
        message = get_userDetails(ch)
        if ch == 6:
            break
        #if the msg is not 'exit', encode and send it to server
        client_socket.send(message.encode())
        #receive any reply from the server
        data = client_socket.recv(1024).decode()
        #printing the received data as text
        handleReply(data)
        #getting the msg to send to the server
        
        
    #close the socket connection once the while loop is exited
    client_socket.close()

if __name__ == '__main__': 
    client_program()   
