import json
import csv
import requests
import scrapy
from scrapy.crawler import CrawlerProcess
import logging

headers = ['Venue Group', 'Venue Name', 'City', 'Country', 'Full Address']
fileinputcsv = open('solotel.csv', 'w',encoding='utf-8', newline='')
csvwriter = csv.DictWriter(fileinputcsv, fieldnames=headers)
csvwriter.writeheader()

class solotel(scrapy.Spider):
    name = 'solotel'
    def start_requests(self):
        url = 'https://www.solotel.com.au/pubs-and-bars'
        yield scrapy.Request(url=url)
    def parse(self, response, **kwargs):
        for res in response.css('#block-mainpagecontent > article > div > div > div:nth-child(4) > div > div > div > div > div .grid-block'):
            link = res.css('a::attr("href")').extract_first()
            name = res.css('h3::text').extract_first()
            city = res.css('h6::text').extract_first()
            yield scrapy.Request(url=link, callback= self.parse_data, dont_filter= True, meta={'name':name,'city':city})

    def parse_data(self, response):
        item = dict()
        item['Venue Group'] = 'solotel'
        item['Venue Name'] = response.meta['name']
        item['City'] = response.meta['city']
        item['Country'] = 'Australia'
        item['Full Address'] = response.css('#block-solotelfooter > div > footer > div > div.footer-blocks > div:nth-child(1) > div > p:nth-child(1)::text').extract_first('').strip()
        if item['Full Address'] == '' or item['Full Address'] == None:
            item['Full Address'] = response.css('#block-solotelfooter > div > footer > div > div.footer-blocks > div:nth-child(1) > div > p:nth-child(2)::text').extract_first('').strip()
        if item['Full Address'] == '' or item['Full Address'] == None:
            item['Full Address'] = response.css('#block-solotelfooter > div > footer > div > div.footer-blocks > div:nth-child(1) > div > p:nth-child(1) > a:nth-child(1)::text').extract_first('').strip()
        if item['Full Address'] == '' or item['Full Address'] == None:
            item['Full Address'] = response.css('#block-solotelfooter > div > footer > div > div.footer-blocks > div:nth-child(1) > div > p:nth-child(3)::text').extract_first('').strip()
        csvwriter.writerow(item)
        fileinputcsv.flush()




process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(solotel)
process.start()