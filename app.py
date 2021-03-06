from datetime import datetime, timedelta
import hashlib, jwt, werkzeug
import logging

from flask.cli import DispatchingApp

from flask.json import jsonify
from flask import app, request, make_response,Response
from flask.templating import render_template
from models import *
from functools import wraps
from flask import Flask, render_template, jsonify, request,redirect,flash,session
from models import *


logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


# If you programmatically wants to create the database then use create_all() function
db.create_all()
db.session.commit()

app.config['SECRET_KEY'] = 'torfabrik'

session = {}
session['answers'] = {}

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('jwt') 
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            print(token)
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
            print(data)
            current_user = data['user']

        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated

#First Flask code to display Hello World
@app.route('/test')
def hello_world():
    return "Hello World"


#Create an index page
@app.route('/')
def indexPage():
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    return render_template('index.html')


#creating login page
@app.route('/login/', methods=['GET', 'POST'])
def loginPage():
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    return render_template('login.html')


#creating register page
@app.route('/register/')
def registerPage():
    # app.logger.info('Info level log')
    # app.logger.warning('Warning level log')
    return render_template('register.html')

@app.route('/registersuccess', methods=['POST'])
def registerSuccess():
    # app.logger.info('Info level log')
    # app.logger.warning('Warning level log')
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        #hashing the password before storing
        hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        hashedPassword = hashedPassword.hexdigest()
        print(name+" "+email+" "+hashedPassword)
        entry = Users(name=name,email=email,password=hashedPassword)
        db.session.add(entry)
        db.session.commit()
    return make_response(redirect('/login'))

#creating admin login page
@app.route('/admin/')
def adminPage():
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    return render_template('admin.html')

@app.route('/adminsuccess', methods=['GET', 'POST'])
def adminSucess():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #hashing the input and comparing the hash
        # hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        # hashedPassword = hashedPassword.hexdigest()
        result = db.session.query(Admins).filter(Admins.email==email, Admins.password==password)
        print(email)
        print("pass1")
        print(password)
        for row in result:
            if (len(row.email)!=0):
                print(row.email)
                token = jwt.encode({'user':row.email, 'exp': datetime.utcnow()+timedelta(minutes=15)}, app.config['SECRET_KEY'])
                token= token.decode('utf-8')
                print("Token ",token)
            return render_template('adminAdd.html')
    return make_response('could not verify', 401, {'WWW-Authenticate':'Basic="Login Required"'})


#creating admin login page
@app.route('/admin/add')
def adminAddPage():
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    return render_template('adminAdd.html')


@app.route('/loginsuccess', methods=['GET', 'POST'])
def loginSucess():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #hashing the input and comparing the hash
        hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        hashedPassword = hashedPassword.hexdigest()
        result = db.session.query(Users).filter(Users.email==email, Users.password==hashedPassword)
        print("db pass")
        print(Users.password)
        print("Hash")
        print(hashedPassword)
        for row in result:
            if (len(row.email)!=0):
                print(row.email)
                token = jwt.encode({'user':row.email, 'exp': datetime.utcnow()+timedelta(minutes=15)}, app.config['SECRET_KEY'])
                token= token.decode('utf-8')
                print("Token ",token)
                # return make_response(jsonify({'jwt' : token}), 201)
        # return render_template('dashboard.html')
        return make_response(redirect('/dashboard'))

    return make_response('could not verify', 401, {'WWW-Authenticate':'Basic="Login Required"'})


@app.route('/admin/addSuccess', methods=['POST'])
def addSuccess():
    # app.logger.info('Info level log')
    # app.logger.warning('Warning level log')
    if request.method == "POST":
        subject=request.form.get('sub')
        type= request.form.get('Qtype')
        question = request.form.get('Que')
        option1 = request.form.get('opt1')
        option2 = request.form.get('opt2')
        if  type=='mcq':
            option3 = request.form.get('opt3')
            option4 = request.form.get('opt4')
            answer = request.form.get('ansA')
        else:
            option3 = None
            option4 = None
            answer = request.form.get('tf')
        marks= request.form.get('marks')
        entry = questions(subject=subject,question=question,option1=option1,option2=option2,option3=option3,option4=option4, answer=answer, type=type,marks=marks)
        db.session.add(entry)
        db.session.commit()
    return make_response(redirect('/admin/'))




@app.errorhandler(werkzeug.exceptions.BadRequest)
def badRequest(e):
    # app.logger.info('Info level log')
    # app.logger.warning('Warning level log')
    return "Bad request", 400
app.register_error_handler(400, badRequest)

@app.errorhandler(404)
def notFound(e):
    return "Page not found", 404
app.register_error_handler(404,notFound )


# Change color of buttons of the questions which are attempted. 
def setStatus(qlist):
    questionAttempt = {}
    print(qlist, session['answers'])

    for i in session['answers'].keys():
        questionAttempt[i]=session['answers'][i]
 
    print(qlist, questionAttempt, session['answers'])
    for row in qlist:
        if str(row.qid) in questionAttempt.keys():
            row.bcol='green'  

@app.route('/dashboard')
# @token_required
def dashboard(): # http://127.0.0.1:8000/dashboard?jwt=def index():
    session['result']=""
    session['answers'] = {}
    subjectList=questions.query.with_entities(questions.subject).distinct()
    return render_template("subject.html",subList=subjectList)  

@app.route('/quiz', methods=["POST"])
def quiz(): 
    
    subject= request.form.get('sub')
    
    questList=questions.query.filter_by(subject=subject).all()
    
    total_marks = 0

    for q in questList:
        total_marks += q.marks

    # Setting Total Marks in the session.
    session['total_marks']=total_marks

    question=questions.query.filter_by(subject=subject).first()
    return render_template("dashboard.html",questList=questList, quest=question) 

# This API is used to render the question when question number button is clicked.   
@app.route("/showQuest/<string:subject>,<int:qid>")
def showQuest(subject,qid):
    questList=questions.query.filter_by(subject=subject).all()

    question=questions.query.filter_by(qid=qid).first()

    print("show Quest", session['answers'])
    setStatus(questList)

    return render_template("dashboard.html",questList=questList, quest=question)  
    
# This API will save the answer of every question.
@app.route('/saveAns',methods=["POST"]) 
def saveAns():
    qid=request.form.get('qid')
    ans=request.form.get('answer')
    sub=request.form.get('subject')
    #update the question id and its selected answer in session variable result
    if ans != None:
        session['answers'][qid] = ans

    questList=questions.query.filter_by(subject=sub).all()
    print("Save Ans: ",questList)
    setStatus(questList)
    question=questions.query.filter_by(qid=qid).first()
    return render_template("dashboard.html",questList=questList, quest=question)  

# This route is basically used to  show the result of the Quiz  
@app.route("/result")
def result():
    #calculate result
    count=0
    recv_marks = 0

    for i in session['answers'].keys():
        question=questions.query.filter_by(qid=i).first()
        if question.answer == int(session['answers'][i]):
            count += 1
            recv_marks += question.marks

    text='You have '+ str(count)+ ' correct questions out of '+ str(len(session['answers']))+ ' questions and marks are ' + str(recv_marks) + " out of " + str(session['total_marks']) # set the result statement
    return render_template("result.html",txt=text) 



if __name__ == "__main__":
    app.run(debug=True, port=8000)