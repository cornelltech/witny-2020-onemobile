from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    message= request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
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
        url = 'https://www.nbcnewyork.com/weather/school-closings/'
        html = requests.get(url = url).text
        index = html.find('<h3 class="closings__heading">')
        x = len('<h3 class="closings__heading">')
        html = html[index + x:]
        index2 = html.find('</h3>')
        school = html[:index2].replace("&#039;", "'")

        msg.body(school)
        responded = True


    latitude = request.values.get('Latitude')
    if (latitude):
        longitude = request.values.get('Longitude')

        url = 'http://dev.virtualearth.net/REST/v1/Locations/{},{}?key=ArP15xfjwVa7vSxzqSSYajkXDbdSjM2VsAvAWmV2FzsQUGe5g3s4JdVS4tqy7Gln'

        r = requests.get(url = url.format(latitude, longitude))
        data = r.json()

        for key in data.get('resourceSets')[0].get('resources')[0].keys():
            print(key)

        address = data.get('resourceSets')[0].get('resources')[0].get('address')

        msgBody = ''
        for key in address.keys():
            msgBody += '' + key + ': ' + address.get(key) + '\n'

        msg.body(msgBody)
        responded = True

    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')

    return str(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
