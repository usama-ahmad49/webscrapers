import json
import csv

import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from seleniumwire import webdriver
from datetime import datetime, timedelta
from scrapy.exceptions import CloseSpider

fileout = open('dubizzle.txt', 'w')
filein=open('Input_dubizzle.txt','r')
inputreader=filein.read().split(',')
N = int(inputreader[0])
date_N_days_ago = datetime.now() - timedelta(days=N)
date_N_days_ago=date_N_days_ago.strftime('%d %B %Y')
class CustomProxyMiddleware(object):

    def process_request(self, request, spider):
        proxy = '5.79.66.2:13010'
        request.meta["proxy"] = "http://{}".format(proxy)
        # request.headers["Proxy-Authorization"] = basic_auth_header(proxy[2], proxy[3])


class DubizzleSpider(scrapy.Spider):
    name = 'dubizzle'
    headers = None
    detail_headers = []
    CONCURRENT_REQUESTS = 1
    DOWNLOAD_DELAY = 1

    def start_requests(self):
        driver = webdriver.Chrome()
        driver.set_page_load_timeout(5)
        try:
            driver.get(inputreader[1]+'?page=1')
        except:
            pass
        req = [v for v in driver.requests if inputreader[1]+'?page=1' == v.url][0]
        self.headers = dict(req.headers)
        response = scrapy.Selector(text=driver.page_source)
        url = response.css('.results-listing-title a ::attr(href)').extract_first('')
        driver.close()
        driver = webdriver.Chrome()
        driver.set_page_load_timeout(5)
        try:
            driver.get(url)
        except:
            pass
        req = [v for v in driver.requests if url == v.url][0]
        self.detail_headers = dict(req.headers)
        driver.close()
        del self.headers['Accept-Encoding']
        page=1
        while page<50:
            yield scrapy.Request(inputreader[1]+f'?page={page}', headers=self.headers, meta={'dont_redirect': True})
            page=page+1

    def parse(self, response):
        for respon in response.css('.list-item-wrapper'):
            if respon.css('.date::text').extract_first()>date_N_days_ago:
                raise CloseSpider("spider closed")
            link=respon.css('.results-listing-title a::attr(href)').extract_first()
            resp = requests.get(link, headers=self.detail_headers)
            while resp.status_code != 200:
                resp = requests.get(link, headers=self.detail_headers,
                                    proxies={'https': 'https://5.79.66.2:13010', 'http': 'http://5.79.66.2:13010'})

            detailed_response = scrapy.Selector(text=resp.text)
            item = dict()
            item['name'] = detailed_response.css('h1[data-ui-id="listing-name"] ::text').extract_first('')
            item['link'] = link
            item['Images'] = ' || '.join(detailed_response.css('.image-gallery-thumbnails button img::attr(src)').extract())
            item['time'] = detailed_response.css('.sc-1pns9yx-2.kzWQGI ::text').extract_first('')
            item['price'] = detailed_response.css('.sc-1q498l3-0.sc-1q498l3-1.cbFSkA.jsxojh.sc-1pns9yx-3.ZXdGJ ::text').extract_first('')
            item['posted_by'] = detailed_response.css('.sc-1pns9yx-2.kzWQGI::text').extract_first('')
            for D_resp in detailed_response.css('.sc-bdfBwQ.sc-gsTCUz.sc-19hd12a-4.dbXXNJ.dFfFa-d.jXOFSS .sc-bdfBwQ.sc-gsTCUz.sc-19hd12a-1.dbXXNJ.dFfFa-d.jYLyTV'):
                key=D_resp.css('.sc-1q498l3-0.sc-1q498l3-1.dBzLdK.ektmar.sc-19hd12a-2.kZjZWe::text').extract_first('')
                item[key]=D_resp.css('.sc-1q498l3-0.sc-1q498l3-1.dBzLdK.ektmar.sc-19hd12a-3.jIpACZ::text').extract_first('')
            for DT_resp in detailed_response.css('.v3x7e5-1.jCcmsE li'):
                key=DT_resp.css('.sc-1q498l3-0.sc-1q498l3-1.dBzLdK.gOEwzJ::text').extract()[0]
                item[key]=DT_resp.css('.sc-1q498l3-0.sc-1q498l3-1.dBzLdK.gOEwzJ::text').extract()[1]
            json_data = json.loads(detailed_response.css('#__NEXT_DATA__ ::Text').extract_first(''))
            phone = ''
            try:
                phone = json_data['props']['pageProps']['0']['payload']['leads']['phone_number']
            except:
                pass
            item['phone'] = phone
            data=str(item)
            fileout.write(data+'\n')
            fileout.flush()


process = CrawlerProcess({
    'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36",
    'DOWNLOADER_MIDDLEWARES': {'dubizzle.CustomProxyMiddleware': 500}})

process.crawl(DubizzleSpider)
process.start()
