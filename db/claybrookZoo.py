from pymongo import MongoClient
client = MongoClient("localhost",27017)
db = client.claybrookZoo

birds = db.Birds
mammals = db.Mammals
users = db.Users