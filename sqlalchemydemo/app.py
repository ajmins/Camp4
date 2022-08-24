from flask import Flask, render_template, request, flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Declaring the connection string or databse uri into the configuration object
#mssql+pyodbc://server/dbname?driver=driver
#mssql+pyodbc://DESKTOP-CJEOG7N\SQLEXPRESS/empdb?driver=SQL+Server+Native+Client+11.0
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-CJEOG7N\SQLEXPRESS/empdb?driver=SQL+Server+Native+Client+11.0'

#track the modifications key to false to optimize memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#SET THE SECRET KEY FOR THE FORMS
app.config['SECRET_KEY'] = 'my secret key'

#instantiate the db object 
db = SQLAlchemy(app)

#create a class for the model. Class name will be table name and attributes will be the columns
class Employees(db.Model):
    id = db.Column('employee_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    salary = db.Column(db.Float(50))    
    age = db.Column(db.String(50))
    
    #define the constructor
    def __init__(self, name, salary, age):
        self.name = name
        self.salary = salary
        self.age = age

#route to list employees
@app.route('/') #default route
def list_employees():
    #return render_template('list.html', Employees=Employees.drop_all())
    return render_template('list.html', Employees=Employees.query.all())

#route to add employees
@app.route('/add', methods=['GET','POST'])
def addEmployees():
    #checking if the form was submitted by post method/by clicking the button
    if request.method =='POST':
        if not request.form['name'] or not request.form['salary'] or not request.form['age']:
            flash('please enter all the fields','error')
            return redirect(url_for('addEmployees'))
        else:
            #if all the variables are set, we will proceed with data adding
            #create an instance of Employees
            employee = Employees(request.form['name'],request.form['salary'],request.form['age'])
            #add the row of data to the Employees Table
            db.session.add(employee)
            db.session.commit()
            return redirect(url_for('list_employees'))
    #if the user is accessing the page directly, give the template add.html
    return render_template('add.html')





#last line of the code
if __name__ == "__main__":
    db.create_all() #create a databse and all tables
    app.run(debug=True)









