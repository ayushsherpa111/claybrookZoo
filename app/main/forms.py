from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField, IntegerField, RadioField, SelectField

class SearchForm(FlaskForm):
  animal_name = StringField('Animal Name')
  species = StringField('Species')
  # gender = RadioField("Gender",choices=[('M',"Male"),('F',"Female")])
  category = SelectField("Category",choices=[("total","All"),("compound","Mammals"),("aviary","Birds"),("hothouse","Reptiles"),("hothouse","Amphibians"),("aquarium","Fishes")])
  fromDate = IntegerField('From')
  toDate = IntegerField('To')
  submit = SubmitField("Search")
