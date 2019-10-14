import json
import datetime
import uuid
import re
import pandas as pd
from flask import Flask, request, Response
from flask_restplus import Resource, Api, fields, inputs, reqparse
from setup_database import *


col = Collection()
# upload_local_items(col)

app = Flask(__name__)
api = Api(app, default="Auction", title="Auction")

indicator_model = api.model('Indicator', {
    'indicator_id': fields.String
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

        return result,200



    @api.response(200, 'OK')
    @api.response(201, 'Created')
    @api.response(404, 'Requested Resource Does Not Exist')
    @api.doc(description='Import auction items from local database')
    @api.expect(indicator_model)
    def post(self):

        return response, 200





@api.route('/auction_items/<string:cid>')
@api.doc(params={'cid': 'collection id'})
class OnOneCollection(Resource):

    @api.response(200, 'OK')
    @api.response(404, 'Requested Resource Does Not Exist')
    @api.doc(description="Delete one auction item")
    def delete(self,cid):
        return response, 200


    @api.response(200, 'OK')
    @api.response(404, 'Requested Resource Does Not Exist')
    @api.doc(description="Retrieve one auction item")
    def get(self,cid):
        return response, 200





@api.route('/auction_items/<string:cid>/<string:time>/<string:owner>')
class IndicatorByYearCountry(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Requested Resource Does Not Exist')
    @api.doc(description="Retrieve specific auction items")    
    def get(self,cid,year,country):

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
        
        return response,200

if __name__ == '__main__':
    app.run(debug=True)

