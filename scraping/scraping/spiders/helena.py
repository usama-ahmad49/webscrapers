import os
import sys
import requests
import csv

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_PATH)
from copy import deepcopy
import json
import time

# from scraping.spiders.base_spider import BaseSpider
from scrapy import Spider
from scraping.spiders import helenaHeaders
import scrapy
from selenium import webdriver

csv_columns = ['tramite', 'fechaFin', 'razonSocial', 'nombre', 'marca', 'modelo', 'pm', 'expediente', ]
csv_file = open('helena.csv', 'w', encoding="utf-8", newline='')
writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
writer.writeheader()


class HelenaSpider(Spider):
    name = 'helena'
    title = 'Helena'
    handle_httpstatus_list = [500]
    start_urls = ['https://helena.anmat.gob.ar/Boletin/']

    count = 0
    custom_settings = {
        # 'ITEM_PIPELINES': {'scraping.pipelines.helena.HelenaPipeline': 600}
    }

    def start_requests(self):

        yield scrapy.Request('https://helena.anmat.gob.ar/Boletin/', meta={'page': 1})

    def parse(self, response):

        count = 0
        for product in response.css('#ctl00_ContentPlaceHolder1_gvTramites tr'):
            item = dict()
            # item['page_no'] = response.meta['page']
            item['tramite'] = product.css('td:nth-child(1) ::text').extract_first('')
            item['fechaFin'] = product.css('td:nth-child(2) ::text').extract_first('')
            item['razonSocial'] = product.css('td:nth-child(3) ::text').extract_first('')
            item['nombre'] = product.css('td:nth-child(4) ::text').extract_first('')
            item['marca'] = product.css('td:nth-child(5) ::text').extract_first('')
            item['modelo'] = product.css('td:nth-child(6) ::text').extract_first('')
            item['pm'] = product.css('td:nth-child(7) ::text').extract_first('')
            item['expediente'] = product.css('td:nth-child(8) ::text').extract_first('')

            if item['tramite'].strip() and not item['tramite'].strip().isdigit():
                count += 1
                writer.writerow(item)
                csv_file.flush()
                print('row printed')


        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 10:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})
        if response.meta['page'] > 10 and response.meta['page'] < 20:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data1)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 20 and response.meta[
            'page'] > 19:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data1)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})

        if response.meta['page'] > 20 and response.meta['page'] <= 29:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data2)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 30 and response.meta[
            'page'] > 29:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data2)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})

        if response.meta['page'] > 30 and response.meta['page'] <= 39:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data3)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 40 and response.meta[
            'page'] > 39:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data3)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})
        if response.meta['page'] > 40 and response.meta['page'] <= 49:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data4)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 50 and response.meta[
            'page'] > 49:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data4)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})
        if response.meta['page'] > 50 and response.meta['page'] <= 59:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data5)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 60 and response.meta[
            'page'] > 59:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data5)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})

        if response.meta['page'] > 60 and response.meta['page'] <= 69:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data6)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 70 and response.meta[
            'page'] > 69:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data6)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})

        if response.meta['page'] > 70 and response.meta['page'] <= 79:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data7)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 80 and response.meta[
            'page'] > 79:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data7)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})

        if response.meta['page'] > 80 and response.meta['page'] <= 89:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data8)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 90 and response.meta[
            'page'] > 89:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data8)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})
        if response.meta['page'] > 90 and response.meta['page'] <= 99:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data9)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 100 and response.meta[
            'page'] > 99:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data9)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})
        if response.meta['page'] > 100 and response.meta['page'] <= 109:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data10)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 110 and response.meta[
            'page'] > 109:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data10)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})
        if response.meta['page'] > 110 and response.meta['page'] <= 119:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data11)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 120 and response.meta[
            'page'] > 119:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data11)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})
        if response.meta['page'] > 120 and response.meta['page'] <= 129:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data12)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 130 and response.meta[
            'page'] > 129:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data12)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})
        if response.meta['page'] > 130 and response.meta['page'] <= 139:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data13)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 140 and response.meta[
            'page'] > 139:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data13)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})
        if response.meta['page'] > 140 and response.meta['page'] <= 149:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data14)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 150 and response.meta[
            'page'] > 149:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data14)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})
        if response.meta['page'] > 150 and response.meta['page'] <= 159:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data15)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 160 and response.meta[
            'page'] > 159:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data15)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})
        if response.meta['page'] > 160 and response.meta['page'] <= 169:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data16)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 170 and response.meta[
            'page'] > 169:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data16)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})
        if response.meta['page'] > 170 and response.meta['page'] <= 179:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data17)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 180 and response.meta[
            'page'] > 179:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data17)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})
        if response.meta['page'] > 180 and response.meta['page'] <= 189:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data18)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 190 and response.meta[
            'page'] > 189:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data18)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})
        if response.meta['page'] > 190 and response.meta['page'] <= 199:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data19)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

        if response.css('#ctl00_ContentPlaceHolder1_gvTramites tr') and response.meta['page'] <= 200 and response.meta[
            'page'] > 199:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data19)
            data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
            yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                     meta={'page': response.meta['page'] + 1})
        if response.meta['page'] > 200 and response.meta['page'] <= 204:
            print('{} : {}'.format(response.meta['page'], count))
            data = deepcopy(helenaHeaders.data20)
            if response.meta['page'] % 10 == 0:
                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 2)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 2})
            else:

                data['__EVENTARGUMENT'] = data['__EVENTARGUMENT'].format(response.meta['page'] + 1)
                yield scrapy.FormRequest('https://helena.anmat.gob.ar/Boletin/', method='POST', formdata=data,
                                         meta={'page': response.meta['page'] + 1})

    #     if response.meta['page'] >= 11:
    #         driver = webdriver.Chrome()
    #         driver.get(response.url)
    #         self.click_button(driver, "//a[text()='...']")
    #         time.sleep(5)
    #         for x in range(1, 211):
    #             for page_number in range(9, 10):
    #                 resp = scrapy.Selector(text=driver.page_source)
    #
    #                 for product in resp.css('#ctl00_ContentPlaceHolder1_gvTramites tr'):
    #                     item = dict()
    #                     # item['page_no'] = response.meta['page']
    #                     item['tramite'] = product.css('td:nth-child(1) ::text').extract_first('')
    #                     item['fechaFin'] = product.css('td:nth-child(2) ::text').extract_first('')
    #                     item['razonSocial'] = product.css('td:nth-child(3) ::text').extract_first('')
    #                     item['nombre'] = product.css('td:nth-child(4) ::text').extract_first('')
    #                     item['marca'] = product.css('td:nth-child(5) ::text').extract_first('')
    #                     item['modelo'] = product.css('td:nth-child(6) ::text').extract_first('')
    #                     item['pm'] = product.css('td:nth-child(7) ::text').extract_first('')
    #                     item['expediente'] = product.css('td:nth-child(8) ::text').extract_first('')
    #                     if item['tramite'].strip() and not item['tramite'].strip().isdigit():
    #                         count += 1
    #                         yield item
    #                 self.click_button(driver, "//a[text()='{}']".format((x * 10) + page_number))
    #                 time.sleep(5)
    #             self.click_button(driver, "//a[text()='...']")
    #             time.sleep(10)
    #
    # @staticmethod
    # def click_button(driver, xpath):
    #     scroll_pause_time = 1
    #     last_height = driver.execute_script("return document.body.scrollHeight")
    #     while True:
    #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         time.sleep(scroll_pause_time)
    #         new_height = driver.execute_script("return document.body.scrollHeight")
    #         if new_height == last_height:
    #             break
    #         last_height = new_height
    #     got = False
    #     while not got:
    #         try:
    #             driver.find_element_by_xpath(xpath).click()
    #             got = True
    #         except:
    #             time.sleep(1)
    #             pass
