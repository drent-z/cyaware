from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp
from app.models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[
                                 DataRequired(), 
                                 Length(min=8, message='Password must be at least 8 characters long.'),
                                 Regexp('(?=.*[A-Z])', message='Password must contain at least one uppercase letter.'),
                                 Regexp('(?=.*[a-z])', message='Password must contain at least one lowercase letter.'),
                                 Regexp('(?=.*[0-9])', message='Password must contain at least one digit.'),
                                 Regexp('(?=.*[@$!%*?&])', message='Password must contain at least one special character (@$!%*?&).')
                             ])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
