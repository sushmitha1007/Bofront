import requests
from config.config import SERVER_URL
from utils.logger import create_error_log
import json
from config import constants


ERROR_RESPONSE = {"events": [], "responses": [
    {"text": "error fetching results"}]}

EMPTY_RESPONSE = {"events": [], "responses": [
    {"text": "no items found for your request."}]}



def create_response(query):
    try:
        post_load = {}
        post_load['utterence'] = query
        post_load['language'] = "en"
        post_load['zipcode'] = 48393
        post_load['offset'] = 0
        post_load['limit'] = 100
        # post_load = {"utterence": query,"language": "en","zipcode": 48393,"offset": 0,"limit": 100}
        carousels = []
        header = {'Content-Type': 'application/json'}
        # print("payload", type(post_load))
        resp_data = requests.post(SERVER_URL, data=json.dumps(
            post_load, indent=4), headers=header).json()
        # print("this is bulk response", resp_data)

        for dicts in resp_data['products']:
            my_dict = {}
            my_dict['title'] = dicts['name']
            my_dict['subtitle'] = dicts['description']
            my_dict['image_url'] = dicts['imageSrc']
            my_dict['buttons'] = [
                {"title": "click to knowmore", "url": dicts['productlink'], "type": "web_url"}]
            carousels.append(my_dict)

        # make carousel from response data
        # print("carousel to return", carousels)
        if len(carousels) > 0:
            carousel_data = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": carousels
                }
            }

            payload = {
                "events": [],
                "responses": [
                    {
                        "attachment": carousel_data
                    }
                ]
            }
        
        else:
            payload = EMPTY_RESPONSE

        return payload
    except Exception as e:
        # print(e)
        create_error_log(e)
        return ERROR_RESPONSE


def get_quantity(payload):
    quantity = None
    entities_list = payload['tracker']['latest_message']['entities']
    for entity in entities_list:
        if entity['entity'] == "quantity":
            print("got quantity")
            quantity = entity['value']

    return quantity


def get_item(payload):
    item = payload['tracker']['slots']['item']
    return item


def get_prev_item(payload):
    prev_item = None
    for dic in payload['tracker']['events']:
        # print("checking this", dic)
        for k,v in dic.items():
            if k == "name" and v == "item":
                # print("cond satisfied for", dic)
                prev_item = dic['value']
                break
        if prev_item != "":        
            break 
    return prev_item


def get_response(intent, item, quantity):
    query = ""
    if intent == "get.status":
        print("get.status intent matched")

        # if str(item) == "None":
        #     item = prev_item
        #     print("updated item slot with", str(item))

        if str(item) == "None":
            return constants.ASK_ITEM
        
        if str(item) != "None" and str(quantity) != "None" :
            query = "get me " + str(item)
            response = create_response(query)
            return response

        return constants.ASK_QUANTITY
    
    else:
        print("in get quantity intent")
        # if str(item) == "None":
        #     if prev_item != "":
        #         item = prev_item
        if str(item) == "None":
            return constants.ASK_ITEM
        print("this is updated item", item)
        query = "get me " + item
        print("this is query", query)
        response = create_response(query)
        return response