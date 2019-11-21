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

# ===== database connection ===
client = pymongo.MongoClient(config.MONGO_URI)
mydb = client[config.MONGO_DB]
# =============================

# ==============================   Helper functions   ==========================
# validate_datetime_str -- datetime validation
# getUserById
# getAuctionById
# getBuyerInfoByIds
# =============================================================================


def validate_datetime_str(str):
    try:
        # check if the str match the format : YYYY-MM-DD HH:MM:SS e.g 2010-01-01 12:00:00
        datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False


def getUserByIds(ids):
    col = mydb['user']
    res = list([col.find_one({"user_id": int(id)}, {'_id': 0}) for id in ids])
    if len(ids) == 1:
        return res[0]
    else:
        return res


def getBuyerInfoByIds(ids):
    col = mydb['user']
    res = list([col.find_one({"user_id": int(id)}, {'_id': 0, "user_id": 1, "avatar": 1,
                                                    "rating": 1, "location": 1, "first_name": 1, "last_name": 1}) for id in ids])
    if len(ids) == 1:
        return res[0]
    else:
        return res


def getAuctionWithSellerByAuctionId(id=None):
    pineline = []
    if isinstance(id, int):
        pineline.append({"$match": {"id": id}})
    # without id, it will return all auctions
    pineline += \
        [{"$lookup":
          {
              "from": "user",
              "localField": "seller_id",
              "foreignField": "user_id",
              "as": "seller"
          }
          }, {
            "$unwind": "$seller"
        }, {
            "$project":
            {
                "_id": 0,
                "id": 1,
                "seller_name": 1,
                "seller_id": 1,
                "category": 1,
                "title": 1,
                "description": 1,
                "created": 1,
                "updated": 1,
                "end_time": 1,
                "location": 1,
                "price": 1,
                "image": 1,
                "bidding_info": 1,
                "seller.user_id": 1,
                "seller.avatar": 1,
                "seller.phone_number": 1,
                "seller.email": 1,
                "seller.first_name": 1,
                "seller.last_name": 1,
                "seller.favorites": 1,
                "seller.rating": 1,
                "seller.location": 1,
                "seller.payment_method": 1,
                "users_bidding": 1
            }
        }]

    au_col = mydb['auctions']
    res = au_col.aggregate(pineline)

    if isinstance(id, int):
        return list(res)[0]
    return list(res)


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
        "item_id": fields.Integer,
        "proposal_price": fields.Float,
    }
)


