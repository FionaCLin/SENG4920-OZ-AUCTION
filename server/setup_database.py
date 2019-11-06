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



# user account database
class local_database:
    def __init__(self):
        self.users = {}

        # load account info from local csv file
        if not os.path.isfile('user_accounts.csv'):
            with open('user_accounts.csv', 'w', newline='') as csvfile:
                accountWriter = csv.writer(csvfile)
                accountWriter.writerow(['username', 'password'])
        else:
            usr_info_df = pd.read_csv('user_accounts.csv')
            for index, row in usr_info_df.iterrows():
                username, password = row['username'], row['password']
                if username not in self.users:
                    self.users[username] = password

    def save_user(self, username, password):
        self.users.setdefault(username, password)

        # save account info to local csv file
        with open('user_accounts.csv', 'a', newline='') as csvfile:
            accountWriter = csv.writer(csvfile)
            accountWriter.writerow([username, password])
    
    def varifyUser(self, username, password):
        if username in self.users and self.users[username] == password:
            return True
        else:
            return False

    def get_all_users(self):
        return self.users

    def is_in_userDatabase(self, username):
        return username in self.users


