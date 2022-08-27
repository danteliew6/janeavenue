import pyrebase
import my_secrets
import datetime

firebase = pyrebase.initialize_app(my_secrets.get_firebase_config())
auth = firebase.auth()
db = firebase.database()

def get_avg_successful_company_metrics():
    return db.child("AvgSuccessfulCompanies").get().val()

def get_avg_unsuccessful_company_metrics():
    return db.child("AvgUnsuccessfulCompanies").get().val()

def get_private_companies():
    return db.child("PrivateCompanies").get().val()

def get_industry():
    return db.child("IndustryMap").get().val()

def add_history(user_input,classification):
    curr = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%f")
    toAdd = {curr:{}}
    ind_dict = get_industry()
    for i,j in user_input.items():
        if i == "Industry":
            toAdd[curr][i] = ind_dict[j]
        else:
            toAdd[curr][i] = j
    toAdd[curr]["Success"] = 1 if classification else 0
    db.child("History").update(toAdd)
    return True
