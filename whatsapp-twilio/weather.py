from flask import Flask, request
import requests
from bs4 import BeautifulSoup, SoupStrainer

from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    message= request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    
    if 'weather' in message:
      page = requests.get("https://weather.com/en-IN/weather/tenday/l/ccb09a4a3cb9ff4c8c5324b73d8cc6c986ab1e58789e0d37c0a1154b46ec30e9")
      soup=BeautifulSoup(page.content,"html.parser")
    
      all=soup.find("div",{"class":"locations-title ten-day-page-title"}).find("h1").text
      table=soup.find_all("table",{"class":"twc-table"})
      l=[]
      for items in table:
        for i in range(len(items.find_all("tr"))-1):
          d = {}  
          d["day"]=items.find_all("span",{"class":"date-time"})[i].text
          d["date"]=items.find_all("span",{"class":"day-detail"})[i].text
          d["desc"]=items.find_all("td",{"class":"description"})[i].text 
          d["temp"]=items.find_all("td",{"class":"temp"})[i].text 
          d["precip"]=items.find_all("td",{"class":"precip"})[i].text
          d["wind"]=items.find_all("td",{"class":"wind"})[i].text  
          d["humidity"]=items.find_all("td",{"class":"humidity"})[i].text 
          l.append(d)

    
      if 'today' in message:
        msg.body("New York, NY, United States of America"+'\n')
        msg.body(l[0].get('day'))
        msg.body(l[0].get('date'))
        msg.body(l[0].get('desc'))
        msg.body(l[0].get('temp'))
        msg.body(l[0].get('precip'))
        msg.body(l[0].get('wind'))
        msg.body(l[0].get('humidity'))
        
        responded = True
      if 'tomorrow' in message:
        msg.body("New York, NY, United States of America")
        msg.body(l[1].get('day'))
        msg.body(l[1].get('date'))
        msg.body(l[1].get('desc'))
        msg.body(l[1].get('temp'))
        msg.body(l[1].get('precip'))
        msg.body(l[1].get('wind'))
        msg.body(l[1].get('humidity'))
        
        responded = True
      
      if 'mon' in message:
       for i in range(0,7):
          if 'Mon' == l[i].get('day'):
           msg.body("New York, NY, United States of America")
           msg.body(l[i].get('day'))
           msg.body(l[i].get('date'))
           msg.body(l[i].get('desc'))
           msg.body(l[i].get('temp'))
           msg.body(l[i].get('precip'))
           msg.body(l[i].get('wind'))
           msg.body(l[i].get('humidity'))
      responded = True

      if 'tue' in message:
       for i in range(0,7):
          if 'Tue' == l[i].get('day'):
           msg.body("New York, NY, United States of America")
           msg.body(l[i].get('day'))
           msg.body(l[i].get('date'))
           msg.body(l[i].get('desc'))
           msg.body(l[i].get('temp'))
           msg.body(l[i].get('precip'))
           msg.body(l[i].get('wind'))
           msg.body(l[i].get('humidity'))
      responded = True

      if 'wed' in message:
       for i in range(0,7):
          if 'Wed' == l[i].get('day'):
           msg.body("New York, NY, United States of America")
           msg.body(l[i].get('day'))
           msg.body(l[i].get('date'))
           msg.body(l[i].get('desc'))
           msg.body(l[i].get('temp'))
           msg.body(l[i].get('precip'))
           msg.body(l[i].get('wind'))
           msg.body(l[i].get('humidity'))
      responded = True
      if 'thu' in message:
       for i in range(0,7):
          if 'Thu' == l[i].get('day'):
           msg.body("New York, NY, United States of America")
           msg.body(l[i].get('day'))
           msg.body(l[i].get('date'))
           msg.body(l[i].get('desc'))
           msg.body(l[i].get('temp'))
           msg.body(l[i].get('precip'))
           msg.body(l[i].get('wind'))
           msg.body(l[i].get('humidity'))
      responded = True
      if 'fri' in message:
       for i in range(0,7):
          if 'Fri' == l[i].get('day'):
           msg.body("New York, NY, United States of America")
           msg.body(l[i].get('day'))
           msg.body(l[i].get('date'))
           msg.body(l[i].get('desc'))
           msg.body(l[i].get('temp'))
           msg.body(l[i].get('precip'))
           msg.body(l[i].get('wind'))
           msg.body(l[i].get('humidity'))
      responded = True
      if 'sat' in message:
       for i in range(0,7):
          if 'Sat' == l[i].get('day'):
           msg.body("New York, NY, United States of America")
           msg.body(l[i].get('day'))
           msg.body(l[i].get('date'))
           msg.body(l[i].get('desc'))
           msg.body(l[i].get('temp'))
           msg.body(l[i].get('precip'))
           msg.body(l[i].get('wind'))
           msg.body(l[i].get('humidity'))
      responded = True
      if 'sun' in message:
       for i in range(0,7):
          if 'Sun' == l[i].get('day'):
           msg.body("New York, NY, United States of America")
           msg.body(l[i].get('day'))
           msg.body(l[i].get('date'))
           msg.body(l[i].get('desc'))
           msg.body(l[i].get('temp'))
           msg.body(l[i].get('precip'))
           msg.body(l[i].get('wind'))
           msg.body(l[i].get('humidity'))
      responded = True
      
      if '10' in message:
        msg.body(all)
        for i in range(10):
          msg.body(l[i].get('day'))
          msg.body(l[i].get('date'))
          msg.body(l[i].get('desc'))
          msg.body(l[i].get('temp'))
          msg.body(l[i].get('precip'))
          msg.body(l[i].get('wind'))
          msg.body(l[i].get('humidity'))
          msg.body("\n")
      responded = True
    
    return str(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
