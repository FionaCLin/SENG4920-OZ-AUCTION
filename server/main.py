#!/usr/local/bin/python3

import json
from datetime import datetime, time
import pymongo
import uuid
from flask_cors import CORS
import re
import os
import config
import csv
import base64
from flask import Flask, request, Response
from flask_restplus import Resource, Api, fields, inputs, reqparse, abort
from setup_database import *
from functools import wraps
from time import time
from itsdangerous import SignatureExpired, JSONWebSignatureSerializer, BadSignature
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

# ============================== database connection ==========================
client = pymongo.MongoClient(config.MONGO_URI)
mydb = client[config.MONGO_DB]
# =============================================================================

# ==============================   Helper functions   ==========================
# validate_datetime_str
# getUserById
# getAuctionById
# =============================================================================


def getAuctionById(id):
    au_col = mydb['auctions']
    return au_col.find_one({'id': int(id)})


def getUserById(id):
    col = mydb['user']
    return col.find_one({"user_id": int(id)})

# datetime validation


def validate_datetime_str(str):
    try:
        # check if the str match the format : YYYY-MM-DD HH:MM:SS e.g 2010-01-01 12:00:00
        datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False


app = Flask(__name__)

api = Api(app, authorizations={
    'API-KEY': {
          'type': 'apiKey',
          'in': 'header',
          'name': 'AUTH-TOKEN'
          }
},
    security='API-KEY',
    title="Online Auction",
    description="Auction Website")


CORS(app)

# define namespaces
ns_auction = api.namespace(
    'auctions', description='Operations related to auction information management')


#########################
#  Routes for Auction.  #
#########################
"""
POST: Create a an auction item
GET: Get auction information by item id
"""

# this is also the data model stored in server

returned_bidding_info = api.model(
    "Bidding response returned",
    {
        "item_id": fields.Integer,
        "user_id": fields.Integer,
        "proposal_price": fields.Float,
        "overbid": fields.Boolean,
    }
)

user_input_single_auction_item = api.model(
    'User input to create auction',
    {
        "seller_id": fields.Integer,
        "seller_name": fields.String,
        "title": fields.String,
        "description": fields.String,
        "price": fields.Float,
        "end_time": fields.String(required=True, pattern='%Y-%m-%d %H:%M:%S'),
        "location": fields.String,
        "category": fields.Integer,
        "image": fields.List(fields.String)
    }
)

auction_info_update = api.model(
    'Update auction details (user may specify only some of the fields)',
    {
        "category": fields.Integer,
        "title": fields.String,
        "description": fields.String,
        "end_time": fields.String,
        "price": fields.Float,
        "image": fields.String,
        "location": fields.String
    }
)


