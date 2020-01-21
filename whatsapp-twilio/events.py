import requests
import time

data_dict={

}

def update_all_events_data():
    page=requests.get("https://www1.nyc.gov/calendar/api/json/search.htm?sort=DATE&pageNumber=1").json()
    num_pages = page['pagination']['numPages']
    events_array = page['items']

    for i in range(2, num_pages + 1):
        new_page = requests.get("https://www1.nyc.gov/calendar/api/json/search.htm?sort=DATE&pageNumber={}".format(i)).json()
        new_items = new_page['items']
        events_array += new_items

    return events_array

def get_all_events_data():
    currentTime=time.time()
    if 'events' not in data_dict:
        data_dict['events'] = {'time':None, 'data':None}
    lastTime=data_dict['events']['time']
    if lastTime == None or lastTime + 3600000 < currentTime:
        data = update_all_events_data()

        data_dict['events']['time']=currentTime
        data_dict['events']['data']=data

    
    return data_dict['events']['data']
        
