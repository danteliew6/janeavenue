from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import not_, func
from src.olympus import db
from datetime import datetime
import json
import functools
from src.olympus.ml_models.knn import KNN
from src.olympus import database

class AthenaApiController():

    def classify_company():
        # Good models: KNN, RF
        knn = KNN()
        print(request.data)
        #user_input = request.form.to_dict()
        user_input = json.loads(request.data.decode('utf-8'))
        classification = knn.classify(user_input,database.get_private_companies())
        print("Final output")
        print(classification)
        database.add_history(user_input,classification["Prediction"])
        return jsonify(classification)

    def avg_successful_companies_metrics():
        return jsonify(database.get_avg_successful_company_metrics())

    def avg_unsuccessful_companies_metrics():
        return jsonify(database.get_avg_unsuccessful_company_metrics())


