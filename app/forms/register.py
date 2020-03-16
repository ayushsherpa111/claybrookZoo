from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length,Email, EqualTo,ValidationError
from db.claybrookZoo import users
from app.utils.helper import Helper

userDB = Helper(users)

def validate_name(field):
  if field == "Email":
    message = f"The given email is already taken"    
  elif field == "Username":
    message = f"The given username is already taken"

  def _taken(form,field):
    if field == "Email":
      if userDB.find_by_email(field.data):
        raise ValidationError(message)
    else:
      if userDB.find_by_username(field.data):
        raise ValidationError(message)
  return _taken


class RegistrationForm(FlaskForm):
  username = StringField('Username',validators=[DataRequired(),Length(min=3,max=24),validate_name('Username')])
  email = StringField('Email',validators=[DataRequired(),Email(),validate_name("Email")])
  password = PasswordField('Password',validators=[ DataRequired() ])
  confirmPassword = PasswordField('Confirm Password', validators=[ DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')




class LoginForm(FlaskForm):
  email = StringField('Email',validators=[DataRequired(),Email()])
  password = PasswordField('Password',validators=[ DataRequired() ])
  rememberMe = BooleanField('Remember Me')
  submit = SubmitField('Sign Up')


