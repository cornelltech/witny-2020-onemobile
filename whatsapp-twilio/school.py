import requests

url = 'https://www.nbcnewyork.com/weather/school-closings/'

def get_school_data():
    html = requests.get(url=url).text
    index = html.find('<h3 class="closings__heading">')
    html = html[index + 30:]
    index2 = html.find('</h3>')
    school = html[:index2].replace("&#039;", "'")
    return school
