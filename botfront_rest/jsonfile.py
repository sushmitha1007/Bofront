import json

with open('C:\\Users\\HP\Downloads\\botfront_rest (4)\\botfront_rest\\manufacture.json', 'r') as openfile:
   
    json_object = json.load(openfile)
  
# print(json_object['emails'])
# print(type(json_object['emails']))
for i in json_object['emails']:
    # print(i["email"])
    if i['manufacture'] == "Continental":
        
        if str(i['email']).split(","):
            list_va = str(i['email']).split(",")
            if len(list_va) == 3:
                contact1 = list_va[0]
                contact2=list_va[1]
                contact3 = list_va[2]
                print(contact1,contact2,contact3)
            elif len(list_va) == 2:
                contact1 = list_va[0]
                contact2=list_va[1]
                print(contact1,contact2)
            else:
                contact = list_va[0]
                print(contact)

        else:
            pass

