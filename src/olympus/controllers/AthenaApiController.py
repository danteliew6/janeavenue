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
        user_input = request.form.to_dict()
        classification = knn.classify(user_input,database.get_private_companies())
        database.add_history(user_input,classification)
        return jsonify("Predicted Successful") if classification else jsonify("Predicted Unsuccessful")

    def avg_successful_companies_metrics():
        return jsonify(database.get_avg_successful_company_metrics())

    def avg_unsuccessful_companies_metrics():
        return jsonify(database.get_avg_unsuccessful_company_metrics())


