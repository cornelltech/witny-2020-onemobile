import requests

def donation_data(address):
    data = requests.get("https://dsnydonate.nyc.gov/donate-web/user/api/v1/vendor/SearchVendors?Radius={}&Address={}".format(1, address)).json()
    return data

def get_donation_data(address):
    data = requests.get("https://dsnydonate.nyc.gov/donate-web/user/api/v1/vendor/SearchVendors?Radius={}&Address={}".format(1, address)).json()
    count=len(data)
    for i in range(count):
        get_donation=[]
        get_donation.append(str(i+1)+'. '+data[i]['fullOrganizationName']+'\n'+data[i]['storeAddress']+'\n') 
        return get_donation

