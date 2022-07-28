import scrapy
import csv
import json
from datetime import datetime
import time
import requests


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


def read_csv():

    file = open('stockwitsspider.csv', 'r')
    list = file.read().split('\n')
    file.close()
    for ls in list[1:]:
        if ls.split(',').__len__()==6:
            datadict = dict()
            datadict['Name'] = ls.split(',')[0]
            datadict['Symbol'] = ls.split(',')[1]
            datadict['Score'] = ls.split(',')[2]
            datadict['Price'] = ls.split(',')[3]
            datadict['Price_Change'] = ls.split(',')[4]
            datadict['Time_of_Check'] = ls.split(',')[5]
            itemdata.append(datadict)
        else:
            datadict = dict()
            datadict['Name'] = ls.split(',')[0].strip('"')+', '+ls.split(',')[1].strip('"')
            datadict['Symbol'] = ls.split(',')[2]
            datadict['Score'] = ls.split(',')[3]
            datadict['Price'] = ls.split(',')[4]
            datadict['Price_Change'] = ls.split(',')[5]
            datadict['Time_of_Check'] = ls.split(',')[6]
            itemdata.append(datadict)
    print('file about to close')
    file.close()


def getStockData():
    try:
        read_csv()
    except:
        pass
    headers = ['Name', 'Symbol', 'Score', 'Price', 'Price_Change', 'Time_of_Check']
    file = open('stockwitsspider.csv', 'w', newline='', encoding='utf-8')
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for olditem in itemdata:
        writer.writerow(olditem)
        file.flush()
    if itemdata:
        itemdata.clear()
    url = 'https://api.stocktwits.com/api/2/charts/ts'
    response = requests.get(url)
    json_data = json.loads(response.text)
    for stock in get_dict_value(json_data, ['table', 'ts'], []):
        item = dict()
        stock_id = stock.get('stock_id')
        item['Name'] = get_dict_value(json_data, ['stocks', '{}'.format(stock_id), 'name'])
        item['Symbol'] = get_dict_value(json_data, ['stocks', '{}'.format(stock_id), 'symbol'])
        item['Score'] = stock.get('val')
        item['Price'] = get_dict_value(json_data, ['stocks', '{}'.format(stock_id), 'price'])
        item['Price_Change'] = get_dict_value(json_data, ['stocks', '{}'.format(stock_id), 'change'])
        item['Time_of_Check'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow(item)
        file.flush()
    file.close()


if __name__ == '__main__':
    time_list_str = ['9:00', '18:48']
    itemdata = []
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        if current_time in time_list_str:
            getStockData()
        else:
            time.sleep(30)
