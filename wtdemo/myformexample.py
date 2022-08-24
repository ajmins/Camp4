from flask import Flask, render_template
#from a cutom module importing a class
from myformclass import NameForm
app = Flask(__name__)

#including a secret key for preventing CSRF attacks in the app.config
#app.config is a dictionary stores all these configurations
app.config['SECRET_KEY'] = 'secret string'

@app.route('/enquiry',methods = ['GET','POST'])
def enquiry(): #function is called as view function
    #create an instance of the NameForm class from myfromclass(.py)
    form = NameForm()
    name = None
    #checking if all the validators were passed and TtheHE form was submitted
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('enquiry.html', form=form, name=name)





#last line of the code
#check if its the main module, then run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True) 
    #0.0.0.0.0 denotes local host; development mode -> debug = true










