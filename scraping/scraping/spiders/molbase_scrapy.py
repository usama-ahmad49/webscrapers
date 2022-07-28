from scraper_api import ScraperAPIClient
import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime
import csv
import time

client = ScraperAPIClient('134a0138472c19f83a3a31dc4f11fb08')
result = client.get(url='http://httpbin.org/ip').text

headers = ['Record_No.', 'Link', 'Breadcrumbs', 'Chemical Name', 'Synonyms', 'CAS No.', 'Molecular Formula',
           'MDL Number', 'HS Code', 'Presursor', 'Product']
fileOut = open('molbase.csv', 'a', newline='', encoding='utf-8')
writer = csv.DictWriter(fileOut, fieldnames=headers)
writer.writeheader()
count = 0


class MolbaseSpider(scrapy.Spider):
    name = 'molbase'
    handle_httpstatus_list = [403]
    custom_settings = {'ROBOTSTXT_OBEY': False, 'DOWNLOAD_TIMEOUT': 1000,
                       'CONCURRENT_REQUESTS': 10, 'AUTOTHROTTLE_ENABLED': False,
                       'CONCURRENT_REQUESTS_PER_DOMAIN': 10,
                       # 'DOWNLOAD_DELAY': 1,
                       'RETRY_TIMES': 20, 'RETRY_HTTP_CODES': ['429', '400']}

    # start_urls = [client.scrapyGet(url='http://www.molbase.com/moldata/category-17')]
    done_file = None
    done_links = []

    def start_requests(self):
        try:
            done_file = open('done_links.txt', 'r', encoding='utf-8')
            self.done_links = done_file.read().split('\n')
        except:
            pass
        self.done_file = open('done_links.txt', 'a', encoding='utf-8')
        file_in = open('category_link.txt', 'r', encoding='utf-8')
        category_links = file_in.read().split('\n')
        for cat_link in category_links[:5]:
            api_link = client.scrapyGet(url=cat_link)
            yield scrapy.Request(api_link, meta={'cat': cat_link})

    def parse(self, response, **kwargs):
        try:
            T_page = int(response.css('.m-page form a')[-2].css('::text').extract_first())
            # if T_page > 251:
            #     T_page=251
        except:
            T_page = 1
        for page in range(1, T_page+2):
            newUrl = response.meta['cat'] + '-' + str(page)
            yield scrapy.Request(client.scrapyGet(url=newUrl), self.parse_categoty, meta={'cat': response.meta['cat']}, dont_filter=True)

    def parse_categoty(self, response):
        urlList = []
        for elem in response.css('.s-list li'):
            link = elem.css('a::attr(href)').extract_first()
            url = f'http://www.molbase.com{link}'
            urlList.append(url)
        for url in urlList:
            if url not in self.done_links:
                yield scrapy.Request(client.scrapyGet(url=url), self.parse_item, meta={'cat': response.meta['cat'],
                                                                                       'url': url})

    def parse_item(self, response):
        self.done_file.write('{}\n'.format(response.meta['url']))
        new_url_cat = response.meta['cat']
        item = dict()
        global count
        count = count + 1
        item['Record_No.'] = count
        item['Link'] = new_url_cat
        try:
            item['Breadcrumbs'] = ''.join(response.css('.crumbs ::text').extract()).replace('\n', '').replace(' ',
                                                                                                              '').replace(
                '  ', '').replace('>', ' > ')
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
            pass
        try:
            for HS in response.css('#safe tr'):
                if 'HS Code' in HS.css('th::text').extract_first():
                    item['HS Code'] = HS.css('td::text').extract_first()
                    break
        except:
            pass

        for resp in response.css('.sxy-p dl'):
            if 'Precursor' in resp.css('dt::text').extract_first():
                try:
                    item['Presursor'] = '|||'.join(resp.css('dd a::text').extract())
                except:
                    pass
            if 'Product' in resp.css('dt::text').extract_first():
                try:
                    item['Product'] = '|||'.join(resp.css('dd a::text').extract())
                except:
                    pass
        # if not item['Breadcrumbs'].strip():
            # print(str(try_count) + 'record not found: ' + resp_raw.url)
            # url_1 = f"http://api.scraperapi.com?api_key=134a0138472c19f83a3a31dc4f11fb08&url={resp_raw.url}"
            # resp3 = make_request(url_1)
            # parse_ind_data(resp3, new_url_cat, try_count + 1)
            # return
            # yield scrapy.Request(client.scrapyGet(url=response.url), self.parse_item,
            #                      meta={'cat': response.meta['cat'], 'tries': response.meta.get('tries', 1) + 1},
            #                      dont_filter=True)

        writer.writerow(item)
        fileOut.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(MolbaseSpider)
process.start()
