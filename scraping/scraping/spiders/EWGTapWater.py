import csv

import scrapy
from scrapy.crawler import CrawlerProcess

csvfileR = open('US Zip Codes.csv', 'r', encoding='utf-8')
input_reader = csvfileR.read()

headers = ["Zip Code", "Utility Name", "City Served", "Population Served", "Data Available", "Source", "TTL Contaminants Exceed", "TTL Contaminants", "Contaminant Exceeds 1", "CE 1 PE", "CE 1 X EXCEED MHG", "CE 1THIS UTILITY", "CE 1EWG MHG", "CE 1LEGAL LIMIT", "Contaminant Exceeds 2", "CE 2 PE", "CE 2 X EXCEED MHG", "CE 2THIS UTILITY", "CE 2EWG MHG", "CE 2LEGAL LIMIT", "Contaminant Exceeds 3", "CE 3 PE", "CE 3 X EXCEED MHG", "CE 3THIS UTILITY", "CE 3EWG MHG", "CE 3LEGAL LIMIT", "Contaminant Exceeds 4", "CE 4 PE", "CE 4 X EXCEED MHG", "CE 4THIS UTILITY", "CE 4EWG MHG", "CE 4LEGAL LIMIT", "Contaminant Exceeds 5", "CE 5 PE", "CE 5 X EXCEED MHG", "CE 5THIS UTILITY", "CE 5EWG MHG", "CE 5LEGAL LIMIT", "Contaminant Exceeds 6", "CE 6 PE", "CE 6 X EXCEED MHG", "CE 6THIS UTILITY", "CE 6EWG MHG", "CE 6LEGAL LIMIT", "Contaminant Exceeds 7", "CE 7 PE", "CE 7 X EXCEED MHG", "CE 7THIS UTILITY",
           "CE 7EWG MHG", "CE 7LEGAL LIMIT", "Contaminant Exceeds 8", "CE 8 PE", "CE 8 X EXCEED MHG", "CE 8THIS UTILITY", "CE 8EWG MHG", "CE 8LEGAL LIMIT", "Contaminant Exceeds 9", "CE 9 PE", "CE 9 X EXCEED MHG", "CE 9THIS UTILITY", "CE 9EWG MHG", "CE 9LEGAL LIMIT", "Contaminant Exceeds 10", "CE 10 PE", "CE 10 X EXCEED MHG", "CE 10THIS UTILITY", "CE 10EWG MHG", "CE 10LEGAL LIMIT", "Contaminant Exceeds 11", "CE 11 PE", "CE 11 X EXCEED MHG", "CE 11THIS UTILITY", "CE 11EWG MHG", "CE 11LEGAL LIMIT", "Contaminant Exceeds 12", "CE 12 PE", "CE 12 X EXCEED MHG", "CE 12THIS UTILITY", "CE 12EWG MHG", "CE 12LEGAL LIMIT", "Contaminant Exceeds 13", "CE 13 PE", "CE 13 X EXCEED MHG", "CE 13THIS UTILITY", "CE 13EWG MHG", "CE 13LEGAL LIMIT", "Contaminant Exceeds 14", "CE 14 PE", "CE 14 X EXCEED MHG", "CE 14THIS UTILITY", "CE 14EWG MHG", "CE 14LEGAL LIMIT", "Contaminant Exceeds 15", "CE 15 PE",
           "CE 15 X EXCEED MHG", "CE 15THIS UTILITY", "CE 15EWG MHG", "CE 15LEGAL LIMIT", "Contaminant Exceeds 16", "CE 16 PE", "CE 16 X EXCEED MHG", "CE 16THIS UTILITY", "CE 16EWG MHG", "CE 16LEGAL LIMIT", "Contaminant Exceeds 17", "CE 17 PE", "CE 17 X EXCEED MHG", "CE 17THIS UTILITY", "CE 17EWG MHG", "CE 17LEGAL LIMIT", "Contaminant Exceeds 18", "CE 18 PE", "CE 18 X EXCEED MHG", "CE 18THIS UTILITY", "CE 18EWG MHG", "CE 18LEGAL LIMIT", "Contaminant Exceeds 19", "CE 19 PE", "CE 19 X EXCEED MHG", "CE 19THIS UTILITY", "CE 19EWG MHG", "CE 19LEGAL LIMIT", "Contaminant Exceeds 20", "CE 20 PE", "CE 20 X EXCEED MHG", "CE 20THIS UTILITY", "CE 20EWG MHG", "CE 20LEGAL LIMIT", "Contaminant Exceeds 21", "CE 21 PE", "CE 21 X EXCEED MHG", "CE 21THIS UTILITY", "CE 21EWG MHG", "CE 21LEGAL LIMIT", "Contaminant Exceeds 22", "CE 22 PE", "CE 22 X EXCEED MHG", "CE 22THIS UTILITY", "CE 22EWG MHG",
           "CE 22LEGAL LIMIT", "Contaminant Exceeds 23", "CE 23 PE", "CE 23 X EXCEED MHG", "CE 23THIS UTILITY", "CE 23EWG MHG", "CE 23LEGAL LIMIT", "Contaminant Exceeds 24", "CE 24 PE", "CE 24 X EXCEED MHG", "CE 24THIS UTILITY", "CE 24EWG MHG", "CE 24LEGAL LIMIT", "Contaminant Exceeds 25", "CE 25 PE", "CE 25 X EXCEED MHG", "CE 25THIS UTILITY", "CE 25EWG MHG", "CE 25LEGAL LIMIT", "Contaminant Exceeds 26", "CE 26 PE", "CE 26 X EXCEED MHG", "CE 26THIS UTILITY", "CE 26EWG MHG", "CE 26LEGAL LIMIT", "Contaminant Exceeds 27", "CE 27 PE", "CE 27 X EXCEED MHG", "CE 27THIS UTILITY", "CE 27EWG MHG", "CE 27LEGAL LIMIT", "Contaminant Exceeds 28", "CE 28 PE", "CE 28 X EXCEED MHG", "CE 28THIS UTILITY", "CE 28EWG MHG", "CE 28LEGAL LIMIT", "Contaminant Exceeds 29", "CE 29 PE", "CE 29 X EXCEED MHG", "CE 29THIS UTILITY", "CE 29EWG MHG", "CE 29LEGAL LIMIT", "Contaminant Exceeds 30", "CE 30 PE",
           "CE 30 X EXCEED MHG", "CE 30THIS UTILITY", "CE 30EWG MHG", "CE 30LEGAL LIMIT", "Contaminant Exceeds 31", "CE 31 PE", "CE 31 X EXCEED MHG", "CE 31THIS UTILITY", "CE 31EWG MHG", "CE 31LEGAL LIMIT", "Contaminant Exceeds 32", "CE 32 PE", "CE 32 X EXCEED MHG", "CE 32THIS UTILITY", "CE 32EWG MHG", "CE 32LEGAL LIMIT", "Contaminant Exceeds 33", "CE 33 PE", "CE 33 X EXCEED MHG", "CE 33THIS UTILITY", "CE 33EWG MHG", "CE 33LEGAL LIMIT", "Contaminant Exceeds 34", "CE 34 PE", "CE 34 X EXCEED MHG", "CE 34THIS UTILITY", "CE 34EWG MHG", "CE 34LEGAL LIMIT", "Contaminant Exceeds 35", "CE 35 PE", "CE 35 X EXCEED MHG", "CE 35THIS UTILITY", "CE 35EWG MHG", "CE 35LEGAL LIMIT", "Contaminant TTL - 1", "Contaminant TTL - 2", "Contaminant TTL - 3", "Contaminant TTL - 4", "Contaminant TTL - 5", "Contaminant TTL - 6", "Contaminant TTL - 7", "Contaminant TTL - 8", "Contaminant TTL - 9",
           "Contaminant TTL - 10", "Contaminant TTL - 11", "Contaminant TTL - 12", "Contaminant TTL - 13", "Contaminant TTL - 14", "Contaminant TTL - 15", "Contaminant TTL - 16", "Contaminant TTL - 17", "Contaminant TTL - 18", "Contaminant TTL - 19", "Contaminant TTL - 20", "Contaminant TTL - 21", "Contaminant TTL - 22", "Contaminant TTL - 23", "Contaminant TTL - 24", "Contaminant TTL - 25", "Contaminant TTL - 26", "Contaminant TTL - 27", "Contaminant TTL - 28", "Contaminant TTL - 29", "Contaminant TTL - 30", "Contaminant TTL - 31", "Contaminant TTL - 32", "Contaminant TTL - 33", "Contaminant TTL - 34", "Contaminant TTL - 35 "]

