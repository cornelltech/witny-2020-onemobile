import requests
import maps

def list_to_string_line(l):
    string = ''
    for x in l:
        string += x + '\n'

    return string

def predict_with_luis(phrase):
    result = requests.get('https://westus.api.cognitive.microsoft.com/luis/prediction/v3.0/apps/b5cee869-91ee-4c3b-8a96-50742cadca6e/slots/staging/predict?subscription-key=182adf9393da4a6e8df931f93d8aa01d&verbose=true&show-all-intents=true&log=true&query={}'.format(phrase)).json()
    return result

def parse_results(data):
    top_intent = data['prediction']['topIntent']
    if top_intent == 'directions':
        places = data['prediction']['entities']['Places.PlaceName']
        return {'top_intent': top_intent, 'data': places}

def luis(message):
    data = predict_with_luis(message)
    return parse_results(data)

#test()