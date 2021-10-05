import requests
import json

def resp_to_chatbot(sender_id, image_msg, images, jira_msg):
    print("inside resp to chatbot function")
    headers = {
        'Content-Type': 'application/json',
    }

    entities = {"image_msg": image_msg, "images": images, "jira_msg": jira_msg}
    # print(json.dumps(entities))
    raw_data = {"name": "external.event", "entities": entities}
    data = '{}'.format(json.dumps(raw_data))
    print("final data", data)
    # data = '{"name": "external.event", "entities": {"image_msg": "3 images uploaded", "images": "this is image link\nthis is different image link", "jira_msg": "ticket created"}}'
    response = requests.post(
        'http://2800-2600-1f18-13f0-5500-6ce0-ba0a-8e81-fa71.ngrok.io/conversations/{}/trigger_intent?output_channel=latest'.format(sender_id), headers=headers, data='{}'.format(data))

    # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    # print("this is response", response.text)


# resp_to_chatbot('Hchx0ZZ3McU0ErBkAABU', "3 images uploaded", "\n".join([
#                 "this is image link", "this is different image link"]), "ticket created")
