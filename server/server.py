import json
from datetime import datetime as dt
import uuid
import re
import pandas as pd
import os, csv, base64,requests
from flask import Flask, request, Response
from flask_restplus import Resource, Api, fields, inputs, reqparse, abort
from setup_database import *
from functools import wraps
from time import time
from itsdangerous import SignatureExpired, JSONWebSignatureSerializer, BadSignature



class Token_authentication:
    def __init__(self, secret_key, expire_time):
        self.secret_key = secret_key
        self.expire_time = expire_time
        self.active_token = set()
        self.serializer = JSONWebSignatureSerializer(secret_key)


    def generate_token(self, username):
        info = {
            'username': username,
            'creation_time': time()
        }

        token = self.serializer.dumps(info)
        print('token serializer is '+str(token))

        new_token = token.decode()
        self.active_token.add(new_token)
        print(f'adding a new token {new_token}')
        print(f'active tokens are {self.active_token}')
        return new_token


    def get_token_info(self, token):
        print(f'validating token {token}')
        info = self.serializer.loads(token.encode())
        return info['username']


    def validate_token(self, token):
        print(f'validating token {token}')
        info = self.serializer.loads(token.encode())

        if token not in self.active_token:
            raise SignatureExpired("The Token is no longer active!")
        elif time() - info['creation_time'] > self.expire_time:
            self.active_token.discard(token)
            print(f'now deleting token {token}')
            print(f'now active tokens are {self.active_token}')
            raise SignatureExpired("The Token has been expired; get a new token!")
        return info['username']


    def delete_token(self, token):
        print ('--- now active tokens are '+str(self.active_token))
        self.active_token.discard(token)
        print(f'now deleting token {token}')
        print(f'now active tokens are {self.active_token}')
        return True



def upload_local_items(col):
    with open('../data/data1.json', 'r') as f:
        content = json.load(f)
        col.insert_many_collections([content])




def requires_authentication(authen):
    @wraps(authen)
    def decorated(*args, **kwargs):
        token = request.headers.get('AUTH-TOKEN')
        print(f'geting token {token}')
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




col = Collection()
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

# define namespaces
ns_account = api.namespace('account',description='Operations related to user accounts')
ns_auction = api.namespace('auction',description='Operations related to auction information management')
ns_bidding = api.namespace('bidding',description='Operations related to management')


# signin_model = api.model('signin_info', {
#     'username': fields.String,
#     'password': fields.String
# })

# signin_parser = reqparse.RequestParser()
# signin_parser.add_argument('username', type=str)
# signin_parser.add_argument('password', type=str)

db = local_user_account_database()
profile_tmp_database = []


########################################
#  Routes for user account management  #
########################################


indicator_model = api.model(
    'credentials', {
        'username': fields.String,
        'password': fields.String
    }
)

indicator_parser = reqparse.RequestParser()
indicator_parser.add_argument('username', type=str)
indicator_parser.add_argument('password', type=str)


payment_method_visa = api.model(
    'Payment method: visa',
    {
        "card_number":fields.Integer,
        "name_on_card":fields.String,
        "expiry_month":fields.Integer,
        "expiry_year":fields.Integer,
        "cvv":fields.Integer
    }
)


payment_method_master = api.model(
    'Payment method: master',
    {
        "card_number":fields.Integer,
        "name_on_card":fields.String,
        "expiry_month":fields.Integer,
        "expiry_year":fields.Integer,
        "cvv":fields.Integer
    }
)


payment_method_wechat = api.model(
    'Payment method: wechat',
    {
        "payment_number":fields.Integer
    }
)


user_profile_visiable = api.model(
    "User profile visiable",{
        "first_name":fields.String,
        "last_name":fields.String,
        "email":fields.String,
        "age":fields.Integer,
        "password":fields.String,
        "payment_method":fields.String,
        "payment_method_visa":fields.List(fields.Nested(payment_method_visa)),
        "payment_method_master":fields.List(fields.Nested(payment_method_master)),
        "payment_method_wechat":fields.List(fields.Nested(payment_method_wechat))
    }
)


user_profile_invisiable = api.model(
    "User profile invisiable",{
        "first_name":fields.String,
        "last_name":fields.String,
        "email":fields.String,
    }
)


user_profile = api.model(
    'User profile',{
        "invisiable":fields.List(fields.Nested(user_profile_invisiable)),
        "visiable":fields.List(fields.Nested(user_profile_visiable))
    }
)



