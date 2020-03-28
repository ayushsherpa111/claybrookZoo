from random import randint
from markupsafe import escape
from flask import Blueprint, render_template, session, url_for,redirect,flash,request,abort
from functools import wraps
import json
from app.users.forms import LoginForm,RegistrationForm,StaffForm
from app.users.helper import Helper,checkSession,assignRole
from app.db.claybrookZoo import users
from app import bcrypt
from app.models.user import User

userDB = Helper(users)
user = Blueprint('user',__name__)

@user.route("/login",methods=["GET","POST"])
def loginUser():
  logForm = LoginForm()
  loginFail = False
  color = ""
  print(request.method)
  if 'email' in session:
    # flash("You are already logged in",'notification is-success')
    return redirect(url_for('home.index'))
  if request.method == "POST":
    if logForm.validate_on_submit():
      userInst = userDB.login({'email':logForm.email.data,'password':logForm.password.data})
      if userInst != None:
        print(userInst)
        flash(f'Welcome! {escape(userInst["username"])}.','notification is-success')
        session['email'] = escape(userInst['email'])
        if userInst.get("role",None):
          session["role"] = escape(userInst["role"])
        return redirect(url_for('home.index' if session['role'] == "Sponsor" else "user.staffHome"))
      else:
        loginFail = True
        color = "#b70606"
  return render_template('login.html',form=logForm,notification=6,fail=loginFail,color=color)



@user.route('/register',methods=["GET","POST"])
def register():
  if 'email' in session:
    return redirect(url_for('home.index'))
  regForm = RegistrationForm()
  if regForm.validate_on_submit():
    userID = userDB.register({'username':regForm.username.data,'password':regForm.password.data,'email':regForm.email.data,'checked': False})
    session['email'] = escape(regForm.email.data)
    session['role'] = "Visitor"
    return redirect(url_for('home.index'))
  elif request.method == "POST":
    flash(f'Failed to create account {regForm.username.data}! ','notification is-danger')
  return render_template('register.html',form=regForm)


@user.route("/logout",methods=["GET","POST"])
def logout():
  if request.method == "GET":
    if "email" in session:
      print(session)
      session.pop('email')
      session.pop('role')
      flash("You have now been logged out","notification is-danger")
      return redirect(url_for('home.index'))
    else:
      flash("You must first Login","notification is-warning")
      return redirect(url_for('home.index'))


@user.route("/staff",methods=["GET"])
def staffHome():
  if checkSession(session,["Admin","Manager","Staff"]):
    return render_template('staff/staff.html',profile="ssg-goku.jpg",total=randint(1,100),newUsers=userDB.get_all_users().count())
  else:
    return redirect(url_for("home.index"))


@user.route("/evaluate",methods=["GET"])
def staffEvaluate():
  if checkSession(session,["Admin"]):
    newUsers = userDB.get_all_users()
    return render_template("staff/evaluate.html",evaluateUsers=newUsers,profile="ssg-goku.jpg")
  else:
    return redirect(url_for("user.staffHome"))

@user.route("/evaluate/<string:email>",methods=["GET","POST"])
def updateStaff(email):
  if checkSession(session,["Admin"]):
    user = userDB.find_by_email(email)
    _id = user['_id']
    currVis = User({'email':user['email'],'username':user['username']})
    editForm = StaffForm()
    if editForm.validate_on_submit():
      currVis = assignRole(editForm.role.data,currVis.__dict__,{'username': editForm.username.data,'role':editForm.role.data,'checked':True})
      return str(currVis.__dict__)
    return render_template("staff/editStaff.html",profile="ssg-goku.jpg",form=editForm,user=currVis)
  else:
    return render_template("staff/staff.html")

