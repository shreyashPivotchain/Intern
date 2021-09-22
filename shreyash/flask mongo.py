from flask_pymongo import pymongo
import flask
from pymongo import MongoClient

app = flask.Flask(__name__)

import json
from flask import Flask, request, jsonify


client = MongoClient('localhost', 27017)
db = client['database']
collection = db['collection']
 



@app.route('/distinct', methods=['GET'])

def distinct_f () :

 mydoc = collection.distinct('birds')
 
 
 return flask.jsonify([mydoc])


if __name__ == "__main__":
    app.run(debug=True)










@app.route('/findvisit', methods=['POST'])




def findvisit():

  data = request.get_json()


  birds = data['birds']
  age = data['age']
  visits = data['visits']
  priority = data['priority']



  return jsonify({'birds' : birds, 'age' : age, 'visits' : visits, 'priority' : priority})

if __name__ == '__main__':
    app.run(debug = True)










 














