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
#  Routes for a single auction item.   #
#######################################

"""

POST: Create a an auction item
GET: Get auction information by item id

"""
dummy_database = []

user_input_single_auction_item = api.model(
    'credential',
    {
        "ItemName":fields.String,
        "Price":fields.Float,
        "Location":fields.String,
        "Description":fields.String
    }
)


@api.route('/auction_item/')
class CreateSingleAuctionItem(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Failed to create a new auction')
    @api.expect(user_input_single_auction_item)
    @api.doc(description="create an auction item")
    def post(self):

        user_input_json = request.json
        description = user_input_json["Description"]
        price = user_input_json["Price"]
        item_name = user_input_json["ItemName"]
        location = user_input_json["Location"]

        new_auction = \
        {
            "ItemId": 0,
            "ItemName":item_name,
            "Price":price,
            "Description":description,
            "Location":location,
            "CreatedTime":datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        message = "Auction create successfully"
        response = \
        {
            "message":message,
            "result":new_auction
        }

        dummy_database.append(new_auction)
        return response,200

@api.route('/auction_item/<item_id>')
@api.param('item_id','Item ID given when the auction is created')
class RetrieveSingleAuctionItem(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Specified item does not exist')
    @api.doc(description="get information of an auction item")
    def get(self,item_id):
        item_id = int(item_id)
        try:
            retrieved_item = dummy_database[item_id]
            message = "OK"
        except IndexError:
            retrieved_item = ""
            message = "Specified item does not exist"

        response = \
            {
                "message": message,
                "result":retrieved_item
            }

        return response,200



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

