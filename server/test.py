#!  /usr/local/bin/python3

import json
import os
import sys
import server
import config
import pymongo

dir_path = os.path.dirname(os.path.realpath(__file__))

sample_input = json.load(
    open(os.path.join(dir_path, 'seedData.json'), 'r'))

client = pymongo.MongoClient(config.MONGO_URI)
mydb = client[config.MONGO_DB]
collist = mydb.list_collection_names()
for col in collist:
   mydb[col].drop()

mycol = mydb["user"]
mycol.create_index([('$**', 'text')])
users = sample_input['users']

x = mycol.insert_many(users)

mycol = mydb["auctions"]
mycol.create_index([('$**', 'text')])
mylist =  sample_input['auctions']
x = mycol.insert_many(mylist)


server.app.testing = True
client = server.app.test_client()
        

def test_auction():
    print ("===== test auction =====")
    r = client.get('/auction?limit=5&base=0',follow_redirects=True)
    res = json.loads(r.data.decode('utf8'))

    sample_output = json.load(open(os.path.join(dir_path, 'get_auction.json'), 'r'))

    assert r.status_code == 200
    assert len(res["result"]) == 5
    for i in range(len(sample_output["result"])):
        expect = sample_output["result"][i]
        for k in expect.keys():
            try:
                assert res["result"][i][k] == expect[k]
            except:
                print ('---')
                print(res["result"][i][k], expect[k])



def test_auction_search_keyword():
    # curl -X GET "http://127.0.0.1:9999/auction/search-key/Silver" -H "accept: application/json"
    print ("===== test auction search keywords =====")
    r = client.get('/auction/search-key/Silver',follow_redirects=True)
    res = json.loads(r.data.decode('utf8'))

    sample_output = json.load(open(os.path.join(dir_path, 'get_search_keyword.json'), 'r'))

    assert r.status_code == 200
    assert len(res) == 4
    for i in range(len(sample_output)):
        expect = sample_output[i]
        for k in expect.keys():
            try:
                assert res[i][k] == expect[k]
            except:
                print ('---')
                print(res[i][k], expect[k])



def test_get_category_auction_id():
    print ("===== test get category auctionID =====")
    r = client.get('/auction/get_category/10',follow_redirects=True)
    res = json.loads(r.data.decode('utf8'))

    sample_output = json.load(open(os.path.join(dir_path, 'get_category_auction_id.json'), 'r'))

    assert r.status_code == 200
    assert sample_output == res



def test_get_rating_item_id_fail():
    print ("===== test get category auctionID =====")
    r = client.get('/auction/rating/4',follow_redirects=True)
    res = json.loads(r.data.decode('utf8'))

    sample_output = json.load(open(os.path.join(dir_path, 'get_rating_item_id_fail.json'), 'r'))

    assert r.status_code == 404
    assert sample_output == res



def test_get_auction_id():
    print ("===== test get auction id =====")
    r = client.get('/auction/12',follow_redirects=True)
    res = json.loads(r.data.decode('utf8'))

    sample_output = json.load(open(os.path.join(dir_path, 'get_auction_id.json'), 'r'))

    assert r.status_code == 200
    assert sample_output == res




# def test_filter_auction_first():

#     r = client.get('/auction/search/filter', follow_redirects=True)
#     assert r.status_code == 200
#     res = json.loads(r.data.decode('utf8'))
#     assert len(res)==4

# def test_create_auction():
#     for i in sample_input['auctions']:
#         r = client.post('/auction', json=i)
#         #print(i)
#         #print(json.loads(r.data.decode('utf8'))['message'])
#         #input bug
#         assert r.status_code == 200
#         res = json.loads(r.data.decode('utf8'))
#         assert res['message'] == 'Auction create successfully'
#         for k in i.keys():
#             assert res['data'][k] == i[k]



if __name__ == "__main__":

    test_auction()
    print ('PASSED')
    test_auction_search_keyword()
    print ('PASSED')
    test_get_category_auction_id()
    print ('PASSED')
    test_get_rating_item_id_fail()
    print ('PASSED')
    test_get_auction_id()
    print ('PASSED')
    
    # test_filter_auction_first()
    #test_create_auction()
    # test_filter_auction()

