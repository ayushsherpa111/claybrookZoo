class Helper:
  def __init__(self,db):
    self.db = db

  def find_by_username(self,username):
    return self.db.find_one({'username':username})
  
  def find_by_email(self,email):
    return self.db.find_one({'email':email})

  def register(self,user):

    return self.db.insert_one(user).inserted_id