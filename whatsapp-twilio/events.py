import requests
        
def get_events_data():
    quote_page = 'https://www1.nyc.gov/calendar/api/json/search.htm?sort=DATE&pageNumber=1'
    page = requests.get(url=quote_page).json()
    items = page['items']
    print(items)
    return items

get_events_data()
