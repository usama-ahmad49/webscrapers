import json

import requests
import scrapy
from scrapy.crawler import CrawlerProcess
import logging
import AirtableApiryersonindex

basekey = 'appEU3Fjfj6fXA92A'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'ryersonindex'

airtable_client = AirtableApiryersonindex.AirtableClient(apikey, basekey)

processed = []

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Length": "107",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "_ga=GA1.2.1223961069.1624862994; _gid=GA1.2.234556552.1624862994; _gat_gtag_UA_111761574_1=1",
    "DNT": "1",
    "Host": "ryersonindex.org",
    "Origin": "http://ryersonindex.org",
    "Referer": "http://ryersonindex.org/search.php",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}


if __name__ == '__main__':
    listofsates = ['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']

    for state in listofsates:
        formdata = {
            "search_sn": '',
            "search_sx": '0',
            "search_gn": '',
            'search_lo': f'{state}',
            'search_y1': '',
            'search_y2': '',
            'search_pu': '',
            'search_st': '',
            'search_up': '',
            'search': '1',
        }
        logging.warning(f'searching {state}')
        url = 'http://ryersonindex.org/search.php'
        while True:
            req = requests.post(url=url, data=formdata, headers=headers)
            if req.status_code == 200:
                break
        res = scrapy.Selector(text=req.content.decode('utf-8'))
        pages = int(' '.join(res.css('.noprint a::text').extract()).split('Next')[0].split()[-1])
        i=1
        while i<=pages:
            link = f'http://ryersonindex.org/search.php?page={i}'
            logging.warning(f'searching {state} page {i}')
            i+=1
            try:
                while True:
                    req = requests.post(url=link, data=formdata, headers=headers)
                    if req.status_code == 200:
                        break
                res = scrapy.Selector(text=req.content.decode('utf-8'))
                for data in res.css('table')[-1].css('tr')[1:]:
                    item = dict()
                    item['Surname'] = data.css('td')[0].css('::text').extract_first('')
                    item['GivenName'] = data.css('td')[1].css('::text').extract_first('')
                    item['NoticeType'] = data.css('td')[2].css('::text').extract_first('')
                    item['Date'] = data.css('td')[3].css('::text').extract_first('')
                    item['Event'] = data.css('td')[4].css('::text').extract_first('')
                    item['Age'] = data.css('td')[5].css('::text').extract_first('')
                    item['OtherDetail'] = data.css('td')[6].css('::text').extract_first('')
                    item['Publication'] = data.css('td')[7].css('::text').extract_first('')
                    item['Published'] = data.css('td')[8].css('::text').extract_first('')
                    item['State'] = state
                    item['key'] = item['Surname']+item['GivenName']+item['NoticeType']+item['Date']+item['Event']+item['Age']+item['OtherDetail']+item['Publication']+item['Published']+item['State']
                    processed.append(item)
            except:
                pass

    airtable_client.insert_records(table_name, processed)
