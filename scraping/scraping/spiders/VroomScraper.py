import datetime
import json
import csv
import os
import sys
from copy import deepcopy
# from urllib.request import Request

from scrapy import Spider
import scrapy
csvheaders=['year', 'make', 'model', 'trim', 'mileage','tag', 'price']
file=open('shiftScraper.csv','w',newline='',encoding='utf-8')
writer=csv.DictWriter(file,fieldnames=csvheaders)
writer.writeheader()

data={'offset':0,
      'sortby':'geo',
      'fulldetails':'false',
      'limit':24,
      'source':'@vroom-web/listing-1.3.3'
      }
headers={'accept':'application/json, text/plain, */*','accept-encoding':'gzip, deflate, br','accept-language':'en-US,en;q=0.9','cache-control':'no-cache','content-length':'95','content-type':'application/json;charset=UTF-8','origin':'https://www.vroom.com','pragma':'no-cache',
         'referer':'https://www.vroom.com/','sec-fetch-dest':'empty','sec-fetch-mode':'cors','sec-fetch-site':'cross-site','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
counter=0
class shitfScraper(scrapy.Spider):
    name = 'shitfcraper'
    title = 'ShitfScraper'
    start_urls = ['https://www.vroom.com/']

    @staticmethod
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

    def start_requests(self):
        # yield scrapy.Request(url='https://invsearch-v3-prod-ext.aws.vroomapi.com/v3/inventory',callback=self.parse,headers=headers, body=json.dumps(data), method="POST", meta={'proxy':'140.227.80.230:3128'})
        yield scrapy.FormRequest(url='https://invsearch-v3-prod-ext.aws.vroomapi.com/v3/inventory', callback=self.parse, headers=headers, formdata=data, meta={'proxy':'140.227.80.230:3128'})


    def parse(self, response):
        start_json = response.text
        # json_str = start_json[:start_json.find('</script')]
        json_data = json.loads(start_json)
        for car in self.get_dict_value(json_data, ['data', 'hits','hits'], []):
            item = dict()
            try:
                item['year'] = car.get('year')
            except:
                item['year']=''
            try:
                item['make'] = car.get('make')
            except:
                item['make'] =''
            try:
                item['model'] = car.get('model')
            except:
                item['model'] =''
            try:
                item['trim'] = car.get('trim')
            except:
                item['trim'] = ''
            try:
                item['mileage'] = car.get('miles')
            except:
                item['mileage'] =''
            try:
                item['price'] = car.get('listingPrice') #self.get_dict_value(car, ['price', 'total'])
            except:
                item['price'] =''
            try:
                item['tag'] = car.get('tags',[])[0]
            except:
                item['tag'] =''
            writer.writerow(item)
            file.flush()
        while (counter+24) < 9976:
            body={"offset":(counter+24),"sortby":"geo","fulldetails":False,"limit":24,"source":"@vroom-web/listing-1.3.3"}
            yield scrapy.FormRequest(url='https://shift.com/clientapi/consumer/buyer/get_slim_cars_by_zip_1?request=%7B%22zip_code%22%3A%2202112%22%7D', callback=self.parse,headers=headers,formdata=body)
        yield item
