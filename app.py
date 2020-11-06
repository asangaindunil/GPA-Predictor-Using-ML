from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_mysqldb import MySQL
from sqlalchemy.orm import sessionmaker
from sqlalchemy_batch_inserts import enable_batch_inserting

from kanpai import Kanpai
import jwt
import datetime
import pickle
from functools import wraps
app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'studymatesliit' 

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:Asanga@123@localhost/student_helper'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
Session = sessionmaker()
Session.configure(bind='mysql://root:Asanga@123@localhost/student_helper')

session = Session()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Asanga@123'
app.config['MYSQL_DB'] = 'student_helper'
mysql = MySQL(app)
model = pickle.load(open('gpa_pred_model.pkl','rb'))
model_database = pickle.load(open('database_pred_model.pkl','rb'))
model_genarel = pickle.load(open('genarel_pred_model.pkl','rb'))
model_programming = pickle.load(open('programming_pred_model.pkl','rb'))
model_networking = pickle.load(open('networking_pred_model.pkl','rb'))

db = SQLAlchemy(app)
class Subjects(db.Model):
    __tablename__="subject"
    id = db.Column('id',db.Integer,primary_key=True)
    name = db.Column('name',db.Unicode)
    year = db.Column('year',db.Unicode)
    semester = db.Column('semester',db.Unicode)
    def __init__(self,id, name):
        self.name = name

class SubjectMarks(db.Model):
    __tablename__="student_marks"
    id = db.Column('id',db.Integer,primary_key=True)
    subject_id = db.Column('subject_id',db.Unicode)
    student_it = db.Column('student_it',db.Unicode)
    marks = db.Column('marks',db.Unicode)
    

    # def __init__(self, student_it, subject_id, marks):
    #     self.subject_id = subject_id
    #     self.student_it = student_it
    #     self.marks = marks 
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing'}),403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()

        except:
            return jsonify({'message' : 'Token is invalid'}),403    
    
        return f(current_user,*args, **kwargs)  
    return decorated    

@app.route('/')     
def index():    
    return 'Welcome to Study Helper backend'    
    
@app.route('/unprotected')  
def unprotected():  
    return jsonify({'message' : 'anyone can view'})     
    
@app.route('/protected')    
@token_required     
def protected():
    return jsonify({'message' : 'This is private'})

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required!"'})

    if auth and auth.password == 'password':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow()+ datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Unauthorized Login!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


studentValidationSchema = Kanpai.Object({
 "name"    : Kanpai.String().trim().required("Name is required").max(20,'Maximum allowed length is 20'),
 "indexno"    : Kanpai.String().trim().required("Index Number is required").max(10, 'Maximum allowed length is 10'),
 "nic"    : Kanpai.String().trim().required("NIC is required"),
 "email" : Kanpai.Email().required(),
 "semester": Kanpai.String().required("Semester is required")
})

subjectValidationSchema = Kanpai.Object({
 "student_id"    : Kanpai.String().trim().required("Name is required").max(20,'Maximum allowed length is 20'),
 "res"    : Kanpai.String().trim().required("Index Number is required").max(10, 'Maximum allowed length is 10'),
 
})

@app.route('/create-student', methods=['POST'])
def create_student():
    
    req_data  = request.get_json()
    validation_result = studentValidationSchema.validate(req_data)

    if validation_result.get('success', False) is False:
        return jsonify({
        "status" : "Error",
        "errors" : validation_result.get("error")
        })
    
    
    name = req_data['name']
    index_number = req_data['indexno']
    nic = req_data['nic']
    email = req_data['email']
    academic_year_sem = req_data['semester']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `students`(`name`, `indexno`, `nic`, `email`, `semester`, `password`, `status`) VALUES (%s, %s, %s, %s, %s,%s,%s)",(name,index_number,nic,email,academic_year_sem,nic,'0'))
    mysql.connection.commit()
    return jsonify({
    'code' : 200,
    'status' : 'Success'
    })

@app.route('/get-subjects')
def getSubjects():
    subjectArr = [] 
    subjects = Subjects.query.all()
    for subject in subjects:
        sub = {"id": subject.id, "subject": subject.name, "year": subject.year, "semester":subject.semester}  
        subjectArr.append(sub)
    return jsonify(subjectArr)

