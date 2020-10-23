from flask import Flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('autorewards.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://autorewards-92ae1.firebaseio.com/'
})

ref = db.reference('accounts')
result = ref.get()

accounts = []
if result:
    for key, value in result.items():
        accounts.append((key, value))


app = Flask('__main__')

@app.route("/")
def home():
    string = ""
    for account in accounts:
        string += str(account[0]) + ": " + str(account[1]) + "\n"
    return string

if __name__ == '__main__':
    app.run()

