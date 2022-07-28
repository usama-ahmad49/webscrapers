import json
import csv
import requests
import scrapy
from scrapy.crawler import CrawlerProcess
import logging

headers = ['Venue Group', 'Venue Name', 'City', 'Country', 'Full Address']
fileinputcsv = open('sydneycollective.csv', 'w',encoding='utf-8', newline='')
csvwriter = csv.DictWriter(fileinputcsv, fieldnames=headers)
csvwriter.writeheader()

class sydneycollective(scrapy.Spider):
    name = 'sydneycollective'
    def start_requests(self):
        url = 'https://www.sydneycollective.com.au/venue/'
        yield scrapy.Request(url=url)
    def parse(self, response, **kwargs):
        for res in response.css('#page > section > section:nth-child(2) > section > div > div > figure'):
            link = res.css('a::attr("href")').extract_first()
            name = res.css('a::attr(title)').extract_first()
            # city = res.css('h6::text').extract_first()
            yield scrapy.Request(url=link, callback= self.parse_data, dont_filter= True, meta={'name':name})

    def parse_data(self, response):
        item = dict()
        item['Venue Group'] = 'sydneycollective'
        item['Venue Name'] = response.meta['name']
        # item['City'] = response.meta['city']
        item['Country'] = 'Australia'
        item['Full Address'] = ''.join(response.css('.content-4-box.show-content span::text').extract()).replace('\n',' ').strip()
        if item['Full Address'] == '':
            item['Full Address'] = ''.join(response.css('#page > section > section:nth-child(5) > section > div.content-4-box.show-content > div > p:nth-child(2)::text').extract()).replace('\n',' ').strip()
        if item['Full Address'] == '':
            item['Full Address'] = ''.join(response.css('#page > section > section:nth-child(10) > section > div:nth-child(1) > div > p:nth-child(4)::text').extract()).replace('\n',' ').strip()
        if item['Full Address'] == '':
            pass

        # item['City'] = item['Full Address'].split()[-4]
        csvwriter.writerow(item)
        fileinputcsv.flush()




process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(sydneycollective)
process.start()