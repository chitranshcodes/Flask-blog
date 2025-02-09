import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm, UpdationForm
from flaskblog import app, db,bcrypt
from flask_login import login_user, current_user, logout_user, login_required

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
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Check username and password!', 'danger')

    return render_template("login.html",title="LoginPage", form=form)

@app.route("/Logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/Profile", methods=['GET', 'POST'])
@login_required
def Profile():
    form=UpdationForm()
    profile_pic = url_for('static', filename=current_user.img)
    if form.validate_on_submit():
        if form.picture.data:
            filename=save_picture(form.picture.data)
            current_user.img=filename
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Account details updated successfully!', 'success')
        return redirect(url_for('Profile'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    return render_template("Profile.html",title="Your Profile", profile_pic=profile_pic, form=form)


def save_picture(picture_file):
    hex_name=secrets.token_hex(8)
    _, file_ext=os.path.splitext(picture_file.filename)
    new_name=hex_name+file_ext
    new_path=os.path.join(app.root_path,'static', new_name)
    picture_file.save(new_path)
    return new_name
