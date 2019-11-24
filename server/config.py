
import os
import sys
import re


# There are three different ways to store the data in the application.
# You can choose 'datastore', 'cloudsql', or 'mongodb'. Be sure to
# configure the respective settings for the one you choose below.
# You do not have to configure the other data backends. If unsure, choose
# 'datastore' as it does not require any additional configuration.
DATA_BACKEND = 'mongodb'


# Mongo configuration
# If using mongolab, the connection URI is available from the mongolab control
# panel. If self-hosting on compute engine, replace the values below.

if re.match(r'.*test.*', sys.argv[0]):
    # update this and save as config.py
    MONGO_URI = \
        "mongodb+srv://jiedian233:0m9n8b7v6c@cluster0-u5lvi.mongodb.net/test?retryWrites=true&w=majority"
    MONGO_PORT = 27017

    MONGO_DB = 'runoobdb_test'
else:
    MONGO_URI = \
        "mongodb+srv://jiedian233:0m9n8b7v6c@cluster0-u5lvi.mongodb.net/test?retryWrites=true&w=majority"
    MONGO_PORT = 27017
    MONGO_DB = 'runoobdb_test'	
