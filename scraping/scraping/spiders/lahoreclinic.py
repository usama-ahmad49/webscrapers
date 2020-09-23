import csv
import json

import requests


# inputfile
inputfile='input.txt'
Ifile=open(inputfile,'r')
input=Ifile.readlines()




# for dental clinic
csv_file1="Dental_Clinic_LocationData.csv"
csv_header1=['name','address','phone_number','business_status','rating','reference','icon_link','Location Lat','Location Lng','place_id','Opening_Days']
file1 = open(csv_file1, 'w', newline='', encoding='utf-8')
writer1 = csv.DictWriter(file1, fieldnames=csv_header1)
writer1.writeheader()

csv_file2="Medical_Clinic_LocationData.csv"
csv_header2=['name','address','phone_number','business_status','rating','reference','icon_link','Location Lat','Location Lng','place_id','Opening_Days']
file2 = open(csv_file2, 'w', newline='', encoding='utf-8')
writer2 = csv.DictWriter(file2, fieldnames=csv_header2)
writer2.writeheader()


# key='AIzaSyCjzKQmZwR2OYbodDtZXtEH1klDuT6pols'
# long=31.471000
# print(long)
# # lat=input("Enter Latitude: ")
# lat=74.398875
# print(lat)

for data in input:
    list=data.split(' ')
    key=list[0]
    lat=list[1]
    long=list[2]


def main():
    getlocation_dentalClinic()
    getlocation_medicalClinic()


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


def getlocation_dentalClinic():
    # long=input("enter longitude: ")

    nextpage = ''

    item = dict()
    while True:
        url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=dentalclinic&location={},{}&radius=200000&pagetoken={}&key={}'.format(
            long, lat,nextpage, key)
        resp = requests.get(url)
        data = json.loads(resp.content.decode('utf-8'))

        for result in get_dict_value(data, ['results']):
            item['name'] = result.get('name')
            item['address'] = result.get('formatted_address')
            placeid=result.get('place_id')
            resp_phone = requests.get('https://maps.googleapis.com/maps/api/place/details/json?place_id={}&key={}'.format(placeid,key))
            phonenum = json.loads(resp_phone.content.decode('utf-8'))
            item['phone_number']=get_dict_value(phonenum,['result','formatted_phone_number'])
            item['Opening_Days']=',' .join(get_dict_value(phonenum,['result','opening_hours','weekday_text']))
            item['business_status']=result.get('business_status')
            item['rating']=result.get('rating')
            item['reference']=result.get('reference')
            item['icon_link']=result.get('icon')
            item['place_id']=placeid
            item['Location Lat']=get_dict_value(result,['geometry', 'location', 'lat'])
            item['Location Lng']=get_dict_value(result,['geometry', 'location', 'lng'])
            writer1.writerow(item)

        nextpage = get_dict_value(data, ['next_page_token'])
        if (nextpage == ''):
            break
            # csv.flush()


def getlocation_medicalClinic():
    nextpage=''
    item = dict()
    while True:
        url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=medicalclinic&location={},{}&radius=200000&pagetoken={}&key={}'.format(
            long, lat, nextpage, key)
        resp = requests.get(url)
        data = json.loads(resp.content.decode('utf-8'))
        for result in get_dict_value(data, ['results']):
            item['name'] = result.get('name')
            item['address'] = result.get('formatted_address')
            placeid = result.get('place_id')
            resp_phone = requests.get(
                'https://maps.googleapis.com/maps/api/place/details/json?place_id={}&key={}'.format(
                    placeid, key))
            phonenum = json.loads(resp_phone.content.decode('utf-8'))
            item['phone_number'] = get_dict_value(phonenum, ['result', 'formatted_phone_number'])
            item['Opening_Days'] = ','.join(get_dict_value(phonenum, ['result', 'opening_hours', 'weekday_text']))
            item['business_status'] = result.get('business_status')
            item['rating'] = result.get('rating')
            item['reference'] = result.get('reference')
            item['icon_link'] = result.get('icon')
            item['place_id'] = placeid
            item['Location Lat'] = get_dict_value(result, ['geometry', 'location', 'lat'])
            item['Location Lng'] = get_dict_value(result, ['geometry', 'location', 'lng'])
            writer2.writerow(item)
            # csv.flush()

        nextpage = get_dict_value(data, ['next_page_token'])
        if (nextpage == ''):
            break


if __name__ == '__main__':
    main()

