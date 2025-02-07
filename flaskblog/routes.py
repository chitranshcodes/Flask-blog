from flask import render_template, url_for, flash, redirect 
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app, db,bcrypt
from flask_login import login_user, current_user, logout_user

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Check username and password!', 'danger')

    return render_template("login.html",title="LoginPage", form=form)

@app.route("/Logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/Profile")
def Profile():
    return render_template("Profile.html",title="Your Profile")