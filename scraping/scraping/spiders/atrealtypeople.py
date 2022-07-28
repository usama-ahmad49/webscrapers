try:
    import pkg_resources.py2_warn
except ImportError:
    pass

import json
import requests
import scrapy
from scrapy.crawler import CrawlerProcess
import AirtableApi

basekey = 'app9kA16Z7EukfnX1'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'atrealtypeople'

airtable_client = AirtableApi.AirtableClient(apikey, basekey)
processed = []

class atrealtypeople(scrapy.Spider):
    name = 'atrealty'

    def start_requests(self):
        url = "https://www.atrealty.com.au/wp-json/hi-api/v1/team?page=1&per_page=9"
        res = requests.get(url)
        resjson = json.loads(res.text)
        resp = scrapy.Selector(text=resjson['page_button'])
        totalpages = int(resp.css('a')[-2].css('::Text').extract_first())
        i=1
        while i <= totalpages:
            link = f"https://www.atrealty.com.au/wp-json/hi-api/v1/team?page={i}&per_page=9"
            i += 1
            yield scrapy.Request(url=link, dont_filter=True)

    def parse(self, response, **kwargs):
        resjson = json.loads(response.text)
        for da in resjson['data']:
            item = dict()
            item['url'] = da['permalink']
            item['Name'] = da['name']
            item['Domain'] = 'https://www.atrealty.com.au/'
            item['Job Title'] = da['tp_job_title']
            item['Address'] = da['tp_address']
            try:
                item['Phone'] = da['tp_phone_number']
            except:
                pass
            try:
                item['Email'] = da['tp_email_address']
            except:
                pass
            try:
                item['Linkedin'] = da['tp_linkedin']
            except:
                pass
            processed.append(item)
    def close(spider, reason):
        firstcol = 'url'
        airtable_client.insert_records(table_name, processed, firstcol)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(atrealtypeople)
process.start()
