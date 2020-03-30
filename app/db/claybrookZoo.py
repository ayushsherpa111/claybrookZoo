from pymongo import MongoClient, ASCENDING
client = MongoClient("localhost",27017)

db = client.claybrookZoo

aviary = db.Aviary
compound = db.Compounds
aquarium = db.Aquarium
hothouse = db.Hothouse
categories = db.Categories
users = db.Users


index = users.create_index([('email',ASCENDING)],unique=True)