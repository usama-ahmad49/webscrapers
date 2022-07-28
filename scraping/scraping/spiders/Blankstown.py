try:
    import pkg_resources.py2_warn
except ImportError:
    pass

import requests
import scrapy
from scrapy.crawler import CrawlerProcess

import AirtableApi

processed = []
basekey = 'appZw5uQo3gxzMI2I'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'bankstown'

airtable_client = AirtableApi.AirtableClient(apikey, basekey)


class blackstown(scrapy.Spider):
    name = 'blankstown'

    def start_requests(self):
        url = 'https://datrack.canterbury.nsw.gov.au/cgi/datrack.pl?search=search&startidx=0'
        req = requests.get(url)
        reqdata = scrapy.Selector(text=req.content.decode('utf-8'))
        totalresults = int(reqdata.css('.datrack_countheader .datrack_count::text').extract_first().split('of')[-1].strip())
        i = 0
        while i < 1:
            url = f'https://datrack.canterbury.nsw.gov.au/cgi/datrack.pl?search=search&startidx={i}'
            yield scrapy.Request(url=url)
            i += 10

    def parse(self, response, **kwargs):
        for i, urlprop in enumerate(response.css('table.datrack_resultcontainer tr td.datrack_danumber_cell')):
            urlpropind = urlprop.css('a::attr(href)').extract_first()
            suburb = response.css('table.datrack_resultcontainer tr td.datrack_town_cell')[i].css('::text').extract_first('')
            yield scrapy.Request(url=urlpropind, callback=self.parse_prop, meta={'suburb': suburb})

    def parse_prop(self, response):
        item = dict()
        item['Suburb'] = response.meta['suburb']
        for res in response.css('.wh_preview_master tr'):
            if 'Application No:' in res.css('th::text').extract_first(''):
                item['Application Number'] = res.css('td::text').extract_first('')
            if 'Description:' in res.css('th::text').extract_first(''):
                item['Application Description'] = res.css('td::text').extract_first('')
            if 'Date Lodged:' in res.css('th::text').extract_first(''):
                item['Date of application'] = res.css('td::text').extract_first('')
            if 'Status:' in res.css('th::text').extract_first(''):
                item['Application Status'] = res.css('td::text').extract_first('')

        for resp in response.css('.wh_preview_detail'):
            try:
                if 'Address' in resp.css('th::text').extract()[-1]:
                    item['Property Address'] = resp.css('tr')[1].css('td')[-1].css('::text').extract_first()
            except:
                pass

            try:
                if 'Names' in resp.css('.wh_preview_detail_heading::text').extract_first():
                    item['Name of applicant'] = resp.css('tr')[2].css('td')[-1].css('::text').extract_first()
            except:
                pass

        processed.append(item)

    def close(spider, reason):
        fcol = 'Application Number'
        airtable_client.insert_records(table_name, processed,fcol)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(blackstown)
process.start()
