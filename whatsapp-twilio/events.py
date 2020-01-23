import requests
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
        #print('getting data')
        data = update_all_events_data()

        data_dict['events']['time']=currentTime
        data_dict['events']['data']=data

    #print('returned data')
    return data_dict['events']['data']


def group_by_boroughs():
    event_array=get_all_events_data()
    count=len(event_array) #552
         
    queens = [] #Qn
    manhattan=[] #Mn
    bronx=[] #Bx
    brooklyn=[] #Bk
    sIsland=[] #Si

    for i in range(count):
        boroughs = event_array[i]['boroughs']
        if 'Mn' in boroughs:
            manhattan.append(event_array[i])
        elif 'Qn' in boroughs:
            queens.append(event_array[i])
        elif 'Bx' in boroughs:
            bronx.append(event_array[i])
        elif 'Bk' in boroughs:
            brooklyn.append(event_array[i])
        elif 'Si' in boroughs:
            sIsland.append(event_array[i])

   
    data_dict['events']['manhattan'] = manhattan
    data_dict['events']['queens'] =  queens
    data_dict['events']['bronx'] = bronx
    data_dict['events']['brooklyn'] = brooklyn
    data_dict['events']['sIsland'] = sIsland


def get_events_data_borough(boroughs):
    if boroughs == 'manhattan':
        return data_dict['events']['manhattan']
    elif boroughs == 'brooklyn':
        return data_dict['events']['brooklyn']
    elif boroughs == 'bronx':
        return data_dict['events']['bronx']
    elif boroughs == 'queens':
        return data_dict['events']['queens']
    elif boroughs == 'staten island':
        return data_dict['events']['sIsland']


def get_events_borough(borough):

    currentTime = time.time()
    if time not in data_dict:
        data_dict['time'] = None
    lastTime = data_dict['time']
    if lastTime == None or lastTime + 3600000 < currentTime:
        get_all_events_data()
        group_by_boroughs()
        data_dict['time'] = currentTime

    data = get_events_data_borough(borough)
    count = len(data)
    get_events =['Here some upcoming events in ' + borough + ': \n']
    for i in range(count):
        get_events.append(str(i+1)+'. '+data[i]['name']+'\n'+data[i]['address']+'\n')
        #print(get_events.append(str(i+1)+'. '+data[i]['name']+'\n'+data[i]['address']+'\n'))
    return get_events
