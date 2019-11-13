import json
from datetime import datetime, time
import pymongo
import uuid
from flask_cors import CORS
import re
import os
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

# ===== database connection ===
client = pymongo.MongoClient("mongodb+srv://jiedian233:0m9n8b7v6c@cluster0-u5lvi.mongodb.net/test?retryWrites=true&w=majority")
mydb = client["runoobdb"]
# =============================


UPLOAD_FOLDER = './image/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# datetime validation
def validate_datetime_str(str):
    try:
        # check if the str match the format : YYYY-MM-DD HH:MM:SS e.g 2010-01-01 12:00:00
        datetime.datetime.strptime(str,'%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False



class Token_authentication:
    def __init__(self, secret_key, expire_time):
        self.secret_key = secret_key
        self.expire_time = expire_time
        self.active_token = set()
        self.serializer = JSONWebSignatureSerializer(secret_key)

    def generate_token(self, email):
        info = {
            'email': email,
            'creation_time': time()
        }

        token = self.serializer.dumps(info)
        print('token serializer is '+str(token))

        new_token = token.decode()
        self.active_token.add(new_token)
        return new_token

    def get_token_info(self, token):
        info = self.serializer.loads(token.encode())
        return info['email']

    def validate_token(self, token):
        info = self.serializer.loads(token.encode())

        if token not in self.active_token:
            raise SignatureExpired("The Token is no longer active!")
        elif time() - info['creation_time'] > self.expire_time:
            self.active_token.discard(token)
            raise SignatureExpired(
                "The Token has been expired; get a new token!")
        return info['email']

    def delete_token(self, token):
        print('--- now active tokens are '+str(self.active_token))
        self.active_token.discard(token)
        return True


def requires_authentication(authen):
    @wraps(authen)
    def decorated(*args, **kwargs):
        token = request.headers.get('AUTH-TOKEN')
        if not token:
            abort(401, 'Authentication token is missing')
        try:
            user = auth.validate_token(token)
        except SignatureExpired as e:
            abort(401, e.message)
        except BadSignature as e:
            abort(401, e.message)
        return f(*args, **kwargs)
    return decorated


# upload_local_items(col)
SECRET_KEY = "SENG4920"

expire_time = 1000
auth = Token_authentication(SECRET_KEY, expire_time)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    'auction', description='Operations related to auction information management')
ns_account = api.namespace(
    'account', description='Operations related to user accounts')
ns_bidding = api.namespace(
    'bidding', description='Operations related to management')


# signin_model = api.model('signin_info', {
#     'email': fields.String,
#     'password': fields.String
# })

# signin_parser = reqparse.RequestParser()
# signin_parser.add_argument('email', type=str)
# signin_parser.add_argument('password', type=str)

db = local_user_account_database()
########################################
#  Temporary DB                       #
########################################
# client = pymongo.MongoClient(
    # "mongodb+srv://jiedian233:0m9n8b7v6c@cluster0-u5lvi.mongodb.net/test?retryWrites=true&w=majority")
# mydb = client["runoobdb"]


########################################
#  Routes for user account management  #
########################################


indicator_model = api.model(
    'credentials', {
        'email': fields.String,
        'password': fields.String
    }
)

indicator_parser = reqparse.RequestParser()
indicator_parser.add_argument('email', type=str)
indicator_parser.add_argument('password', type=str)


user_input_bidding_info = api.model(
    "User input to propose a bid & bidding info stored in server",
    {
        "user_id": fields.Integer,
        "proposal_price": fields.Float,
    }
)


auction_info = api.model(
    'Auction item information',
    {
        "item_id": fields.Integer,
        "seller_name": fields.String,
        "seller_id": fields.Integer,
        "category_id": fields.Integer,
        "title": fields.String,
        "description": fields.String,
        "updated": fields.String,
        "created": fields.String,
        "end_time": fields.String,
        "price": fields.Float,  # start price
        "image_url": fields.String,
        "bidding_info": fields.List(fields.Nested(user_input_bidding_info)),
        "status": fields.String
    }
)



user_profile_invisiable = api.model(
    "User profile invisiable", {
        "password": fields.String,
        "payment_method": fields.String
    }
)


user_profile = api.model(
    'User profile', {
        "email": fields.String,
        "first_name": fields.String,
        "last_name": fields.String,
        "age": fields.String,
        "phone_number": fields.String,
        "favorites": fields.List(fields.Nested(auction_info)),
        "invisiable": fields.List(fields.Nested(user_profile_invisiable))
    }
)


