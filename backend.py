from flask import Flask, render_template, request, session, redirect, url_for, flash
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
import googlemaps
import json
#Selenium

# paperclip
app=Flask(__name__)
app.secret_key = os.urandom(22)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:paperclip@localhost:5433/flaskapp'
db = SQLAlchemy(app)

def add(a, b):
    return a+b

# User Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    username = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username

# Form classes
class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=6, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.Length(min=6, max=35),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=6, max=25)])
    password = PasswordField('Password', [validators.InputRequired()])

@app.route("/")
def go_home():
    return render_template("home.html")

@app.route("/home", methods = ['GET', 'POST'])
def home():
    # if request.method == 'POST':
    #     gmaps = googlemaps.Client(key ='AIzaSyAYRrbU6ZFTgq7E_WCkRhDjxU0JueH38mg')
    #     marker = request.form.get("address")
    #     # print(marker)
    #     geo_marker = gmaps.geocode(marker)
    #     if geo_marker:
    #         geo_dict = geo_marker[0]
    #         geometry = geo_dict['geometry']['location']
    #
    #     return render_template('home.html', marker = geometry)

    return render_template('home.html')

# Get it to pass invalid data and try handling the error, and doesnt crash the server
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if request.method =="POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        user_count = User.query.filter_by(username=username).count()
        email_count = User.query.filter_by(email=email).count()

        # Doing a test
        if user_count==0 and email_count==0:
            try:
                db.session.add(User(name=name, username=username, email=email, password=password))
                db.session.commit()
                flash("You Are Registered and Can Log In")
            except:
                flash("Something went wrong")
            return redirect(url_for('login'))
        else:
            flash("Username or Email Already in Use")
    return render_template("register.html", form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    session.clear()
    form= LoginForm(request.form)
    if request.method=='POST' and form.validate():
        username = form.username.data
        password = form.password.data
        # sha256_crypt.verify(password, result[0])

        find_username = User.query.filter_by(username=username).first()
        if find_username == None:
            flash("Invalid Username")
        else:
            user_row = User.query.filter_by(username=username).first()
            if sha256_crypt.verify(password, user_row.password):
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('home'))

    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
