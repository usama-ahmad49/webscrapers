import json
import csv
import requests
import scrapy
from scrapy.crawler import CrawlerProcess
import logging

headers = ['Venue Group', 'Venue Name', 'City', 'Country', 'Full Address']
fileinputcsv = open('metropolitanpubcompany.csv', 'w',encoding='utf-8', newline='')
csvwriter = csv.DictWriter(fileinputcsv, fieldnames=headers)
csvwriter.writeheader()

class metropolitanpubcompany(scrapy.Spider):
    name = 'metropolitanpubcompany'
    def start_requests(self):
        url = 'https://www.metropolitanpubcompany.com/our-pubs/'
        yield scrapy.Request(url=url)
    def parse(self, response, **kwargs):
        for res in response.css('.ourpubs.pub-list .cat-section'):
            link = res.css('a::attr("href")').extract_first()
            yield scrapy.Request(url=link, callback= self.parse_data, dont_filter= True)

    def parse_data(self, response):
        for res in response.css('.pub-list .wppl-single-result'):
            link = res.css('a::attr("href")').extract_first()
            name = res.css('h2::text').extract_first()
            city = res.css('h3::text').extract_first()
            yield scrapy.Request(url=link, callback=self.parse_second_data, meta={'name':name, 'city':city})

    def parse_second_data(self,response):
        item = dict()
        item['Venue Group'] = 'metropolitan pub company'
        item['Venue Name'] = response.meta['name']
        item['City'] = response.meta['city']
        try:
            item['Country'] = response.css('span.country::text').extract_first()
            item['Full Address'] = ''.join(response.css('.LocationInfo.LocationInfo--address .LocationInfo-content')[0].css('::text').extract()).replace('\n',' ')
        except:
            pass
        csvwriter.writerow(item)
        fileinputcsv.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(metropolitanpubcompany)
process.start()