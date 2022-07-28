import json
import csv
import requests
import scrapy
from scrapy.crawler import CrawlerProcess
import logging

headers = ['Venue Group', 'Venue Name', 'City', 'Country', 'Full Address']
fileinputcsv = open('Dirtybones.csv', 'w',encoding='utf-8', newline='')
csvwriter = csv.DictWriter(fileinputcsv, fieldnames=headers)
csvwriter.writeheader()
class DirtyBones(scrapy.Spider):
    name = 'DirtyBones'
    def start_requests(self):
        url = 'https://dirty-bones.com/locations'
        yield scrapy.Request(url=url)
    def parse(self, response, **kwargs):
        for res in response.css('section.locations .col.col--right.parallax'):
            if "Find out more" in res.css('a::text').extract_first().strip():
                link  = "https://dirty-bones.com/"+res.css('a::attr(href)').extract_first()
                yield scrapy.Request(url=link, callback = self.parse_data)

    def parse_data(self, response):
        item = dict()
        item['Venue Group'] = 'Dirty Bones'
        item['Venue Name'] = response.css('.banner.pp h1::text').extract_first().strip()
        item['City'] = response.css('[itemprop="streetAddress"] ::text').extract()[-2].strip()
        item['Country'] = 'UK'
        item['Full Address'] = ''.join(response.css('[itemprop="streetAddress"] ::text').extract()).strip().replace('\r\n',' ')
        csvwriter.writerow(item)
        fileinputcsv.flush()

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(DirtyBones)
process.start()