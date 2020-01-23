from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

import maps
import nyc311_data
import predict
import donation

user_data = {}


app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    message = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    print('user: ', message)

    msg_to_send = bot_response(request.values)

    if msg_to_send == None or len(msg_to_send) == 0:
        msg.body("Sorry, I don't understand. Please try rephrasing your query.")
    else:
        msg_to_send_str = ''
        if type(msg_to_send) is str:
            msg_to_send_str = msg_to_send 
        else:
            for line in msg_to_send:
                msg_to_send_str += (line + '\n')
        msg.body(msg_to_send_str)
        print('------')
        print('to send', msg_to_send_str)
        print('------')

    return str(resp)

def bot_response(message_object):
    user = message_object.get('From', '')
    message = message_object.get('Body', '').lower()
    latitude = message_object.get('Latitude')
    print(latitude)
    msg_to_send = []

    if (user in user_data and 'query' in user_data[user]):
        query = user_data[user]['query']
        if query != None:
            if query == 'donate':
                if latitude:
                    longitude = message_object.get('Longitude')
                    a = latitude + ',' + longitude
                else:
                    a = message
                msg_to_send = donation.get_donation_data(a)
                user_data[user]['query'] = None
            elif query == 'direction':
                if latitude:
                    longitude = message_object.get('Longitude')
                    a = latitude + ',' + longitude
                else:
                    a = message
                print(a)
                query_data = user_data[user]['query_data']
                msg_to_send = maps.get_directions_a_to_b(a, query_data)
                user_data[user]['query'] = None
            else:
                msg_to_send = "Sorry, I don't understand."
            return msg_to_send

    if not message:
        return
    data = predict.luis(message)
    if data and data['top_intent'] == 'directions':
        if len(data['data']) > 1:
            a = data['data'][0]
            b = data['data'][1]
            msg_to_send = maps.get_directions_a_to_b(a, b)
            return msg_to_send
        else:
            msg_to_send = 'Please send an address or share your current location.'
            if (user not in user_data): user_data[user] = {}
            user_data[user]['query'] = 'direction'
            user_data[user]['query_data'] = data['data'][0]

    if 'donate' in message or 'donation' in message:
        msg_to_send = 'Please send an address or share your current location.'
        if (user not in user_data): user_data[user] = {}
        user_data[user]['query'] = 'donate'
        return msg_to_send
     
    if 'school' in message:
        msg_to_send.append(nyc311_data.get_data('school'))
    if 'garbage' in message or 'trash' in message:
        msg_to_send.append(nyc311_data.get_data('garbage'))
    if 'parking' in message:
        msg_to_send.append(nyc311_data.get_data('parking'))
    
    return msg_to_send

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


