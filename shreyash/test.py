from re import match
from pandas.core.frame import DataFrame
from pymongo import MongoClient
import pandas as pd
import numpy as np


# Create connection to MongoDB
client = MongoClient('localhost', 27017)
db = client['database']
collection = db['collection']
 


print('1')
myquery = { "birds" : 'Cranes' } 

mydoc = collection.find(myquery)

for x in mydoc:
  print(x)



print('2')




print('3')

myresult = collection.find().limit(2)


for x in myresult:
  print(x)




print('4')

results = collection.find({'age' : 1})

for x in results:
  print(x)




print('6')

mydoc = collection.find({"visits":{"$lt":4}})

for x in mydoc:
  print(x)

print('7')
mydoc = collection.find( { "age":  {"$not": { "$type": 1 } } })

for x in mydoc:
  print(x)


print('8')

mydoc = collection.find({"age":{"$lt":4}})

for x in mydoc:
  print(x)


print('9')

mydoc = collection.find({'$and': [{'age': {"$gte":2}}, 
                            {'age': {"$lt" :4}}]})

for x in mydoc:
  print(x)


print('12')

rec = {'birds': 'New', 'age': 3.5, 'visits': 2, 'priority': 'yes'}

rec_1 = collection.insert_one(rec)

cursor = collection.find()
for record in cursor:
    print(record)


myquery = {'birds': 'New', 'age': 3.5, 'visits': 2, 'priority': 'yes'}
x =collection.delete_one(myquery)    

print(x.deleted_count, " documents deleted.")



print('13')

myquery = { 'birds' : 'Cranes'}

mydoc = collection.find(myquery)
for x in mydoc:
  print(x)


myquery = { 'birds' : 'plovers'}

mydoc = collection.find(myquery)
for x in mydoc:
  print(x)


myquery = { 'birds' : 'spoonbills'}

mydoc = collection.find(myquery)
for x in mydoc:
  print(x)

x = collection.count(myquery)  
print(x)



print('14')


mydoc = collection.find().sort("age")

for x in mydoc:
  print(x)

print('15')

mydoc = collection.find().sort("visits", -1)

for x in mydoc:
  print(x)


print('16')

prev = { "birds" : "plovers"}
newt = { "$set" : {"birds" : "trumpeters"} }

collection.update_many(prev,newt)

mydoc = collection.find()
for x in mydoc:
  print(x)



print('18')

mydoc = collection.find({"$and": [{"visits" :2},
                                 {"priority": "yes"}]})

for x in mydoc:
  print(x)    


print('20')

mydoc = collection.distinct('birds')

for x in mydoc:
  print(x)




