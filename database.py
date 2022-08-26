import pyrebase
import my_secrets
import datetime

firebase = pyrebase.initialize_app(my_secrets.get_firebase_config())
auth = firebase.auth()
db = firebase.database()

def add_company(company_details):
    toAdd = {
        "test": {
            "AvgGrowthFundRound": 1,
            "CurrentValuation": 1,
            "FounderSch": "Stanford",
            "Industry": "AI",
            "InitialValuation": 1,
            "LastUpdated": "datetime",
            "NumCompetitors": 1,
            "NumFounders": 1,
            "YearFounded": 2001
            }
        }
    db.child("PrivateCompanies").update(toAdd)
    return True
