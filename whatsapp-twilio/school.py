import requests
import datetime

def get_school_data():
    page= requests.get("https://portal.311.nyc.gov/home-cal/").json()
    items=page['results']
    today=datetime.datetime.today().weekday()

    if items[2]['CalendarDetailStatus']:
        return items[2]['CalendarDetailMessage'] +' '+ items[2]['CalendarDetailStatus']
    else:
        if today ==5:
            return items[2]['SaturdayContentFormat'] + ''+ items[2]['SaturdayRecordName']
        elif today ==6:
            return items[2]['SundayContentFormat']+' '+items[2]['SundayRecordName']
        else:
            return items[2]['WeekDayContentFormat']+' '+items[2]['WeekDayRecordName']
