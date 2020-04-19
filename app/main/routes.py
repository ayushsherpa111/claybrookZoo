import json
from random import randint
from bson.objectid import ObjectId
from markupsafe import escape
from flask import Blueprint, render_template, request,flash, session, url_for, redirect
from app.users.helper import Helper, InsertAnimal
import re
from app.db.claybrookZoo import compound, aviary, hothouse, aquarium, contract
from app.main.forms import SearchForm
import datetime

home = Blueprint('home',__name__)
insertAnimal = InsertAnimal({'mammals':Helper(compound),'birds':Helper(aviary),'reptiles':Helper(hothouse),'amphibians':Helper(hothouse),'fishes':Helper(aquarium)})

@home.route('/')
@home.route('/index')
def index():
  statics = url_for('static',filename="images")
  return render_template('home.html',feature=f"{statics}/caw.jpg",notification=randint(1,10),banner=True,title="Home")

@home.route('/search',methods=['GET','POST'])
def search():
  if request.method == "POST":
    form = SearchForm()
    body = escape(request.form['animal'])
    form.animal_name.data = body
    results = insertAnimal.get_animals('total',{'animal_name':{'$regex':re.compile(body)}})
    return render_template('search.html',results=results,form=form)
  else:
    return redirect(url_for('home.searchAdvance'))

@home.route('/search/advance',methods=['GET','POST'])
def searchAdvance():
  searchForm = SearchForm()
  if request.method == "GET":
    searchForm.fromDate.data = searchForm.fromDate.data if searchForm.fromDate.data else datetime.datetime.now().year - 1
    searchForm.toDate.data = datetime.datetime.now().year
    return render_template("search.html",form=searchForm)

  if searchForm.validate_on_submit():
    regex = {}
    if searchForm.animal_name.data != "":
      regex.update({'animal_name':{'$regex': re.compile(searchForm.animal_name.data,re.I)}})
    if searchForm.species.data != "":
      regex.update({'species':{'$regex':re.compile(searchForm.species.data,re.I)}})
    if searchForm.fromDate.data and searchForm.toDate.data:
      fromRange = datetime.datetime(searchForm.fromDate.data,1,1)
      toRange = datetime.datetime(searchForm.toDate.data,12,31)
      regex.update({'date_of_birth':{'$gte':fromRange,'$lte':toRange}})
    return render_template("search.html",form=searchForm,results=insertAnimal.get_animals(searchForm.category.data,regex))
  else:
    return render_template("search.html",form=searchForm)


@home.route("/<string:category>/<string:id>")
def getAnimal(category,id):
  unwanted = ["_id","gender","lifespan","diet","image","classif","habitat","status"]
  found = insertAnimal.get_animals(category,{'_id':ObjectId(id)})[0]
  url = found['classif']+"/"+found['image'][0]
  details = f"Meet {found['animal_name']} the {found['species']}"
  animalImg = url_for("static",filename="images/"+url)
  sponsors = contract.find({"animal_sponsor":{'$in':[found['_id']]}})
  return render_template("animalDetail.html",feature=animalImg,details=details,unwanted=unwanted,found=found,sponsors=sponsors)

@home.route("/tickets")
def showTickets():
  return render_template("ticket.html")