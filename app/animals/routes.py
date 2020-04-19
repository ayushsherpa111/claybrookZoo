from flask import Blueprint,url_for,request,render_template
from app.users.helper import Helper, InsertAnimal
from app.db.claybrookZoo import compound, aviary, hothouse, aquarium
import json

animal = Blueprint('animals',__name__)
insertAnimal = InsertAnimal({'mammals':Helper(compound),'birds':Helper(aviary),'reptiles':Helper(hothouse),'amphibians':Helper(hothouse),'fishes':Helper(aquarium)})
@animal.route("/animals",methods=["GET","POST"])
def zooAnimals():
  bannerImage = url_for("static",filename="images/flamgo.jpg")
  if request.method == "GET":
    return render_template("animals.html",banner=False,feature=bannerImage)


@animal.route("/animals/<string:category>",methods=["GET","POST"])
def animalCategory(category):
  if request.method == "GET":
    anim = insertAnimal.mapping.get(category.lower(),None)[0]
    bTemp = f"Come see the {anim} in the {category}"
    mp = insertAnimal.mapping.get(category)[0]
    animals = [*insertAnimal.get_animals(category,{'$or':[{"archive":{"$exists":False}},{"archive":False}]})]
    [i.update({'mascot':url_for('static',filename=f'images/{i["classif"]}/{i["image"][0]}')}) for i in animals]
    return render_template("category.html",feature=url_for('static',filename=f'images/{anim}/generic.jpg'),details=bTemp,animals=animals,mp=mp)