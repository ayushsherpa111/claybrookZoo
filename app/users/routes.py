from random import randint
from markupsafe import escape
from pymongo import ASCENDING
from flask import Blueprint, render_template, session, url_for,redirect,flash,request,abort
from functools import wraps
from bson.objectid import ObjectId
import json
from datetime import datetime, timedelta
from app.users.forms import LoginForm,RegistrationForm,StaffForm,getAnimalForm,MammalForm
from app.users.helper import Helper,checkSession,assignRole,setSession,getAnimal,InsertAnimal
from app.db.claybrookZoo import log,users,categories,compound,aquarium,hothouse,aviary,contract
from app import bcrypt
from app.models.user import User
from app.models.roles import Sponsor
from app.models.mammals import Mammals
from app.models.birds import Birds
from app.models.category import Category
import secrets
import os
from app import app

userDB = Helper(users)
logs = Helper(log)
sponsor_contract = Helper(contract)
insertAnimal = InsertAnimal({'mammals':Helper(compound),'birds':Helper(aviary),'reptiles':Helper(hothouse),'amphibians':Helper(hothouse),'fishes':Helper(aquarium)})
user = Blueprint('user',__name__)
severity = {'healthy':"healthy.png",'moderate':"moderate.png",'moderately severe':"moderateS.png",'severe':'severe.png'}

newSponsors = sponsor_contract.count_items({'approved':False})
newUsers=userDB.get_new_users()

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
  if 'current_user' in session:
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

@user.route("/staff/<string:category>/<string:animalID>/archive",methods=["GET"])
def archiveAnimal(category,animalID):
  if checkSession(session,["Admin","Manager"]):
    _id = insertAnimal.archive(category,animalID) 
    if _id:
      flash("Animal Archived Succesfully")
      log.insert_one({
        "inserted_by": session['current_user']['username'],
        "animal": _id,
        'category':category,
        'operation':'archive',
        "date_added":datetime.now()
      })
    else:
      flash("Archive failed")
    return redirect(f"/staff/{category}")
  else:
    return redirect(url_for("home.index"))



@user.route('/register',methods=["GET","POST"])
def register():
  if 'current_user' in session:
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
    global newSponsors
    latest = insertAnimal.getLastAdded()
    animal_count = insertAnimal.getAllCount()
    return render_template('staff/staff.html',total=randint(1,100),newUsers=userDB.get_new_users(),latest=latest,animal_count=animal_count,newSponsors=newSponsors)
  else:
    return redirect(url_for("home.index"))

@user.route("/staff/animals",methods=["GET","POST"])
@user.route("/staff/animals/<string:category>",methods=["GET","POST"])
def animalOperation(category=None):
  print(app.root_path)
  if checkSession(session,["Admin","Manager","Staff"]):
    global newUsers
    global newSponsors
    global severity
    # newUsers = userDB.get_new_users()
    form = getAnimalForm(category) if category != None else None
    cats = Category.get_all()
    addForm = True
    severAnimals = insertAnimal.health_count()
    if request.method == "GET":
      if category == None:
        form = None
        addForm = False
      else:
        addForm = True
    if form and form.validate_on_submit():
      imagePath = uploadImage(form.image.data,category)
      newAnimal = getAnimal(form.__dict__['_fields'],category)
      newAnimal.update({'image':[imagePath],"dateAdded":datetime.utcnow(),'status':'healthy'})
      _id = insertAnimal.insert_animal(newAnimal.__dict__,category)
      log.insert_one({
        "inserted_by": session['current_user']['username'],
        "animal": _id,
        'operation':'add',
        'category': category,
        "date_added":datetime.now()
      })
      return redirect(url_for("user.staffHome"))
    return render_template("staff/animals.html",profile="profile.png",categories=cats,addForm=addForm,category=category,form=form,newUsers=newUsers,newSponsors=newSponsors,severity=severity,health_dist=severAnimals)
  else:
    return redirect(url_for("animals.zooAnimals"))

@user.route("/staff/<string:category>", methods=["GET"])
def displayCategory(category):
  if checkSession(session,["Admin","Manager","Staff"]):
    category = escape(category)
    global newUsers
    # newUsers = userDB.get_new_users()
    if category.lower() == "sick":
      animals = insertAnimal.get_animals("total",{'status':{'$exists':'true'}})
    else:
      animals = insertAnimal.get_animals(category)
    return render_template("staff/animalinfo.html",category=category,newUsers=newUsers,animals=animals)
  return redirect(url_for("animals.zooAnimals"))

