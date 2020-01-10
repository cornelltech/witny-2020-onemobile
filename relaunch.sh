. .env/bin/activate
cd witny-2020-onemobile/
echo "We get the latest code from the github repo."
git pull
cd whatsapp-twilio/
echo "We kill the previous process and start a new one."
if test -f "witny_bot.pid"; then
    kill `cat witny_bot.pid`
fi
nohup python bot.py > witny_bot.log 2>&1 & echo $! > witny_bot.pid
