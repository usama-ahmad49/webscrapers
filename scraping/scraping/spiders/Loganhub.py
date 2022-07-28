import json

import requests
import scrapy
from scrapy.crawler import CrawlerProcess

import AirtableApi

headers = {
    "authority": "devet-proxy.loganhub.com.au",
    "sec-ch-ua": "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"",
    "accept": "application/json, text/plain, */*",
    "dnt": "1",
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "origin": "https://devet.loganhub.com.au",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://devet.loganhub.com.au/",
    "accept-language": "en-US,en;q=0.9"
}

processed = []
basekey = 'appJ3Xo5EL7C6U15V'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'PADtable'

airtable_client = AirtableApi.AirtableClient(apikey, basekey)


class Loganhub(scrapy.Spider):
    name = "Loganhub"

    def start_requests(self):
        url = 'https://devet-proxy.loganhub.com.au/devetapi/applications?pageOffset=1&pageLimit=250&sortColumn=appNo&sortDesc=0'
        res = requests.get(url=url, headers=headers)
        r = json.loads(res.text)
        TotalPages = r['pagination']['total']
        page = 1
        while page <= TotalPages:
            link = f"https://devet-proxy.loganhub.com.au/devetapi/applications?pageOffset={page}&pageLimit=250&sortColumn=appNo&sortDesc=0"
            page += 1
            yield scrapy.Request(url=link, headers=headers)

    def parse(self, response, **kwargs):
        jsondata = json.loads(response.text)
        for data in jsondata['data']:
            item = dict()
            item['Application Number'] = data['appNo']
            item['Domain'] = 'https://devet.loganhub.com.au/'
            item['Suburb'] = data['propertySuburb']
            item['Date of application'] = data['lodgementDate']
            item['Name of applicant'] = data['applicant']
            item['Property Address'] = data['propertyFmtAddress']
            item['Application Description'] = data['description']
            item['Application Status'] = data['decisionStatus']
            if item['Application Status'] == '':
                item['Application Status'] = data['status']

            processed.append(item)

    def close(spider, reason):
        airtable_client.insert_records(table_name, processed)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(Loganhub)
process.start()
