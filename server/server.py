import json
from datetime import datetime
import uuid
import re
import pandas as pd
from flask import Flask, request, Response
from flask_restplus import Resource, Api, fields, inputs, reqparse
from setup_database import *
# import server.setup_database as db_setup


# global variables
col = Collection()
# upload_local_items(col)

# db = userDatabase()
SECRET_KEY = "SENG4920"
expires_in = 1000
# auth = AuthenticationToken(SECRET_KEY, expires_in)
app = Flask(__name__)
api = Api(app, authorizations={
                'API-KEY': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'AUTH-TOKEN'
                }
            },
          security='API-KEY',
          #default="predict",
          title="Auction", 
          description="Auction Website")


indicator_model = api.model('credential', {
    'username': fields.String,
    'password': fields.String
})




def upload_local_items(col):
    with open('../data/data1.json', 'r') as f:
        content = json.load(f)
        col.insert_many_collections([content])



@api.route('/dashboard')
class Dashboard(Resource):

    @api.response(200, 'OK')
    @api.doc(description='Retrieve auction items')
    def get(self):

        result = {};
        return result,200



    @api.response(200, 'OK')
    @api.response(201, 'Created')
    @api.response(404, 'Requested Resource Does Not Exist')
    @api.doc(description='Import auction items from local database')
    @api.expect(indicator_model)
    def post(self):

        response = {}
        return response, 200


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
    "Bidding proposal user input & bidding info stored in server",
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
    'Create auction user input',
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
        "bidding_info": fields.List(fields.Nested(user_input_bidding_info))
        "status": fields.String
    }
)


@api.route('/auction/')
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
            "created":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "updated":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
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
        return response,200


@api.route('/auction/<item_id>')
@api.param('item_id','Item ID given when the auction is created')
class RetrieveSingleAuctionItem(Resource):
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


###################################
#  Routes for bidding management  #
###################################

# Propose a bidding

@api.route('/bidding/<item_id>')
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
                current_highest_price = dummy_database[item_id]["bidding_info"][0]["proposal_price"];
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

# DOING
# Accept or decline a bidding
@api.route('/bidding_operations/<item_id>/<operation>')
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


# TODO

@api.route('/auction_items/<string:cid>')
@api.doc(params={'cid': 'collection id'})
class OnOneCollection(Resource):

    @api.response(200, 'OK')
    @api.response(404, 'Requested Resource Does Not Exist')
    @api.doc(description="Delete one auction item")
    def delete(self,cid):

        response = {};
        return response, 200

    @api.response(200, 'OK')
    @api.response(404, 'Requested Resource Does Not Exist')
    @api.doc(description="Retrieve one auction item")
    def get(self,cid):
        response = {};
        return response, 200





@api.route('/auction_items/<string:cid>/<string:time>/<string:owner>')
class IndicatorByYearCountry(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Requested Resource Does Not Exist')
    @api.doc(description="Retrieve specific auction items")    
    def get(self,cid,year,country):

        response = {};
        return response, 200




parser = reqparse.RequestParser()
parser.add_argument('query')

@api.route('/auction_items/<string:cid>/<int:time>')
@api.expect(parser)
class SortedIndicatorByYearCountry(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Requested Resource Does Not Exist') 
    @api.doc(description="Retrieve specific items")
    def get(self,cid,year):

        response = {};
        return response,200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)

