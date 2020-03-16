from app import app
from datetime import datetime
from flask import request,redirect,url_for, session, render_template,flash
from db.claybrookZoo import birds,mammals,users
from app.utils import helper
from markupsafe import escape
from models.admin import Admin
from dotenv import load_dotenv
import os
from app.forms.register import LoginForm,RegistrationForm

userDB = helper.Helper(users)

load_dotenv(verbose=True)
app.secret_key = os.environ["COOKIE_SEC"]
app.hashSec = os.environ["HASH_SEC"]

@app.route("/login",methods=["GET","POST"])
def loginUser():
  if 'username' in session:
      redirect(url_for('index'))
  if request.method == "GET":
    return render_template('home.html',posts={'name':"Ayush"},title="BRUH")
  if request.method == "POST":
    body = request.json
    if body["username"] == "Admin" and body["password"] == "Admin":
      session['username'] = body['username']
      print(session)
      return f"You are now logged in as {escape(session['username'])}"
    else:
      return "BRUH WTF WAS THAT SHIT"

@app.route('/')
@app.route('/index')
def index():
  return render_template('home.html',posts={'name':"Ayush"})


  


@app.route('/bird',methods=['GET','POST'])
def findAnimal():
  if request.method == "POST":
    print(request.json)
    return f"You sent {request.data}"
  brb = birds.find()
  brbs = []
  for bb in brb:
    bb.update({"_id":str(bb["_id"])})
    brbs.append(bb)
    # print(brbs)
  return render_template('birds.html',birds=brbs)

@app.route('/register',methods=["GET","POST"])
def register():
  regForm = RegistrationForm()
  if regForm.validate_on_submit():
    userID = userDB.register({'username':regForm.username.data,'password':regForm.password.data,'email':regForm.email.data})
    flash(f'Account created for {userID}! ','notification is-primary')
    return redirect(url_for('index'))
  elif request.method == "POST":
    print(regForm.username.errors)
    flash(f'Failed to create account {regForm.username.data}! ','notification is-danger')
  return render_template('register.html',form=regForm)
