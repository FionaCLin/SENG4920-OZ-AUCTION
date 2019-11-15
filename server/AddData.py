#!/usr/bin/python3
#add some dummy data do not run this
import pymongo
 
client = pymongo.MongoClient("mongodb+srv://jiedian233:0m9n8b7v6c@cluster0-u5lvi.mongodb.net/test?retryWrites=true&w=majority")
mydb = client["runoobdb"]

mycol = mydb["auctions"]
mycol.create_index([('$**', 'text')])
mylist = [
{
    "id": 5,
    "seller_name": "Jaqui",
    "seller_id": 27056,
    "category_id": 4,
    "title": "Sterling Silver Genesa Crystal Pendant Sacred Geometry",
    "description": "Sterling Silver Genesa Crystal Pendant Sacred Geometry",
    "end_time": "2019-08-21 23:33:28",
    "created": "2014-01-31 11:56:34",
    "price": 50,
    "image": "https://static.artfire.com/uploads/mfs/items/03/81/default/03819102983b5f471b27fa9a1a9ef404354582a587806227b0f3dd3d24e3f9bb.jpg",
    "status": 0,
    "biddings": [
      {
        "user_id": 27056,
        "price": 26,
        "item_id": 14138186,
        "created": "2019-09-22 15:50:28"
      },
      {
        "user_id": 27056,
        "price": 30,
        "item_id": 14138186,
        "created": "2019-09-22 15:52:28"
      }
    ]
  },
  {
    "id": 6,
    "seller_name": "Jaqui",
    "seller_id": 27056,
    "category_id": 3,
    "title": "Peaker4Life Sterling Necklace 18\" chain INCLUDED",
    "description": "Peaker4Life Sterling Necklace 18&quot; chain INCLUDED",
    "end_time": "2019-03-27 17:15:41",
    "created": "2017-07-25 17:43:01",
    "price": 50,
    "image": "https://static.artfire.com/uploads/mfs/items/5d/1e/default/5d1ec365331c67f826a0018b48d75d8d2e8dfd7ce8ab4fba870ce34d4dfcf284.jpg",
    "status": 0,
    "biddings": [
      {
        "user_id": 3,
        "price": 26,
        "item_id": 14138186,
        "created": "2019-09-22 15:50:28"
      },
      {
        "user_id": 120844,
        "price": 30,
        "item_id": 14138186,
        "created": "2019-09-22 15:52:28"
      }
    ]
  },
  {
    "id": 7,
    "seller_name": "Jaqui",
    "seller_id": 27056,
    "category_id": 45,
    "title": "MPC Sterling Silver Mountain Peak Ring Sz 5 to 10",
    "description": "MPC Sterling Silver Mountain Peak Ring Sz 6 to 10",
    "end_time": "2018-11-06 18:37:13",
    "created": "2016-09-10 14:01:38",
    "price": 45,
    "image": "https://static.artfire.com/uploads/mfs/items/b7/88/default/b7885b641a4d6785b05f4bb91dd572e41b58c776a5e8bcbbc9da3ea60c9da5d6.jpg",
    "status": 0,
    "biddings": []
  },
  {
    "id": 8,
    "seller_name": "Jaqui",
    "seller_id": 27056,
    "category_id": 31,
    "title": "MPC Sterling Mountain Peaks Bracelet/Anklet 8.5\"",
    "description": "MPC Sterling Mountain Peaks Bracelet/Anklet 8.5&quot;",
    "end_time": "2018-07-04 20:32:55",
    "created": "2016-04-02 03:07:39",
    "price": 53,
    "image": "https://static.artfire.com/uploads/mfs/items/81/93/default/8193de5b3214040c0f77712008e1b7c453eebdc09c7bc293b2c8be8fe77421fa.jpg",
    "status": 0,
    "biddings": []
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
