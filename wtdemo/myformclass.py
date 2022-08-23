from unicodedata import name
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#creating the form class inheriting from FlaskForm
class NameForm(FlaskForm):
    name = StringField("Enter your name",validators=[DataRequired()])
    submit = SubmitField("Submit")  
    #(StringField represents input type text
    # SubmitField represents type submit)