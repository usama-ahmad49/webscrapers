import random
import csv
import scrapy
from scrapy.crawler import CrawlerProcess
from w3lib.http import basic_auth_header
import requests


# try:
#     proxy_file = open('proxy.txt', 'r')
#     proxies = [v for v in proxy_file.read().split('\n') if v.strip()]
# except:
#     pass

headers = ['Record_No.', 'Link', 'Breadcrumbs', 'Chemical Name', 'Synonyms', 'CAS No.', 'Molecular Formula', 'MDL Number', 'HS Code', 'Presursor', 'Product']
fileOut = open('molbase.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileOut, fieldnames=headers)
writer.writeheader()
count = 0

# class CustomProxyMiddleware(object):
#     def process_request(self, request, spider):
#         # print('proxy start')
#         # proxy = random.choice(proxies)
#         # proxy = proxy.split(':')
#         request.meta["proxy"] = "http://{}:{}".format('142.54.161.98', '19004')
#         # request.headers["Proxy-Authorization"] = basic_auth_header(proxy[2], proxy[3])
#         # print('proxy end')


class molbase(scrapy.Spider):
    name = 'molbase'
    CONCURRENT_REQUESTS = 1
    DOWNLOAD_DELAY = 5
    urlList = []

    def start_requests(self):
        file_input = open('category_link.txt', 'r')
        input_list = file_input.read()
        for url in input_list.split('\n')[2:]:
            url_1=f"http://api.scraperapi.com?api_key=5ece4fea4f0c7433b79e38021d252e3a&url={url}"
            yield scrapy.Request(url=url_1)

    def parse(self, response, **kwargs):
        try:
            T_page = int(response.css('.m-page form a')[-2].css('::text').extract_first())
        except:
            T_page = 1
        page = 1
        while page <= T_page:
            urlnew = response.url+'-'+str(page)
            page = page + 1
            url=f'http://api.scraperapi.com?api_key=5ece4fea4f0c7433b79e38021d252e3a&url={urlnew}'
            yield scrapy.Request(url=url, callback=self.parse_Chem_Url, dont_filter=True, meta={'link':urlnew})

    def parse_Chem_Url(self, response):
        for elem in response.css('.s-list li'):
            link = elem.css('a::attr(href)').extract_first()
            url = f'http://www.molbase.com{link}'
            self.urlList.append(url)
        for url in self.urlList:
            url_1=f'http://api.scraperapi.com?api_key=5ece4fea4f0c7433b79e38021d252e3a&url={url}'
            yield scrapy.Request(url=url_1, callback=self.parse_Chem_details, meta={'link':response.meta['link']})

    def parse_Chem_details(self, response):
        item = dict()
        global count
        count = count + 1
        item['Record_No.'] = count
        item['Link'] = response.meta['link']
        try:
            item['Breadcrumbs'] = ''.join(response.css('.crumbs ::text').extract()).replace('\n', '').replace('Â ', '').replace(' ', '').replace('>', ' > ')
        except:
            pass
        try:
            item['Chemical Name'] = response.css('a.cpd-name ::text').extract_first()
        except:
            pass
        try:
            item['Synonyms'] = '|||'.join(response.css('#basic .en-list a.synonyms::text').extract())
        except:
            pass
        try:
            item['CAS No.'] = response.css('.bk-head dd .col em span::text').extract()[0]
        except:
            pass
        try:
            item['Molecular Formula'] = response.css('.bk-head dd .col em span::text').extract()[1]
        except:
            pass
        try:
            for MDL in response.css('#number tr'):
                if 'MDL' in MDL.css('th::text').extract_first():
                    item['MDL Number'] = MDL.css('td::text').extract_first()
                    break
        except:
            item['MDL Number'] = ''
        try:
            for HS in response.css('#safe tr'):
                if 'HS Code' in HS.css('th::text').extract_first():
                    item['HS Code'] = HS.css('td::text').extract_first()
                    break
        except:
            item['HS Code'] = ''
        try:
            item['Presursor'] = '|||'.join(response.css('#precursor dl dd a p::text').extract())
        except:
            pass
        try:
            item['Product'] = '|||'.join(response.css('#downstream dl dd a p::text').extract())
        except:
            pass
        writer.writerow(item)
        fileOut.flush()
        print('record recieved: ' + response.url)


# try:
#     # open('proxy.txt', 'r')
#     process = CrawlerProcess({
#         'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36",
#         'DOWNLOADER_MIDDLEWARES': {'molbase.CustomProxyMiddleware': 500}})
#
#     process.crawl(molbase)
#     process.start()
# except:
# print('crawler except')
process = CrawlerProcess({
    'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"})

process.crawl(molbase)
process.start()
