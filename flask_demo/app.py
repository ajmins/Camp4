#importing Flask class from Flask library
from flask import Flask, redirect, url_for,request,jsonify,abort
import requests

#creating an application instance 
#the argument for the construtor is the main module name
#main module name will be there in the dunder __name__
app = Flask(__name__)

#(to define a route in flask, use app.route decorator
# app is our flask applictaion obj
# '/' is the root of the webiste, like the default index.html
# greet function will be executed when accessing default route
# if just type local host these will be executed)
@app.route('/')
def greet():
    return "Have a good day!"

#(another route  if local host hello
# use same decorator name and function name as convention)
@app.route('/hello')
def hello():
    return '<h1>Hello World!!</h1>'
    
"""
#(new route with variables)
@app.route('/user/<name>')
def user(name):
    return f'<h1>Hi {name} <br> Hello World!!!</h1>'
"""

#(demonstrate dynamic URL building)
@app.route('/admin')
def welcome_admin():
    return f'<h2>Welcome admin</h2>'

@app.route('/guest/<guest>')
def hello_guest(guest):
    return f'<h1>Hello {guest} <br> You are our guest!!!</h1>'
#(dynamically redirect to the routes based on the user name)
@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':
        return redirect(url_for('welcome_admin'))
    else:
        return redirect(url_for('hello_guest',guest = name))
"""
#(Form 
# for post method: import request object)
@app.route('/myloginpost',methods=['GET','POST'])
def myloginpost():
    username = request.form['username']
    password = request.form['password']
    if username == 'ajmi' and password == 'ajmipass':
        return f"Welcome {username}"
    else:
        return f"Username/password is not valid"

#in html method is post
"""
#(Form 
# for get method: import request.args.get object)
#in html method is get
@app.route('/myloginget',methods=['GET'])
def myloginget():
    username = request.args.get('username')
    password = request.args.get('password')
    if username == 'ajmi' and password == 'ajmipass':
        return f"Welcome {username}"
    else:
        return f"Username/password is not valid"


#(list of dictionaries for demonstrating REST aPI methods
# 'id field should be id itself becz there is a built-in function which process it)
books = [{'id':1,'title':"Harry Potter", 'author':"JK Rowling"},
        {'id':2,'title':"Jungle Book", 'author':"Rudyard Kipling"},
        {'id':3,'title':"Alice In Wonderland", 'author':"Lewis Carroll"}]

#GET request to get the data in json format
@app.route('/books',methods=['GET'])
def get_books():
    #jsonify will convert list/dict to json format
    return jsonify({'books':books})

#GET request to get the  a particular data in json format
#typecasting string to integer
@app.route('/books/<int:book_id>',methods=['GET'])
def get_book(book_id):
    #list comprehension, iterate through a list and obtain a sublist
    book = [book for book in books if book['id']==book_id]
    if len(book) == 0:#no book is found
        abort(404)
    return jsonify({'books':book[0]})

#POST request to save the data in json format
#input details from user in json format
#so need to check valid json or not
@app.route('/books',methods=['POST'])
def create_book():
    #checking if the received string is valid json
    if not request.json:
        abort(400) #400 means its a bad request
    #create a new book as a dict item which can be inserted into the list
    #the 'id' will be the next id number, use negative index for last item
    book = {'id':books[-1]['id']+1,
    'title':request.json['title'],
    'author':request.json['author']}
    #append the new item into the books list
    books.append(book)
    #jsonify will convert list/dict to json format
    return jsonify({'book':book}),201

#PUT request to edit the particular data in json format
#typecasting string to integer
@app.route('/books/<int:book_id>',methods=['PUT'])
def update_book(book_id):
    #list comprehension, iterate through a list and obtain a sublist
    book = [book for book in books if book['id']==book_id]
    if len(book) == 0:#no book is found
        abort(404)
    #checking if the json from the client has valid title, author keys
    if 'title' in request.json and type(request.json['title'])!=str:
        abort(400)
    if 'author' in request.json and type(request.json['author'])!=str:
        abort(400)

    book[0]['title'] = request.json['title']
    book[0]['author'] = request.json['author']

    #return the updated book
    return jsonify({'books':book[0]})


#DELETE request to remove a particular data in json format
#typecasting string to integer
@app.route('/books/<int:book_id>',methods=['DELETE'])
def delete_book(book_id):
    #list comprehension, iterate through a list and obtain a sublist
    book = [book for book in books if book['id']==book_id]
    if len(book) == 0:#no book is found
        abort(404)
    #remove that item from the books list
    books.remove(book[0])
    return jsonify({'status':'deleted'}),201


#install a module called requests to send the API request
#using the command pip install requests
#defining the aPI URL
API_URL = ('https://api.genderize.io/?name={}')

#create a new function for sending the API request to the url
def send_api(name):
    print(API_URL)
    #trying to send the api request using requests.get() method
    try:
        data = requests.get(API_URL.format(name)).json()
    except Exception as exec:
        print(exec)
        data = None
    return data

#if we're using browser, the default http method will be GET
#router to access the function send_api
@app.route('/gender/<name>')
def gender(name):
    #call send_api and pass the name and receive the response
    response = send_api(name)
    return_text = "your name "+ response["name"]+" is "+response["gender"]
    return return_text






#last line of the code
#check if its the main module, then run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True) 
    #0.0.0.0.0 denotes local host; development mode -> debug = true