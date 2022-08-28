from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import not_, func
from src.olympus import db
from datetime import datetime
import json
import functools
import time

class HermesApiController():
    global EXCHANGE_RATE

    EXCHANGE_RATE = {
        "SGD/IDR": 10660,
        "SGD/INR": 57.41,
        "SGD/MYR": 3.2,
        "SGD/PHP": 40,
        "SGD/THB": 25.7,
        "USD/IDR": 14850,
        "USD/INR": 79.5,
        "USD/MYR": 4.4,
        "USD/PHP": 56,
        "USD/THB": 36,
        "SGD/USD": 0.72,
        "USD/SGD" : 1.39
    } 

    # message -> Cost of food and id of who ate
    def getAllInvestments():
        result = db.child("Investments").get()
        return jsonify({
                "message": "Investments Retrieved Successfully",
                "investments": result.val()
            }), 200

    def addDeposit():
        # name - fund name
        # user - user name
        # amount - monetary value in indicated currency
        # currency - currency that user wishes to deposit
        data = request.get_json()

        investment = db.child('Investments').child(data['name']).get().val()

        user_balance = db.child('Investors').child(data['user']).get().val()['Balance'][data['currency']]
        if user_balance < data['amount']:
            return jsonify({
            "message": "Insufficient Balance"
        }), 400
        

        db.child('Investors').child(data['user']).child('Balance').update({data['currency'] : user_balance - data['amount']})


        currency = investment['Currency']
        if currency != data['currency']:
            exchange_rate = EXCHANGE_RATE[currency + '/' + data['currency']]
            amount = data['amount'] / exchange_rate
        else:
            amount = data['amount']

        new_balance = db.child('Investors').child(data['user']).child('Investments').child(data['name']).get().val() + amount
        db.child('Investors').child(data['user']).child('Investments').update({data['name'] : new_balance})
        db.child('Investments').child(data['name']).update({'TotalDeposits': investment['TotalDeposits']+amount})
        
        return jsonify({
            "message": "Deposited Successfully",
            "user": db.child('Investors').child(data['user']).get().val()
        }), 200

    def withdrawDeposit():
        # name - fund name
        # user - user name
        # amount - monetary value in indicated currency
        data = request.get_json()
        investment = db.child('Investments').child(data['name']).get().val()
        currency = investment['Currency']
        curr_deposit = investment['TotalDeposits']

        if curr_deposit < data['amount']:
            return jsonify({
            "message": "Insufficient Balance",
            "investment_details": db.child('Investments').child(data['name']).get().val()
        }), 400

        user = db.child('Investors').child(data['user']).get().val()
        user_balance = user['Balance'][currency]
        user_investment = user['Investments'][data['name']]
        db.child('Investors').child(data['user']).child('Balance').update({currency : user_balance + data['amount']})
        db.child('Investors').child(data['user']).child('Investments').update({data['name'] : user_investment - data['amount']})
        db.child('Investments').child(data['name']).update({'TotalDeposits': curr_deposit-data['amount']})
        # time.sleep(1)

        return jsonify({
            "message": "Withdrawed Successfully",
            "user_details": db.child('Investors').child(data['user']).get().val()
        }), 200

    
    def getUserInvestments(name):
        curr_user = db.child('Investors').child(name).get().val()
        investments = curr_user['Investments']
        balance = curr_user['Balance']
        fund_details = db.child('Investments').get()
        result = {}
        for fund in fund_details.each():
            if fund.val()['Selected']:
                result[fund.key()] = fund.val()
                result[fund.key()]['Invested'] = investments[fund.key()]
                result[fund.key()].pop('TotalDeposits')

            
        return jsonify({
            "message": "User Investments Retrieved",
            "investments": result,
            "balance": balance
        }), 200

    def toggleFundSelection():
        fund_name = request.args.get('fund_name')
        is_selected = db.child('Investments').child(fund_name).get().val()['Selected']
        db.child('Investments').child(fund_name).update({'Selected': not is_selected})
        return jsonify({
            "message": "Toggled"
        }), 200
