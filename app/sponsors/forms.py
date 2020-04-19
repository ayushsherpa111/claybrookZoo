from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileField
from wtforms import StringField, PasswordField, SubmitField,BooleanField,SelectMultipleField,DateField,RadioField,IntegerField,TextAreaField
from wtforms.validators import DataRequired
from app.users.helper import InsertAnimal,Helper
from app.db.claybrookZoo import compound, aviary,aquarium,hothouse

insertAnimal = InsertAnimal({'mammals':Helper(compound),'birds':Helper(aviary),'reptiles':Helper(hothouse),'amphibians':Helper(hothouse),'fishes':Helper(aquarium)})

def get_all_animals():
  animals = insertAnimal.get_animals('total',{'$or':[{'archive':{'$exists':False}},{'archive':False}]})
  choices = []
  for i in animals:
    choices.append((i['_id'],i['animal_name']))
  return choices

class ApplyForm(FlaskForm):
  client_name = StringField('Client / Company Name',validators=[DataRequired('Please provide your Business/Client Name')])
  client_address = StringField("Address",validators=[DataRequired("Please provide the address your business is established in")])
  client_estate = StringField("Estate",validators=[DataRequired("Please provide the town your business is established in")])
  client_city = StringField("City",validators=[DataRequired("Please provide the city your business is established in")])
  client_country = StringField("Country",validators=[DataRequired("Please provide the country your business is established in")])
  animal_sponsor = SelectMultipleField("Animal To Sponsor",validators=[DataRequired("Please Select atleast one animal")],coerce=str)
  sponsor_band = RadioField('Sponsor Band',choices=[('A','A - $2500'),('B','B - $2000'),('C','C - $1500'),('D','D - $1000'),('E','E - $500')])
  signage = FileField('Signage',validators=[FileAllowed(['jpg','jpeg','png'])])
  submit = SubmitField("Apply")