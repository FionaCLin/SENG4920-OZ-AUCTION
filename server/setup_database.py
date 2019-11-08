import csv
import base64 
import datetime 
import requests 
import json
import pymongo
import sys
import re
import os
import pandas as pd


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

    def select_all_collection(self):
        return self.col.find({})

    def insert_many_collections(self, data):
        self.col.insert_many(data)

    def add_one_dict_to_array(self, query, newdata):
        self.col.update(query, newdata)

    def delete_specific_collection(self, query, data):
        self.col.update(query, data)


    # def delete_one_collection(self, query):
    #     self.col.delete_one(query)

    # def select_count_collection(self, query):
    #     return self.col.find(query).count()

    # def select_all_collection_query(self, query):
    #     return self.col.find(query)

    # def select_one_collection(self, query):
    #     return self.col.find_one(query)



# temporary user account
class local_user_account_database:
    def __init__(self):
        self.users = {}
        self.num_users = 0
        if not os.path.isfile('user_accounts.csv'):
            with open('user_accounts.csv', 'w', newline='') as csvf:
                accountWriter = csv.writer(csvf)
                accountWriter.writerow(['username', 'password'])
        else:
            acc = pd.read_csv('user_accounts.csv')
            for index, row in acc.iterrows():
                username, password = row['username'], row['password']
                if username not in self.users:
                    self.users[username] = password
                self.num_users = index + 1

    def save_user(self, username, password):
        self.users.setdefault(username, password)
        with open('user_accounts.csv', 'a', newline='') as csvf:
            accountWriter = csv.writer(csvf)
            accountWriter.writerow([username, password])
            self.num_users += 1
    
    def varify_user(self, username, password):
        if username in self.users and self.users[username] == password:
            return True
        else:
            return False

    def get_all_users(self):
        return self.users

    def get_users_num(self):
        return self.num_users


    def is_in_database(self, username):
        return username in self.users


col = Collection()



if __name__ == '__main__':
    user_profile = {
        "col_id":"c1",
        "user_profile":[
        ]
    }
    col.insert_many_collections([user_profile])

    auction_items = {
        "col_id":"c2",
        "auction_items": [
        ]
    }
    col.insert_many_collections([auction_items])



