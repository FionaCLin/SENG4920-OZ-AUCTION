import json, pymongo, sys, re

class Client():
    # connecting mlab
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://seng4920_project:seng4920_project@ds333248.mlab.com:33248/seng4920')


class Auction_db_client(Client):
    def __init__(self):
        super().__init__() 
        self.auction_db =  self.client['seng4920']