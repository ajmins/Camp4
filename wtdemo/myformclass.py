
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#creating the form class inheriting from FlaskForm
class NameForm(FlaskForm):
    #creating object for class StringField and have validators
    name = StringField("Enter your name",validators=[DataRequired()])
    submit = SubmitField("Submit")  
    #(StringField class represents input type text
    # SubmitField class represents input type submit)