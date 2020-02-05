import json
from botocore.vendored import requests
from os import environ

def lambda_handler(event, context):
    api_url = "https://api.sl.se/api2/realtimedeparturesV4.json?key=" + environ['apikey'] + "&siteid=" + environ['siteid'] + "&timewindow=31&Bus=false&Metro=true&Train=false&Ship=false&Tram=false"
  
    response = requests.get(api_url)
    json_data = json.loads(response.text)
    deviation = "."
    destination = json_data['ResponseData']['Metros'][0]['Destination']
    if json_data['ResponseData']['Metros'][0]['Deviations'] != None:
        deviation = " but with deviations " + json_data['ResponseData']['Metros'][0]['Deviations'][0]['Text']
    if json_data['ResponseData']['Metros'][0]['DisplayTime'] == 'Nu':
        lexical_response = "The subway departs just now with destination " + destination + deviation
    else:
        lexical_response = "Next subway departs in " + json_data['ResponseData']['Metros'][0]['DisplayTime'] + " with destination " + destination + deviation
    r_data = {
        "Version": "1.0",
        "SessionsAttributes": {},
        "shouldEndSession": True,
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": lexical_response
            },
            "textContent": {
                "type": "PlainText",
                "text": lexical_response
            }
        },
        "card": {
            "type": "Simple",
            "title": "Subway",
            "content": lexical_response
        },
        }
        # 'statusCode': 200,
        # 'body': json.dumps(r_data)

    return r_data

