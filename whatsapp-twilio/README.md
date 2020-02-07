To set-up your Twilio account:
- https://www.twilio.com/docs/usage/tutorials/how-to-set-up-your-python-and-flask-development-environment .

To build a service for it:
- https://www.twilio.com/blog/build-a-whatsapp-chatbot-with-python-flask-and-twilio
- https://medium.com/better-programming/i-wrote-a-script-to-whatsapp-my-parents-every-morning-in-just-20-lines-of-python-code-5d203c3b36c1

You confifure the end-point of the bot at https://www.twilio.com/console/sms/whatsapp/sandbox .

## Water data (for WAIT program)
- `curl -X GET -H "Content-type: application/json" -H "Accept: application/json"  https://nycwaterbodyadvisory.azurewebsites.net/api/sensors/ > water_fall.json` to get the data
