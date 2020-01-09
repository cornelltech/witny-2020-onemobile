import requests
url = 'https://www.nbcnewyork.com/weather/school-closings/'
html = requests.get(url = url).content

index = html.find('<h3 class="closings__heading">')

x = len('<h3 class="closings__heading">')

html = html[index + x:]

index2 = html.find('</h3>');

school = html[:index2]

print(school)
