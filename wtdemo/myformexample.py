from flask import Flask

app = Flask(__name__)

#including a secret key for preventing CSRF attacks in the app.config
#app.config is a dictionary stores all these configurations
app.config['SECRET_KEY'] = 'secret string'