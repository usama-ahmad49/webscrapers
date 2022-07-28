import json
import time

import scrapy
from scrapy.crawler import CrawlerProcess
from seleniumwire import webdriver

import AirtableApi

basekey = 'appCpRqZ4zT3J3PKA'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'insolvencynotices'

airtable_client = AirtableApi.AirtableClient(apikey, basekey)

processed = []


class insolvencynoticesAirtable(scrapy.Spider):
    name = 'insolvencynotices'

    def start_requests(self):
        url = 'https://www.insolvencynotices.com.au/browse/20000'
        driver = webdriver.Firefox()
        driver.get(url)
        time.sleep(5)
        res = scrapy.Selector(text=driver.page_source)
        Lastpage = int(res.css('.ng-scope.active ::text').extract_first())
        headers = dict([v for v in driver.requests if 'https://www.insolvencynotices.com.au/rest/notice/summarize/' in v.url][1].headers)
        driver.close()
        i = 0
        while i <= Lastpage:
            url = f'https://www.insolvencynotices.com.au/rest/notice/summarize/{i}'
            i+=1
            yield scrapy.Request(url=url, headers=headers)

    def parse(self, response, **kwargs):
        data = json.loads(response.text)
        for dat in data['list']:
            item = dict()
            try:
                item['url'] = f'https://www.insolvencynotices.com.au{dat["id"]}'
            except:
                pass
            try:
                item['Notice'] = dat["discriminator"]
            except:
                pass
            try:
                item['CompanyName'] = dat['companies'][0]['name']
            except:
                pass
            try:
                item['CompanyNumber'] = dat['companies'][0]['australianCompanyNumber']
            except:
                pass
            try:
                item['DateCreated'] = dat['dateCreated'].split('T')[0]
            except:
                pass
            try:
                item['Liquidators'] = dat['liquidators']
            except:
                pass
            processed.append(item)

    def close(spider, reason):
        airtable_client.insert_records(table_name, processed)


process = CrawlerProcess({
    'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"})

process.crawl(insolvencynoticesAirtable)
process.start()
