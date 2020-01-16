from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
import json
from flask import g

### DATABASE STUFF

DATABASE = 'witny-onenyc.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def create_schema_if_needed():
    db = get_db()
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id varchar(25) PRIMARY KEY, data json)")
    db.commit()

def update_profile(user_id, profile):
    db = get_db()
    c = db.cursor()
    c.execute("INSERT OR REPLACE INTO users VALUES (?, ?)", [user_id, json.dumps(profile)])
    db.commit()

def get_profile(user_id):
    db = get_db()
    c = db.cursor()
    c.execute('SELECT data FROM users WHERE id = ?', (user_id,))
    results = c.fetchone()
    if results is None:
        return {}
    else:
        return json.loads(list(results)[0])

### END OF DATABASE STUFF.

app = Flask(__name__)

# We create the database if it does not exist yet.
# create_schema_if_needed()

MTA_OUTAGE_DATA = '/home/witny-2020/MTA_outages.txt'

### ROUTES 

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

    if 'set' in incoming_msg:
        (key, value) = incoming_msg.split(' ')[1:]
        print (key, value)
        profile = get_profile(user_id)
        profile[key] = value
        update_profile(user_id, profile) 
        msg.body('update')
        responded = True

    if 'elevators' in incoming_msg:
        profile = get_profile(user_id)
        my_elevators = set(profile.get('my_elevators', '').lower().split(','))
        out_of_order_elevators = set(line.strip().lower() for line in open(MTA_OUTAGE_DATA))
        my_out_of_order_elevators = my_elevators & out_of_order_elevators
        if len(my_out_of_order_elevators) == 0:
            msg.body('Your elevators are working fine.')
        else:
            msg.body("Elevators %s are not working." % str(my_out_of_order_elevators)))
        responded = True

    if 'profile' in incoming_msg:
        profile = get_profile(user_id)
        msg.body(profile)
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

### END OF ROUTES.

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