@ns_auction.route('')
class AuctionsOperations(Resource):

    @api.response(200, 'OK')
    @api.response(404, 'No auction data stored in database')
    @api.param('base', 'The item to start at(default 0)')
    @api.param('limit', 'How many records to return (max 1000, defaut 10)')
    @api.doc(description="get information of all auction data in the database")
    def get(self):
        base = 0
        max_result_size = 10
        try:
            if request.args.get('base'):
                base = int(request.args.get('base'))
        except TypeError:
            return {'result': "fail", "message": 'invalid base'}, 400
        try:
            if request.args.get('limit'):
                max_result_size = int(request.args.get('limit'))
        except TypeError:
            return {'result': "fail", "message": 'invalid limit'}, 400
        au_col = mydb['auctions']
        retrieved_items = []
        res = au_col.find()

        print(res.count())
        for item in res[base: base+max_result_size]:
            del item['_id']
            retrieved_items.append(item)

        if len(retrieved_items) == 0:
            return {"message": "No auctions stored in database"}, 404

        response = \
            {
                "message": "OK",
                "result_size": len(retrieved_items),
                "result": retrieved_items
            }
        return response, 200

    @api.response(200, 'OK')
    @api.response(400, 'Failed to create a new auction')
    @api.response(404, 'Seller not found')
    @api.expect(user_input_single_auction_item)
    @api.doc(description="create an auction item")
    def post(self):
        au_col = mydb['auctions']

        user_input = request.json

        seller = getUserById(user_input['seller_id'])
        if seller == None:
            return {'result': 'fail', 'message': 'Seller not found'}, 404

        print(request.json)

        new_auction = \
            {
                "id": au_col.count_documents({}),
                "created": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "updated": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "end_time": user_input['end_time'],
                "price": float(user_input['price']),
                "bidding_info": [],
                "status": "bidding"
            }

        # Input validation: End_time validation
        if not validate_datetime_str(user_input['end_time']):
            return {'message': 'Bad Request: invalid end_time format'}, 400

        for i in ['seller_name', 'seller_id',  "location", 'category', 'title', "description", "image"]:
            new_auction[i] = user_input[i]
            # Input validation: Detect missing fields
            # if user_input[i] == "" or user_input[i] is None:
            if user_input[i] is None:
                return {'message': 'Bad Request: field ' + i + ' is missing'}, 400

        try:
            au_col.insert_one(new_auction)
            del new_auction['_id']

            message = "Auction create successfully"
            response = \
                {
                    "message": message,
                    "data": new_auction
                }

            # Change user
            # seller = user_col.find_one({"user_id":  user_input['seller_id']})
            seller['auctions'].append(new_auction)
            mydb['user'].update_one({"user_id":  user_input['seller_id']}, {
                "$set": {"auctions": seller['auctions']}})  # :-()
            return response, 200
        except:
            return {'message': 'Bad Request'}, 400


@ns_auction.route('/user/<request_user_id>/auctions')
@api.param('request_user_id', 'Request User Id')
class User_auctions(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'User Does Not Exist')
    @api.doc(description="get user's auctions")
    def get(self, request_user_id):
        col = mydb['user']
        single_user = col.find_one({"user_id": int(request_user_id)})
        del single_user['_id']

        if single_user is None:
            response = {
                "message": "User does not exist",
                "data": ""
            }
            return response, 404

        new_user_auctions = dict()
        new_user_auctions["auctions"] = single_user["auctions"]

        response = {
            "message": "OK",
            "data": new_user_auctions
        }
        return response, 200

@ns_auction.route('/user/<request_user_id>/biddings')
@api.param('request_user_id', 'Request User Id')
class User_biddings(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'User Does Not Exist')
    @api.doc(description="get user's biddings")
    def get(self, request_user_id):
        col = mydb['user']
        single_user = col.find_one({"user_id": int(request_user_id)})
        del single_user['_id']

        if single_user is None:
            response = {
                "message": "User does not exist",
                "data": ""
            }
            return response, 404

        new_user_biddings = dict()
        new_user_biddings["bids"] = single_user["bids"]

        response = {
            "message": "OK",
            "data": new_user_biddings
        }
        return response, 200

@ns_auction.route('/user/<request_user_id>/favorites')
@api.param('request_user_id', 'Request User Id')
class User_biddings(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'User Does Not Exist')
    @api.doc(description="get user's favorites")
    def get(self, request_user_id):
        col = mydb['user']
        single_user = col.find_one({"user_id": int(request_user_id)})
        del single_user['_id']

        if single_user is None:
            response = {
                "message": "User does not exist",
                "data": ""
            }
            return response, 404

        new_user_favorites = dict()
        new_user_favorites["favorites"] = single_user["favorites"]

        response = {
            "message": "OK",
            "data": new_user_favorites
        }
        return response, 200


