import requests
import datetime

def get_garbage_data():
    page= requests.get("https://portal.311.nyc.gov/home-cal/").json()
    items=page['results']
    today=datetime.datetime.today().weekday()

    if items[1]['CalendarDetailStatus']:
        return items[1]['CalendarDetailMessage']+' '+items[1]['CalendarDetailStatus']
    else:
        if today ==5:
            return items[1]['SaturdayContentFormat']+' '+items[1]['SaturdayRecordName']
        elif today ==6:
            return items[1]['SundayContentFormat']+' '+items[1]['SundayRecordName']
        else:
            return items[1]['WeekDayContentFormat']+' '+items[1]['WeekDayRecordName']
