from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField,DateField,RadioField,IntegerField,TextAreaField
from wtforms.validators import DataRequired, Length,Email,Optional, EqualTo,ValidationError,Regexp,any_of,NumberRange
from app.db.claybrookZoo import users
from app.users.helper import Helper
import re
userDB = Helper(users)

def validate_name(field):
  if field == "Email":
    message = f"The given email is already taken"    
  elif field == "Username":
    message = f"The given username is already taken"

  def _taken(form,field):
    if field == "Email":
      if userDB.find_by_email(field.data).count() > 0:
        raise ValidationError(message)
    else:
      if userDB.find_by_username(field.data).count() > 0:
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


def changeUsername(field):
  message = f"The given username is already taken"
  def _taken(form,field):
    if userDB.find_by_username(field.data).count() > 1:
      raise ValidationError(message)
  return _taken

class StaffForm(FlaskForm):
  email = StringField('Email',validators=[DataRequired(),Email()],render_kw={'readonly':True})
  username = StringField('Username',validators=[DataRequired(),Regexp("^[^\s<>][a-zA-Z0-9_]*$",message="Invalid Username"),changeUsername('Username')])
  role = SelectField("Role",choices=[("Visitor","Visitor"),("Sponsor","Sponsor"),("Staff","Staff"),("Manager","Manager")],validators=[])
  submit = SubmitField('Change')



class AnimalForm(FlaskForm):
  species = StringField("Species",validators=[DataRequired(),Regexp("^[^\d\W][a-zA-Z\s()]+$",message="Invalid Species Name")])
  animal_name = StringField("Animal Name",validators=[DataRequired(),Regexp("^[^\d\W][a-zA-Z\s()]+$",message="Invalid Animal Name")])
  classification = StringField("Animal Class",validators=[DataRequired(),Regexp("^[^\d\W][a-zA-Z\s()]+$",message="Invalid Animal Name")])
  date_of_birth = DateField("Date Of Birth",validators=[DataRequired()])
  gender = RadioField("Gender",choices=[('M',"Male"),('F',"Female")],validators=[DataRequired()])
  lifespan = IntegerField("Lifespan",validators=[DataRequired(),NumberRange(min=1)])
  spanType = SelectField("Lifespan",choices=[('Months',"Months"),('Years',"Years")])
  diet = TextAreaField("Dietary Requirements",validators=[DataRequired()])
  habitat = TextAreaField("Natural Habitat Description",validators=[DataRequired()])
  global_population = IntegerField("Global Population Distribution",validators=[DataRequired(),NumberRange(min=1)])
  height = IntegerField("Height in CM",validators=[DataRequired(),NumberRange(min=1)])
  weight = IntegerField("Weight in KG",validators=[DataRequired(),NumberRange(min=1)])
  image = FileField("Animal Pictures",validators=[DataRequired(),FileAllowed(['jpg','png'])])



class MammalForm(AnimalForm):
  gestationa_period = IntegerField("Gestational Period [ IN MONTHS ]",validators=[DataRequired(),NumberRange(min=1)])
  category = StringField("Mammal Classification",validators=[DataRequired(),Regexp("^[a-zA-Z\s]*$")])
  average_body_temp = IntegerField("Average Body Temperature in °C",validators=[DataRequired()])

class BirdForm(AnimalForm):
  nest_construction = StringField("Nest Construction method",validators=[DataRequired()])
  clutch_size = IntegerField("Bird Clutch Size in inches",validators=[DataRequired(),NumberRange(min=1)])
  wing_span = IntegerField("Wing span in inches",validators=[DataRequired(),NumberRange(min=1)])
  fly = BooleanField("Can fly?")
  plumage = StringField("Plumage color variants",validators=[DataRequired()])

class ReptileAndAmphForm(AnimalForm):
  reproduction_type = StringField('Reproduction type',validators=[DataRequired()])
  average_clutch_size = IntegerField("Average clutch size",validators=[DataRequired(),NumberRange(min=1)])
  average_offspring_number = IntegerField("Average offspring",validators=[DataRequired(),NumberRange(min=1)])

class FishForm(AnimalForm):
  average_body_temp = IntegerField("Average Body Temperature",validators=[DataRequired()])
  water_type = StringField("Water Type",validators=[DataRequired()])
  color_variant = IntegerField("Color Variant",validators=[DataRequired()])

def getAnimalForm(animal):
  arrOfAnimals = {'mammals':MammalForm(),'birds':BirdForm(),'reptiles':ReptileAndAmphForm(),'amphibians':ReptileAndAmphForm(),'fishes':FishForm()}
  animal = animal.lower()
  return arrOfAnimals.get(animal,None)
