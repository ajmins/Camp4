import functools
import re
import pyodbc

from flask import Flask, jsonify, abort, request
#decorator for dbms connection
def dbms(func):
    @functools.wraps(func)
    def innerWrapper(*args):
        try:
            conn = pyodbc.connect('Driver={SQL Server};'
            'Server=DESKTOP-CJEOG7N\SQLEXPRESS;'
            'Database=Camp2;'
            'Trusted_Connection=yes')
        except:
            print('Connection Error')
            return None
        else:
            curr = conn.cursor()
            value = func(curr, *args)
            conn.commit()
            conn.close()
            return value
    return innerWrapper

@dbms
def searchNo(curr: pyodbc.Cursor, n):
    try:
        curr.execute(
            'SELECT id, name, phone FROM phonebook WHERE Phone=?',
            (n)
        )
    except:
        return None
    else:
        return [{'id': id, 'name': name, 'phone': phone} for id, name, phone in curr.fetchall()]
        
@dbms
def searchName(curr, n):
    try:
        curr.execute(
            'SELECT id, name, phone FROM phonebook WHERE Name LIKE ?',
            (f'%{n}%')
        )
    except:
        return None
    else:
        return [{'id': id, 'name': name, 'phone': phone} for id, name, phone in curr.fetchall()]
        

@dbms
def edit(curr: pyodbc.Cursor, id, name, number):
    try:
        curr.execute(
            'UPDATE phonebook SET Name=?, Phone=? WHERE id=?;',
            (name, number, id)
        )
    except:
        return None
    else:
        curr.execute('SELECT id, Name, Phone FROM phonebook WHERE id=?;', (id))
        return [{'id': id, 'name': name, 'phone': phone} for id, name, phone in curr.fetchall()]

@dbms
def add(curr: pyodbc.Cursor, name, number):
    try:
        curr.execute(
            'INSERT INTO phonebook VALUES (?, ?);',
            (name, number)
        )
    except:
        return None
    else:
        id = curr.execute('SELECT @@IDENTITY AS id;').fetchone()[0]
        curr.execute('SELECT id, Name, Phone FROM phonebook WHERE id=?;', (id))
        return [{'id': id, 'name': name, 'phone': phone} for id, name, phone in curr.fetchall()][0]

@dbms
def delete(curr: pyodbc.Cursor, id):
    try:
        curr.execute(
            'DELETE FROM phonebook WHERE id=?',
            (id)
        )
    except:
        return None
    else:
        return curr.rowcount > 0

@dbms
def sort(curr: pyodbc.Cursor):
    try:
        curr.execute('SELECT id, Name, Phone FROM phonebook ORDER BY Name;')
    except:
        return None
    else:
        return [{'id': id, 'name': name, 'phone': phone} for id, name, phone in curr.fetchall()]

@dbms
def get_one_contact(curr: pyodbc.Cursor, id):
    try:
        curr.execute('SELECT id, Name, Phone FROM phonebook WHERE id=?;', (id))
    except:
        return None
    else:
        return [{'id': id, 'name': name, 'phone': phone} for id, name, phone in curr.fetchall()]


app = Flask(__name__)

@app.route('/contacts')
def list_contacts():
    if request.args.get('name'):
        contacts = searchName(request.args.get('name'))
    elif request.args.get('phone'):
        contacts = searchNo(request.args.get('phone'))
    else:
        contacts = sort()
    if contacts == None:
        abort(500)
    elif len(contacts) == 0:
        return jsonify(), 204
    else:
        return jsonify({'contacts': contacts})

@app.route('/contacts/<int:id>')
def view_contact(id):
    contact = get_one_contact(id)
    if contact == None:
        abort(500)
    elif len(contact) == 0:
        abort(404)
    else:
        return jsonify({'contact': contact[0]})

@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    match delete(id):
        case True: return jsonify({}), 204
        case False: abort(404)
        case _: return abort(500)

@app.route('/contacts', methods=['POST'])
def add_contact():
    name = request.json.get('name')
    phone = request.json.get('phone')
    if name == '' or not re.match(r'\+[0-9]*', phone):
        abort(400)
    res = add(name, phone)
    if not res:
        abort(500)
    return jsonify({'contact': res}), 201

@app.route('/contacts/<int:id>', methods=['PUT'])
def edit_contact(id):
    name = request.json.get('name')
    phone = request.json.get('phone')
    if name == '' or not re.match(r'\+[0-9]*', phone):
        abort(400)
    res = edit(id, name, phone)
    if res == None:
        abort(500)
    elif len(res) == 0:
        abort(404)
    else:
        return jsonify({'contact': res[0]}), 201

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)