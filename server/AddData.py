#!/usr/local/bin/python3
# add some dummy data do not run this
import pymongo
from datetime import datetime, time
import json
import os
import sys
import server
import config
import pymongo

dir_path = os.path.dirname(os.path.realpath(__file__))

seedData = json.load(
    open(os.path.join(dir_path, 'seedData.json'), 'r'))

client = pymongo.MongoClient(config.MONGO_URI)
client.drop_database(config.MONGO_DB)
mydb = client[config.MONGO_DB] #this use dev db not test

collist = mydb.list_collection_names()
for col in collist:
    mydb[col].drop()


mycol = mydb["user"]
mycol.create_index([('$**', 'text')])
users = seedData['users']

x = mycol.insert_many(users)

# mydb.auctions.ensureIndex({seller_name:"text",description:"text",title:"text"})
collection = mydb["users"]
# 输出插入的所有文档对应的 _id 值
print(x.inserted_ids)

for test in collection.find():
    print("123")
    print(test)
# for test2 in mylist:
#    print(test2)


mycol = mydb["auctions"]
mycol.create_index([('$**', 'text')])
mylist =  seedData['auctions']
x = mycol.insert_many(mylist)

# mydb.auctions.ensureIndex({seller_name:"text",description:"text",title:"text"})
collection = mydb["auctions"]
# 输出插入的所有文档对应的 _id 值
print(x.inserted_ids)

for test in collection.find():
    print("123")
    print(test)
# for test2 in mylist:
#    print(test2)
