from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

import time

import school
import maps

data = {
    'school': {
        'time': None,
        'data': None,
    },
}

def get_school_data():
    currentTime = time.time()
    lastTime = data['school']['time']
    if lastTime == None or lastTime + 3600000 < currentTime:
        school = school.get_school_data()
        data['school']['data'] = school
        data['school']['time'] = currentTime
        return school
    return data['school']['data']


def get_directions(message):
    message = message.split()
    if 'from' in message:
        direction_index = message.index('from')
    elif 'direction' in message:
        direction_index = message.index('direction')
    elif 'directions' in message:
        direction_index = message.index('directions')
    
    to_index = message.index('to')

    a = ' '.join(message[direction_index + 1: to_index])
    b = ' '.join(message[to_index + 1:])

    directions_arr = maps.get_directions_a_to_b(a, b)

    msg = ''
    for x in directions_arr:
        msg += x + '\n'

    return msg


app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    message = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if message:
        r = requests.get('https://westus.api.cognitive.microsoft.com/luis/prediction/v3.0/apps/b5cee869-91ee-4c3b-8a96-50742cadca6e/slots/staging/predict?subscription-key=182adf9393da4a6e8df931f93d8aa01d&verbose=true&show-all-intents=true&log=true&query={}'.format(message))
        print(r.json())

    if 'quote' in message:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in message:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True

    if 'school' in message and ('open' in message or 'closed' in message):
        msg.body(get_school_data())
        responded = True

    latitude = request.values.get('Latitude')
    if (latitude):
        longitude = request.values.get('Longitude')

        url = 'http://dev.virtualearth.net/REST/v1/Locations/{},{}?key=ArP15xfjwVa7vSxzqSSYajkXDbdSjM2VsAvAWmV2FzsQUGe5g3s4JdVS4tqy7Gln'

        r = requests.get(url=url.format(latitude, longitude))
        data = r.json()

        address = data.get('resourceSets')[0].get(
            'resources')[0].get('address')

        msgBody = ''
        for key in address.keys():
            msgBody += '' + key + ': ' + str(address.get(key)) + '\n'

        msg.body(msgBody)
        responded = True

    if 'direction' in message:
        direction = get_directions(message)
        msg.body(direction)
        responded = True

    if 'weather' in message:
        weather = weather.get_weather(message);
        msg.body(weather)
        responded = True

    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')

    return str(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
