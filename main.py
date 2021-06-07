from flask import Flask, request,redirect,url_for,jsonify
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
app = Flask(__name__)
client =MongoClient("mongodb://localhost:27017/")
db=client.todo # db name

@app.route("/")
def display():
    return "welcome to this page"

@app.route("/view")
def view():
    _item=list(db.tododb.find({}))
    #items=dict[x for x in _item]
    return json.dumps(_item,default=json_util.default)
@app.route("/count")
def count():
    y=str(db.tododb.find().count())
    return y

@app.route("/find/<id>")
def find(id):
    x=list(db.tododb.find({"_id":id}))
    return json.dumps(x)

@app.route('/manual_add', methods=['GET', 'POST'])
def manual_add():
    data = []
    if request.method == 'POST':
        data = dict(_id='10', name='maximum', email='maximum@gmail.com1')
        db.tododb.insert_one(data)
        # response = jsonify(data)
        # response.status_code = 202

        return data # Returns the HTTP response
    else:
        data = dict(id='none', name='none', email='none')
        # response = jsonify(data)
        # response.status_code = 406

        return data # Returns the HTTP response

@app.route("/add",methods=["POST"])
def add():

        data = request.get_json()   # plse give every key in string format
       # data = data["data"]
       #  id = data["_id"]
       #  name = data["name"]
       #  email = data["email"]
        db.tododb.insert_one(data)
        return "data added successfully"  # jsonify({"your data" :"successfully added","id" :id ,"name" : name ,"email":"email"})

@app.route("/delete/<id>",methods=["DELETE"])
def delete(id):
    if request.method == "DELETE":
        db.tododb.delete_one({"_id":id})
        return ("deleted the id {} data successfully".format(id))

@app.route("/search/<name>")
def search(name):
    if request.method=="GET":
        #ab=db.tododb.find({email: /^name/})
        ab=list(db.tododb.find({"phone_no": {'$regex': name}}))
        return json.dumps(ab)

if __name__ == '__main__':
    app.run(debug = True)