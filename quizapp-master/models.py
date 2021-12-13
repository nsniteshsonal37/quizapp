from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///quiz.db"
app.config["SESSION_PERMANENT"] = True

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

class questions(db.Model):
    __tablename__="question"
    qid = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    subject =db.Column(db.String, nullable=False)
    question =db.Column(db.String, nullable=False)
    option1 = db.Column(db.String, nullable=False)
    option2 = db.Column(db.String, nullable=True)
    option3 = db.Column(db.String, nullable=True)
    option4 = db.Column(db.String, nullable=True)
    answer = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String, nullable=False)
    bcol = db.Column(db.String, nullable=True) 
    marks = db.Column(db.Numeric, nullable=False) 