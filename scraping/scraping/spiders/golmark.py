import datetime
import json
import os
import sys

from scrapy import Spider
import scrapy
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_PATH)


class Glomark(Spider):
    name = 'glomark'
    title = 'Glomark'
    start_urls = ['https://glomark.lk/']

    custom_settings = {
        'ITEM_PIPELINES': {'scraping.pipelines.golmark.GolmarkPipeline': 600}
    }

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

    def parse(self, response):
        for category_link in response.css('.full_nav_dep_block_ a ::attr(href)').extract():
            if '/dp/' in category_link:
                dept_id = category_link.split('/')[-1] if category_link.split('/') else None
                if dept_id:
                    yield scrapy.Request('https://glomark.lk/ajax_products_by_department?depId={}'.format(dept_id),
                                         callback=self.parse_category)

    def parse_category(self, response):
        data = json.loads(response.text)
        for product in self.get_dict_value(data, ['data', 'products_list'], []):
            item = dict()
            item['name'] = product.get('name')
            item['url'] ='https://glomark.lk/{}/p/{}'.format(product['name'].replace(' ', '-').lower(), product['id'])
            item['price'] = self.get_dict_value(product, ['priceDetails', 'price'])
            item['createdDate'] = datetime.datetime.now().date()
            item['imageUrl'] = 'https://objectstorage.ap-mumbai-1.oraclecloud.com/n/softlogicbicloud/b/cdn/o/products/{}'.format(product.get('image', ''))
            for category in self.get_dict_value(data, ['data', 'categories'], {}).items():
                if category[1]['id'] == product.get('category'):
                    item['category'] = category[1]['name']
                    break
            yield item



