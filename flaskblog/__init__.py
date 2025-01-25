from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config["SECRET_KEY"]="d7d187b1cd34edb71bbe5038d34e90ff"
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'

db=SQLAlchemy(app)

from flaskblog import routes