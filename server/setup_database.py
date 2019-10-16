import json
import pymongo
import sys
import re


class Client():
    # connecting mlab
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://seng4920_project:seng4920_project@ds333248.mlab.com:33248/seng4920')


class Auction_db_client(Client):
    def __init__(self):
        super().__init__() 
        self.auction_db =  self.client['seng4920']


# after creating the database, create some collection methods
class Collection(Auction_db_client):
    def __init__(self):
        super().__init__()
        self.col = self.auction_db['project']

    def insert_many_collections(self, data):
        self.col.insert_many(data)

    def delete_one_collection(self, query):
        self.col.delete_one(query)

    def select_count_collection(self, query):
        return self.col.find(query).count()

    def select_all_collection_query(self, query):
        return self.col.find(query)

    def select_all_collection(self):
        return self.col.find({})

    def select_one_collection(self, query):
        return self.col.find_one(query)

