import socket
import re
import json

phoneBook = dict()

def add(args):
    name = args['name']
    num = args['num']
    phoneBook[name] = num 
    print("Contact added")
    details = json.dumps({"status" : "Contact added successfully",
    "value" :None})
    return details

def list():
    value = ""
    for i,x in enumerate(phoneBook):
        value += "\n{}. Name: {} Phonenumber: {}".format(i+1,x,phoneBook[x])
    details = json.dumps({"status" : "Found Contact",
    "value" :value})
    return details

def delete(args):
    
    name = args['name']
    if name in phoneBook.keys():
        del phoneBook[name]
        status = "Number Deleted!"
    else: 
        status = "Name not found"
    details = json.dumps({"status" : status,
    "value" :None})
    return details

def searchName(args):
    name = args['name']
    if name in phoneBook.keys():
        status = "Name found"
        value = "Name: {}     Phone Number: {}".format(name,phoneBook[name])
    else:
        status = "Name not found"
    details = json.dumps({"status" : status,
    "value" :value})
    return details

def searchNo(args):
    num = args['phn']
    if num in phoneBook.values():
        for name,phn_number in phoneBook.items():
            if phn_number == num:
                status = "Name found"
                value = "Name : {} Phone Number: {}".format(name,phn_number)
    else:
        status = "Phone number not found"
    details = json.dumps({"status" : status,
    "value" :value})
    return details

def get_userDetails(ch, args):
    global details
    details =""
    if ch == 1:
        details = list()
    elif ch == 2:
        details = add(args)
    elif ch == 3:
        details = delete(args)
    elif ch == 4:
        details = searchName(args)
    elif ch == 5:
        details = searchNo(args)
    elif ch == 6:
        exit()
    else:
        print("Wrong choice")
    return details

def handleRequest(jsonString):
    message = json.loads(jsonString)
    details = get_userDetails(message["ch"],message["args"],)
    return details


def server_program():
    host = socket.gethostname() #get the hostname
    port = 5000 #initiate port no above 1024 till 65535

    server_socket = socket.socket() #get instance of socket

    server_socket.bind((host,port))

    server_socket.listen(2)
    #the accept method will give back the connection object and ip address of the incoming connection request
    conn, address = server_socket.accept() #accept new connection
    print("Connection from: " + str(address))

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
        details = handleRequest(str(data))
        conn.send(details.encode()) #encode the data and send data to the client    
    conn.close() #close the connection once the while loop breaks

if __name__ == '__main__': 
    server_program()