@ns_account.route('/register')
class Register(Resource):
    @api.response(200, 'Email Already Exists')
    @api.response(201, 'Account Created Successfully')
    @api.response(400, 'Bad Request Error')
    @api.doc(description="Register an account")
    @api.expect(indicator_model, validate=True)
    def post(self):
        alldata = col.select_all_collection()
        selected_data = []
        for item in alldata:
            if "user_profile" in item:
                selected_data = item["user_profile"]
        try:
            accountInfo = request.json
        except:
            return {'message': 'Bad Request!'}, 400
        try:
            for single_user in selected_data:
                if single_user["email"] == accountInfo['email']:
                    return {'message': 'Email Already Exists'}, 200

            new_user = {
                "user_id": len(selected_data),
                "email": accountInfo['email'],
                "password": accountInfo['password'],
                "first_name": "",
                "last_name": "",
                "age": "",
                "phone_number": "",
                "payment_method": "",
                "favorites": []
            }
            col.add_one_dict_to_array(
                {"col_id": "c1"}, {"$push": {"user_profile": new_user}})

            return {'message': 'Account Created Successfully!'}, 201

        except KeyError:
            return {'message': 'Bad Request!'}, 400


@ns_account.route('/signin')
class Signin(Resource):
    @api.response(200, 'Successful')
    @api.response(401, 'Unauthorized')
    @api.response(400, 'Bad Request Error')
    @api.doc(description="Generates a authentication token")
    @api.expect(indicator_model, validate=True)
    def post(self):
        try:
            account_info = request.json
        except:
            return {'message': 'Bad Request!'}, 400

        try:
            alldata = col.select_all_collection()
            selected_data = []
            for item in alldata:
                if "user_profile" in item:
                    selected_data = item["user_profile"]

            for single_user in selected_data:
                if single_user["email"] == account_info['email'] and single_user["password"] == account_info['password']:
                    return {"token": auth.generate_token(account_info['email'])}, 200
            return {"message": "authorization has been refused."}, 401
        except:
            return {"message": "authorization has been refused."}, 401


@ns_account.route('/signout/<string:token>')
class Signout(Resource):
    @api.response(200, 'Successful')
    @api.doc(description="Signout current user.")
    # @requires_authentication
    def delete(self, token):
        auth.delete_token(token)
        return {'message': 'Deletion Successful'}, 200


@ns_account.route('/manage_profile/<string:request_user_id>')
class Manage_profile(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Profile Does Not Exist')
    @api.doc(description="get other user's profile")
    def get(self, request_user_id):
        alldata = col.select_all_collection()
        selected_data = []
        for item in alldata:
            if "user_profile" in item:
                selected_data = item["user_profile"]

        for single_user in selected_data:
            if str(single_user["user_id"]) == str(request_user_id):
                new_user_profile = dict()
                new_user_profile["age"] = single_user["age"]
                new_user_profile["phone_number"] = single_user["phone_number"]
                new_user_profile["email"] = single_user["email"]
                new_user_profile["first_name"] = single_user["first_name"]
                new_user_profile["last_name"] = single_user["last_name"]
                new_user_profile["favorites"] = single_user["favorites"]

                response = {
                    "message": "OK",
                    "data": new_user_profile
                }
                return response, 200

        response = {
            "message": "Profile does not exist",
            "data": ""
        }
        return response, 404

    @api.response(200, 'User Profile Updated Successfully')
    @api.response(400, 'Bad Request Error')
    @api.response(404, 'Profile Does Not Exist')
    @api.doc(description="manage user's profile")
    @api.expect(user_profile, validate=True)
    def put(self, request_user_id):
        try:
            user_profile_json = request.json
        except:
            return {'message': 'Bad Request!', "data": ""}, 400

        alldata = col.select_all_collection()
        selected_data = []
        for item in alldata:
            if "user_profile" in item:
                selected_data = item["user_profile"]

        found = False
        col.delete_specific_collection(
            {"col_id": "c1"}, {"$unset": {"user_profile": 1}})
        for single_user in selected_data:
            if str(single_user["user_id"]) != str(request_user_id):
                col.add_one_dict_to_array(
                    {"col_id": "c1"}, {"$push": {"user_profile": single_user}})
            else:
                found = True
                if len(user_profile_json.keys()) != 0:
                    new_user_profile = dict()
                    update_single_user = single_user
                    for key, value in user_profile_json.items():
                        new_user_profile[key] = value

                        if isinstance(value, list):
                            if key == 'invisiable':
                                update_single_user["password"] = value[0]["password"]
                                update_single_user["payment_method"] = value[0]["payment_method"]
                            elif key == 'favorites':
                                # print (update_single_user["favorites"])
                                # print (value[0]["favorites"])
                                update_single_user["favorites"] = value[0]
                        else:
                            update_single_user[key] = value
                    # selected_data[index] = update_single_user
                    col.add_one_dict_to_array(
                        {"col_id": "c1"}, {"$push": {"user_profile": update_single_user}})
                    response = {
                        "message": "OK",
                        "data": new_user_profile
                    }
                else:
                    response = {
                        "message": "User did not specify any field to update",
                        "data": single_user
                    }
                    return response, 200

        if found == True:
            return response, 200

        response = {
            "message": "Specified user id does not exist",
            "data": ""
        }
        return response, 404


#######################################
#  Routes for a single auction item.  #
#######################################
"""

POST: Create a an auction item
GET: Get auction information by item id

"""
dummy_database = []

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
        "seller_name": fields.String,
        "seller_id": fields.Integer,
        "category_id": fields.Integer,
        "title": fields.String,
        "description": fields.String,
        "end_time": fields.String,
        "price": fields.Float,
        "image": fields.String,
    }
)

