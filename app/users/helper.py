from markupsafe import escape
from app import app
from datetime import datetime
from app import bcrypt
from app.models.roles import Sponsor, Visitor, Manager,Staff
from app.models.mammals import Mammals
from app.models.birds import Birds
from pprint import pprint

class Helper:
  def __init__(self,db):
    self.db = db

  def get_new_users(self):
    return self.db.find({'role':{'$ne':'Admin'},'checked':'False'})
  
  def find_by_username(self,username):
    user = self.escapeEverything(username)
    return self.db.find({'username':user})
  
  def find_by_email(self,email):
    email = self.escapeEverything(email)
    return self.db.find_one({'email':email})

  def login(self,userDict):
    userDict = self.escapeEverything(userDict)
    found = self.db.find_one({"email":userDict["email"]}) 
    if found:
      if bcrypt.check_password_hash(found["password"],userDict["password"]):
        return found
    return None

  def insert_record(self,obj):
    _sanitized = self.escapeEverything(obj)
    try:
      self.db.insert_one(_sanitized)
      return True
    except Exception as e:
      return e


  def find_and_update(self,option,setVal):
    setVal = self.escapeEverything(setVal)
    self.db.update_one(option,{"$set":setVal})
    return True

  def register(self,user):
    user = self.escapeEverything(user)
    userPassword  = bcrypt.generate_password_hash(user['password'],app.passRounds)
    user.update({'password':userPassword,'role':"Visitor",'registerDate':datetime.utcnow(),'archive':False})
    if self.db.find_one({'email':user['email']}) == None:
      return self.db.insert_one(user).inserted_id
    else:
      return False
  
  def escapeEverything(self,data):
    if isinstance(data,dict):
      for key in data:
        newVal = escape(data[key])
        data.update({key:newVal})
    elif isinstance(data,str):
      data = escape(data)
    return data

def checkSession(session,roles):
  if session.get('current_user',None) and session.get('current_user')['role'] in roles:
    return True
  else:
    return False

def assignRole(role,object,newProp):
  if role == "Visitor":
    newUser = Visitor(object,newProp)
  elif role == "Manager":
    newUser = Manager(object,newProp)
  elif role == "Sponsor":
    newUser = Sponsor(object,newProp)
  else:
    newUser = Staff(object,newProp)
  return newUser


def setSession(session,userInstance):
  dct = {
      'username':escape(userInstance['username']), 
      'email' : escape(userInstance['email']),
      'role': escape(userInstance["role"]),
      "profile": userInstance.get('profile') if userInstance.get('profile',None) else "default.png" 
  }
  session['current_user'] = dct


def getAnimal(form_data,animal):
  animalDct = {}
  for key,value in form_data.items():
    if key != "image" and key != "csrf_token":
      animalDct.update({key:value.data})
  new_life_span = str(animalDct['lifespan']) + animalDct.pop('spanType')
  animalDct.update({'lifespan':new_life_span})
  print(animalDct)
  if animal.lower() == "mammals":
    return Mammals(animalDct,{})
  if animal.lower() == "birds":
    return Birds(animalDct,{})

class InsertAnimal:
  def __init__(self,animal_dbs):
    self.dbs = animal_dbs
  
  def insert_animal(self,animal,animType):
    animType = animType.lower()
    return self.dbs.get(animType,None).insert_record(animal)