from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import pyrebase
import my_secrets

app = Flask(__name__)
CORS(app)
app.config.from_object('config')


firebase = pyrebase.initialize_app(my_secrets.get_firebase_config())
auth = firebase.auth()
db = firebase.database()



