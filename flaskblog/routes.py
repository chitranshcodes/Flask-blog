import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm, UpdationForm, NewPostForm, UpdatePostForm, ResetPasswordForm, ResetRequestForm
from flaskblog import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route('/')
def welcome():
    return render_template('welcome.html')
@app.route('/home')
def home():
    page=request.args.get('page',1, type=int)
    posts=Post.query.order_by(Post.Date_Posted.desc()).paginate(per_page=4, page=page)
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
    profile_pic = url_for('static', filename='pfps/'+current_user.img)
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
    new_path=os.path.join(app.root_path,'static/pfps', new_name)
    op_size=(150,150)
    i=Image.open(picture_file)
    i=i.resize(op_size)
    i.save(new_path)
    return new_name

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form=NewPostForm()
    if form.validate_on_submit():
        post= Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('HURRAYYYY...Posted!!!', 'success')
        return redirect(url_for('home'))
    return render_template('new_post.html', title='New Post', form=form)

@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    form=UpdatePostForm()
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Updated changes', 'success')
        return redirect(url_for('home'))
    if request.method=='GET':
        form.title.data=post.title
        form.content.data=post.content


    return render_template('post_update.html', title='Update Post', form=form)

@app.route("/post/<int:post_id>/delete")
@login_required
def post_delete(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted!', 'danger')
    return redirect(url_for('home'))

@app.route('/reset_request', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=ResetRequestForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash('a passwor reset mail has been sent to your email id. Meet you there!', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password', methods=['GET','POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= ResetPasswordForm()
    user=User.verify_reset_token(token)
    if not user:
        flash('Token is invalid or expired', 'warning')
        return redirect(url_for('reset_request'))
    if form.validate_on_submit():
        hashed_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_pw
        db.session.commit()
        flash('Your password has been changed!, Please login with the new password', 'success')
        return redirect(url_for('login'))
    form= ResetPasswordForm()
    return render_template('reset_password.html', title='Reset Password', form=form)


def send_email(user):
    token = user.get_reset_token()
    msg= Message('Password reset email', sender='noreplydemo@gmail.com', recipients=[user.email])
    msg.body= f"""Follow the given link ton reset your password
{url_for('reset_password', token=token, _external=True)}

if you did not request it, ignore and no changes will be made
"""
    mail.send(msg)