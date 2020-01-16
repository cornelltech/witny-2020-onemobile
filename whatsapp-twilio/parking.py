import requests
import datetime

def get_parking_data():

    page= requests.get("https://portal.311.nyc.gov/home-cal/").json()
    items=page['results']
    today=datetime.datetime.today().weekday()

    if items[0]['CalendarDetailStatus']:
        return items[0]['CalendarDetailMessage'] +' '+ items[0]['CalendarDetailStatus']
    else:
        if today ==5:
            return items[0]['SaturdayContentFormat'] + ''+ items[0]['SaturdayRecordName']
        elif today ==6:
            return items[0]['SundayContentFormat']+' '+items[0]['SundayRecordName']
        else:
            return items[0]['WeekDayContentFormat']+' '+items[0]['WeekDayRecordName']
