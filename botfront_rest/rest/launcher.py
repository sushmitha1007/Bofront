from flask import Flask, jsonify, request, redirect, url_for, make_response
import os
from flask_restful import reqparse, abort, Api, Resource
from config import constants
from utils.logger import create_error_log
from utils.create_response import create_response, ERROR_RESPONSE, get_item, get_quantity, get_response

# Creating Flask App Variable
app = Flask(__name__)
api = Api(app)

class FetchStatus(Resource):
    def post(self):
        try :
            payload = request.get_json()
            print("tracker", payload['tracker'])
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            quantity = get_quantity(payload)
            item = get_item(payload)
            print("this is item", str(item))
            print("this is quantity", str(quantity))
            intent = payload['tracker']['latest_message']['intent']['name']
            print("this is intent", intent)
            resp = get_response(intent, item, quantity)
            return resp
        except Exception as e:
            print(e)
            create_error_log(e)
            return ERROR_RESPONSE
        
api.add_resource(FetchStatus, '/webhook')

if __name__== "__main__":
    app.run(debug=True)