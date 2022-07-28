import datetime
import json

import scrapy
from scrapy.crawler import CrawlerProcess


import AirtableApi

processed = []
basekey = 'appJ3Xo5EL7C6U15V'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'PADtable'

airtable_client = AirtableApi.AirtableClient(apikey, basekey)


class moretonbay(scrapy.Spider):
    name = 'moretonbay'

    def start_requests(self):
        startdate = (datetime.datetime.now() - datetime.timedelta(days=10 * 365)).strftime('%Y-%B-%d')
        enddate = datetime.datetime.now().strftime('%Y-%B-%d')
        url = f'https://api.moretonbay.qld.gov.au/mplu/da/search/advanced?currentPage=1&dateRange=custom&end={enddate}&propertyType=address&searchType=advanced&start={startdate}'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        jsondata = json.loads(response.text)
        for data in jsondata:
            item = dict()
            item['Application Number'] = str(data['fileId'])
            item['Domain'] = 'https://www.moretonbay.qld.gov.au/'
            item['Date of application'] = data['lodgedDate'].split('T')[0]
            item['Property Address'] = data['siteName']
            item['Application Description'] = data['description']
            item['Application Status'] = data['applicationType']

            processed.append(item)

    def close(spider, reason):
        airtable_client.insert_records(table_name, processed)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(moretonbay)
process.start()
