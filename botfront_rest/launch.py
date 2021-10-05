import os
from typing_extensions import final
from flask import Flask, request
from flask_restful import Api, Resource
import jira
from requests.api import head
# from config import constants
from utils.logger import create_error_log
from utils.create_response import ERROR_RESPONSE, get_item, get_quantity, get_response
import json
from utils.jira import RepzyJira
from utils.send_email import send_mail
from flask_cors import CORS
from test import resp_to_chatbot

app = Flask(__name__)
# api = CORS(app)
# Creating Flask App Variable
# app = Flask(__name__)
api = Api(app)
Query = []
class FetchStatus(Resource):
    def post(self):
        try:
            header = {'Content-Type': 'application/json'}
            payload = request.get_json()
            print("------------------------------------------------------------------")
            print("------------------------------------------------------------------")
            print("this is payload", payload)
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx")
            # print("this is sender id", payload['tracker']['sender_id'])
            print("this is metadata", payload['tracker']['latest_message']['metadata'])

            if "text" in payload['tracker']['latest_message']:
                query = payload['tracker']['latest_message']['text']
            else:
                query = None
            print("------------------------------------------------")
            print("query is", query)
            if "text" in payload['tracker']['latest_message']:
                list_query = payload['tracker']['latest_message']['text']
                Query.append(list_query)
            else:
                list_query = None
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print("query is", list_query)
            print(Query)
            # print(len(ss))
            issue_type = payload['tracker']['slots']['issue_type']
            print(issue_type)
            if len(Query) == 6:
                jiraobj = RepzyJira()
                summary = issue_type + " PartNumber "+ Query[2]
                description ="Issue type - " + issue_type + "\\n" + "Part Number - " + Query[2] + "\\n" +"Manufacturer - "+Query[3]+ "\\n"+"Quantity - "+Query[4]+"\\n"+"Date - "+Query[5]
                ticket = jiraobj.create_issue(summary=summary, description=description)
                print("issue created with no: ", ticket)

                Ticket_message = "Thank you! Ticket is created you can use ticket no."+ticket['key']+" to get updates on the issue. A copy with details has been sent to your mail id ."

                greeting = "Hello ," + "\n" + "\n" + "Thanks for reaching out to Repzy, please find the copy of the details sent to the support team below." + "\n"
                # email_description = "Issue description - " + ss + "\n"
                # email_ticket_msg = "Ticket number - {}".format(ticket['key'])  + "\n" + "\n"
                # signature = "regards," + "\n" + "Team AHGroup"
                # email_body = greeting + email_description + email_ticket_msg + signature
                
                # print("sending mail to ", session_started_metadata['email'])
                # send_mail(text=email_body, to_emails=[session_started_metadata['email']])
                # print("mail sent!!")
                final_message = {"events": [], "responses": [
                                        {"text": Ticket_message}]}


                return final_message

            
            
            
            # for dic in payload['tracker']['events']:
            #     if "parse_data" in dic.keys():
            #         print("this is channel", dic['input_channel'])
            #         channel = dic['input_channel']
            #         break

            # if channel == "slack":
            #     SEND_IMAGE = {"events": [], "responses": [
            #         {"image": "https://cdn.shopify.com/s/files/1/0445/8545/1685/products/9_360x.png"},
            #         {"text": "Name - iphone12 pro"},
            #         {"image": "https://cdn.shopify.com/s/files/1/0445/8545/1685/products/9_360x.png"},
            #         {"text" : "Description - 6.1-inch (15.5 cm diagonal) Super Retina XDR display, Ceramic Shield, tougher than any smartphone glass, A14 Bionic chip, the fastest chip ever in a smartphone"}]}
            #     return SEND_IMAGE

            # print("received json", payload)
            # print("tracker", payload['payload']['payload']['text'])

           ############################################################################################
           #
            # for whatsapp
            # if not "tracker" in payload:
            #     import requests
            #     data = {}
            #     data['sender'] = "rasa"
            #     data['message'] = payload['payload']['payload']['text']
            #     # print("this is data", data, type(data))
            #     if data['message'] != None:
            #         print("query -->", data['message'])
            #         res = requests.post(
            #             "http://localhost:5005/webhooks/rest/webhook", data=json.dumps(data), headers=header).json()
            #         print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            #         print(res)

            #         if "text" in res[0]:
            #             print("returning from if block")
            #             return res[0]['text']
            #         else:
            #             print("-------------------------------------------------------------")
            #             print("in else part")
            #             import requests
            #             link = res[0]['attachment']['payload']['elements'][0]['image_url'].split(" ")
            #             caption = res[0]['attachment']['payload']['elements'][0]['subtitle']

            #             message = {"type": "image",
            #                     "previewUrl": "https://www.buildquickbots.com/whatsapp/media/sample/jpg/sample01.jpg",
            #                     "originalUrl": "https://www.buildquickbots.com/whatsapp/media/sample/jpg/sample01.jpg",
            #                     "caption": caption,
            #                     "filename": "Sample.jpeg"}

            #             headers = {
            #                 'Cache-Control': 'no-cache',
            #                 'Content-Type': 'application/x-www-form-urlencoded',
            #                 'apikey': 'sjwi7ajh7ipx5ah9b0bqswpolp8gq07m',
            #                 'cache-control': 'no-cache',
            #             }

            #             data = {
            #                 'channel': 'whatsapp',
            #                 'source': '917834811114',
            #                 'destination': '918527281232',
            #                 'message': '{}'.format(message),
            #                 'src.name': 'gfwhatsapp'
            #             }

            #             print("this is data", data)

            #             response = requests.post(
            #                 'https://api.gupshup.io/sm/api/v1/msg', headers=headers, data=data)

            #             print(response.json())

            #            #  to return no content since gupshup api will be responsible to return messages
            #             return ('', 204)

            # # print("outside else part")
            # quantity = get_quantity(payload)
            # if isinstance(quantity, list):
            #     # print("multiple request in request")
            #     resp = get_response("", "", "", quantity)
            #     return resp
            # item = get_item(payload)
            # intent = payload['tracker']['latest_message']['intent']['name']
            # resp = get_response(intent, item, quantity, "")
            # print("returning", resp)

            # name = get_session_params()

            metadata = payload['tracker']['latest_message']['metadata']

            if "email" in metadata:
                user_mail = metadata['email']
            
            if "userName" in metadata:
                user_name = metadata['userName']

            #get image uploaded if any using socket url
            image = "https://cdn.shopify.com/s/files/1/0445/8545/1685/products/9_360x.png"
            json_path = os.path.join(os.getcwd(), "temp", "images.json")

            #to store conversation/sender id and greet user with his first name
            if "text" in payload['tracker']['latest_message'] and payload['tracker']['latest_message']['text'] == "/get_started":
                
                    print("text found in input")
                    # if payload['tracker']['latest_message']['text'] == "/get_started":
                    session_started_metadata = payload['tracker']['slots']['session_started_metadata']
                    full_name = None
                    if "userName" in session_started_metadata:
                        full_name = str(payload['tracker']['slots']['session_started_metadata']['userName'])
                    if full_name != None:
                        if " " in full_name:
                            first_name = full_name.split(" ")[0]
                        else:
                            first_name = full_name
                    else:
                        first_name = ""
                
                    return {"events": [], "responses": [
                                        {"text": "Hey {}, Welcome to OMS helper!".format(first_name)}
                                        ]}

            #call to create issue without images
            if "text" in payload['tracker']['latest_message'] and payload['tracker']['latest_message']['text'] == "/create.issue":
                    print("call to directly create issue")
                    issue_type_oms = payload['tracker']['slots']['issue_type_oms']
                    session_started_metadata = payload['tracker']['slots']['session_started_metadata']
                    with open(json_path, "r") as f:
                        data = json.load(f)
                    count = 0
                    for child_dic in data[::-1]:
                        # print("looking for", payload['tracker']['sender_id'])
                        # print("considering", child_dic)
                        count += 1
                        if user_mail == child_dic['user_email'] and str(child_dic['used']) == "false":
                            index = len(data) - count
                            act_query = child_dic['query']
                            print("query to be use", act_query)
                            data[index]['used'] = "true"
                            break
                    with open(json_path, "w") as f:
                        json.dump(data, f)

                    print("creating jira with no image for query", act_query)
                    #create jira issue and return user with ticket number
                    if act_query != None:
                        jiraobj = RepzyJira()
                        description ="Issue type - " + issue_type_oms + "\\n" + "query - " + act_query + "\\n" + "user email - " + session_started_metadata['email']
                        ticket = jiraobj.create_issue(summary=act_query, description=description)
                        print("issue created with no: ", ticket)

                    Ticket_message = "Thank you! Ticket is created you can use ticket no. {} to get updates on the issue. A copy with details has been sent to your mail id {}.".format(ticket['key'], metadata['email'])

                    greeting = "Hello {},".format(str(session_started_metadata['userName']).capitalize()) + "\n" + "\n" + "Thanks for reaching out to Repzy, please find the copy of the details sent to the support team below." + "\n"
                    email_description = "Issue description - " + act_query + "\n"
                    email_ticket_msg = "Ticket number - {}".format(ticket['key'])  + "\n" + "\n"
                    signature = "regards," + "\n" + "Team AHGroup"
                    email_body = greeting + email_description + email_ticket_msg + signature
                    
                    print("sending mail to ", session_started_metadata['email'])
                    send_mail(text=email_body, to_emails=[session_started_metadata['email']])
                    print("mail sent!!")
                    final_message = {"events": [], "responses": [
                                            {"text": Ticket_message},
                                            {"text": "Anything else you would need help with?"}]}


                    return final_message
            
            #images are uploaded
            elif "image" in metadata:
                print("image upload request from ", metadata['session_id'])
                image_list = metadata['image'] #from custom data

                with open(json_path, "r") as f:
                    data = json.load(f)
                query = None
                issue_type = None
                for child_dic in data[::-1]:
                    if user_mail == child_dic['user_email'] and str(child_dic['used']) == "false":
                        query = child_dic["query"]
                        issue_type = child_dic["issue_type"]
                        print("json extracted query and issue type", query, issue_type)
                        break

                print("len of image list", len(image_list))
                if len(image_list) == 1:
                    image_resp = "{} image uploaded successfully.".format(len(image_list))
                elif len(image_list) > 1:
                    image_resp = "{} images uploaded successfully.".format(len(image_list))
                else:
                    image_resp = None

                #create jira issue and return user with ticket number
                if query != None:
                    jiraobj = RepzyJira()
                    description ="Issue type - " + issue_type + "\\n" + "query - " + query + "\\n" + "user email - " + metadata['email'] + "\\n" + "images :" + "\\n"
                    ticket = jiraobj.create_issue(summary=query, description=description, image_link= image_list)
                    print("issue created with no: ", ticket['key'])

                Ticket_message = "Thank you! Ticket is created you can use ticket no. {} to get updates on the issue. A copy with details has been sent to your mail id {}.".format(ticket['key'], metadata['email'])

                greeting = "Hello {},".format(str(metadata['userName']).capitalize()) + "\n" + "\n" + "Thanks for reaching out to Repzy, please find the copy of the details sent to the support team below." + "\n"
                email_description = "Issue description - " + query + "\n"
                email_ticket_msg = "Ticket number - {}".format(ticket['key']) + "\n" + "\n"
                signature = "regards," + "\n" + "Team AHGroup"
                email_body = greeting + email_description + email_ticket_msg + signature
                print("sending mail to ", metadata['email'])
                send_mail(text=email_body, to_emails=[metadata['email']])
                print("mail sent!!")
                final_message = {"events": [], "responses": [
                                            {"text": Ticket_message},
                                            {"text": "Anything else you would need help with?"}]}
                
                # print("mail sent!!")

                # if image_resp != None:
                #     final_message = {"events": [], "responses": [
                #                         {"text": image_resp},
                #                         {"text": Ticket_message}]}
                # else:
                #     final_message = {"events": [], "responses": [
                #                         {"text": Ticket_message}]}
                
                
                with open(json_path, "r") as f:
                    data = json.load(f)
                count = 0
                for child_dic in data[::-1]:
                    count += 1
                    # print("checking for" + user_mail + "in" + child_dic['user_email'])
                    if user_mail == child_dic['user_email'] and str(child_dic['used']) == "false":
                        index = len(data) - count
                        data[index]['used'] = "true"
                        # session_id = child_dic['session_id']
                        break
                with open(json_path, "w") as f:
                    json.dump(data, f)
                
                print("calling resp to chatbot function with args: ", metadata['session_id'], image_resp, "\n".join(image_list), Ticket_message)
                resp_to_chatbot(metadata['session_id'], image_resp, "\n".join(image_list), Ticket_message)

                return True

            #read latest images for email id with used flag as false
            elif "is_external" in metadata:
                print("external intent triggered")
                session_id = payload['tracker']['sender_id']
                user_mail = payload['tracker']['slots']['session_started_metadata']['email']
                with open(json_path, "r") as f:
                    data = json.load(f)
                image_list = []
                for child_dic in data[::-1]:
                    #need to stop loop at first match
                    print("checking {} in {}".format(session_id, child_dic))
                    if session_id == child_dic['session_id'] and str(child_dic['used']) == "false":
                        image_list = child_dic[user_mail]
                        break
                
                if len(image_list) == 1:
                    image_resp = "{} image uploaded successfully. \n {}".format(len(image_list), "\n".join(image_list))
                elif len(image_list) > 1:
                    image_resp = "{} images uploaded successfully. \n {}".format(len(image_list), "\n".join(image_list))
                else:
                    image_resp = None
                
                if image_resp != None:
                    image_msg = {"events": [], "responses": [
                                        {"text": image_resp},
                                        {"text": "please describe the issue or query"}]}
                else:
                    image_msg = {"events": [], "responses": [
                                        {"text": "please describe the issue or query"}]}
                
                return image_msg
       
            #query is provided
            else:
                query = payload['tracker']['latest_message']['text']
                print("query is typed", query)

                with open(json_path, "r") as f:
                    data = json.load(f)
                    # print("data loaded", data)
                data.append({"user_email" : user_mail, "query" : query, "session_id" : payload['tracker']['sender_id'] , "issue_type" : payload['tracker']['slots']['issue_type'], "used" : "false"})
                # print("this is json file data", data)
                with open(json_path, "w") as f:
                    json.dump(data, f)

                return ('', 204)
                
        


        except Exception as e:
            print(e)
            # create_error_log(e)
            # return ERROR_RESPONSE
            pass


api.add_resource(FetchStatus, '/webhook')

if __name__ == "__main__":
    app.run(debug=True)
