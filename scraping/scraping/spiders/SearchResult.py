import csv
import json

import requests

csv_file="LocationData.csv"
csv_header=['name','address','phone_number','business_status','rating','reference','icon_link']

file = open(csv_file, 'w', newline='')
writer = csv.DictWriter(file, fieldnames=csv_header)
writer.writeheader()

def get_dict_value(data, key_list, default=''):

    """

    gets a dictionary and key_list, apply key_list sequentially on dictionary and return value

    :param data: dictionary

    :param key_list: list of key

    :param default: return value if key not found

    :return:

    """

    for key in key_list:

        if data and isinstance(data, dict):

            data = data.get(key, default)

        else:

            return default

    return data


def getlocation():
    # long=input("enter longitude: ")
    long=28.695406
    print(long)
    # lat=input("Enter Latitude: ")
    lat=77.223930
    print(lat)
    key='AIzaSyCjzKQmZwR2OYbodDtZXtEH1klDuT6pols'
    url='https://maps.googleapis.com/maps/api/place/textsearch/json?query=apparel%20manufacturers&location={},{}&radius=10000&key={}'.format(long,lat,key)
    print(url)
    resp = requests.get(url)

    data = json.loads(resp.content.decode('utf-8'))

    item=dict()
    # item['name'] = get_dict_value(data, ['results','name'])
    for result in get_dict_value(data, ['results']):
        item['name'] = result.get('name')
        item['address'] = result.get('formatted_address')
        placeid=result.get('place_id')
        resp_phone = requests.get('https://maps.googleapis.com/maps/api/place/details/json?place_id={}&fields=formatted_phone_number&key={}'.format(placeid,key))
        phonenum = json.loads(resp_phone.content.decode('utf-8'))
        item['phone_number']=get_dict_value(phonenum,['result','formatted_phone_number'])
        item['business_status']=result.get('business_status')
        item['rating']=result.get('rating')
        item['reference']=result.get('reference')
        item['icon_link']=result.get('icon')
        writer.writerow(item)
        # csv.flush()

if __name__ == '__main__':
    getlocation()

