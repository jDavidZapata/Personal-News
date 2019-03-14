from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, length
from models import User, Channel
from flask_login import current_user
from wtforms.widgets import HiddenInput


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class CreateChannelForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField(u'Descriction', validators=[DataRequired(), length(max=200)])
    message = TextAreaField(u'Message', validators=[length(max=200)])
    
    submit = SubmitField('Create Channel')

    def validate_user_id(self, user_id):
        channel = Channel.query.filter_by(user_id=user_id).first()
        if channel:
            raise ValidationError('You Already Have A Channel.')

    def validate_title(self, title):
        channel = Channel.query.filter_by(title=title.data).first()
        if channel:
            raise ValidationError('Please use a different Title.')
    

class CreateStoryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    story_text = TextAreaField(u'Share Your Story', validators=[DataRequired(), length(max=400)])
    submit = SubmitField('Create Story')
