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

#BluePrints
# from .routes.course_bp import course_bp
# from .routes.competition_bp import class_bp
# from .routes.enrollment_bp import enrollment_bp
from .routes.api_bp import api_bp
app.register_blueprint(api_bp, url_prefix='/api')