@ns_auction.route('/<item_id>')
@api.param('item_id', 'Item ID given when the auction is created')
class SingleAuctionItemOperations(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Specified item does not exist')
    @api.doc(description="get information of an auction item")
    def get(self, item_id):
        try:
            retrieved_item = getAuctionById(item_id)
            del retrieved_item['_id']

            return {"message": "OK", "data": retrieved_item}, 200
        except:
            return {"message":  "Specified item does not exist"}, 404

    @api.response(200, 'OK')
    @api.response(404, 'Specified item does not exist')
    @api.doc(description="Delete an auction")
    def delete(self, item_id):
        try:
            retrieved_item = getAuctionById(item_id)
            del retrieved_item['_id']
            au_col = mydb['auctions']
            if retrieved_item is None:
                return {"message": "Specified item does not exist"}, 404
            res = au_col.remove({"id": int(item_id)})
            if res['n'] == 1:
                return {"message": "Specified item is deleted successfully", "data": retrieved_item}, 200
            else:
                return {"message": "Failed to delete specified item"}, 400
        except:
            return {"message":  "Specified item does not exist"}, 404

    @api.response(200, 'OK')
    @api.response(404, 'Specified item does not exist')
    @api.expect(auction_info_update)
    @api.doc(description="Update auction item details")
    def put(self, item_id):
        user_input = request.json

        # Input validation: End_time validation
        if not validate_datetime_str(user_input['end_time']):
            return {'message': 'Bad Request: invalid end_time format'}

        try:
            au_col = mydb['auctions']
            retrieved_item = getAuctionById(item_id)
            del retrieved_item['_id']
            if retrieved_item is None:
                return {"message":  "Specified item does not exist"}, 404

            update_data = {}
            for k in ['category', 'title', "description", "end_time", "price", "image", "location"]:
                if k in user_input.keys() and k in retrieved_item.keys() and retrieved_item[k] != user_input[k]:
                    update_data[k] = user_input[k]

            res = au_col.update_one({"id": int(item_id)}, {
                                    "$set": update_data})
            print(res.modified_count, type(res))

            if res.modified_count == 1:
                return {"message": "Auction details have been updated"}, 200
            else:
                return {"message":  "Auction details fail to update"}, 400
        except:
            return {"message":  "Auction details update not allowed"}, 404


# search by key
@ns_auction.route('/search-key/<string:search_key>')
class Auction_search1(Resource):
    @api.response(200, 'Data fetched successfully')
    @api.response(400, 'Bad request')
    @api.response(404, 'No data found')
    @api.doc(description="Search by key-word")
    def get(self, search_key):
        collection = mydb['auctions']
        result = []
        easy_search = "\'" + search_key + "\'"

        cursor = collection.find(
            {"$text": {"$search": easy_search}}, {"_id": 0})
        result = []
        for entry in cursor:
            result.append(entry)

        if not result:
            return {
                'message':
                    'no auction find'
            }, 404

        return result, 200

# search by filter
@ns_auction.route('/search/filter')
class Auction_search2(Resource):
    @api.response(200, 'Data fetched successfully')
    @api.response(400, 'Bad request')
    @api.response(404, 'No data found')
    # @api.expect(user_input_filter)
    @api.param('location', '')
    @api.param('category', '')
    @api.param('user_id', '')
    @api.param('endPrice', '')
    @api.param('startPrice', '')
    @api.param('endDate', 'YYYY/MM/DD')
    @api.param('startDate', 'YYYY/MM/DD')
    @api.doc(description="Search by filter")
    def get(self):
        collection = mydb['auctions']
        result = []
        mid = []

        location = request.args.get('location')
        endDate = request.args.get('endDate')
        startDate = request.args.get('startDate')
        category = request.args.get('category')
        endPrice = request.args.get('endPrice')
        startPrice = request.args.get('startPrice')
        user_id = request.args.get('user_id')

        if startPrice is None:
            startPrice = 0
        if endPrice is None:
            endPrice = 10000  # change later

        # if start < 0 happen?

        # change data format
        if startDate is None:
            startDate = '2000/01/10'
        if endDate is None:
            endDate = datetime.datetime.now().strftime("%Y/%m/%d")

        endDateP = datetime.datetime.strptime(endDate, "%Y/%m/%d")
        startDateP = datetime.datetime.strptime(startDate, "%Y/%m/%d")

        cursor = collection.find()

        for entry in cursor:
            entry['_id'] = str(entry['_id'])
            result.append(entry)
            mid.append(entry)

        for entry in mid:
            print(entry)
            entryDateP = datetime.datetime.strptime(
                entry['end_time'], "%Y-%m-%d %H:%M:%S")
            if entryDateP <= startDateP or entryDateP >= endDateP:
                if entry in result:
                    result.remove(entry)

        for entry in mid:
            if entry['price'] < int(startPrice) or entry['price'] > int(endPrice):
                if entry in result:
                    result.remove(entry)

        for entry in mid:
            if category and entry['category'] is not None:
                if entry in result:
                    result.remove(entry)

        for entry in mid:
            if user_id and entry['seller_id'] != int(user_id):
                if entry in result:
                    result.remove(entry)

        return result, 200


###################################
#  Routes for bidding management  #
###################################
user_input_bidding_info = api.model(
    "User input to propose a bid & bidding info stored in server",
    {
        "user_id": fields.Integer,
        "item_id": fields.Integer,
        "proposal_price": fields.Float,
    }
)


user_input_bidding_operations = api.model(
    'User input to accept or decline a bid',
    {
        "user_id": fields.Integer,
        "item_id": fields.Integer,
        "operation": fields.String
    }
)

ns_bidding = api.namespace(
    'bidding', description='Operations related to management')

# Propose a bidding
@ns_bidding.route('')
class BiddingManagement(Resource):

    @api.response(200, 'OK')
    @api.response(404, 'Requested Resource Does Not Exist')
    @api.expect(user_input_bidding_info)
    @api.doc(description="Propose a bid on an item")
    def post(self):
        result = "OK"
        user_input = request.json
        item_id = user_input["item_id"]

        au_col = mydb['auctions']
        retrieved_item = au_col.find_one({'id': int(item_id)})
        item_min_price = retrieved_item["price"]

        if retrieved_item is None:
            return {"result": "Fail", "message": "Item not found"}, 404

        del retrieved_item['_id']

        # Input validation: Detect missing fields
        for k in ['user_id', 'proposal_price']:
            if user_input[k] == "" or user_input[k] is None:
                return {'message': 'Bad Request: field ' + k + ' is missing'}, 400

        message = "The bid has been proposed successfully"
        status_code = 200
        new_proposed_price = user_input["proposal_price"]
        if len(retrieved_item["bidding_info"]) == 0:
            current_highest_price = 0
        else:
            # sort bidding info by proposal_price (descending)
            sorted_bidding_info_list = sorted(retrieved_item["bidding_info"],
                                              key=lambda i: i['proposal_price'], reverse=True)
            current_highest_price = sorted_bidding_info_list[0]["proposal_price"]
        if_overbid = True if new_proposed_price > current_highest_price else False
        if if_overbid and new_proposed_price > item_min_price:
            print(retrieved_item)
            bid_id = len(retrieved_item['bidding_info'])
            new_bidding_info = {
                "bid_id": bid_id,
                "created": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            for key in user_input.keys():
                new_bidding_info[key] = user_input[key]
            retrieved_item["bidding_info"].append(new_bidding_info)
            au_col.insert_one(new_bidding_info)
            del new_bidding_info["_id"]
            au_col.update_one({"id": int(item_id)}, {"$set": retrieved_item})
        else:
            message = "Proposal price can't be less than current bidding price"
            return {"result": "Fail", "message": message}, 400

        response = \
            {
                "result": result,
                "message": message,
                "data": new_bidding_info
            }
        return response, status_code


# Accept or decline a bidding
@ns_bidding.route('/operations')
class AcceptOrDeclineBiddings(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Specified auction does not exists')
    @api.expect(user_input_bidding_operations)
    @api.doc(description="Accept or decline a the highest bidding on an item")
    def put(self):
        user_input = request.json
        au_col = mydb['auctions']
        item_id = user_input['item_id']
        operation = user_input['operation']
        retrieved_item = au_col.find_one({'id': int(item_id)})
        result = "Fail"
        if retrieved_item is None:
            return {"result": result, "message": "Auction item not found"}, 404

        del retrieved_item['_id']

        if len(retrieved_item['bidding_info']) == 0:
            return {"result": result, "message": "No bid on this item"}, 400

        if int(retrieved_item['seller_id']) != int(user_input['user_id']):
            return {"result": result, "message": "The user is not the seller of this item"}, 400

        status_code = 200
        if operation == "accept":
            retrieved_item["status"] = "Accepted"
            result = "OK"
            message = "The bid is accepted successfully"
        elif operation == "decline":
            retrieved_item["status"] = "Declined"
            result = "OK"
            message = "The bid is declined successfully"
        else:
            return {"result": result, "message": "Invalid operation"}, 400

        # sort bidding info by proposal_price (descending)
        sorted_bidding_info_list = sorted(retrieved_item["bidding_info"],
                                          key=lambda i: i['proposal_price'], reverse=True)
        highest_bidding_id = sorted_bidding_info_list[0]["bid_id"]

        au_col.update_one({"id": int(item_id)}, {"$set": retrieved_item})
        response = \
            {
                "result": result,
                "message": message,
                "bid_id": highest_bidding_id
            }
        return response, status_code


@ns_bidding.route('/<bid_id>')
@api.param('bid_id', 'Bidding ID given when the bid was proposed')
class SingleBiddingOperations(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Item not found')
    @api.doc(description="Get bidding information by id")
    def get(self, bid_id):
        au_col = mydb["auctions"]
        result = "OK"
        retrieved_item = au_col.find_one({"bid_id": int(bid_id)})
        if retrieved_item is None:
            result = "Fail"
            return {"result": result, "message": "Item not found"}, 404
        del retrieved_item["_id"]
        response = \
            {
                "result": result,
                "data": retrieved_item
            }

        return response, 200

    @api.response(200, 'OK')
    @api.response(404, 'Specified item does not exist')
    @api.doc(description="Delete a proposed bid")
    def delete(self, bid_id):
        au_col = mydb['auctions']
        result = "Fail"
        retrieved_bid = au_col.find_one({'bid_id': int(bid_id)})
        if retrieved_bid is None:
            return {"result": result, "message": "Specified bidding does not exist"}, 404
        del retrieved_bid['_id']
        item_id = retrieved_bid["item_id"]
        retrieved_item = au_col.find_one({'id': int(item_id)})

        if retrieved_item is None:
            return {"result": result, "message": "Specified auction item does not exist"}, 404
        del retrieved_item['_id']

        if retrieved_item["status"] == "Accepted":
            return {"result": result, "message": "The bid is already accepted"}

        try:
            au_col.remove({"bid_id": int(bid_id)})

            # remove the specified bidding from the bidding_info of the auction
            retrieved_item['bidding_info'] = \
                [x for x in retrieved_item['bidding_info']
                    if int(x["bid_id"]) != int(bid_id)]
            au_col.update_one({"id": int(item_id)}, {"$set": retrieved_item})

            return {"message": "Specified bidding is deleted successfully"}
        except:
            return {"message": "Failed to delete "}, 400


ns_account = api.namespace(
    'account', description='Operations related to user accounts')


@ns_account.route('/manage_profile/<string:request_user_id>')
class Manage_profile(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Profile Does Not Exist')
    @api.doc(description="get other user's profile")
    def get(self, request_user_id):
        single_user = getUserById(request_user_id)
        del single_user['_id']

        new_user_profile = dict()
        out_key = ["user_id", "dob", "phone_number", "email", "first_name",
                   "last_name", "favorites", "avatar", "rating", "location", "payment_method"]
        for k in out_key:
            new_user_profile[k] = single_user[k]
        response = {
            "message": "OK",
            "data": new_user_profile
        }
        return response, 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
