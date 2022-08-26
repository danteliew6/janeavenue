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

    