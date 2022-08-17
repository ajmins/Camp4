import socket
import json
phoneNumbers = {}

def add(args):
    name = args['name']
    phoneNumber = args['phn']
    phoneNumbers[name] = phoneNumber 
    msg = json.dumps({"status" : "Contact added successfully",
    "value" :None})
    return msg
    

def list():
    value = ""
    for i,x in enumerate(phoneNumbers):
        value += "\n{}. Name: {}\nPhonenumber: {}".format(i+1,x,phoneNumbers[x])
    msg = json.dumps({"status" : "Found Contacts",
    "value" :value})
    return msg
    
def delete(args):
    nameToBeDeleted = args['name']
    if nameToBeDeleted in phoneNumbers.keys():
        del phoneNumbers[nameToBeDeleted]
        status = "Number Deleted!"
    else: 
        status = "Name not found"
    msg = json.dumps({"status" : status,
    "value" :None})
    return msg

def searchByName(args):
    name = args['name']
    if name in phoneNumbers.keys():
        status = "Name found"
        value = "Name: {}\nPhone Number: {}".format(name,phoneNumbers[name])
    else:
        status = "Name not found"
        value = None
    msg = json.dumps({"status" : status,
    "value" :value})
    return msg


def searchbyNumber(args):
    phn = args['phn']
    if phn in phoneNumbers.values():
        for name,phn_number in phoneNumbers.items():
            if phn_number == phn:
                status = "Name found"
                value = "Name : {}\nPhone Number: {}".format(name,phn_number)
    else:
        status = "Phone number not found"
        value = None
    msg = json.dumps({"status" : status,
    "value" :value})
    return msg

def actionToSelectedOption(ch, args):
    global msg
    msg = ""
    match(ch):
        case 1: msg = list()
        case 2: msg =  add(args)
        case 3: msg = delete(args)
        case 4: msg = searchByName(args)
        case 5: msg = searchbyNumber(args)
        case 6: msg = exit()
        case _: msg =print("Wrong choice")
    return msg   

def handlerequest(jsonString):
    message = json.loads(jsonString)
    msg = actionToSelectedOption(message["ch"],message["args"],)
    return msg

    
def server_program():
    host = socket.gethostname() # getting the ip of host
    port = 5000
    server_socket = socket.socket()
    server_socket.bind((host,port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection accepted from " + str(address))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("Message from client" + str(address) + " -> " + str(data))
        msg = handlerequest(str(data))
        conn.send(msg.encode())
    conn.close()

if __name__ == '__main__':
    server_program()