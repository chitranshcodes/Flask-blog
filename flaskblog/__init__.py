import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app=Flask(__name__)

app.config["SECRET_KEY"]="d7d187b1cd34edb71bbe5038d34e90ff"
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
LM=LoginManager(app)
LM.login_view='login'
LM.login_message_category='info'

app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('USER_EMAIL')
app.config['MAIL_PASSWORD']=os.environ.get('USER_PASS')

mail=Mail(app)

from flaskblog import routes