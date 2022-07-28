import csv
import requests
import scrapy
from scrapy.crawler import CrawlerProcess

headers = ['EIN', 'NAME', 'ADDRESS LINE 1', 'ADDRESS LINE 2', 'CITY', 'STATE', 'POSTAL CODE', 'COUNTRY', 'ORG TYPE', 'NTEE CODE 1', 'NTEE CLASSIFICATION 1', 'NTEE CODE 2', 'NTEE CLASSIFICATION 2', 'NTEE CODE 3', 'NTEE CLASSIFICATION 3', 'MISSION', 'ALAIS', 'WEBSITE', 'FACEBOOK', 'TWITTER', 'INSTAGRAM', 'NTEE TYPE', 'WEBSITE URL', 'DESCRIPTION', ]
fileout = open('guidstarspider.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=headers)
writer.writeheader()

# data_list=[]

def file_input():
    file = open('targetfile.csv', 'r')
    list = file.read().split('\n')

    for l in list[1:-1]:
        l = l.split(',')
        item = dict()
        item['EIN'] = '0' + l[0]
        item['NAME'] = l[1]
        item['ADDRESS LINE 1'] = l[2]
        item['ADDRESS LINE 2'] = l[3]
        item['CITY'] = l[4]
        item['STATE'] = l[5]
        item['POSTAL CODE'] = l[6]
        item['COUNTRY'] = l[7]
        item['ORG TYPE'] = l[8]
        item['NTEE CODE 1'] = l[9]
        item['NTEE CLASSIFICATION 1'] = l[10]
        item['NTEE CODE 2'] = l[11]
        item['NTEE CLASSIFICATION 2'] = l[12]
        item['NTEE CODE 3'] = l[13]
        item['NTEE CLASSIFICATION 3'] = l[14]
        item['MISSION'] = l[15]
        item['ALAIS'] = l[16]
        item['WEBSITE'] = l[17]
        item['FACEBOOK'] = l[18]
        item['TWITTER'] = l[19]
        item['INSTAGRAM'] = l[20]
        item['NTEE TYPE'] = l[21]
        item['WEBSITE URL'] = l[22]
        item['DESCRIPTION'] = l[23]
        data_list.append(item)
    # for item in data_list:
    #     inputlist.append(get_string(item))
    # return inputlist


# class guidstarspider(scrapy.Spider):
#     name = 'guidstarspider'
#     custom_settings = {'ROBOTSTXT_OBEY': False, 'LOG_LEVEL': 'INFO',
#                        'DOWNLOAD_TIMEOUT': 120,
#                        'CONCURRENT_REQUESTS': 1,
#                        'CONCURRENT_REQUESTS_PER_DOMAIN': 1}
#     def start_requests(self):
#         file_input()
#         for item in data_list[1:5]:
#             ein = item['EIN'][:2] + '-' + item['EIN'][2:]
#             newURL = 'https://www.guidestar.org/profile/{}'.format(ein)
#             url='http://api.scraperapi.com?api_key=32e40a13cd12385cbd90f7ed5a3cdc38&url={}'.format(newURL)
#             yield scrapy.Request(url=url, meta={'item':item})
#     def parse(self, response):
#         newitem=response.meta('item')
#         try:
#             newitem['ALAIS'] = response.css('#profileHeader .description.pt-3 span:nth-child(2)::text').extract()[0]
#         except:
#             newitem['ALAIS'] = ''
#         try:
#             newitem['WEBSITE'] = response.css('#profileHeader .description.pt-3 span.website a::attr(href)').extract()[0]
#         except:
#             newitem['WEBSITE'] = ''
#         try:
#             newitem['FACEBOOK'] = response.css('#profileHeader .description.pt-3 span.facebook a::attr(href)').extract()[0]
#         except:
#             newitem['FACEBOOK'] = ''
#         try:
#             newitem['TWITTER'] = response.css('#profileHeader .description.pt-3 span.twitter a::attr(href)').extract()[0]
#         except:
#             newitem['TWITTER'] = ''
#         try:
#             newitem['INSTAGRAM'] = response.css('#profileHeader .description.pt-3 span.instagram a::attr(href)').extract()[0]
#         except:
#             newitem['INSTAGRAM'] = ''
#         try:
#             newitem['MISSION'] = response.css('#summary #mission-statement ::text').extract()[0]
#         except:
#             newitem['MISSION'] = ''
#         try:
#             newitem['ADDRESS LINE 1'] = response.css('#summary > div:nth-child(2) > section:nth-child(2) > p.report-section-text.mb-0::text').extract()[0]
#         except:
#             newitem['ADDRESS LINE 1'] = ''
#         try:
#             newitem['CITY'] = response.css('#summary > div:nth-child(2) > section:nth-child(2) > p:nth-child(3)::text').extract()[0].split(',')[0]
#         except:
#             newitem['CITY'] = ''
#         try:
#             newitem['STATE'] = response.css('#summary > div:nth-child(2) > section:nth-child(2) > p:nth-child(3)::text').extract()[0].split(' ')[1]
#         except:
#             newitem['STATE'] = ''
#         try:
#             newitem['POSTAL CODE'] = response.css('#summary > div:nth-child(2) > section:nth-child(2) > p:nth-child(3)::text').extract()[0].split(' ')[2]
#         except:
#             newitem['POSTAL CODE'] = ''
#
#         try:
#             newitem['NTEE CODE 1'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(2)::text').extract()[0].split('(')[1].replace(')', '')
#         except:
#             try:
#                 newitem['NTEE CODE 1'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p.report-section-text::text').extract()[0].split('(')[1].replace(')', '')
#             except:
#                 newitem['NTEE CODE 1'] = ''
#         try:
#             newitem['NTEE CLASSIFICATION 1'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(2)::text').extract()[0].split('(')[0]
#         except:
#             try:
#                 newitem['NTEE CLASSIFICATION 1'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p.report-section-text::text').extract()[0].split('(')[0]
#             except:
#                 newitem['NTEE CLASSIFICATION 1'] = ''
#         try:
#             newitem['NTEE CODE 2'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(3)::text').extract()[0].split('(')[1].replace(')', '')
#         except:
#             newitem['NTEE CODE 2'] = ''
#         try:
#             newitem['NTEE CLASSIFICATION 2'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(3)::text').extract()[0].split('(')[0]
#         except:
#             newitem['NTEE CLASSIFICATION 2'] = ''
#         try:
#             newitem['NTEE CODE 3'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(4)::text').extract()[0].split('(')[1].replace(')', '')
#         except:
#             newitem['NTEE CODE 3'] = ''
#         try:
#             newitem['NTEE CLASSIFICATION 3'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(4)::text').extract()[0].split('(')[0]
#         except:
#             newitem['NTEE CLASSIFICATION 3'] = ''
#         writer.writerow(newitem)
#         fileout.flush()
#
# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })
#
# process.crawl(guidstarspider)
# process.start()

def search_key(url, newitem):
    res = 'http://api.scraperapi.com?api_key=32e40a13cd12385cbd90f7ed5a3cdc38&url={}'.format(url)
    resp = requests.get(url,proxies={"http": "http://510eee15bd7f47f0b24bbcbb84cdf537:@proxy.crawlera.com:8010/"}, timeout=120)
    while resp.status_code != 200:
        resp = requests.get(url,proxies={"http": "http://510eee15bd7f47f0b24bbcbb84cdf537:@proxy.crawlera.com:8010/"}, timeout=120)
    # try:
    #     resp = requests.get(res, proxies={"http": "http://510eee15bd7f47f0b24bbcbb84cdf537:@proxy.crawlera.com:8010/"}, timeout=20)
    # except:
    #     try:
    #         resp = requests.get(res, timeout=20)
    #     except:
    #         badurls.append(url)
    #         print('unable to get ' + url)
    #         return
    response = scrapy.Selector(text=resp.text)

    try:
        newitem['ALAIS'] = response.css('#profileHeader .description.pt-3 span:nth-child(2)::text').extract()[0]
    except:
        newitem['ALAIS'] = ''
    try:
        newitem['WEBSITE'] = response.css('#profileHeader .description.pt-3 span.website a::attr(href)').extract()[0]
    except:
        newitem['WEBSITE'] = ''
    try:
        newitem['FACEBOOK'] = response.css('#profileHeader .description.pt-3 span.facebook a::attr(href)').extract()[0]
    except:
        newitem['FACEBOOK'] = ''
    try:
        newitem['TWITTER'] = response.css('#profileHeader .description.pt-3 span.twitter a::attr(href)').extract()[0]
    except:
        newitem['TWITTER'] = ''
    try:
        newitem['INSTAGRAM'] = response.css('#profileHeader .description.pt-3 span.instagram a::attr(href)').extract()[0]
    except:
        newitem['INSTAGRAM'] = ''
    try:
        newitem['MISSION'] = response.css('#summary #mission-statement ::text').extract()[0]
    except:
        newitem['MISSION'] = ''
    try:
        newitem['ADDRESS LINE 1'] = response.css('#summary > div:nth-child(2) > section:nth-child(2) > p.report-section-text.mb-0::text').extract()[0]
    except:
        newitem['ADDRESS LINE 1'] = ''
    try:
        newitem['CITY'] = response.css('#summary > div:nth-child(2) > section:nth-child(2) > p:nth-child(3)::text').extract()[0].split(',')[0]
    except:
        newitem['CITY'] = ''
    try:
        newitem['STATE'] = response.css('#summary > div:nth-child(2) > section:nth-child(2) > p:nth-child(3)::text').extract()[0].split(' ')[1]
    except:
        newitem['STATE'] = ''
    try:
        newitem['POSTAL CODE'] = response.css('#summary > div:nth-child(2) > section:nth-child(2) > p:nth-child(3)::text').extract()[0].split(' ')[2]
    except:
        newitem['POSTAL CODE'] = ''

    try:
        newitem['NTEE CODE 1'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(2)::text').extract()[0].split('(')[1].replace(')', '')
    except:
        try:
            newitem['NTEE CODE 1'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p.report-section-text::text').extract()[0].split('(')[1].replace(')', '')
        except:
            newitem['NTEE CODE 1'] = ''
    try:
        newitem['NTEE CLASSIFICATION 1'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(2)::text').extract()[0].split('(')[0]
    except:
        try:
            newitem['NTEE CLASSIFICATION 1'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p.report-section-text::text').extract()[0].split('(')[0]
        except:
            newitem['NTEE CLASSIFICATION 1'] = ''
    try:
        newitem['NTEE CODE 2'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(3)::text').extract()[0].split('(')[1].replace(')', '')
    except:
        newitem['NTEE CODE 2'] = ''
    try:
        newitem['NTEE CLASSIFICATION 2'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(3)::text').extract()[0].split('(')[0]
    except:
        newitem['NTEE CLASSIFICATION 2'] = ''
    try:
        newitem['NTEE CODE 3'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(4)::text').extract()[0].split('(')[1].replace(')', '')
    except:
        newitem['NTEE CODE 3'] = ''
    try:
        newitem['NTEE CLASSIFICATION 3'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(4)::text').extract()[0].split('(')[0]
    except:
        newitem['NTEE CLASSIFICATION 3'] = ''
    writer.writerow(newitem)
    fileout.flush()



if __name__ == '__main__':
    data_list = []
    threads = []
    badurls = []
    file_input()
    for item in data_list[1:5]:
        ein = item['EIN'][:2] + '-' + item['EIN'][2:]
        newURL = 'https://www.guidestar.org/profile/{}'.format(ein)
        search_key(newURL, item)
