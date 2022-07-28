import json

import requests
import scrapy
from scrapy.crawler import CrawlerProcess
import logging
import csv
headers = ['Venue Group','Brand','Venue Name', 'City', 'Country', 'Full Address']
fileinputcsv = open('BedsandBars.csv', 'w',encoding='utf-8', newline='')
csvwriter = csv.DictWriter(fileinputcsv, fieldnames=headers)
csvwriter.writeheader()
class BedsandBars(scrapy.Spider):
    name = 'BedsandBars'
    def start_requests(self):
        urls = ['https://www.st-christophers.co.uk/hostels',
                'https://www.belushis.com/bars',
                'https://www.flyingpig.nl',
                'http://www.winston.nl/',
                'http://www.bauhaus.be/']
        for url in urls:
            yield scrapy.Request(url=url)
    def parse(self, response, **kwargs):
        if 'st-christophers' in response.url:
            for res in response.css('.destination-accordion.mb-2'):
                for re in res.css('ul li.mb-2'):
                    link = 'https://www.st-christophers.co.uk'+re.css('a::attr(href)').extract_first()
                    city = res.css('h4::text').extract_first().strip()
                    yield scrapy.Request(url=link, callback=self.parse_data, meta={'brand': 'st-christophers','city':city})
        elif 'belushis' in response.url:
            for res in response.css('.card.thumb.pure-u-1.pure-u-md-1-3'):
                link = res.css('a::attr(href)').extract_first()
                yield scrapy.Request(url=link, callback=self.parse_data, meta={'brand': 'belushis'})
        elif 'flyingpig' in response.url:
            for res in response.css('#__layout > div > div > div > main > section.layout-local > article:nth-child(1) > div:nth-child(3) a'):
                link = 'https://www.flyingpig.nl'+res.css('a::attr(href)').extract_first()
                yield scrapy.Request(url=link, callback=self.parse_data, meta={'brand': 'flyingpig'})
        elif 'winston' in response.url:
            yield scrapy.Request(url='http://www.winston.nl/about/directions', callback=self.parse_data, meta={'brand': 'winston'})
        elif 'bauhaus' in response.url:
            yield scrapy.Request(url='http://www.bauhaus.be/directions', callback=self.parse_data, meta={'brand': 'bauhaus'})


    def parse_data(self, response):
        item = dict()
        if 'st-christophers' in response.meta['brand']:
            item['Brand'] = response.meta['brand']
            item['Venue Group'] = 'bedsandbars'
            item['Venue Name'] = response.css('h1::text').extract_first().strip()
            item ['Full Address'] = response.css('.hostel-address::Text').extract_first().strip()
            item['City'] = response.meta['city'].replace('+','').strip()
            if 'Kingdom' in item ['Full Address'].split()[-1]:
                item['Country'] = ' '.join(item ['Full Address'].split()[-2:])
            elif item['City'] in ['London', 'Edinburgh']:
                item['Country'] = 'United Kingdom'
            else:
                item['Country'] = item['Full Address'].split()[-1]
            csvwriter.writerow(item)
            fileinputcsv.flush()
        elif 'belushis' in response.meta['brand']:
            item['Brand'] = response.meta['brand']
            item['Venue Group'] = 'bedsandbars'
            item['Venue Name'] = response.css('h2::text').extract_first().strip()
            item['Full Address'] = response.css('.street-address::Text').extract_first().strip()
            item['City'] = response.css('.locality::Text').extract_first().strip()
            item['Country'] = response.css('.country-name::Text').extract_first().strip()
            csvwriter.writerow(item)
            fileinputcsv.flush()
        elif 'flyingpig' in response.meta['brand']:
            item['Brand'] = response.meta['brand']
            item['Full Address'] = response.css('#__layout > div > div > div > main > section:nth-child(3) > article > div:nth-child(2) > ul > li:nth-child(3)::text').extract_first()
            item['City'] = item['Full Address'].split()[-1]
            item['Country'] = 'Netherlands'
            item['Venue Group'] = 'bedsandbars'
            item['Venue Name'] = ''.join(response.url.split('/')[-2:-1])
            csvwriter.writerow(item)
            fileinputcsv.flush()
        elif 'winston' in response.meta['brand']:
            item['Brand'] = response.meta['brand']
            item['Full Address'] = response.css('#new_div_75862 > p:nth-child(3)::text').extract_first()
            item['City'] = 'Amsterdam'
            item['Country'] = 'Netherlands'
            item['Venue Group'] = 'bedsandbars'
            item['Venue Name'] = 'Winston'
            csvwriter.writerow(item)
            fileinputcsv.flush()
        elif 'bauhaus' in response.meta['brand']:
            item['Brand'] = response.meta['brand']
            item['Full Address'] = response.css('body > section.footer > footer > div.bottom-bar > div > div > address ::text').extract_first().replace('\r\n',' ').strip()
            item['City'] = 'Bruges'
            item['Country'] = 'Belgium'
            item['Venue Group'] = 'bedsandbars'
            item['Venue Name'] = 'bauhaus'
            csvwriter.writerow(item)
            fileinputcsv.flush()

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(BedsandBars)
process.start()