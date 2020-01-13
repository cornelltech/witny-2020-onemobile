from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3


app = Flask(__name__)

conn = sqlite3.connect('witny-onenyc.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (id varchar(25) PRIMARY KEY, data json)")
conn.commit()

def update_profile(conn, user_id, profile):
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users VALUES (?, ?)", [user_id, json.dumps(profile)])
    conn.commit()

def get_profile(conn, user_id):
    c = conn.cursor()
    c.execute('SELECT data FROM users WHERE id = ?', (user_id,))
    results = c.fetchone()
    if results is None:
        return {}
    else:
        return json.loads(list(results)[0])

# Just for testing.
@app.route('/')
def heartbeath():
  return 'OK'

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    user_id = request.values.get('From', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    print("Message from %s." % user_id)
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = "%s (%s)" % (data["content"], data["author"])
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True

    if 'set' in incoming_message:
        (key, value) = incoming_message.split(' ')[1:]
        print (key, value)
        msg.body('test')
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if 'witny' in incoming_msg:
        msg.body('We need more women in Tech!')
        responded = True
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    return str(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
