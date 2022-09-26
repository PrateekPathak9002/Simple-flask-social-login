import os
import re
from flask import Flask, render_template, redirect, url_for,session , request , jsonify
from flask_dance.contrib.google import make_google_blueprint, google
import logging
from flask_login import logout_user, LoginManager
import json
import sqlite3 as sql
from os.path import exists


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

client_id =  "Enter your google client id here"
client_secret = "enter your google client secret here"
app.config['SECRET_KEY']='add a secret key'

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email"]
)

app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/")
def index():
    google_data_local = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        google_data_local = google.get(user_info_endpoint).json()

    session['google_data'] = google_data_local
    return render_template('index.html',
                           fetch_url=google.base_url + user_info_endpoint)

@login_manager.user_loader
def load_user(user_id):

    return User.get(user_id)

@app.route('/login')
def login():
    return redirect(url_for('google.login'))

@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect('/')


    
if __name__ == "__main__":
    app.debug = True
    app.run()

