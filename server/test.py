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
#for col in collist:
#    mydb[col].drop()

server.app.testing = True
client = server.app.test_client()


def test_filter_auction_first():
    r = client.get('/auction/search/filter', follow_redirects=True)
    assert r.status_code == 200
    res = json.loads(r.data.decode('utf8'))
    assert res == []

def test_create_auction():
    for i in sample_input['auctions']:
        r = client.post('/auction', json=i)
        #print(i)
        #print(json.loads(r.data.decode('utf8'))['message'])
        #input bug
        assert r.status_code == 200
        res = json.loads(r.data.decode('utf8'))
        assert res['message'] == 'Auction create successfully'
        for k in i.keys():
            assert res['data'][k] == i[k]
        
def test_filter_auction():
    r = client.get('/auction/search/filter',follow_redirects=True)
    assert r.status_code == 200
    res = json.loads(r.data.decode('utf8'))
    for i in range(len(sample_input['auctions'])):
        expect = sample_input['auctions'][i]
        for k in expect.keys():
            assert res[i][k] == expect[k]

if __name__ == "__main__":
    print('##### test API #####')
    #test_filter_auction_first()
    #test_create_auction()
    test_filter_auction()
