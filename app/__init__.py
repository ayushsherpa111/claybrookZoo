from flask import Flask
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)

load_dotenv(verbose=True)
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
app.hashSec = os.environ["HASH_SEC"]
app.passRounds = int(os.environ["PASS_ROUND"])



from app.main.routes import home
from app.users.routes import user
from app.animals.routes import animal

app.register_blueprint(home)
app.register_blueprint(user)
app.register_blueprint(animal)