from flask import Flask, render_template, request, session, redirect, url_for, session
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os

# paperclip
app=Flask(__name__)
app.secret_key = os.urandom(22)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:paperclip@localhost:5433/flaskapp'
db = SQLAlchemy(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
# %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

# User Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    # def __init__(self, name, username, email, password):
    #     self.name = name
    #     self.username = username
    #     self.email=email
    #     self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

# Form classes
class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=6, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')

# class LoginForm(Form):
#     name = StringField('Name', [validators.Length(min=4, max=25)])
#     username = StringField('Username', [validators.Length(min=6, max=25)])
#     email = StringField('Email Address', [validators.Length(min=6, max=35)])
#     password = PasswordField('Password', [
#         validators.DataRequired(),
#         validators.EqualTo('confirm', message='Passwords must match')
#     ])
#     confirm = PasswordField('Confirm Password')


@app.route("/")
def home():
    return render_template('home.html')

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

        if user_count==0 and email_count==0:
            db.session.add(User(name=name, username=username, email=email, password=password))
            db.session.commit()
            return redirect(url_for('login'))

    return render_template("register.html", form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    return render_template('login.html')

if __name__=='__main__':
    app.run(debug=True)
