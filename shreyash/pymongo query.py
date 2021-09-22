from re import match
from pandas.core.frame import DataFrame
from pymongo import MongoClient
import pandas as pd
import numpy as np







# Create connection to MongoDB
client = MongoClient('localhost', 27017)
db = client['database']
collection = db['collection']
 



myquery = { "birds" : 'Cranes' } 

mydoc = collection.find(myquery)

for x in mydoc:
  print(x)



print('2')

print('a')
mydoc =  collection.aggregate(
   [
      { '$sample': { 'size': 12 } },
      { '$group': { '_id' : 'null', 'ageStdDev': { '$stdDevSamp': "$age" } } }
   ]
)
 

print('b')
mydoc = collection.aggregate([
   { '$project': { 'Avg': { '$avg': "$visits"}  } }
])




print('3')

myresult = collection.find().limit(2)


for x in myresult:
  print(x)




print('4')

results = collection.find({'age' : 1})

for x in results:
  print(x)



print('5')

for x in collection.find({},{  "birds": 1, "age": 1 , "visits" : 1}):
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

print('10')


av = collection.aggregate([
   { '$project': { 'Avg': { '$avg': "$age"}  } }
])

print(av)


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




print('19')

#result = collection.replace_many(
        #{"age": np.nan},
        #{
                
                #"age": av,

print('20')

mydoc = collection.distinct('birds')

for x in mydoc:
  print(x)



               
                  
      
