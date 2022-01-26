from flask import Flask , render_template, request
import pyodbc
import textwrap
from flask_sqlalchemy import SQLAlchemy
import urllib.parse 



# Configure Database URI: 
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:database-server-name.database.windows.net;DATABASE=database-name;UID=Admin-name;PWD=Password@123")


# initialization

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# extensions
db = SQLAlchemy(app)
class Appointment_db(db.Model):
    sno = db.Column(db.Integer, primary_key = True,autoincrement=True)
    fname = db.Column(db.String(50), nullable = False)
    lname = db.Column(db.String(50),nullable = False)
    phone1 = db.Column(db.String(12),nullable = False)
    mail = db.Column(db.String(100),nullable = False)
    bdate = db.Column(db.DateTime,nullable = False)
    visit = db.Column(db.String(50),nullable = False)
    date_ = db.Column(db.DateTime,nullable = False)
    visit_time = db.Column(db.String(60),nullable = False)
    physician = db.Column(db.String(50),nullable = False)
    reason_for_visit = db.Column(db.String(200),nullable = False)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.fname} - {self.lname} - {self.date_} - {self.visit_time}"

class bloodtest_db(db.Model):
    sno = db.Column(db.Integer, primary_key = True,autoincrement=True)
    fname = db.Column(db.String(50), nullable = False)
    lname = db.Column(db.String(50),nullable = False)
    phone1 = db.Column(db.String(12),nullable = False)
    mail = db.Column(db.String(100),nullable = False)
    bdate = db.Column(db.DateTime,nullable = False)
    visit = db.Column(db.String(50),nullable = False)
    date_ = db.Column(db.DateTime,nullable = False)
    visit_time = db.Column(db.String(60),nullable = False)
    address = db.Column(db.String(100),nullable = False)
    city = db.Column(db.String(50),nullable = False)
    pincode = db.Column(db.Integer,nullable = False)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.fname} - {self.lname} - {self.date_} - {self.visit_time}"

db.create_all()
@app.route("/",methods=['GET','POST'])
def index():
   
    return render_template('index.html')


@app.route("/appointment")
def appointment():

    
    return render_template('appointment.html')


@app.route("/documents")
def documents():
   
    
    return render_template('Appointment_details.html')

@app.route("/HealthCheckUpForm",methods=['GET','POST'])
def HealthCheckUpForm():
    return render_template('HealthCheckUpForm.html')

@app.route("/BloodTestForm") 
def BloodTestForm():
    
    
    return render_template('BloodTestForm.html')

@app.route("/HealthCheckUpformsubmit",methods=['POST'])
def HealthCheckUpformsubmit():
    
    if request.method == 'POST':
       fname =  request.form.get('fname')
       lname =  request.form.get('lname')
       phone1 = request.form.get('phone1')
       email = request.form.get('phone2')
       bdate = request.form.get('bdate')
       visit =  request.form.get('visit')
       date = request.form.get('date')
       visit_time = request.form.get('visit_time') 
       physician = request.form.get('physician')
       reason_for_visit = request.form.get('reason_for_visit')
       appointment_db = Appointment_db(fname =fname,lname =lname ,phone1 = phone1,mail = email,bdate = bdate,visit = visit,date_ = date,visit_time = visit_time,physician = physician,reason_for_visit = reason_for_visit)
       db.session.add(appointment_db)
       db.session.commit()
    allappointment = Appointment_db.query.all()
    
    return render_template('Thank_You_appointment.html',allappointment=allappointment,visit_time =visit_time,date = date ,physician =physician)

@app.route("/BloodTestformsubmit",methods=['POST'])
def BloodTestformsubmit():
    if request.method == 'POST':
       fname =  request.form.get('fname')
       lname =  request.form.get('lname')
       phone1 = request.form.get('phone1')
       email = request.form.get('phone2')
       bdate = request.form.get('bdate')
       visit =  request.form.get('visit')
       date = request.form.get('date')
       visit_time = request.form.get('visit_time') 
       address = request.form.get('address')
       city = request.form.get('City')
       pincode = request.form.get('pincode')

       Bloodtest_db = bloodtest_db( fname = fname, lname = lname ,phone1 = phone1,mail = email,bdate = dbate,visit = visit,date_ = date,visit_time = visit_time,address = address,city= city,pincode = pincode)
       db.session.add(Bloodtest_db)
       db.session.commit()
    allbloodtest = Bloodtest_db.query.all()

    return render_template('Thank_You_bloodtest.html',allbloodtest = allbloodtest,fname =fname,lname=lname,visit_time =visit_time,date=date, address=address)

@app.route("/healthAppointmentdetails") 
def healthAppointmentdetails():
  
    return render_template('HealthCheckUp-details.html')

@app.route("/bloodAppointmentdetails")
def bloodAppointmentdetails():
    
    return render_template('bloodtest-details.html')


@app.route("/checkdetailshealth",methods=['POST'])
def checkdetailshealth():
    if request.method == 'POST':
       email_given =  request.form.get('mail')
    allappointment = Appointment_db.query.all()
    a = Appointment_db.query.filter_by(mail=email_given).first()
    return render_template('showbooking.html',a =a)

@app.route("/checkdetails_blood",methods=['POST'])
def checkdetails_blood():
    if request.method == 'POST':
       email_given =  request.form.get('mail')
    allbloodtest = bloodtest_db.query.all()
    a = bloodtest_db.query.filter_by(mail=email_given).first()
    return render_template('showbooking.html',a = a) 



if __name__ == "__main__":
    app.run(debug=True)
