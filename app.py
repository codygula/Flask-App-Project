#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, redirect, flash, url_for
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
import boto3
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

from boto3.dynamodb.conditions import Key, Attr

dbclient = boto3.resource("dynamodb")
table = dbclient.Table("email_list")



#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    # Query database
    # return Users.query.get(int(user_id))
    print("@login_manager.user_loader called")



#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    print("home page entereded!!")
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


# Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    print("!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!login function called")
    form = LoginForm(request.form)
    print("!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!!~!~!~!~!~!~login function still working")
    return render_template("forms/login.html", form=form)


@app.route("/submit/", methods=['POST'])
def move_forward():
    
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!MOVE FORWARD CALLED!!!")
    forward_message = "Moving Forward..."
    form = LoginForm(request.form)
    if request.method=='POST':
        print("login thing!!! in /submit/ ")
   
        
        email = form.name.data
        password = form.password.data

        # if email and password match database: 
   
        print("email = ", email)
        print("password = ", password)
        return render_template('pages/dashboard.html', forward_message=forward_message);


@app.route('/dashboard', methods =["GET", "POST"])
@login_required
def gfg():
    if request.method == "POST":
       
       first_name = request.form.get("fname")
       
       last_name = request.form.get("lname")
       email = request.form.get("email")
       messageNumber = request.form.get("messageNumber")
       
       print("first name = ", first_name)
       print("last name = ", last_name)
       print("number of messages = ", messageNumber)
       print("email = ", email)

       Primary_Column_Name = "email"

       response = table.put_item(
            Item={
                Primary_Column_Name: email,
                "fname": first_name,
                "lname": last_name,
                "messageNumber": messageNumber,
                })
       print(response) 
       print("SUCCESS!") 
    else:
        print("ERROR!")

    return render_template('pages/dashboard.html')
  

@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

