from flask import Flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('autorewards.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://autorewards-92ae1.firebaseio.com/'
})

app = Flask('__main__')

@app.route("/")
def home():
    ref = db.reference('accounts')
    result = ref.get()

    accounts = []
    if result:
        for key, value in result.items():
            accounts.append((key, value))
    string = ""
    for account in accounts:
        string += "<p>" + str(account[0]) + ": " + str(account[1]) + "</p>"
    return string

if __name__ == '__main__':
    app.run()