auction_info = api.model(
    'Auction item information',
    {
        "id": fields.Integer,
        "seller_name": fields.String,
        "seller_id": fields.Integer,
        "category": fields.Integer,
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
        "dob": fields.String,
        "phone_number": fields.String,
        "favorites": fields.List(fields.Nested(auction_info)),
        "avatar": fields.String,
        "location": fields.String,
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
        col = mydb['user']
        cursor = col.find()
        id_counter = 0

        try:
            accountInfo = request.json
        except:
            return {'message': 'Bad Request!??'}, 400

        print(request.json)

        found = False
        for single_user in cursor:
            id_counter = id_counter + 1
            if single_user["email"] == accountInfo["email"]:
                found = True

        if found == True:
            return {'message': 'Email Already Exists'}, 200
        else:
            print('+++++++ '+str(id_counter)+' +++++++++')
            new_user = {
                "user_id": id_counter,
                "email": accountInfo["email"],
                "password": accountInfo["password"],
                "first_name": "",
                "last_name": "",
                "dob": "",
                "phone_number": "",
                "payment_method": "",
                "favorites": [],
                "location": "",
                "rating": 0,
                "avatar": "",
                "auctions": [],
                "bids": []
            }
            col.insert_one(new_user)

            print("new user is")
            print(new_user)
            return {'message': 'Account Created Successfully!'}, 201


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
        col = mydb['user']
        cursor = col.find()

        print(account_info)

        for single_user in cursor:
            print(single_user)
            if single_user["email"] == account_info["email"] and single_user["password"] == account_info["password"]:
                print('find')
                return_m = {  # Just response all user informatin change if some of that is not needed
                    "user_id": single_user['user_id'],
                    "email": single_user['email'],
                    "first_name": single_user['first_name'],
                    "last_name": single_user['last_name'],
                    "dob": single_user['dob'],
                    "phone_number": single_user['phone_number'],
                    "payment_method": single_user['payment_method'],
                    "favorites": single_user['favorites'],
                    "auctions": single_user['auctions'],
                    "location": single_user['location'],
                    "rating": single_user['rating'],
                    "avatar": single_user['avatar'],
                    "bids": single_user['bids'],
                    "token": auth.generate_token(account_info['email'])
                }

                return return_m, 200
        return {"message": "authorization has been refused."}, 401


@ns_account.route('/signout/<string:token>')
class Signout(Resource):
    @api.response(200, 'Successful')
    @api.doc(description="Signout current user.")
    # @requires_authentication
    def delete(self, token):
        auth.delete_token(token)
        return {'message': 'Deletion Successful'}, 200


@ns_account.route('/get_user_auctions/<string:request_user_id>')
class User_auctions(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'User Does Not Exist')
    @api.doc(description="get user's auctions")
    def get(self, request_user_id):
        col = mydb['user']
        au_col = mydb['auctions']
        single_user = col.find_one({"user_id": int(request_user_id)})
        # del single_user['_id']

        if single_user is None:
            response = {
                "message": "User does not exist",
                "data": ""
            }
            return response, 404

        retrieved_auctions = []
        auction_id_list = single_user["auctions"]
        for single_auction in auction_id_list:
            try:
                retrieved_item = getAuctionWithSellerByAuctionId(
                    int(single_auction))
                buyers = getBuyerInfoByIds(
                    [str(id) for id in retrieved_item['users_bidding']])
                if len(retrieved_item['users_bidding']) == 1:
                    buyers = [buyers]
                for bid in retrieved_item['bidding_info']:
                    for u in buyers:
                        if u['user_id'] == bid['user_id']:
                            bid['buyer'] = u
                            del bid['user_id']
                            break

                del retrieved_item['users_bidding']
                retrieved_auctions.append(retrieved_item)
            except:
                return {"message":  "Specified item does not exist"}, 404

        response = {
            "message": "OK",
            "data": retrieved_auctions
        }
        return response, 200


@ns_account.route('/get_user_biddings/<string:request_user_id>')
class User_biddings(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'User Does Not Exist')
    @api.doc(description="get user's biddings")
    def get(self, request_user_id):
        col = mydb['user']
        au_col = mydb['auctions']
        single_user = col.find_one({"user_id": int(request_user_id)})
        if single_user is None:
            response = {
                "message": "User does not exist",
                "data": ""
            }
            return response, 404

        try:
            retrieved_favorites = []
            auction_id_list = single_user["bids"]
            for single_auction in auction_id_list:
                retrieved_item = getAuctionWithSellerByAuctionId(
                    int(single_auction))
                buyers = getBuyerInfoByIds(
                    [str(id) for id in retrieved_item['users_bidding']])
                if len(retrieved_item['users_bidding']) == 1:
                    buyers = [buyers]
                for bid in retrieved_item['bidding_info']:
                    for u in buyers:
                        if u['user_id'] == bid['user_id']:
                            bid['buyer'] = u
                            del bid['user_id']
                            break

                del retrieved_item['users_bidding']
                retrieved_favorites.append(retrieved_item)

            response = {
                "message": "OK",
                "data": retrieved_favorites
            }
            return response, 200
        except:
            return {"message":  "Specified item does not exist"}, 404


@ns_account.route('/get_user_favorites/<string:request_user_id>')
class User_favorites(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'User Does Not Exist')
    @api.doc(description="get user's favorites")
    def get(self, request_user_id):
        col = mydb['user']
        au_col = mydb['auctions']
        single_user = col.find_one({"user_id": int(request_user_id)})
        # del single_user['_id']

        if single_user is None:
            response = {
                "message": "User does not exist",
                "data": ""
            }
            return response, 404

        try:
            retrieved_favorites = []
            auction_id_list = single_user["favorites"]
            for single_auction in auction_id_list:
                # retrieved_item = au_col.find_one({'id': int(single_auction)})
                # del retrieved_item['_id']
                retrieved_item = getAuctionWithSellerByAuctionId(
                    int(single_auction))
                buyers = getBuyerInfoByIds(
                    [str(id) for id in retrieved_item['users_bidding']])
                if len(retrieved_item['users_bidding']) == 1:
                    buyers = [buyers]
                for bid in retrieved_item['bidding_info']:
                    for u in buyers:
                        if u['user_id'] == bid['user_id']:
                            bid['buyer'] = u
                            del bid['user_id']
                            break

            del retrieved_item['users_bidding']

            retrieved_favorites.append(retrieved_item)

            response = {
                "message": "OK",
                "data": retrieved_favorites
            }
            return response, 200

        except:
            print(single_user["favorites"], '@@@')

            return {"message":  "Specified item does not exist"}, 404


@ns_account.route('/manage_profile/<string:request_user_id>')
class Manage_profile(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Profile Does Not Exist')
    @api.doc(description="get other user's profile")
    # @api.param('request_user_id',  'Request User Id',type=int,required=True)
    def get(self, request_user_id):
        col = mydb['user']
        single_user = col.find_one({"user_id": int(request_user_id)})
        del single_user['_id']

        new_user_profile = dict()
        new_user_profile["user_id"] = single_user["user_id"]
        new_user_profile["dob"] = single_user["dob"]
        new_user_profile["phone_number"] = single_user["phone_number"]
        new_user_profile["email"] = single_user["email"]
        new_user_profile["first_name"] = single_user["first_name"]
        new_user_profile["last_name"] = single_user["last_name"]
        new_user_profile["favorites"] = single_user["favorites"]
        new_user_profile["avatar"] = single_user["avatar"]
        new_user_profile["rating"] = single_user["rating"]
        new_user_profile["location"] = single_user["location"]
        new_user_profile["payment_method"] = single_user["payment_method"]

        response = {
            "message": "OK",
            "data": new_user_profile
        }
        return response, 200

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

        col = mydb['user']
        single_user = col.find_one({"user_id": int(request_user_id)})
        del single_user['_id']
        print(single_user)

        if single_user is None:
            response = {
                "message": "Specified user id does not exist",
                "data": ""
            }
            return response, 404

        if len(user_profile_json.keys()) == 0:
            response = {
                "message": "User did not specify any field to update",
                "data": single_user
            }
            return response, 200

        update_single_user = single_user
        for key, value in user_profile_json.items():

            if key == 'invisiable':
                update_single_user["password"] = value[0]["password"]
                update_single_user["payment_method"] = value[0]["payment_method"]
            # elif key == 'favorites':
            #     update_single_user["favorites"] = value[0]
            else:
                update_single_user[key] = value
        col.update_one({"user_id": int(request_user_id)},
                       {"$set": update_single_user})

        response = {
            "message": "OK",
            "data": update_single_user
        }
        return response, 200


#########################
#  Routes for Auction.  #
#########################
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
    }
)

user_input_single_auction_item = api.model(
    'User input to create auction',
    {
        "seller_name": fields.String,
        "seller_id": fields.Integer,
        "category": fields.Integer,
        "title": fields.String,
        "description": fields.String,
        "end_time": fields.String,
        "price": fields.Float,
        "image": fields.List(fields.String),
        "location": fields.String

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
    @api.response(404, 'Failed to create a new auction')
    @api.expect(user_input_single_auction_item)
    @api.doc(description="create an auction item")
    def post(self):
        au_col = mydb['auctions']

        user_col = mydb['user']
        created_time = datetime.datetime.now()
        # created_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        auction_id = au_col.count_documents({})
        new_auction = \
            {
                "id": auction_id,
                "created": created_time.strftime('%Y-%m-%d %H:%M:%S'),
                "updated": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "bidding_info": [],
                "status": "bidding"
            }

        user_input = request.json
        for i in ['seller_name', 'seller_id', 'category', 'title', "description",
                  "end_time", "price", "image", "location"]:
            new_auction[i] = user_input[i]
            # Input validation: Detect missing fields
            if user_input[i] is None:
                return {'message': 'Bad Request: field ' + i + ' is missing'}, 400

        # Input validation: End_time validation
        end_time = user_input['end_time']
        if not validate_datetime_str(end_time):
            return {'message': 'Bad Request: invalid end_time format'}

        # Input validation: End_time should be later than create time
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        if end_time <= created_time:
            return {'message': "Bad Request: end time must be later than the created time "}, 400
        try:
            au_col.insert_one(new_auction)
            del new_auction['_id']

            message = "Auction create successfully"
            response = \
                {
                    "message": message,
                    "data": new_auction
                }

            # add auction to user's 'auction' field
            seller = user_col.find_one({"user_id":  user_input['seller_id']})
            seller['auctions'].append(auction_id)
            user_col.update_one({"user_id":  user_input['seller_id']}, {
                                "$set": {"auctions": seller['auctions']}})  # :-()
            return response, 200
        except:
            return {'message': 'Bad Request'}, 400

    @api.response(200, 'OK')
    @api.response(404, 'No auction data stored in database')
    @api.doc(description="get information of all auction data in the database")
    def get(self):
        au_col = mydb['auctions']
        retrieved_items = []
        max_result_size = 10
        res = getAuctionWithSellerByAuctionId()
        for item in res[:max_result_size]:

            buyers = getBuyerInfoByIds([str(id)
                                        for id in item['users_bidding']])
            if len(item['users_bidding']) == 1:
                buyers = [buyers]
            for bid in item['bidding_info']:
                for u in buyers:
                    if u['user_id'] == bid['user_id']:
                        bid['buyer'] = u
                        del bid['user_id']
                        break

            del item['users_bidding']
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


user_input_add_or_remove_fav_auction = api.model(
    'User input to add an auction to the favourite list',
    {
        "user_id": fields.Integer,
        "auction_id": fields.Integer

    }
)


@ns_auction.route('/favorite/set')
class AddFavAuction(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Specified item does not exist')
    @api.expect(user_input_add_or_remove_fav_auction)
    @api.doc(description="add an auction item to the favourite list of a user")
    def put(self):
        user_input = request.json
        user_id = int(user_input["user_id"])
        auction_id = int(user_input["auction_id"])

        user_col = mydb['user']
        user = user_col.find_one({"user_id": user_id})

        if user is None:
            response = {
                "message": "User does not exist",
                "result": "Fail"
            }
            status_code = 404
            return response, status_code
        del user['_id']
        auc_col = mydb['auctions']
        auction = auc_col.find_one({"id": auction_id})

        if auction is None:
            response = {
                "message": "Auction item does not exist",
                "result": "Fail"
            }
            status_code = 404
            return response, status_code

        fav = set(user["favorites"])
        fav.add(auction_id)
        if len(fav) != len(user['favorites']):
            user["favorites"].append(auction_id)

        user_col.update_one({"user_id": user_id}, {"$set": user})

        response = {
            "message": "favourite auction is added",
            "result": "OK"
        }
        status_code = 200
        return response, status_code


@ns_auction.route('/favorite/unset')
class RemoveFavAuction(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Specified item does not exist')
    @api.expect(user_input_add_or_remove_fav_auction)
    @api.doc(description="remove an auction item from the favourite list of a user")
    def put(self):
        user_input = request.json
        user_id = int(user_input["user_id"])
        auction_id = int(user_input["auction_id"])

        user_col = mydb['user']
        user = user_col.find_one({"user_id": user_id})

        if user is None:
            response = {
                "message": "User does not exist",
                "result": "Fail"
            }
            status_code = 404
            return response, status_code
        del user['_id']
        auc_col = mydb['auctions']
        auction = auc_col.find_one({"id": auction_id})

        if auction is None:
            response = {
                "message": "Auction item does not exist",
                "result": "Fail"
            }
            status_code = 404
            return response, status_code

        try:
            user["favorites"].remove(auction_id)
        except ValueError:
            response = {
                "message": "Auction is not in the favourite list of the user",
                "result": "Fail"
            }
            return response, 404

        user_col.update_one({"user_id": user_id}, {"$set": user})

        response = {
            "message": "favourite auction is removed",
            "result": "OK"
        }
        status_code = 200
        return response, status_code


user_input_rating = api.model(
    'User input to rate an auction',
    {
        "buyer_id": fields.Integer,
        "item_id": fields.Integer,
        "rating": fields.Integer

    }
)


@ns_auction.route('/rating')
class Rating(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Specified item does not exist')
    @api.expect(user_input_rating)
    @api.doc(description="rate an auction item after winning a bidding")
    def put(self):
        user_input = request.json
        user_id = int(user_input["user_id"])
        auction_id = int(user_input["item_id"])

        user_col = mydb['user']
        user = user_col.find_one({"user_id": user_id})

        # Validations
        if user is None:
            response = {
                "message": "User does not exist",
                "result": "Fail"
            }
            status_code = 404
            return response, status_code

        del user['_id']
        auc_col = mydb['auctions']
        auction = auc_col.find_one({"id": auction_id})

        if auction is None:
            response = {
                "message": "Auction item does not exist",
                "result": "Fail"
            }
            status_code = 404
            return response, status_code
        del auction['_id']

        auction_status = auction['status']
        if auction_status != "Accepted":
            response = {
                "message": "The auction is currently in bidding or already declined",
                "result": "Fail"
            }
            status_code = 400
            return response, status_code

        biddings = auction['bidding_info']
        sorted_bidding_info_list = sorted(
            biddings, key=lambda i: i['proposal_price'], reverse=True)

        bidding_winner = sorted_bidding_info_list[0]["user_id"]
        if bidding_winner != user_id:
            response = {
                "message": "Only buyer who won the bidding can rate the auction item and seller",
                "result": "Fail"
            }
            status_code = 400
            return response, status_code

        # end of validations
        rating_info = user_input
        rating_info["rating_id"] = user_col.count_documents({})
        user_col.insert_one(rating_info)

        response = {
            "message": "The auction has been rated",
            "result": "OK"
        }
        status_code = 200
        return response, status_code


@ns_auction.route('/rating/<item_id>')
@api.param('item_id', 'Item ID given when the auction is created')
class GetRating(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Specified item does not exist')
    @api.doc(description="get all ratings on an auction item specified by")
    def get(self, item_id):
        user_col = mydb['user']
        ratings = user_col.find({"item_id": item_id})
        data = []
        for rating in ratings:
            data.append(rating)

        if len(data) == 0:
            response = \
                {
                    "message": "No ratings on the auction so far",
                    "result": "Fail"
                }
            return response, 400

        response = \
            {
                "result": "OK",
                "item_id": item_id,
                "ratings": data
            }
        return response, 200


# what use case this for??
@ns_auction.route('/get_category/<auction_id>')
class SingleAuctionCategory(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Auction item does not exist')
    @api.doc(description="get category of an auction item")
    def get(self, auction_id):
        au_col = mydb['auctions']
        try:
            # retrieved_item = au_col.find_one({'id': int(auction_id)})
            # del retrieved_item['_id']
            retrieved_item = getAuctionWithSellerByAuctionId(int(auction_id))

            category = retrieved_item['category']

            return {"message": "OK", "data": category}, 200
        except:
            return {"message":  "Auction item does not exist"}, 404


@ns_auction.route('/<item_id>')
@api.param('item_id', 'Item ID given when the auction is created')
class SingleAuctionItemOperations(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Specified item does not exist')
    @api.doc(description="get information of an auction item")
    def get(self, item_id):
        try:
            retrieved_item = getAuctionWithSellerByAuctionId(int(item_id))
            buyers = getBuyerInfoByIds(
                [str(id) for id in retrieved_item['users_bidding']])
            for bid in retrieved_item['bidding_info']:
                buyer_info = next(
                    filter(lambda x: x['user_id'] == bid['user_id'], buyers))
                bid['buyer'] = buyer_info
                del bid['user_id']

            del retrieved_item['users_bidding']
            if retrieved_item is None:
                return {"message":  "Specified item does not exist"}, 404
            return {"message": "OK", "data": retrieved_item}, 200
        except:
            return {"message":  "Specified item does not exist"}, 404

    @api.response(200, 'OK')
    @api.response(404, 'Specified item does not exist')
    @api.doc(description="Delete an auction")
    def delete(self, item_id):
        au_col = mydb['auctions']
        user_col = mydb['user']
        # retrieved_item = au_col.find_one({'id': int(item_id)})
        # del retrieved_item['_id']
        retrieved_item = getAuctionWithSellerByAuctionId(int(item_id))

        if retrieved_item is None:
            return {"message": "Specified item does not exist"}, 404

        seller_id = int(retrieved_item['seller_id'])
        seller = user_col.find_one({"user_id": seller_id})
        del seller['_id']

        try:
            res = au_col.remove({"id": int(item_id)})
            # remove the specified auction from the auction list of the user
            # seller['auctions'] = \
            #     [x for x in seller['auctions'] if int(x["id"]) != int(item_id)]

            seller['auctions'].remove(item_id)
            seller['bids'].remove(item_id)
            seller['favorites'].remove(item_id)

            user_col.update_one({"user_id": seller_id}, {"$set": seller})
            return {"message": "Specified item is deleted successfully", "data": retrieved_item}
        except:
            return {"message": "Failed to delete specified item"}, 200

    @api.response(200, 'OK')
    @api.response(404, 'Specified item does not exist')
    @api.expect(auction_info_update)
    @api.doc(description="Update auction item details")
    def put(self, item_id):
        user_input = request.json
        try:
            au_col = mydb['auctions']
            user_col = mydb['user']
            retrieved_item = au_col.find_one({'id': int(item_id)})
            del retrieved_item['_id']

            if retrieved_item is None:
                return {"message":  "Specified item does not exist"}, 404

            seller_id = int(retrieved_item['seller_id'])
            seller = user_col.find_one({"user_id": seller_id})

            update_data = {}
            for k in ['category', 'title', "description", "end_time", "price", "image", "location"]:
                if k in user_input.keys() and retrieved_item[k] != user_input[k]:
                    if k == 'end_time' and not validate_datetime_str(user_input['end_time']):
                        return {'message': 'Bad Request: invalid end_time format'}
                    update_data[k] = user_input[k]

            # Input validation: End_time validation

            update_data['updated'] = datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')
            # update auction in user's auctions list
            # for auction in seller['auctions']:
            #     if auction['id'] == int(item_id):
            #         auction_to_be_updated_index = seller['auctions'].index(auction)
            #
            # updated_auction = seller['auctions'][auction_to_be_updated_index]
            # for k in update_data.keys():
            #     updated_auction[k] = update_data[k]
            #
            # seller['auctions'][auction_to_be_updated_index] = updated_auction

            au_col.update_one({"id": int(item_id)}, {
                "$set": update_data})
            return {"message": "Auction details have been updated"}, 200
        except:
            return {"message":  "Auction details fail to updated"}, 404


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
        for e in cursor:
            entry = getAuctionWithSellerByAuctionId(e['id'])
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
    @api.param('endDate', 'YYYY-MM-DD')
    @api.param('startDate', 'YYYY-MM-DD')
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
            startDate = '2000-01-10 00:00:00'
        if endDate is None:
            endDate = datetime.datetime.now().strftime("'%Y-%m-%d %H:%M:%S'")

        endDateP = datetime.datetime.strptime(endDate, "'%Y-%m-%d %H:%M:%S'")
        startDateP = datetime.datetime.strptime(
            startDate, "'%Y-%m-%d %H:%M:%S'")

        cursor = collection.find()

        for entry in cursor:
            entry['_id'] = str(entry['_id'])
            result.append(entry)
            mid.append(entry)

        for entry in mid:
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

        # location is db

        return result, 200


###################################
#  Routes for bidding management  #
###################################

user_input_bidding_operations = api.model(
    'User input to accept or decline a bid',
    {
        "user_id": fields.Integer,
        "item_id": fields.Integer,
        "operation": fields.String
    }
)


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
        user_id = user_input['user_id']
        au_col = mydb['auctions']
        user_col = mydb['user']
        # retrieved_item = au_col.find_one({'id': int(item_id)})
        # del retrieved_item['_id']
        retrieved_item = getAuctionWithSellerByAuctionId(int(item_id))

        item_min_price = retrieved_item["price"]

        if retrieved_item is None:
            return {"result": "Fail", "message": "Item not found"}, 404

        buyer = user_col.find_one({'user_id': int(user_id)})
        if buyer is None:
            return {"result": "Fail", "message": "User does not exist"}, 404

        del buyer['_id']

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
            bid_id = au_col.count_documents({})
            new_bidding_info = {
                # "bid_id":bid_id,
                "created": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            for key in user_input.keys():
                new_bidding_info[key] = user_input[key]
            retrieved_item["bidding_info"].append(new_bidding_info)
            # insert into database
            # au_col.insert_one(new_bidding_info)
            del new_bidding_info["_id"]
            buyer['bids'].append(item_id)
            au_col.update_one({"id": int(item_id)}, {"$set": retrieved_item})
            user_col.update_one({"user_id": int(user_id)}, {"$set": buyer})
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
        # retrieved_item = au_col.find_one({'id': int(item_id)})
        # del retrieved_item['_id']
        retrieved_item = getAuctionWithSellerByAuctionId(int(item_id))

        result = "Fail"
        if retrieved_item is None:
            return {"result": result, "message": "Auction item not found"}, 404

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
        user_col = mydb['user']
        result = "Fail"
        retrieved_bid = au_col.find_one({'bid_id': int(bid_id)})
        if retrieved_bid is None:
            return {"result": result, "message": "Specified bidding does not exist"}, 404
        del retrieved_bid['_id']
        item_id = retrieved_bid["item_id"]
        # retrieved_item = au_col.find_one({'id': int(item_id)})
        # del retrieved_item['_id']
        retrieved_item = getAuctionWithSellerByAuctionId(int(item_id))

        if retrieved_item is None:
            return {"result": result, "message": "Specified auction item does not exist"}, 404

        if retrieved_item["status"] == "Accepted":
            return {"result": result, "message": "The bid is already accepted"}

        buyer_id = retrieved_bid["user_id"]
        buyer = user_col.find_one({'user_id': int(buyer_id)})
        del buyer['_id']

        try:
            au_col.remove({"bid_id": int(bid_id)})

            # remove the specified bidding from the bidding_info of the auction
            retrieved_item['bidding_info'] = \
                [x for x in retrieved_item['bidding_info']
                    if int(x["bid_id"]) != int(bid_id)]
            au_col.update_one({"id": int(item_id)}, {"$set": retrieved_item})
            # remove the specified bidding from the bids of the user
            # buyer['bids'] = \
            #     [x for x in buyer['bids'] if int(x["bid_id"]) != int(bid_id)]
            buyer['bids'].remove(item_id)

            user_col.update_one({"user_id": int(buyer_id)}, {"$set": buyer})
            return {"message": "Specified bidding is deleted successfully"}
        except:
            return {"message": "Failed to delete "}, 400


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9999, debug=True)
