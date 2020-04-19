from markupsafe import escape
from pymongo import ASCENDING
from bson.objectid import ObjectId
from app import app
from datetime import datetime,time,timedelta
from app import bcrypt
from app.models.roles import Sponsor, Visitor, Manager,Staff
from app.models.mammals import Mammals
from app.models.reptsAndAmph import ReptileAndAmphForm
from app.models.birds import Birds
from app.models.fish import Fish
from pprint import pprint
import copy

class Helper:
  def __init__(self,db):
    self.db = db

  def get_new_users(self):
    return self.db.find({'role':{'$ne':'Admin'},'checked':False})
  
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
      return self.db.insert_one(_sanitized).inserted_id
    except Exception as e:
      print(e)
      return e

  def find_limit(self,count, skip,limit,condition):
    _sanitized = self.escapeEverything(condition)

  def sortBy(self,field,order,lim,prev):
    data = []
    prevDate = datetime.utcnow() - timedelta(prev)
    for i in self.db.find({"dateAdded":{"$lte":datetime.utcnow(),"$gt":prevDate}},{"animal_name":1,"species":1,"classification":1,"dateAdded":1,"location":1,"_id":0},limit=lim).sort([(field,order)]):
      data.append(i)
    return data

  def find_and_update(self,option,setVal):
    setVal = self.escapeEverything(setVal)
    self.db.update_one(option,{"$set":setVal})
    return True

  def register(self,user):
    user = self.escapeEverything(user)
    userPassword  = bcrypt.generate_password_hash(user['password'],app.passRounds)
    user.update({'password':userPassword,'role':"Visitor",'registerDate':datetime.utcnow(),'archive':False})
    found = self.db.find_one({'email':user['email']})
    if found == None:
      self.db.insert_one(user)
      return self.db.find_one({'email':user['email']})
    else:
      return False
  
  def count_items(self,condition={}):
    return self.db.count_documents(condition)

  def getProp(self,property):
    return self.db.find(property)

  def escapeEverything(self,data):
    if isinstance(data,dict):
      for key in data:
        if key != "date_of_birth" and key != "image" and key != "dateAdded":
          if isinstance(data[key],str):
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
      '_id': escape(userInstance['_id']),
      'username':escape(userInstance['username']), 
      'email' : escape(userInstance['email']),
      'role': escape(userInstance["role"]),
      "profile": userInstance.get('profile',"default.png")
  }
  session['current_user'] = dct


def getAnimal(form_data,animal):
  animalDct = {}
  for key,value in form_data.items():
    if key != "image" and key != "csrf_token":
      animalDct.update({key:value.data})
  new_life_span = str(animalDct['lifespan']) +' '+ animalDct.pop('spanType')
  animalDct.update({'lifespan':new_life_span})
  print(type(animalDct['date_of_birth']))
  newDOB = datetime.combine(animalDct['date_of_birth'],time())
  animalDct.update({'date_of_birth':newDOB})
  print(animalDct)
  if animal.lower() == "mammals":
    return Mammals(animalDct,{'classif': animal.lower()})
  if animal.lower() == "birds":
    return Birds(animalDct,{'classif': animal.lower()})
  if animal.lower() == "reptiles" or animal.lower() == "amphibians":
    return ReptileAndAmphForm(animalDct,{'classif': animal.lower()})
  if animal.lower() == "fishes":
    return Fish(animalDct,{'classif': animal.lower()})

class InsertAnimal:
  def __init__(self,animal_dbs):
    self.dbs = animal_dbs
    self.mapping = {
      'compound':['mammals','paw.png'],
      'aviary':['birds','bird.png'],
      'hothouse':['reptiles','dino.png'],
      'aquarium':['fishes','fin.png'],
      'sick':['Sick','sick.png'],
      'total':['Total','wild.png']
    }
    self.mapping2 = {
      'mammals':['compound','paw.png'],
      'birds':['aviary','bird.png'],
      'reptiles':['hothouse','dino.png'],
      'fishes':['aquarium','fin.png'],
      'sick':['Sick','sick.png'],
      'total':['Total','wild.png']
    }
  
  def insert_animal(self,animalRec,animType):
    animType = animType.lower()
    return self.dbs.get(animType,None).insert_record(animalRec)

  def getAllCount(self):
    animal_count = {}
    total = 0
    sick = 0
    imageString = "static/images/"
    for animal in self.dbs:
      if animal == "amphibians":
        continue
      count = self.dbs[animal].count_items()
      total += count
      sick += self.dbs[animal].getProp({'sick':{'$exists': True}}).count()
      lbl = self.mapping2[animal]
      animal_count.update({lbl[0]:{
        "count": count,
        "image": imageString+animal+'/'+lbl[1]
      }})
    animal_count.update({
      'sick':{
        "count": sick,
        "image": imageString+'/'+self.mapping['sick'][1]
      },
      'total':{
        "count":total,
        "image":imageString+'/'+self.mapping['total'][1]
      }
    })
    return animal_count

  def get_animals(self,category: str,option=None):
    if category.lower() != "total":
      cat = self.mapping.get(category.lower(),None)
      if cat:
        fnd = [*self.dbs[cat[0]].getProp(option)]
        
        return fnd
      else:
        return []
    else:
      allAnimal = []
      for animals in self.dbs:
        anims = [*self.dbs[animals].getProp(option)]
        
        allAnimal += anims
      return allAnimal

  def health_count(self):
    allAnims = self.get_animals('total')
    helth = {'healthy':0,'moderate':0,'moderately severe':0,'severe':0}
    for i in allAnims:
      helth[i['status']] += 1
    return helth


  def archive(self,category,animalID):
    cat = self.mapping.get(category)[0]
    dbVal = self.dbs.get(cat,None)
    if dbVal:
      return dbVal.find_and_update({"_id":ObjectId(animalID)},{"archive": True})
    else:
      return False

  def getLastAdded(self):
    latest = []
    cpy = copy.copy(self.dbs)
    cpy.pop('amphibians')
    for animal in cpy.values():
      collectedArr = animal.sortBy('dateAdded',ASCENDING,10,2)
      if len(collectedArr) > 0:
        latest += collectedArr
    return latest