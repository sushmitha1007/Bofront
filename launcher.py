from fastapi import FastAPI, Request
import os
import json
# from utils.logger import create_error_log
# from utils.create_response import ERROR_RESPONSE, get_item, get_quantity, get_response
import jira
from utils.jira import RepzyJira
from utils.send_email import send_mail
from test import resp_to_chatbot
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/webhook')
async def fetch_status(request: Request):
    try:
        payload = await request.json()
        print("------------------------------------------------------------------")
        print("------------------------------------------------------------------")
        print("this is payload", payload)
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx")
        print("this is metadata", payload['tracker']['latest_message']['metadata'])
        metadata = payload['tracker']['latest_message']['metadata']
        if "text" in payload['tracker']['latest_message']:
            query = payload['tracker']['latest_message']['text']
        else:
            query = None

        # store query
        # query = payload['tracker']['latest_message']['text']
        print("query ", query)
        metadata = payload['tracker']['latest_message']['metadata']
        if "email" in metadata:
            user_mail = metadata['email']

        if "userName" in metadata:
            user_name = metadata['userName']

        # get image uploaded if any using socket url
        json_path = os.path.join(os.getcwd(), "temp", "images.json")

        # to store conversation/sender id
        if "text" in payload['tracker']['latest_message'] and payload['tracker']['latest_message']['text'] == "/get_started":
            print("text found in input")
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
                    {"text": "Hey {}, Welcome to OMS helper, let me know how can I help with?".format(first_name)}]}

        #call to create issue without images
        if "text" in payload['tracker']['latest_message'] and payload['tracker']['latest_message']['text'] == "/create.issue":
            print("call to directly create issue")
            issue_type = payload['tracker']['slots']['issue_type']
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
                description ="Issue type - " + issue_type + "\\n" + "query - " + act_query + "\\n" + "user email - " + session_started_metadata['email']
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
            
        elif "image" in metadata:
            print("image upload request from ", metadata['session_id'])
            image_list = metadata['image']  # from custom data
            print(image_list)
            # print("this is jsonpath", json_path)
            with open(json_path, "r") as f:
                data = json.load(f)
                # print("data loaded", data)
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
            
        # read latest images for email id with used flag as false
        elif "is_external" in metadata:
            print("external intent triggered")
            session_id = payload['tracker']['sender_id']
            user_mail = payload['tracker']['slots']['session_started_metadata']['email']
            with open(json_path, "r") as f:
                data = json.load(f)
            image_list = []
            for child_dic in data[::-1]:
                # need to stop loop at first match
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
        else:
            query = payload['tracker']['latest_message']['text']
            print("query is typed", query)
            with open(json_path, "r") as f:
                data = json.load(f)
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
            
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=3000)
