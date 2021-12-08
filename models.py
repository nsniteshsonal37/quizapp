from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///quiz.db"
db = SQLAlchemy(app)


class Users(db.Model):
    # you can even specify the table name with which you are working.
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, unique=True, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), unique = False, nullable=False)

class Admins(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key = True, unique=True, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), unique = False, nullable=False)

class Questions(db.Model):
    __tablename__ ='questions'
    # for true/false questions insert option1 as true and 2 as false.
    id = db.Column(db.Integer, primary_key = True, unique=True, nullable=False)
    question = db.Column(db.String(500), unique=False, nullable=False)
    option1 = db.Column(db.String(200), unique=False, nullable=False)
    option2 = db.Column(db.String(200), unique=False, nullable=False)
    option3 = db.Column(db.String(200), unique=False, nullable=True)
    option4 = db.Column(db.String(200), unique=False, nullable=True)
    answer = db.Column(db.Integer, unique = False, nullable=False)