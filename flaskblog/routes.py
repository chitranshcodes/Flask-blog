from flask import render_template, url_for, flash, redirect 
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app, db,bcrypt

posts=[
{
    "title":"First Post",
    "author":"Chitransh Gaur",
    "Date_Posted":"19/01/25",
    "content":"aise hi likh rha hu ainwaiyyn"
},
{
    "title":"Second Post",
    "author":"Chitransh Gaur",
    "Date_Posted":"23/01/25",
    "content":"M hu dunia ka PAPA"
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
        hashed_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! Please Login','success')
        return redirect(url_for('login'))
    return render_template("register.html",title="RegistrationPage", form=form)

@app.route("/LoginPage",methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        
        if form.email.data=='xyz@gmail.com' and form.password.data=='password':
            flash('You have been successfully logged in !','success')
            return redirect(url_for('home'))
    return render_template("login.html",title="LoginPage", form=form)