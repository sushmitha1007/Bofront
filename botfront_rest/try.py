# from botfront_rest.launch import Query
import os
import json
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
import pandas as pd    
app = Flask(__name__)
# api = CORS(app)
# Creating Flask App Variable
# app = Flask(__name__)
api = Api(app)
Query = []
global lists
import threading
class FetchStatus(Resource):
    def post(self):
         
        payload = request.get_json()
        print("------------------------------------------------------------------")
        print("------------------------------------------------------------------")
        # print("this is payload", payload)
        # print("xxxxxxxx")
        
        if "text" in payload['tracker']['latest_message']:
            query = payload['tracker']['latest_message']['text']
            Query.append(query)
        else:
            query = None

        print("query is", query)
        print(Query)
        if Query[0] == '/get_started':
            Query.pop()
        else:
            pass
        for i in Query:
            print(i)
            if i =='/get_started':
                Query.clear()
        print(len(Query))
        print(Query)
        # su  = payload['tracker']['slots']['issue.part']
        # print(su)
        issue_type = payload['tracker']['slots']['issue_type']
        print(issue_type)
        if len(Query) == 5:
            jiraobj = RepzyJira()
          
            summary = issue_type + " PartNumber "+ Query[1]
            description ="Issue type - " + issue_type + "\\n" + "Part Number - " + Query[1] + "\\n" +"Manufacturer - "+Query[2]+ "\\n"+"Quantity - "+Query[3]+"\\n"+"Date - "+Query[4]
            email_description ="Issue type - " + issue_type + "\n" + "Part Number - " + Query[1] + "\n" +"Manufacturer - "+Query[2]+ "\n"+"Quantity - "+Query[3]+"\n"+"Date - "+Query[4]
            
            ticket = jiraobj.create_issue(summary=summary, description=description,Components=issue_type)
            print("issue created with no: ", ticket)
            
            Ticket_message = "Thank you! Ticket is created you can use ticket no."+ticket['key']+" to get updates on the issue. A copy with details has been sent to your mail id sushmithasherigar1998@gmail.com."
            with open('C:\\Users\\HP\Downloads\\botfront_rest (4)\\botfront_rest\\manufacture.json', 'r') as openfile:
   
                json_object = json.load(openfile)
            
            # print(json_object['emails'])
            # print(type(json_object['emails']))
            for i in json_object['emails']:
                # print(i["email"])
                if str(i['manufacture']).lower() == str(Query[2]).lower():
                    
                    if str(i['email']).split(","):
                        list_va = str(i['email']).split(",")
                        if len(list_va) == 3:
                            contact1 = list_va[0]
                            contact2=list_va[1]
                            contact3 = list_va[2]
                            print(contact1,contact2,contact3)
                            contact_details = "Please reach out to the below contacts as per the order of"+'\n'+ "priority:" +'\n'+"contact1 - "+contact1+'\n'+"contact2 - "+contact2+'\n'+"contact3 - "+contact3+'\n'+'\n'
                        elif len(list_va) == 2:
                            contact1 = list_va[0]
                            contact2=list_va[1]
                            print(contact1,contact2)
                            contact_details = "Please reach out to the below contacts as per the order of"+'\n'+ "priority:" +'\n'+"contact1 - "+contact1+'\n'+"contact2 - "+contact2+'\n'+'\n'
                        else:
                            contact = list_va[0]
                            print(contact)
                            if contact == " ":
                                contact_details = " "
                            else:
                                contact_details = "Please reach out to the below contacts as per the order of"+'\n'+ "priority:" +'\n'+"contact - "+contact+'\n'+'\n'
                        

                    else:

                        pass
                
            Query.clear()   
            greeting = "Hello ," + "\n" + "\n" + "Thanks for reaching out to Repzy, please find the copy of the details sent to the support team below." + "\n"
            email_description = "Issue description - " + email_description + "\n"
            email_ticket_msg = "Ticket number - {}".format(ticket['key'])  + "\n" + "\n"
            # print(lists)
            
            signature = "regards," + "\n" + "Team AHGroup"
            
            
            email_body = greeting + email_description + email_ticket_msg +contact_details+ signature
            
            print("sending mail to ", "sushmithasherigar1998@gmail.com")
            send_mail(text=email_body, to_emails=["sushmithasherigar1998@gmail.com"])
            print("mail sent!!")
            
            final_message = {"events": [], "responses": [
                                    {"text": Ticket_message}]}


            return final_message
        

            
api.add_resource(FetchStatus, '/webhook')

if __name__ == "__main__":
    
    app.run(debug=True)
