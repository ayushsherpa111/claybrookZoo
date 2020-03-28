from flask import Blueprint,url_for,request,render_template

animal = Blueprint('animals',__name__)

@animal.route("/animals",methods=["GET","POST"])
def zooAnimals():
  bannerImage = url_for("static",filename="images/flamgo.jpg")
  if request.method == "GET":
    return render_template("animals.html",banner=False,feature=bannerImage)


@animal.route("/animals/<string:category>",methods=["GET","POST"])
def animalCategory(category):
  if request.method == "GET":
    return f"This is the {category} category"