fileout = open('EWGTapWater.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=headers)
writer.writeheader()


class EWGTapWater(scrapy.Spider):
    name = 'EWGTapWater'

    def start_requests(self):
        for data in input_reader.split('\n')[1:]:
            zipcode = data.split(',')[0]
            url = f'https://www.ewg.org/tapwater/search-results.php?zip5={zipcode}&searchtype=zip'
            yield scrapy.Request(url=url, meta={'zip': zipcode})

    def parse(self, response, **kwargs):
        if response.css('.featured-utility h2::text').extract_first() is not None:
            F_link = 'https://www.ewg.org/tapwater/' + response.css('.featured-utility a::attr(href)').extract_first()
            yield scrapy.Request(url=F_link, callback=self.parseweblink, meta={'zip': response.meta['zip']})
        if response.css('.search-results-table') is not None:
            for res in response.css('.search-results-table'):
                for r in res.css('tbody tr'):
                    link = 'https://www.ewg.org/tapwater/' + r.css(' ::attr(href)').extract_first()
                    yield scrapy.Request(url=link, callback=self.parseweblink, meta={'zip': response.meta['zip']})

    def parseweblink(self, response):
        item = dict()
        item['Zip Code'] = response.meta['zip']
        item['Utility Name'] = response.css('h1::Text').extract_first()
        for res in response.css('.utility-details-wrapper ul li'):
            if res.css('span ::text').extract_first() is None:
                item['City Served'] = res.css('::text').extract_first()
            else:
                if 'Serves' in res.css('span ::text').extract_first():
                    item['Population Served'] = ''.join(res.css(' ::text').extract()).split(':')[-1].strip()
                if 'Data available' in res.css('span ::text').extract_first():
                    item['Data Available'] = ''.join(res.css(' ::text').extract()).split(':')[-1].strip()
                if 'Source' in res.css('span ::text').extract_first():
                    item['Source'] = ''.join(res.css(' ::text').extract()).split(':')[-1].strip()

        item['TTL Contaminants Exceed'] = response.css('.contaminant-tile-number::text').extract_first('')
        try:
            item['TTL Contaminants'] = response.css('.total-contaminants::text').extract_first().split()[0]
        except:
            pass

        try:
            for i, reex in enumerate(response.css('.contaminants-grid')[0].css('.contaminant-grid-item')):
                item[f'Contaminant Exceeds {i + 1}'] = reex.css('.contaminant-name h3::text').extract_first()
                item[f'CE {i+1} PE'] = reex.css('.potentital-effect::text').extract_first('')
                item[f'CE {i+1} X EXCEED MHG'] = reex.css('.detect-times-greater-than::text').extract_first('')
                for r in reex.css('.detect-levels-overview.flex div'):
                    if 'UTILITY' in r.css('span::text').extract_first():
                        item[f'CE {i+1}THIS UTILITY'] = r.css('span::text').extract()[-1]
                    if 'EWG HEALTH GUIDELINE' in r.css('span::text').extract_first():
                        item[f'CE {i+1}EWG MHG'] = r.css('span::text').extract()[-1]
                    if 'NO LEGAL LIMIT' in r.css('span::text').extract_first():
                        item[f'CE {i+1}LEGAL LIMIT'] = r.css('span::text').extract()[-1]
        except:
            pass
        try:
            for j, rettl in enumerate(response.css('.contaminants-grid')[1].css('.contaminant-grid-item')):
                item[f'Contaminant TTL - {j + 1}'] = rettl.css('.contaminant-name h3::text').extract_first()
        except:
            pass
        writer.writerow(item)
        fileout.flush()


process = CrawlerProcess({
    'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"})

process.crawl(EWGTapWater)
process.start()
