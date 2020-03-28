from markupsafe import escape
from app import app
from datetime import datetime
from app import bcrypt
from app.models.roles import Sponsor, Visitor, Manager,Staff

class Helper:
  def __init__(self,db):
    self.db = db

  def get_all_users(self):
    return self.db.find({'role':{'$ne':'Admin'},'checked':'False'})

  def find_by_username(self,username):
    username = self.escapeEverything(username)
    return self.db.find_one({'username':username})
  
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

  def find_and_update(self,option,setVal):
    setVal = self.escapeEverything(setVal)

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
  if session.get('email',None) and session.get("role",None) and session.get("role") in roles:
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


