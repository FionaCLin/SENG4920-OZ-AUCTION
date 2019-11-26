#!/usr/bin/python3
#add some dummy data do not run this
import pymongo
 
client = pymongo.MongoClient("mongodb+srv://jiedian233:0m9n8b7v6c@cluster0-u5lvi.mongodb.net/test?retryWrites=true&w=majority")
mydb = client["runoobdb"]

mycol = mydb["auctions"]
mycol.create_index([('$**', 'text')])
mylist = [
  {
    "user_id": 1,
    "email": "test@test",
    "password": "test",
    "first_name": "",
    "last_name": "",
    "age": "",
    "phone_number": "",
    "payment_method": "",
    "favorites": [],
    "auction": [1,2,3],
    "bids": []
  }
]
 
x = mycol.insert_many(mylist)
 
#mydb.auctions.ensureIndex({seller_name:"text",description:"text",title:"text"}) 
collection = mydb["auctions"]
# 输出插入的所有文档对应的 _id 值
print(x.inserted_ids)

for test in collection.find():
    print("123")
    print(test)
#for test2 in mylist:
#    print(test2)
