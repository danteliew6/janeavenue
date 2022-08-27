from crypt import methods
import json
from flask import Flask, render_template, jsonify, flash, request
from flask_cors import CORS
from ml_models.knn import KNN
import database

app = Flask(__name__)
CORS(app)
app.config.from_object('config')
knn = KNN()

@app.route("/api/athena/classify",methods=["POST"])
def classify_company():
    # Good models: KNN, RF
    user_input = request.form.to_dict()
    classification = knn.classify(user_input,database.get_private_companies())
    database.add_history(user_input,classification)
    return jsonify("Predicted Successful") if classification else jsonify("Predicted Unsuccessful")

@app.route("/api/athena/avgsuccessfulmetrics")
def avg_successful_companies_metrics():
    return jsonify(database.get_avg_successful_company_metrics())

@app.route("/api/athena/avgunsuccessfulmetrics")
def avg_unsuccessful_companies_metrics():
    return jsonify(database.get_avg_unsuccessful_company_metrics())

@app.route("/api/athena/test")
def test_api():
    return jsonify(True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)