@ns_account.route('/register')
class Register(Resource):
    @api.response(200, 'Username Already Exists')
    @api.response(201, 'Account Created Successfully')
    @api.response(400, 'Bad Request Error')
    @api.doc(description="Register an account")
    @api.expect(indicator_model, validate=True)
    def post(self):
        global db
        print(f'register request is {request}')
        print(f'before request, the urers in database are {db.get_all_users()}')
        try:
            accountInfo = request.json
        except:
            return {'message': 'Bad Request!'}, 400
        try:
            if db.is_in_database(accountInfo['username']):
                return {'message': 'Username Already Exists'}, 200
            db.save_user(accountInfo['username'], accountInfo['password'])
            return {'message': 'Account Created Successfully!'}, 201

        except KeyError:
            return {'message': 'Bad Request!'}, 400



@ns_account.route('/signin')
class Signin(Resource):
    @api.response(200, 'Successful')
    @api.response(401, 'Unauthorized')
    @api.doc(description="Generates a authentication token")
    @api.expect(indicator_model, validate=True)
    def post(self):
        global db
        try:
            account_info = request.json
        except:
            return {'message': 'Bad Request!'}, 400
        
        try:
            if db.varify_user(account_info['username'], account_info['password']):
                
                return {"token": auth.generate_token(account_info['username'])}, 200
        except KeyError:
            return {"message": "authorization has been refused for those credentials."}, 401




@ns_account.route('/signout/<string:token>')
class Signout(Resource):
    @api.response(200, 'Successful')
    @api.doc(description="Signout current user.")
    # @requires_authentication
    def delete(self, token):
        auth.delete_token(token)
        return {'message': 'Deletion Successful'}, 200



@ns_account.route('/manage_profile/<string:token>')
class Manage_profile(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Profile Does Not Exist')
    @api.doc(description="get user's profile")
    def get(self,token):
        try:
            user = auth.get_token_info(token)
            response = \
                {
                    "message": "OK",
                    "data":user
                }
            return response,200
        except SignatureExpired as e:
            abort(401, e.message)

        except:
            response = \
                {
                    "message": "Profile does not exists",
                    "data":""
                }
            return response,404




    @api.response(200, 'User Profile Updated Successfully')
    @api.response(400, 'Bad Request Error')
    @api.response(404, 'Profile Does Not Exist')
    @api.doc(description="manage user profile")
    @api.expect(user_profile, validate=True)
    def put(self, token):
        try:
            account_info = request.json
        except:
            return {'message': 'Bad Request!'}, 400



# TODO
# @ns_dashboard.route('')
# class Dashboard(Resource):

#     @api.response(200, 'OK')
#     @api.doc(description='Retrieve auction items')
#     def get(self):

#         result = {}
#         return result,200



#     @api.response(200, 'OK')
#     @api.response(201, 'Created')
#     @api.response(404, 'Requested Resource Does Not Exist')
#     @api.doc(description='Import auction items from local database')
#     @api.expect(indicator_model)
#     def post(self):

#         response = {}
#         return response, 200


#######################################
#  Routes for a single auction item.  #
#######################################

"""

POST: Create a an auction item
GET: Get auction information by item id

"""
dummy_database = []

# this is also the data model stored in server
user_input_bidding_info = api.model(
    "User input to propose a bid & bidding info stored in server",
    {
        "user_id": fields.Integer,
        "proposal_price": fields.Float,
    }
)

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
        "seller_name":fields.String,
        "seller_id":fields.Integer,
        "category_id":fields.Integer,
        "title":fields.String,
        "description":fields.String,
        "end_date":fields.String,
        "price":fields.Float,
        "image_url":fields.String,
    }
)

auction_info_update = api.model(
    'Update auction details (user may specify only some of the fields)',
    {
        "category_id":fields.Integer,
        "title":fields.String,
        "description":fields.String,
        "end_date":fields.String,
        "price":fields.Float,
        "image_url":fields.String,
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
        "end_date": fields.String,
        "price": fields.Float,
        "image_url": fields.String,
        "bidding_info": fields.List(fields.Nested(user_input_bidding_info)),
        "status": fields.String
    }
)





