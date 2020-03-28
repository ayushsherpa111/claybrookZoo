from random import randint
from flask import Blueprint,session,url_for,render_template

home = Blueprint('home',__name__)


@home.route('/')
@home.route('/index')
def index():
  statics = url_for('static',filename="images")
  return render_template('home.html',feature=f"{statics}/caw.jpg",notification=randint(1,10),banner=True,title="Home")

