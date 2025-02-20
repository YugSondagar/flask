from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed  #filefield ensures type of file this is and fileallowed ensures it is a certain type of file
from flask_login import current_user
from wtforms import StringField , PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length , Email, EqualTo, ValidationError
from flaskblog.models_blog import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])    #datarequired will make sure that the string is not empty and length will check the username lies in the range.

    email = StringField('Email',validators=[DataRequired(), Email()])

    password = PasswordField('Password',validators=[DataRequired()])

    confirm_password = PasswordField('confirm_Password',validators=[DataRequired(),EqualTo('password')])

    submit = SubmitField('Sign Up')

# function to check if username exist or not i.e. it is unique
    def validate_username(self,username):

        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is taken!')

# function to check if email exist or not i.e. it is unique
    def validate_email(self,email):
        email = User.query.filter_by(email = email.data).first()
        if email:
            raise ValidationError('That email is taken!')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remeber Me!')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    picture = FileField('Update Picture',validators=[FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError('That name is taken.Please take another name!')
    
    def validate_email(self,email):
        if email.data != current_user.email:
            if User.query.filter_by(email = email.data).first():
                raise ValidationError('That email is taken!')

class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit= SubmitField('Post')

class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Account with email does not exist')
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset Passsword')