@ns_auction.route('')
class CreateSingleAuctionItem(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Failed to create a new auction')
    @api.expect(user_input_single_auction_item)
    @api.doc(description="create an auction item")
    def post(self):

        user_input_json = request.json
        seller_name = user_input_json['seller_name']
        seller_id = user_input_json['seller_id']
        category_id = user_input_json['category_id']
        title = user_input_json['title']
        description = user_input_json["description"]
        end_date = user_input_json["end_date"]
        price = user_input_json["price"]
        image_url = user_input_json["image_url"]

        new_auction = \
        {
            "item_id": 0,
            "seller_name": seller_name,
            "seller_id":seller_id,
            "category_id":category_id,
            "title":title,
            "description": description,
            "created":dt.now().strftime('%Y-%m-%d %H:%M:%S'),
            "updated":dt.now().strftime('%Y-%m-%d %H:%M:%S'),
            "end_date":end_date,
            "price":price,
            "image_url":image_url,
            "bidding_info":[],
            "status":"bidding"
        }
        message = "Auction create successfully"
        response = \
        {
            "message":message,
            "data":new_auction
        }

        dummy_database.append(new_auction)
        print ('-------')
        print (dummy_database)
        return response,200






@ns_auction.route('/<item_id>')
@api.param('item_id','Item ID given when the auction is created')
class SingleAuctionItemOperations(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Specified item does not exist')
    @api.doc(description="get information of an auction item")
    def get(self,item_id):
        item_id = int(item_id)
        status_code = 200
        try:
            retrieved_item = dummy_database[item_id]
            message = "OK"
        except IndexError:
            retrieved_item = ""
            message = "Specified item does not exist"
            status_code = 404
        response = \
            {
                "message": message,
                "data":retrieved_item
            }

        return response,status_code

    @api.response(200, 'OK')
    @api.response(404, 'Specified item does not exist')
    @api.expect(auction_info_update)
    @api.doc(description="Update auction item details")
    def put(self,item_id):
        item_id = int(item_id)
        status_code = 200
        user_input_json = request.json
        message = "Auction details have been updated"
        try:
            target_auction = dummy_database[item_id]
        except IndexError:
            target_auction = ""
            message = "Specified item does not exist"
            status_code = 404

        if len(user_input_json.keys()) != 0:
            # update auction details
            for k in user_input_json.keys():
                target_auction[k] = user_input_json[k]

            target_auction["updated"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # hhhhhhhh
            dummy_database[item_id] = target_auction
            updated_auction = target_auction
        else:
            message = "User did not specify any field to update"
            updated_auction = ""
        response = \
            {
                "message":message,
                "data":updated_auction
            }
        return response, status_code






###################################
#  Routes for bidding management  #
###################################

# Propose a bidding
@ns_bidding.route('/<item_id>')
@api.param('item_id','Item ID given when the auction is created')
class BiddingManagement(Resource):

    @api.response(200, 'OK')
    @api.response(404, 'Requested Resource Does Not Exist')
    @api.expect(user_input_bidding_info)
    @api.doc(description="Propose a bid on an item")
    def post(self,item_id):
        item_id = int(item_id)
        user_input_json = request.json
        new_bidding_info = user_input_json
        if_overbid = False
        message = "The bidding has been created successfully"
        status_code = 200
        # update database
        try:
            if_no_bidding = True if len(dummy_database[item_id]["bidding_info"]) == 0 else False
            if if_no_bidding:
                dummy_database[item_id]["bidding_info"].append(new_bidding_info)
            else:
                current_highest_price = dummy_database[item_id]["bidding_info"][0]["proposal_price"]
                new_proposed_price = new_bidding_info["proposal_price"]
                if_overbid = True if new_proposed_price > current_highest_price else False
                if if_overbid:
                    dummy_database[item_id]["bidding_info"][0] = new_bidding_info
                else:
                    message = "Bidding failed, the new price is not higher than the current price"

        except IndexError:
            message = "Specified item does not exist"
            status_code = 404

        data = {
            "item_id":item_id,
            "overbid":if_overbid,
            "bidding_info":new_bidding_info
        }
        response = \
            {
                "message": message,
                "data":data
            }
        return response, status_code




# Accept or decline a bidding
@ns_bidding.route('/operations/<item_id>/<operation>')
@api.param('item_id','Item ID given when the auction is created')
@api.doc(params={
    'item_id': 'Item ID given when the auction is created',
    'operation': '\"accept\"\: accept a bid, \"decline\"\: decline a bid '
     })
class AcceptOrDeclineBiddings(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Requested Resource Does Not Exist')
    @api.doc(description="Accept or decline a the highest bidding on an item")
    def put(self,item_id,operation):
        item_id = int(item_id)
        status_code = 200
        try:
            print(operation)
            if operation == "accept":
                dummy_database[item_id]["status"] = "Accepted"
                message = "The bid has been accepted"
            elif operation == "decline":
                dummy_database[item_id]["status"] = "Declined"
                message = "The bid has been declined"
            else :
                message = "Invalid operation"
        except IndexError:
            message = "Specified item does not exist"
            status_code = 404
        response = \
            {
                "message": message
            }
        return response, status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