auction_info_update = api.model(
    'Update auction details (user may specify only some of the fields)',
    {
        "category_id": fields.Integer,
        "title": fields.String,
        "description": fields.String,
        "end_time": fields.String,
        "price": fields.Float,
        "image": fields.String,
    }
)


# user_input_filter = api.model(
#    'User input to search',
#    {
#        "location":fields.String,
#        "start_price":fields.String,
#        "end_price":fields.Integer,
#        "start_date":fields.Integer,
#        "end_time":fields.String,
#        "category":fields.String,
#    }
# )


@ns_auction.route('')
class CreateSingleAuctionItem(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Failed to create a new auction')
    @api.expect(user_input_single_auction_item)
    @api.doc(description="create an auction item")
    def post(self):
        au_col = mydb['auctions']

        new_auction = \
            {
                "id": au_col.count_documents({}),
                "created": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "updated": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "bidding_info": [],
                "status": "bidding"
            }

        user_input = request.json
        for i in ['seller_name', 'seller_id', 'category_id', 'title', "description", "end_time", "price", "image"]:
            new_auction[i] = user_input[i]
            # Input validation: Detect missing fields
            if user_input[i] == "" or user_input[i] is None:
                return {'message': 'Bad Request: field ' + i + ' is missing'}, 400

        # Input validation: End_time validation
        if not validate_datetime_str(user_input['end_time']):
            return {'message': 'Bad Request: invalid end_time format'}

        try:
            au_col.insert_one(new_auction)
            del new_auction['_id']

            message = "Auction create successfully"
            response = \
                {
                    "message": message,
                    "data": new_auction
                }
            return response, 200
        except:
            return {'message': 'Bad Request'}, 400


@ns_auction.route('/<item_id>')
@api.param('item_id', 'Item ID given when the auction is created')
class SingleAuctionItemOperations(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Specified item does not exist')
    @api.doc(description="get information of an auction item")
    def get(self, item_id):
        au_col = mydb['auctions']
        try:
            retrieved_item = au_col.find_one({'id': int(item_id)})
            del retrieved_item['_id']

            return {"message": "OK", "data": retrieved_item}, 200
        except:
            return {"message":  "Specified item does not exist"}, 404

    @api.response(200, 'OK')
    @api.response(404, 'Specified item does not exist')
    @api.expect(auction_info_update)
    @api.doc(description="Update auction item details")
    def put(self, item_id):
        user_input = request.json
        try:
            au_col = mydb['auctions']
            retrieved_item = au_col.find_one({'id': int(item_id)})

            if retrieved_item == None:
                return {"message":  "Specified item does not exist"}, 404

            del retrieved_item['_id']

            # Input validation: End_time validation
            if not validate_datetime_str(user_input['end_time']):
                return {'message': 'Bad Request: invalid end_time format'}

            update_data = {}
            for k in ['category_id', 'title', "description", "end_time", "price", "image"]:
                if k in user_input.keys() and retrieved_item[k] != user_input[k]:
                    update_data[k] = user_input[k]

            res = au_col.update_one({"id": int(item_id)}, {
                                    "$set": update_data})
            return {"message": "Auction details have been updated"}, 200
        except:
            return {"message":  "Auction details have been updated"}, 404
        # if len(user_input_json.keys()) != 0:
        #     # update auction details
        #     for k in user_input_json.keys():
        #         target_auction[k] = user_input_json[k]

        #     target_auction["updated"] = datetime.now().strftime(
        #         '%Y-%m-%d %H:%M:%S')

        #     dummy_database[item_id] = target_auction
        #     updated_auction = target_auction
        # else:
        #     message = "User did not specify any field to update"
        #     updated_auction = ""
        # response = \
        #     {
        #         "message": message,
        #         "data": updated_auction
        #     }
        # return {"message": "OK", "data": retrieved_item}, 200

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
        print(search_key)
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
    @api.param('endPrice', '')
    @api.param('startPrice', '')
    @api.param('endDate', 'YYYY/MM/DD')
    @api.param('startDate', 'YYYY/MM/DD')
    @api.doc(description="Search by filter")
    def get(self):
        collection = mydb['auctions']
        result = []
        mid = []
        print(request.args)
        print("123")
        location = request.args.get('location')

        endDate = request.args.get('endDate')
        startDate = request.args.get('startDate')

        category = request.args.get('category')

        endPrice = request.args.get('endPrice')
        startPrice = request.args.get('startPrice')

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
            entryDateP = datetime.datetime.strptime(
                entry['end_time'], "%Y-%m-%d %H:%M:%S")
            print(entryDateP)
            print(startDateP)
            print()
            if entryDateP <= startDateP or entryDateP >= endDateP:
                if entry in result:
                    result.remove(entry)

        for entry in mid:
            if entry['price'] < int(startPrice) or entry['price'] > int(endPrice):
                if entry in result:
                    result.remove(entry)

        for entry in mid:
            if category and entry['category_id'] != category:
                if entry in result:
                    result.remove(entry)

        # location is db

        return result, 200


###################################
#  Routes for bidding management  #
###################################

# Propose a bidding
@ns_bidding.route('/<item_id>')
@api.param('item_id', 'Item ID given when the auction is created')
class BiddingManagement(Resource):

    @api.response(200, 'OK')
    @api.response(404, 'Requested Resource Does Not Exist')
    @api.expect(user_input_bidding_info)
    @api.doc(description="Propose a bid on an item")
    def post(self, item_id):
        au_col = mydb['auctions']
        retrieved_item = au_col.find_one({'id': int(item_id)})

        if retrieved_item is None:
            return {"message": "Specified item does not exist"}, 404

        del retrieved_item['_id']
        new_bidding_info = request.json
        # Input validation: Detect missing fields
        for k in ['user_id','proposal_price']:
            if new_bidding_info[k] == "" or new_bidding_info[k] is None:
                return {'message': 'Bad Request: field ' + k + ' is missing'}, 400

        message = "The bidding has been created successfully"
        status_code = 200
        # update database
        # try:
        #     if_no_bidding = True if len(
        #         retrieved_item["bidding_info"]) == 0 else False
        #     if if_no_bidding:
        #         retrieved_item["bidding_info"].append(
        #             new_bidding_info)
        #     else:
        #         current_highest_price = dummy_database[item_id]["bidding_info"][0]["proposal_price"]
        #         new_proposed_price = new_bidding_info["proposal_price"]
        #         if_overbid = True if new_proposed_price > current_highest_price else False
        #         if if_overbid:
        #             dummy_database[item_id]["bidding_info"][0] = new_bidding_info
        #         else:
        #             message = "Bidding failed, the new price is not higher than the current price"
        #
        # except IndexError:
        #     message = "Specified item does not exist"
        #     status_code = 404
        retrieved_item["bidding_info"].append(new_bidding_info)
        # sort bidding info by proposal_price (descending)
        sorted_bidding_info_list = sorted(retrieved_item["bidding_info"],
                                          key=lambda i: i['proposal_price'], reverse=True)
        current_highest_price = sorted_bidding_info_list[0]["proposal_price"]
        new_proposed_price = new_bidding_info["proposal_price"]
        if_overbid = True if new_proposed_price > current_highest_price else False
        if if_overbid:
            retrieved_item["bidding_info"] = sorted_bidding_info_list
            au_col.update_one({"id": int(item_id)}, {"$set": retrieved_item})
        else:
            message = "Bidding failed, the new price is not higher than the current price"

        data = {
            "item_id": item_id,
            "bidding_info": new_bidding_info
        }
        response = \
            {
                "message": message,
                "data": data
            }
        return response, status_code


# Accept or decline a bidding
@ns_bidding.route('/operations/<item_id>/<operation>')
@api.param('item_id', 'Item ID given when the auction is created')
@api.doc(params={
    'item_id': 'Item ID given when the auction is created',
    'operation': '\"accept\"\: accept a bid, \"decline\"\: decline a bid '
})
class AcceptOrDeclineBiddings(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Requested Resource Does Not Exist')
    @api.doc(description="Accept or decline a the highest bidding on an item")
    def put(self, item_id, operation):
        au_col = mydb['auctions']
        retrieved_item = au_col.find_one({'id': int(item_id)})
        if retrieved_item is None:
            return {"message": "Specified item does not exist"}, 404

        del retrieved_item['_id']
        status_code = 200
        if operation == "accept":
            retrieved_item["status"] = "Accepted"
            message = "The bid has been accepted"
        elif operation == "decline":
            retrieved_item["status"] = "Declined"
            message = "The bid has been declined"
        else:
            message = "Invalid operation"
        au_col.update_one({"id": int(item_id)}, {"$set": retrieved_item})
        response = \
            {
                "message": message
            }
        return response, status_code


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9999, debug=True)
