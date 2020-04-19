from app.db.claybrookZoo import categories

class Category:
  db = categories

  @classmethod
  def get_all(cls):
    cats = []
    for i in cls.db.find({}):
      img = i['category'].lower() + "/" + i['profile']
      cats.append({'category':i['category'].capitalize(),'profile':img})
    return cats