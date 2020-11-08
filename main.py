import pymongo
from pymongo import MongoClient
import pprint
from flask import Flask , request, jsonify


client = MongoClient('mongodb://localhost:27017')
db = client["student"]
info_coll=db['info']




flaskappinstance=Flask(__name__)


@flaskappinstance.route('/home',methods=['GET'])
def home():
	return jsonify({'home':'welcome aishwarya'})

@flaskappinstance.route('/data',methods=['POST'])
def stud_data():
	try:
		_jason=request.json
		_name=_jason['name']
		_email=_jason['email'] 

		info_coll.insert_one(_jason).inserted_id
		return jsonify({'status': 1})
		
	except Exception as ex:
		print(ex)

		


@flaskappinstance.route('/users',methods=['GET'])
def stud():
	try:
		data=list(info_coll.find())
		print(data)
		return data

		#return jsonify({'status':1})
	except Exception as ex:
		print(ex)
		return jsonify({'status':0})


@flaskappinstance.route('/delete/<name>',methods=['DELETE'])
def dell(name):
	db.info.delete_one({'name':(name)})
	return jsonify({"status":1})




@flaskappinstance.route('/update/<name>',methods=['PATCH'])
def update_stud(name):

	db.info.update({ "name": (name) },{ "$set": { "email": "aish@gmail.com" }})
	return jsonify({"status":1})








if __name__=='__main__':

	flaskappinstance.run(host="0.0.0.0",port=5000)







