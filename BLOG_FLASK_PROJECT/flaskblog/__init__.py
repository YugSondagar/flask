import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = 'bbb37e94471328745c821976a457c0da' # secret key will help us to protect from cookies and attacks
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #/// ye batayega ki database relative path mein store hoga site.db ke naam se
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  #it is the function name of the route
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587  #Port 587 is used for TLS (Transport Layer Security).
app.config['MAIL_USE_TLS'] = True #Enables TLS encryption for secure email transmission.
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')#Retrieves the email username from an environment variable.
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')#Retrieves the email password securely from an environment variable. 
mail = Mail(app) 

from flaskblog import routes

