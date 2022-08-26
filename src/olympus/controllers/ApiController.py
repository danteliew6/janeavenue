from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from ..models.User import User
from flask_cors import CORS
from sqlalchemy import not_, func
from src.olympus import db
from datetime import datetime
import json
import functools

class ApiController():
    
    # message -> Cost of food and id of who ate
    def two():
        data = request.get_json()
        # bid = request.args.get('bid')
        message = data['message']
        message = message.split(',')
        cost = int(message[0])
        people = message[1:]
        avg_cost = cost / len(people)
        for person in people:
            user = User.query.filter(User.id == person).first()
            user.to_pay += avg_cost
            db.session.commit()
        

        return jsonify({
                "message": "Costs added successfully",
                "next": ""
            }), 200