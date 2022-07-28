import csv
import json
import scrapy
from scrapy.crawler import CrawlerProcess

headers = ['EIN', 'NAME', 'ADDRESS LINE 1', 'ADDRESS LINE 2', 'CITY', 'STATE', 'POSTAL CODE', 'COUNTRY', 'ORG TYPE', 'NTEE CODE 1', 'NTEE CLASSIFICATION 1', 'NTEE CODE 2', 'NTEE CLASSIFICATION 2', 'NTEE CODE 3', 'NTEE CLASSIFICATION 3', 'MISSION', 'ALAIS', 'WEBSITE', 'FACEBOOK', 'TWITTER', 'INSTAGRAM']
fileout = open('open990.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=headers)
writer.writeheader()

data_list=[]

file = open('open990org.csv', 'r',encoding='utf-8')
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
    data_list.append(item)

class open990(scrapy.Spider):
    name = 'open990'
    custom_settings = {'ROBOTSTXT_OBEY': False, 'LOG_LEVEL': 'INFO',
                       'DOWNLOAD_TIMEOUT': 120,
                       'CONCURRENT_REQUESTS': 1,
                       'CONCURRENT_REQUESTS_PER_DOMAIN': 1}
    def start_requests(self):
        for item in data_list[1:25]:
            ein = item['EIN']
            newURL = f'https://www.open990.org/api/org/skeleton/{ein}/'
            # url='http://api.scraperapi.com?api_key=32e40a13cd12385cbd90f7ed5a3cdc38&url={}'.format(newURL)
            yield scrapy.Request(url=newURL, meta={'item':item})

    def parse(self, response, **kwargs):
        newitem=response.meta['item']
        json_data=json.loads(response.text)

        try:
            newitem['EIN'] = json_data.get('ein')
        except:
            newitem['EIN'] = ''
        try:
            newitem['NAME']=json_data.get('header').get('name')
        except:
            newitem['NAME'] = ''

        for data in json_data.get('header').get('vitals')[1].get('lines'):
            if 'www' in data:
                try:
                    newitem['WEBSITE'] = (data.split('href="')[1]).split('" target')[0]
                except:
                    try:
                        newitem['WEBSITE'] = data
                    except:
                        newitem['WEBSITE'] =''
            elif 'facebook' in data:
                try:
                    newitem['FACEBOOK'] = data
                except:
                    newitem['FACEBOOK'] = ''
            elif 'twitter' in data:
                try:
                    newitem['TWITTER'] = data
                except:
                    newitem['TWITTER'] = ''
            elif 'instagram' in data:
                try:
                    newitem['INSTAGRAM'] = data
                except:
                    newitem['INSTAGRAM'] = ''
        try:
            newitem['MISSION'] = json_data.get('header').get('marquee')[0].get('lines')[0]
        except:
            newitem['MISSION'] = ''
        try:
            newitem['ADDRESS LINE 1'] = json_data.get('header').get('vitals')[0].get('lines')[0]
        except:
            newitem['ADDRESS LINE 1'] = ''
        try:
            newitem['ADDRESS LINE 2'] = json_data.get('header').get('vitals')[0].get('lines')[1]
        except:
            newitem['ADDRESS LINE 2'] = ''
        try:
            newitem['CITY'] = json_data.get('header').get('vitals')[0].get('lines')[1].split(',')[0]
        except:
            newitem['CITY'] = ''
        try:
            newitem['STATE'] = (json_data.get('header').get('vitals')[0].get('lines')[1].split(',')[1]).split()[0]
        except:
            newitem['STATE'] = ''
        try:
            newitem['POSTAL CODE'] = (json_data.get('header').get('vitals')[0].get('lines')[1].split(',')[1]).split()[1]
        except:
            newitem['POSTAL CODE'] = ''

        try:
            newitem['NTEE CODE 1'] = json_data.get('header').get('vitals')[2].get('lines')[0].split('-')[0]
        except:
            newitem['NTEE CODE 1'] = ''
        try:
            newitem['NTEE CLASSIFICATION 1'] = json_data.get('header').get('vitals')[2].get('lines')[0].split('-')[1]
        except:
            newitem['NTEE CLASSIFICATION 1'] = ''

        writer.writerow(newitem)
        fileout.flush()

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(open990)
process.start()

# def search_key(url, newitem):
#     res = 'http://api.scraperapi.com?api_key=32e40a13cd12385cbd90f7ed5a3cdc38&url={}'.format(url)
#     resp = requests.get(url,proxies={"http": "http://510eee15bd7f47f0b24bbcbb84cdf537:@proxy.crawlera.com:8010/"}, timeout=120)
#     while resp.status_code != 200:
#         resp = requests.get(url,proxies={"http": "http://510eee15bd7f47f0b24bbcbb84cdf537:@proxy.crawlera.com:8010/"}, timeout=120)
#     # try:
#     #     resp = requests.get(res, proxies={"http": "http://510eee15bd7f47f0b24bbcbb84cdf537:@proxy.crawlera.com:8010/"}, timeout=20)
#     # except:
#     #     try:
#     #         resp = requests.get(res, timeout=20)
#     #     except:
#     #         badurls.append(url)
#     #         print('unable to get ' + url)
#     #         return
#     response = scrapy.Selector(text=resp.text)
#
#     try:
#         newitem['ALAIS'] = response.css('#profileHeader .description.pt-3 span:nth-child(2)::text').extract()[0]
#     except:
#         newitem['ALAIS'] = ''
#     try:
#         newitem['WEBSITE'] = response.css('#profileHeader .description.pt-3 span.website a::attr(href)').extract()[0]
#     except:
#         newitem['WEBSITE'] = ''
#     try:
#         newitem['FACEBOOK'] = response.css('#profileHeader .description.pt-3 span.facebook a::attr(href)').extract()[0]
#     except:
#         newitem['FACEBOOK'] = ''
#     try:
#         newitem['TWITTER'] = response.css('#profileHeader .description.pt-3 span.twitter a::attr(href)').extract()[0]
#     except:
#         newitem['TWITTER'] = ''
#     try:
#         newitem['INSTAGRAM'] = response.css('#profileHeader .description.pt-3 span.instagram a::attr(href)').extract()[0]
#     except:
#         newitem['INSTAGRAM'] = ''
#     try:
#         newitem['MISSION'] = response.css('#summary #mission-statement ::text').extract()[0]
#     except:
#         newitem['MISSION'] = ''
#     try:
#         newitem['ADDRESS LINE 1'] = response.css('#summary > div:nth-child(2) > section:nth-child(2) > p.report-section-text.mb-0::text').extract()[0]
#     except:
#         newitem['ADDRESS LINE 1'] = ''
#     try:
#         newitem['CITY'] = response.css('#summary > div:nth-child(2) > section:nth-child(2) > p:nth-child(3)::text').extract()[0].split(',')[0]
#     except:
#         newitem['CITY'] = ''
#     try:
#         newitem['STATE'] = response.css('#summary > div:nth-child(2) > section:nth-child(2) > p:nth-child(3)::text').extract()[0].split(' ')[1]
#     except:
#         newitem['STATE'] = ''
#     try:
#         newitem['POSTAL CODE'] = response.css('#summary > div:nth-child(2) > section:nth-child(2) > p:nth-child(3)::text').extract()[0].split(' ')[2]
#     except:
#         newitem['POSTAL CODE'] = ''
#
#     try:
#         newitem['NTEE CODE 1'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(2)::text').extract()[0].split('(')[1].replace(')', '')
#     except:
#         try:
#             newitem['NTEE CODE 1'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p.report-section-text::text').extract()[0].split('(')[1].replace(')', '')
#         except:
#             newitem['NTEE CODE 1'] = ''
#     try:
#         newitem['NTEE CLASSIFICATION 1'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(2)::text').extract()[0].split('(')[0]
#     except:
#         try:
#             newitem['NTEE CLASSIFICATION 1'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p.report-section-text::text').extract()[0].split('(')[0]
#         except:
#             newitem['NTEE CLASSIFICATION 1'] = ''
#     try:
#         newitem['NTEE CODE 2'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(3)::text').extract()[0].split('(')[1].replace(')', '')
#     except:
#         newitem['NTEE CODE 2'] = ''
#     try:
#         newitem['NTEE CLASSIFICATION 2'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(3)::text').extract()[0].split('(')[0]
#     except:
#         newitem['NTEE CLASSIFICATION 2'] = ''
#     try:
#         newitem['NTEE CODE 3'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(4)::text').extract()[0].split('(')[1].replace(')', '')
#     except:
#         newitem['NTEE CODE 3'] = ''
#     try:
#         newitem['NTEE CLASSIFICATION 3'] = response.css('#summary > div:nth-child(3) > section:nth-child(2) > p:nth-child(4)::text').extract()[0].split('(')[0]
#     except:
#         newitem['NTEE CLASSIFICATION 3'] = ''
#     writer.writerow(newitem)
#     fileout.flush()
#
#
#
# if __name__ == '__main__':
#     data_list = []
#     threads = []
#     badurls = []
#     file_input()
#     for item in data_list[1:5]:
#         ein = item['EIN'][:2] + '-' + item['EIN'][2:]
#         newURL = 'https://www.guidestar.org/profile/{}'.format(ein)
#         search_key(newURL, item)
