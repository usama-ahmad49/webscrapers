import json
import csv
import requests
import scrapy
from scrapy.crawler import CrawlerProcess
import logging

headers = ['Venue Group', 'Venue Name', 'City', 'Country', 'Full Address']
fileinputcsv = open('funlab.csv', 'w',encoding='utf-8', newline='')
csvwriter = csv.DictWriter(fileinputcsv, fieldnames=headers)
csvwriter.writeheader()

class funlab(scrapy.Spider):
    name = 'funlab'
    def start_requests(self):
        url = 'https://www.fun-lab.com/'
        yield scrapy.Request(url=url)
    def parse(self, response, **kwargs):
        for res in response.css('#page-careers-home > div > section.our-people-container.animated-section > div.container-small > p:nth-child(3) > a'):
            link = res.css('a::attr("href")').extract_first()
            yield scrapy.Request(url=link, callback= self.parse_data, dont_filter= True)

    def parse_data(self, response):
        for res in response.css('ul.dropdown li'):
            link = response.url+res.css('a::attr("href")').extract_first()[1:]
            name = res.css('a::text').extract_first()
            yield scrapy.Request(url=link, callback=self.parse_second_data)

    def parse_second_data(self,response):
        item = dict()
        item['Venue Group'] = 'fun-lab'
        item['Venue Name'] = response.css('title::text').extract_first()
        item['City'] = response.css('#js_location_dropdown > span::text').extract_first()
        try:
            item['Country'] = 'Australia'
            item['Full Address'] = response.css('address::text').extract_first().strip()
        except:
            pass
        csvwriter.writerow(item)
        fileinputcsv.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(funlab)
process.start()