from datetime import datetime
from flask import Flask,render_template, url_for, flash, redirect 
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app=Flask(__name__)

app.config["SECRET_KEY"]="d7d187b1cd34edb71bbe5038d34e90ff"
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'

db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), nullable=False, unique=True)
    email=db.Column(db.String(100), nullable=False, unique=True)
    password= db.Column(db.String(60), nullable=False)
    img=db.Column(db.String(20), nullable=False, default='default.jpg')
    posts=db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}, {self.email}, {self.img}')"

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    Date_Posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content=db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post({self.title}, {self.Date_Posted})"


posts=[
{
    "title":"First Post",
    "author":"Chitransh Gaur",
    "Date_Posted":"19/01/25",
    "content":"aise hi likh rha hu ainwaiyyn"
}

]
@app.route('/')
def welcome():
    return render_template('welcome.html')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts, title='Home')

@app.route('/about')
def about():
    return render_template("about.html", title="About")

@app.route("/RegistrationPage",methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template("register.html",title="RegistrationPage", form=form)

@app.route("/LoginPage",methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if form.email.data=='xyz@gmail.com' and form.password.data=='password':
            flash('You have been successfully logged in !','success')
            return redirect(url_for('home'))
    return render_template("login.html",title="LoginPage", form=form)

if __name__=="__main__":
    app.run(debug=True)