# from logging import exception
# import re
import requests
from config.config import SERVER_URL
from utils.logger import create_error_log
import json
from config import constants


ERROR_RESPONSE = {"events": [], "responses": [
    {"text": "error fetching results"}]}

EMPTY_RESPONSE = {"events": [], "responses": [
    {"text": "no items found for your request."}]}

SEND_IMAGE = {"events": [], "responses": [
    {"image": "https://m.media-amazon.com/images/I/71DVgBTdyLL._SX679_.jpg"},
    {"text": "iphone12 pro"}]}

ASK_QUANTITY = {"events": [], "responses": [
                                {"text": "how much you want?"}]}
            


def make_carousel(translated):
    try:
        post_load = {}
        post_load['utterence'] = translated
        post_load['language'] = "en"
        post_load['zipcode'] = 48393
        post_load['offset'] = 0
        post_load['limit'] = 100
        # post_load = {"utterence": query,"language": "en","zipcode": 48393,"offset": 0,"limit": 100}

        header = {'Content-Type': 'application/json'}
        # print("payload", type(post_load))
        resp_data = requests.post(SERVER_URL, data=json.dumps(
            post_load, indent=4), headers=header).json()
        # print("this is bulk response", resp_data)
        carousel_per_item = []
        for dicts in resp_data['products']:
            my_dict = {}
            my_dict['title'] = dicts['name']
            my_dict['subtitle'] = dicts['description']
            my_dict['image_url'] = dicts['imageSrc']
            my_dict['buttons'] = [
                {"title": "click to knowmore", "url": dicts['productlink'], "type": "web_url"}]
            carousel_per_item.append(my_dict)
        return carousel_per_item
    except Exception as e:
        # print("error while requesting ekirana server ", e)
        create_error_log("error while requesting ekirana server " + str(e))
        return carousel_per_item


def create_response(queries):
    try:
        carousels = []
        for dic in queries:
            # print("using: ", dic)
            for received, translated in dic.items():
                # print("this is item,", received, translated)
                resp_carousels = make_carousel(translated)
                # print(resp_carousels)
                if resp_carousels.__len__() == 0:
                    # print("running received", received)
                    resp_carousels = make_carousel(received)
                carousels.extend(resp_carousels)

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


# def get_quantity(payload):
#     quantity = None
#     entities_list = payload['tracker']['latest_message']['entities']
#     for entity in entities_list:
#         if entity['entity'] == "quantity":
#             print("got quantity")
#             quantity = entity['value']

#     return quantity

def get_quantity(payload):
    multiple_req = False
    item = None
    quantity = None
    entities_list = payload['tracker']['latest_message']['entities']

    item_list = []
    my_dict = {}

    count = 0
    for entity in entities_list:
        # print("this is entity", entity)
        if count > 1:
            # print("breaking loop since count is ", count)
            multiple_req = True
            break
        # if items are more and quantity is singular then also it should be plural request
        if entity['entity'] == "quantity":
            # print("got quantity", entity['value'])
            quantity = entity['value']
            count += 1
        # match item too to increase count in case of single quantity passed
        elif entity['entity'] == "item":
            count += 1
        # print("count is", count)

    if multiple_req == True:
        for entity in entities_list:

            if entity['entity'] == "quantity":
                # print("got quantity in mul req", entity['value'])
                quantity = entity['value']
                my_dict["quantity"] = quantity

            elif entity['entity'] == "item":
                # print("got item in mul req", entity['value'])
                item = entity['value']
                my_dict["item"] = item

            if len(my_dict) == 2:
                if item != None:
                    item_list.append(my_dict)
                my_dict = {}
            elif entity == entities_list[-1]:
                item = None
                quantity = None
                if entity['entity'] == "item":
                    item = entity['value']
                elif entity['entity'] == "quantity":
                    quantity = entity['value']

                if item != None:
                    item_list.append({"quantity": quantity, "item": item})

        # print("final list with data", item_list)
        return item_list

    else:
        return quantity


def get_item(payload):
    item = None
    # item = payload['tracker']['slots']['item']
    entities_list = payload['tracker']['latest_message']['entities']
    for entity in entities_list:
        if entity['entity'] == "item":
            # print("got quantity", entity['value'])
            item = entity['value']
    # print("got this item", str(item))
    if str(item) == "None":
        # print("requesting recent item")
        item = get_prev_item(payload)
    return item


def get_prev_item(payload):
    prev_item = None
    for dic in payload['tracker']['events']:
        if "parse_data" in dic.keys():
            # print("checking this", dic)
            for ent_list in dic['parse_data']['entities']:
                for _, v in ent_list.items():
                    if v == "item":
                        # print("cond satisfied for", dic)
                        prev_item = ent_list['value']
                        break
                    if prev_item != "":
                        break
    return prev_item

# def get_prev_item(payload):
#     prev_item = None
#     for dic in payload['tracker']['events']:
#         # print("checking this", dic)
#         for k,v in dic.items():
#             if k == "name" and v == "item":
#                 # print("cond satisfied for", dic)
#                 prev_item = dic['value']
#                 break
#         if prev_item != "":
#             break
#     return prev_item


def get_response(intent, item, quantity, multiple_req=""):
    try:
        if multiple_req != "":
            queries = []
            for dic in multiple_req:
                for k, v in dic.items():
                    if k != "quantity":
                        received_item = constants.EN_LANG_CONSTANT + v
                        translated_item = get_eng_name(v)
                        queries.append({received_item: translated_item})
            # print("formed queries", queries)
            carousels = create_response(queries)
            return carousels
        query = ""
        # if intent == "get.status":
        if intent == "samaan.lao" or intent == "get.status":
            # print("getstatus intent matched")

            # if str(item) == "None":
            #     item = prev_item
            #     print("updated item slot with", str(item))

            if str(item) == "None":
                return constants.ASK_ITEM

            if str(item) != "None" and str(quantity) != "None":
                received_item = constants.EN_LANG_CONSTANT + item
                translated_item = get_eng_name(item)
                query = {received_item: translated_item}
                # item = get_eng_name(item)
                # query = "get me " + str(item)
                # query = item
                # print("running query", query)
                response = create_response([query])
                return response

            return constants.ASK_QUANTITY

        else:
            # print("in get quantity intent")
            # if str(item) == "None":
            #     if prev_item != "":
            #         item = prev_item
            if str(item) == "None":
                return constants.ASK_ITEM
            # print("this is updated item", item)
            received_item = constants.EN_LANG_CONSTANT + item
            translated_item = get_eng_name(item)
            query = {received_item: translated_item}
            # print("this is query", query)
            response = create_response([query])
            return response
    except Exception as e:
        # print("exc in get resp", e)
        create_error_log("exc in get resp" + str(e))


def get_eng_name(word):
    try:
        # print("received word", word)
        from googletrans import Translator
        translator = Translator(service_urls=['translate.googleapis.com'])
        translated = translator.translate(
            str(word) + constants.HI_LANG_CONSTANT, dest='en')
        # print(translated)
        # src_lang = translated.src
        text = translated.text
        # if src_lang == "hi":
        #     return text

        return text

    except Exception as e:
        print(e)
