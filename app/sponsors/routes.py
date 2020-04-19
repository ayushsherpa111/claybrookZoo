from markupsafe import escape
from bson.objectid import ObjectId
from flask import Blueprint, render_template, request,flash, session, url_for, redirect
from app.users.helper import Helper, InsertAnimal, checkSession
from app.sponsors.forms import ApplyForm, get_all_animals
from app.db.claybrookZoo import users,contract,compound,aviary,hothouse,aquarium
from app.models.roles import Sponsor
from app.users.routes import uploadImage
from app import app
import os

insertAnimal = InsertAnimal({'mammals':Helper(compound),'birds':Helper(aviary),'reptiles':Helper(hothouse),'amphibians':Helper(hothouse),'fishes':Helper(aquarium)})
user = Helper(users)

sponsor = Blueprint('sponsor',__name__)
def getCurrentUser(session):
  return contract.find_one({'sponsor_id': ObjectId(session.get('current_user',None)['_id'])})

@sponsor.route('/apply',methods=["GET","POST"])
def applySponsor():
  try:
    currentUser = user.find_by_email(session.get('current_user',None)['email'])
  except BaseException as e:
    return redirect(url_for('user.loginUser'))
  if checkSession(session,['Visitor']):
    form = ApplyForm()
    form.animal_sponsor.choices = get_all_animals()
    if request.method == "POST":
      if form.signage.data == None:
        flash('Signage Required','notification is-warning')
      else:
        signagePath = uploadImage(form.signage.data,'signage')
        _sponsor = Sponsor({
          'sponsor_id': currentUser['_id'],
          'company_name': escape(form.client_name.data),
          'signage': escape(signagePath),
          'address': escape(form.client_address.data),
          'country':escape(form.client_country.data),
          'city': escape(form.client_city.data),
          'estate': escape(form.client_estate.data),
          'band': escape(form.sponsor_band.data),
          'animal_sponsor':[ObjectId(i) for i in form.animal_sponsor.data],
          'approved':False
        })
        if contract.insert_one(_sponsor.__dict__):
          flash("Your Sponsorship agreement has been submitted!",category="notification is-success")
          return redirect(url_for('home.index'))
        else:
          flash("Failed to submit form","notification is-danger")
    return render_template('apply.html',form=form)
  elif checkSession(session,['Sponsor']):
    sponsorUser = contract.find_one({'sponsor_id':currentUser['_id']})
    form = ApplyForm()
    form.client_name.data = sponsorUser['company_name']
    form.client_address.data = sponsorUser['address']
    form.client_estate.data = sponsorUser['estate']
    form.client_country.data = sponsorUser['country']
    form.client_address.data = sponsorUser['address']
    form.client_city.data = sponsorUser['city']
    form.sponsor_band.data = sponsorUser['band']
    animals_to_sponsor = [i for i in get_all_animals() if i[0] not in sponsorUser['animal_sponsor']]
    form.animal_sponsor.choices = animals_to_sponsor if len(animals_to_sponsor) > 0 else []
    # return str(animals_to_sponsor)
    
    # redirect(url_for("sponsor.sponsorHome")) 
    return render_template('apply.html',form=form)
  else:
    return redirect(url_for("user.loginUser"))

@sponsor.route('/sponsor',methods=["GET"])
def sponsorHome():
  if checkSession(session,["Sponsor"]):
    currentUser = getCurrentUser(session)
    anims = insertAnimal.get_animals('total',{'_id':{'$in':currentUser['animal_sponsor']}})
    return render_template("sponsorDetail.html",animals=anims,sponsor=currentUser)
  else:
    return render_template("sponsorDeals.html")

@sponsor.route("/signageUpdate",methods=["POST"])
def updateSignage():
  if checkSession(session,["Sponsor"]):
    file = request.files['signage']
    currentSponsor = getCurrentUser(session)
    file.save(os.path.join(app.root_path,'static','images','signage',file.filename))
    contract.update_one({'sponsor_id':currentSponsor['sponsor_id']},{'$set':{'signage':file.filename}})
    return redirect(url_for("sponsor.sponsorHome"))