@app.route('/check-result-already-added/<studentID>')
def checkResultExist(studentID) :
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `student_marks` WHERE student_it =  %s",[studentID])
    data = cur.fetchall()
    #mysql.close()
    print(cur.rowcount)
    if(cur.rowcount >= 25):
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("SELECT `predicted_gpa` FROM `student_gpa_pred_result` WHERE student_id =  %s",[studentID])
        result = cur.fetchone()
        result = result[0]
        cur.close()

    else:
        cur.close()
        result = False

    #return jsonify( {
    #'code' : 200,
    #'status' : 'Success',
    #'result' : result
    #})
    return jsonify(result)


@app.route('/create-student-result', methods=['POST'])
def createStudentResult():
        resultsArr = [] 

        req_data  = request.get_json()
        for result in req_data['results']:
             m = SubjectMarks()
             m.student_it = req_data["student_id"]
             m.subject_id = result["subject_id"]
             m.marks = result["marks"]
             mar = {"student_it":req_data["student_id"],"subject_id": result["subject_id"],"marks": result["marks"]}  
             db.session.add(m)

             print(mar)
             resultsArr.append(m.marks)      

        predResult = predict_gpa(resultsArr)  
        print(predResult)   
        
        try:        
            db.session.flush()
            db.session.commit()
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO `student_gpa_pred_result`(`student_id`, `predicted_gpa`) VALUES (%s,%s)",(req_data['student_id'], predResult[0]))
            mysql.connection.commit()
            cur.close()
            return jsonify({'code' : 200,  'status' : 'Success', 'result' : predResult[0]})

        except:
            db.session.rollback()
            return jsonify({'code' : 400, 'status' : 'Failed'})

@app.route('/create-expected-result-adding', methods=['POST'])
def createExpectedResult():
    req_data  = request.get_json()
    #Scalculate_expected_results(req_data['student_id'], req_data['expected_gpa'])
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `student_expect_gpa`(`student_id`, `expected_gpa`) VALUES (%s,%s)",(req_data['student_id'], req_data['expected_gpa']))

    mysql.connection.commit()
    return jsonify({
    'code' : 200,
    'status' : 'Success',
    'result' : {
        'HCI':'A',
        'IAS':'C',
        'DA':'D',
        'BMIT':'C'
    }
    
    })

def calcuzlate_expected_results(student_id,expected_gpa):
    cur = mysql.connection.cursor()
    cur.execute("SELECT `predicted_gpa` FROM `student_gpa_pred_result` WHERE `student_id` = %s",[student_id])
    predicted_gpa = cur.fetchone()
    print(predicted_gpa[0])
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT `marks` FROM `student_marks` WHERE `student_it` = %s ORDER BY `subject_id` Limit 25",[student_id])
    past_marks = [res[0] for res in cur.fetchall()]
    print(past_marks)
    cur.close()
    Grade = {'A+': 95,'A': 85,'A-':77,'B+':72,'B':67,'B-':62,'C+':57,'C':50,'C-':42,'D':37,'D+':32,'E':15,'PC':50,'AB':0,'IC':0,'F':0,'R':0,'WH':0,'W':0} 
    newbie = []
    # for x in range(25):
    #     newbie[x] = [Grade[item] for item in dataset[x]] 
    newbie = [Grade[item] for item in past_marks]
    pred = model_programming([newbie[0],newbie[1],newbie[2],newbie[3],newbie[4],newbie[5],newbie[6],newbie[7],newbie[8]])
    print(newbie)
    return predicted_gpa


def predict_gpa(dataset):
    Grade = {'A+': 95,'A': 85,'A-':77,'B+':72,'B':67,'B-':62,'C+':57,'C':50,'C-':42,'D':37,'D+':32,'E':15,'PC':50,'AB':0,'IC':0,'F':0,'R':0,'WH':0,'W':0} 
    newbie = []
    # for x in range(25):
    #     newbie[x] = [Grade[item] for item in dataset[x]] 
    newbie = [Grade[item] for item in dataset]
    print(newbie)
    prediction = model.predict([newbie])
    #print(prediction)

    return prediction
    

@app.route('/check-result-expected/<studentID>')
def checkExpectedResultExist(studentID) :
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `student_result_expect_gpa` WHERE student_id =  %s",[studentID])
    data = cur.fetchall()
    #mysql.close()
    result = False
    if(cur.rowcount == 0):
        result = False
    else:
        result = {
        'HCI':'A',
        'IAS':'C',
        'DA':'D',
        'BMIT':'C'
    }

    return jsonify({
        'code' : 200,
        'status' : 'Success',
        'result' : result
        })
#  @app.route('/create-student', methods=['POST'])
  
# @app.route('/student-mark', methods=['POST'])
# def get    



if __name__=='__main__':
    app.run(host='0.0.0.0')

        
