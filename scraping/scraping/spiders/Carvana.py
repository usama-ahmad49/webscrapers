import datetime
import json
import os
import sys
# from urllib.request import Request

from scrapy import Spider
import scrapy


class Carvana(scrapy.Spider):
    name = 'carvana'
    title = 'Carvana'
    start_urls = ['https://www.carvana.com/cars']

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
        yield scrapy.Request(url='https://www.carvana.com/cars', callback=self.parse,
                             headers={"User-Agent": "Chrome/84.0.4147.89"},
                             meta={"proxy": "https://144.217.101.245:3129"})
        for page_no in range(2, 5):
            link = 'https://www.carvana.com/cars?page={}'.format(page_no)
            yield scrapy.Request(url=link, callback=self.parse,headers={"User-Agent": "Chrome/84.0.4147.89"},meta={"proxy": "https://144.217.101.245:3129"})


    def parse(self, response):
        start_json = response.text[
                     response.text.find('window.__PRELOADED_STATE__ = ') + len('window.__PRELOADED_STATE__ = '):]
        json_str = start_json[:start_json.find('</script')]
        json_data = json.loads(json_str)
        for car in self.get_dict_value(json_data, ['inventory', 'vehicles'], []):
            item = dict()
            item['year'] = car.get('year')
            item['make'] = car.get('make')
            item['model'] = car.get('model')
            item['trim'] = car.get('trim')
            item['mileage'] = car.get('mileage')
            item['price'] = self.get_dict_value(car, ['price', 'total'])
            item['tag'] = car['vehicleTags'][0]['tagName'] if car['vehicleTags'] else None
            yield item
