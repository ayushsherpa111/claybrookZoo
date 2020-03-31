from random import randint
from markupsafe import escape
from flask import Blueprint, render_template, session, url_for,redirect,flash,request,abort
from functools import wraps
import json
from datetime import datetime
from app.users.forms import LoginForm,RegistrationForm,StaffForm,getAnimalForm,MammalForm
from app.users.helper import Helper,checkSession,assignRole,setSession,getAnimal,InsertAnimal
from app.db.claybrookZoo import users,categories,compound,aquarium,hothouse,aviary
from app import bcrypt
from app.models.user import User
from app.models.mammals import Mammals
from app.models.birds import Birds
from app.models.category import Category
import secrets
import os
from app import app

userDB = Helper(users)
insertAnimal = InsertAnimal({'mammals':Helper(compound),'birds':Helper(aviary),'reptiles':Helper(hothouse),'amphibians':Helper(hothouse),'fishes':Helper(aquarium)})
user = Blueprint('user',__name__)


def uploadImage(image_data,animalType):
  random_hex = secrets.token_hex(16)
  _, fext = os.path.splitext(image_data.filename)
  newFilename = random_hex + fext
  picture_path = os.path.join(app.root_path,'static','images',animalType,newFilename)
  image_data.save(picture_path)
  return newFilename


@user.route("/login",methods=["GET","POST"])
def loginUser():
  logForm = LoginForm()
  loginFail = False
  color = ""
  print(request.method)
  if 'email' in session:
    return redirect(url_for('home.index'))
  if request.method == "POST":
    if logForm.validate_on_submit():
      userInst = userDB.login({'email':logForm.email.data,'password':logForm.password.data})
      if userInst != None:
        flash(f'Welcome! {escape(userInst["username"])}.','notification is-success')
        setSession(session,userInst)
        return redirect(url_for('home.index' if session['current_user']['role'] in ["Sponsor","Visitor"]  else "user.staffHome"))
      else:
        loginFail = True
        color = "#b70606"
  return render_template('login.html',form=logForm,notification=6,fail=loginFail,color=color)



@user.route('/register',methods=["GET","POST"])
def register():
  if 'email' in session:
    return redirect(url_for('home.index'))
  regForm = RegistrationForm()
  if regForm.validate_on_submit():
    userID = userDB.register({'username':regForm.username.data,'password':regForm.password.data,'email':regForm.email.data,'checked': False})
    setSession(session,userID)
    return redirect(url_for('home.index'))
  elif request.method == "POST":
    flash(f'Failed to create account {regForm.username.data}! ','notification is-danger')
  return render_template('register.html',form=regForm)


@user.route("/logout",methods=["GET","POST"])
def logout():
  if request.method == "GET":
    if "current_user" in session:
      session.pop('current_user',None)
      flash("You have now been logged out","notification is-danger")
      return redirect(url_for('home.index'))
    else:
      flash("You must first Login","notification is-warning")
      return redirect(url_for('home.index'))


@user.route("/staff",methods=["GET"])
def staffHome():
  if checkSession(session,["Admin","Manager","Staff"]):
    latest = insertAnimal.getLastAdded()
    return render_template('staff/staff.html',total=randint(1,100),newUsers=userDB.get_new_users(),latest=latest)
  else:
    return redirect(url_for("home.index"))

@user.route("/staff/animals",methods=["GET","POST"])
@user.route("/staff/animals/<string:category>",methods=["GET","POST"])
def animalOperation(category=None):
  print(app.root_path)
  if checkSession(session,["Admin","Manager","Staff"]):
    form = getAnimalForm(category) if category != None else None
    cats = Category.get_all()
    addForm = True
    if request.method == "GET":
      if category == None:
        form = None
        addForm = False
      else:
        addForm = True
    if form and form.validate_on_submit():
      imagePath = uploadImage(form.image.data,category)
      newAnimal = getAnimal(form.__dict__['_fields'],category)
      newAnimal.update({'image':[imagePath],"dateAdded":datetime.utcnow()})
      insertAnimal.insert_animal(newAnimal.__dict__,category)
      return redirect(url_for("user.staffHome"))
    return render_template("staff/animals.html",profile="profile.png",categories=cats,addForm=addForm,category=category,form=form)
  else:
    return redirect(url_for("animals.zooAnimals"))


@user.route("/evaluate",methods=["GET"])
def staffEvaluate():
  if checkSession(session,["Admin"]):
    newUsers = userDB.get_new_users()
    return render_template("staff/evaluate.html",evaluateUsers=newUsers,profile="ssg-goku.jpg")
  else:
    return redirect(url_for("user.staffHome"))

@user.route("/evaluate/<string:email>",methods=["GET","POST"])
def updateStaff(email):
  if checkSession(session,["Admin"]):
    user = userDB.find_by_email(email)
    _id = user['_id']
    currVis = User({'email':user['email'],'username':user['username']})
    editForm = StaffForm()
    if editForm.validate_on_submit():
      currVis = assignRole(editForm.role.data,currVis.__dict__,{'username': editForm.username.data,'role':editForm.role.data,'checked':True})
      if currVis.saveToDb(userDB):
        return redirect(url_for("user.staffEvaluate"))
    return render_template("staff/editStaff.html",profile="ssg-goku.jpg",form=editForm,user=currVis)
  else:
    return render_template("staff/staff.html")

@user.route("/eval",methods=["POST"])
def approveRole():
  if checkSession(session,["Admin"]):
    criteria = request.get_json()
    user = assignRole(criteria['role'],)
    print(criteria)
    if userDB.find_and_update({'email':criteria['email']},{"checked":True,"role":criteria['role']}):
      return redirect(url_for("user.staffHome"))


