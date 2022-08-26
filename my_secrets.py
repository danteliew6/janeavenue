import os

def get_firebase_config():
    config = {
        "apiKey": "AIzaSyAk1wn4ENY7pMSXsEh6hZAU2Dl49UXoDVY",
        "authDomain": "janeavenue-d75a8.firebaseapp.com",
        "databaseURL": "https://janeavenue-d75a8-default-rtdb.asia-southeast1.firebasedatabase.app",
        "projectId": "janeavenue-d75a8",
        "storageBucket": "janeavenue-d75a8.appspot.com",
        "serviceAccount": os.getcwd() + "/janeavenue-d75a8-firebase-adminsdk-34fs5-9b45d9d0c2.json"
    }
    return config
