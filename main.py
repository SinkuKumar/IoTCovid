from flask import Flask, render_template, request
from pymongo import MongoClient
import pprint

app = Flask(__name__)

client = MongoClient(
    'mongodb+srv://sinku:0w7LMEe77eFQn3KX@base.ogkxi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true')

""" Database Connection Check
db = client.test_database
print("DB Details")
print(db)
"""


def readUser():
    covid = client['covid']
    print("Database")
    print(type(covid))
    users = covid['users']
    print("Users")
    print(type(users))
    print(users.count_documents({}))
    for user in users.find():
        print(user)


def nextID():
    covid = client['covid']
    users = covid['users']
    idList = []
    for userid in users.find():
        idList.append(userid['_id'])
    print(idList)
    currID = max(idList)
    print(currID)
    return currID


@app.route('/')
def index():
    return render_template('home.html', name="Dashboard")


@app.route('/patient', methods=["GET", "POST"])
def patient():
    if request.method == "POST":
        name = request.form.get('userName')
        age = request.form.get('userAge')
        oxy = 50
        temp = 37
        currID = nextID()
        data = {
            "_id": currID + 1,
            "name": name,
            "age": age,
            "oxy": oxy,
            "temp": temp,
            "pres": "",
            "med": ""
        }
        covid = client['covid']
        userData = covid.users
        userData.insert_one(data)

    return render_template('user.html', name="User's Dashboard")


@app.route('/doctor', methods=["GET", "POST"])
def doctor():
    if request.method == "POST":
        prescription = request.form.get('prescription')
        medicines = request.form.get('medicines')
        covid = client['covid']
        users = covid['users']
        currID = nextID()
        user = users.find_one({"_id": currID})
        fil = {'_id':currID}
        docUp = {"$set": { 'pres': prescription, 'med': medicines}}
        users.update_one(fil, docUp)
    covid = client['covid']
    users = covid['users']
    currID = nextID()
    user = users.find_one({"_id": currID})
    name = user['name']
    age = user['age']
    temp = user['temp']
    oxy = user['oxy']
    pres = user['pres']
    med = user['med']
    return render_template('doctor.html', name="Doctor's Dashboard", patientName=name, patientAge=age, patientTemp=temp,
                           patientOxy=oxy, prescription=pres, medicine=med)


if __name__ == '__main__':
    app.run(debug=True)
