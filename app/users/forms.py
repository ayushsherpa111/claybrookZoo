from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField
from wtforms.validators import DataRequired, Length,Email, EqualTo,ValidationError,Regexp,any_of
from app.db.claybrookZoo import users
from app.users.helper import Helper
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
  password = PasswordField('Password',validators=[ DataRequired(),Length(min=8,max=64)])
  confirmPassword = PasswordField('Confirm Password', validators=[ DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
  email = StringField('Email',validators=[DataRequired(),Email()])
  password = PasswordField('Password',validators=[ DataRequired() ])
  rememberMe = BooleanField('Remember Me')
  submit = SubmitField('Login')


class StaffForm(FlaskForm):
  email = StringField('Email',validators=[DataRequired(),Email()],render_kw={'readonly':True})
  username = StringField('Username',validators=[DataRequired(),Regexp("^[^\s<>][a-zA-Z0-9_]*$",message="Invalid Username")])
  role = SelectField("Role",choices=[("Visitor","Visitor"),("Sponsor","Sponsor"),("Staff","Staff"),("Manager","Manager")],validators=[])
  submit = SubmitField('Change')



