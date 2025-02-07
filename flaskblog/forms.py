from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField("Email", validators=[DataRequired(), Length(min=5), Email()])
    password= PasswordField("Password", validators=[DataRequired(), Length(min=7, max=15)])
    confirm_password= PasswordField("Confirm Password", validators=[DataRequired(), Length(min=7, max=15), EqualTo('password') ])
    submit=SubmitField('Sign-Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Use a different Username')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email already registered')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(min=5), Email(message='Invalid Email Address')])
    password= PasswordField("Password", validators=[DataRequired(), Length(min=7, max=15)])
    remember=BooleanField("Remember Me")
    submit=SubmitField('Login')


class UpdationForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField("Email", validators=[DataRequired(), Length(min=5), Email()])
    submit=SubmitField('Update Now!')

    def validate_username(self,username):
        if username.data!=current_user.username: 
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Use a different Username')
    def validate_email(self,email):
        if email.data!=current_user.email: 
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('email already registered')