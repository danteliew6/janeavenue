from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import pyrebase
import my_secrets
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app, origins=['*', 'http://localhost:8080'])
app.config.from_object('config')

def compoundUserInterest(investment, rate):
    users = db.child('Investors').get()
    for user in users.each():
        name = user.key()
        details = user.val()
        current_balance = details['Investments'][investment]
        current_balance *= (1 + rate)
        db.child('Investors').child(name).child('Investments').update({investment : current_balance})

def compoundInterest():
    print("Starting Compound Interest Job")
    result = db.child("Investments").get()
    for investment in result.each():
        name = investment.key()
        investment = investment.val()
        curr_deposit = investment['TotalDeposits']
        curr_deposit *= (1 + investment['Interest'])
        db.child('Investments').child(name).update({'TotalDeposits': curr_deposit})
        compoundUserInterest(name, investment['Interest'])

    print("Completed Compound Interest Job")


sched = BackgroundScheduler(daemon=True)
sched.add_job(compoundInterest,'interval',minutes=1)
sched.start()

firebase = pyrebase.initialize_app(my_secrets.get_firebase_config())
auth = firebase.auth()
db = firebase.database()

#BluePrints
# from .routes.course_bp import course_bp
# from .routes.competition_bp import class_bp
# from .routes.enrollment_bp import enrollment_bp
from .routes.api_bp import api_bp
CORS(api_bp)
app.register_blueprint(api_bp, url_prefix='/api')