@user.route("/staff/evaluate",methods=["GET"])
def staffEvaluate():
  if checkSession(session,["Admin"]):
    global newSponsors
    newUsers = userDB.get_new_users()
    # global newUsers
    return render_template("staff/evaluate.html",evaluateUsers=newUsers,newUsers=newUsers,profile="ssg-goku.jpg",newSponsors=newSponsors)
  else:
    return redirect(url_for("user.staffHome"))

@user.route("/evaluate/<string:email>",methods=["GET","POST"])
def updateStaff(email):
  if checkSession(session,["Admin"]):
    global newUsers
    global newSponsors
    user = userDB.find_by_email(email)
    _id = user['_id']
    currVis = User({'email':user['email'],'username':user['username']})
    editForm = StaffForm()
    if editForm.validate_on_submit():
      currVis = assignRole(editForm.role.data,currVis.__dict__,{'username': editForm.username.data,'role':editForm.role.data,'checked':True})
      if currVis.saveToDb(userDB):
        return redirect(url_for("user.staffEvaluate"))
    return render_template("staff/editStaff.html",profile="ssg-goku.jpg",form=editForm,user=currVis,newUsers=newUsers,newSponsors=newSponsors)
  else:
    return render_template("staff/staff.html")

@user.route("/eval",methods=["POST"])
def approveRole():
  if checkSession(session,["Admin"]):
    criteria = request.get_json()
    print(criteria)
    if userDB.find_and_update({'email':criteria['email']},{"checked":True,"role":criteria['role']}):
      return json.dumps({'approve':True})

@user.route("/staff/sponsor",methods=["GET","POST"])
def approveStaff():
  global newUsers
  global newSponsors
  if checkSession(session,['Admin',"Manager","Staff"]):
    sponsors = sponsor_contract.getProp({})
    return render_template("staff/sponsors.html",newSponsors=newSponsors,newUsers=newUsers,role=session['current_user']['role'],sponsors=sponsors)
  else:
    return render_template("sponsor.applySponsor")

@user.route("/staff/health",methods=["GET","POST"])
def assignHealth():
  if checkSession(session,["Admin","Staff","Manager"]):
    global newUsers
    global newSponsors
    global severity
    animals = insertAnimal.get_animals("total")
    return render_template("staff/sickAnimal.html",newUsers=newUsers,newSponsors=newSponsors,animals=animals,severity=severity)
  else:
    return redirect(url_for(""))

@user.route("/staff/approve",methods=["POST"])
def approve():
  if checkSession(session,["Admin"]):
    payload = request.form
    dateApproved = datetime.now() + timedelta(int(payload['months']) * 30)
    sponsor_contract.find_and_update({'_id':ObjectId(payload['id'])},{'end_date':dateApproved,'approved':True})
    newSponsors -= 1
    userDB.find_and_update({'_id':ObjectId(payload['sponsor_id'])},{"role":"Sponsor"})
    return redirect(url_for("user.approveStaff"))

@user.route("/staff/<string:category>/<string:_id>/<string:status>",methods=["GET"])
def updateHealth(category,_id,status):
  if checkSession(session,["Admin","Manager"]):
    global severity
    if status.lower() in severity:
      anim = insertAnimal.dbs.get(category)
      if anim:
        if anim.find_and_update({'_id':ObjectId(_id)},{'status':status}):
          return redirect(url_for("user.assignHealth"))
      else:
        return "Animal Not found"
    else:
      return "Invalid Status"
  else:
    return redirect(url_for("user.staff"))

@user.route("/staff/collect",methods=["GET"])
def returnCount():
  return insertAnimal.getAllCount()

@user.route("/staff/logs",methods=["GET"])
def staffLog():
  if checkSession(session,["Admin"]):
    global newUsers
    global newSponsors
    userLogs = logs.getProp({}).sort([('date_added',ASCENDING)])
    orderd = {}
    for i in userLogs:
      datekey = str(i['date_added']).split(' ')[0]
      if datekey == str(datetime.now()).split(' ')[0]:
        k = "Today"
      else:
        k = datekey
      curr = orderd.get(k,None)
      if not curr:
        orderd[k] = []
      orderd[k].append(i)
    return render_template("staff/activityLog.html",newUsers=newUsers,newSponsors=newSponsors,log=orderd)