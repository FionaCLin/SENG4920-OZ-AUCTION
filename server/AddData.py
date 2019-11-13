#!/usr/bin/python3
#add some dummy data do not run this
import pymongo
 
client = pymongo.MongoClient("mongodb+srv://jiedian233:0m9n8b7v6c@cluster0-u5lvi.mongodb.net/test?retryWrites=true&w=majority")
mydb = client["runoobdb"]

mycol = mydb["auctions"]
mycol.create_index([('$**', 'text')])
mylist = [
  {
    "id": 14138186,
    "seller_name": "AmeliaOriginals",
    "seller_id": 11829,
    "category_id": 4,
    "title": "Silver Wire Woven Tear Drop Pendant with Turquoise Faceted Glass Bead",
    "description": "Silver Wire Woven Tear Drop Pendant with Turquoise Faceted Glass Bead",
    "end_time": "2019-09-22 15:46:28",
    "created": "2018-05-21 21:04:13",
    "price": 25,
    "image": "https://static.artfire.com/uploads/mfs/items/45/0c/default/450c43c3763c1bb9a40bf975fc3a5ead9bc2b468faa6766ff2e99e9ad7b370e8.jpg",
    "status": 0,
    "biddings": []
  },
  {
    "id": 14138168,
    "seller_name": "AmeliaOriginals",
    "seller_id": 11829,
    "category_id": "Pet Supplies",
    "title": "Gold Toned Wire Woven Cursive \"I\" Pendant Necklace",
    "description": "Gold Toned Wire Woven Cursive &quot;I&quot; Pendant Necklace",
    "end_time": "2018-07-07 18:41:54",
    "created": "2018-05-21 20:01:07",
    "price": 15,
    "image": "https://static.artfire.com/uploads/mfs/items/e7/26/default/e726bf372fc6bc236f9c9f067f3024585bdee7a76a0e8e30807b3a457b752eca.jpg",
    "status": 0,
    "biddings": []
  },
  {
    "id": 14138155,
    "seller_name": "AmeliaOriginals",
    "seller_id": 11829,
    "category_id": "Pottery, Glass",
    "title": "Square Ceramic Daisy Pendant on Black Leather Cord Handmade Necklace.",
    "description": "Square Ceramic Daisy Pendant on Black Leather Cord Handmade Necklace.",
    "end_time": "2018-07-07 18:41:09",
    "created": "2018-05-21 19:18:41",
    "price": 15,
    "image": "https://static.artfire.com/uploads/mfs/items/ad/95/default/ad9573b6bc14bccdbb901e7a744083a50379c8c3aced53cf15a15c17936051b4.jpg",
    "status": 0,
    "biddings": []
  },
  {
    "id": 14084599,
    "seller_name": "AmeliaOriginals",
    "seller_id": 11829,
    "category_id": "Services",
    "title": "Portugues Knitting Pin -Non-Tarnish Silver and Black/Green Shell",
    "description": "Portugues Knitting Pin -Non-Tarnish Silver and Black/Green Shell",
    "end_time": "2018-07-02 20:07:13",
    "created": "2018-04-08 20:06:24",
    "price": 10,
    "image": "https://static.artfire.com/uploads/mfs/items/72/3e/default/723e3621097b174fdf44bb0de6f038d5580e60d077b0d7dbcf3a21becd081081.jpg",
    "status": 0,
    "biddings": []
  },
  {
    "id": 13131854,
    "seller_name": "Jaqui",
    "seller_id": 27056,
    "category_id": "Services",
    "title": "Sterling Silver Genesa Crystal Pendant Sacred Geometry",
    "description": "Sterling Silver Genesa Crystal Pendant Sacred Geometry",
    "end_time": "2019-08-21 23:33:28",
    "created": "2014-01-31 11:56:34",
    "price": 50,
    "image": "https://static.artfire.com/uploads/mfs/items/03/81/default/03819102983b5f471b27fa9a1a9ef404354582a587806227b0f3dd3d24e3f9bb.jpg",
    "status": 0,
    "biddings": []
  },
  {
    "id": 13857537,
    "seller_name": "Jaqui",
    "seller_id": 27056,
    "category_id": "Services",
    "title": "Peaker4Life Sterling Necklace 18\" chain INCLUDED",
    "description": "Peaker4Life Sterling Necklace 18&quot; chain INCLUDED",
    "end_time": "2019-03-27 17:15:41",
    "created": "2017-07-25 17:43:01",
    "price": 50,
    "image": "https://static.artfire.com/uploads/mfs/items/5d/1e/default/5d1ec365331c67f826a0018b48d75d8d2e8dfd7ce8ab4fba870ce34d4dfcf284.jpg",
    "status": 0,
    "biddings": []
  },
  {
    "id": 13364828,
    "seller_name": "Jaqui",
    "seller_id": 27056,
    "category_id": "Electronics",
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
    "id": 13074092,
    "seller_name": "Jaqui",
    "seller_id": 27056,
    "category_id": "Food & Drinks",
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
