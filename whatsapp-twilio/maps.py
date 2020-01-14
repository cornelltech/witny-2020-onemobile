import requests

url = 'http://dev.virtualearth.net/REST/V1/Routes/Walking?wp.0={}&wp.1={}&optmz=distance&output=json&key=ArP15xfjwVa7vSxzqSSYajkXDbdSjM2VsAvAWmV2FzsQUGe5g3s4JdVS4tqy7Gln'


def get_directions_a_to_b(a, b):
    r = requests.get(url=url.format(a, b))
    data = r.json()[
        "resourceSets"][0]["resources"][0]['routeLegs'][0]['itineraryItems']

    msg = []
    for i in range(len(data)):
        msg.append(data[i]['instruction']['text'])

    return msg
