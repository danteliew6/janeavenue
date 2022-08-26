from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import not_, func
from src.olympus import db
from datetime import datetime
import json
import functools

class HermesApiController():
    
    # message -> Cost of food and id of who ate
    def getAllInvestments():
        result = db.child("Investments").get()
        return jsonify({
                "message": "Investments Retrieved Successfully",
                "investments": result.val()
            }), 200

    def addDeposit():
        data = request.get_json()
        curr_deposit = db.child('Investments').child(data['name']).get()
        curr_deposit = curr_deposit.val()
        curr_deposit = curr_deposit['TotalDeposits']
        db.child('Investments').child(data['name']).update({'TotalDeposits': curr_deposit+data['deposit']})
        return jsonify({
            "message": "Deposited Successfully",
            "investment_details": db.child('Investments').child(data['name']).get().val()
        }), 200