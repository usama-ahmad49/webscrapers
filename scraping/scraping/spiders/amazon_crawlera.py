try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass

import csv
import json
import re

import scrapy
from scrapy.crawler import CrawlerProcess

headers_csv = ['title', 'price', "ASIN", 'link', 'category', "Manufacturer", "Brand", "Product Dimensions",
               "Pre-printed", "Sheet Size", "Paper Finish", "Manufacturer Part Number", "Item Weight",
               "Customer Reviews", "Best Sellers Rank", "Date First Available",
               "image_1", "image_2", "image_3", "image_4", "image_5", "image_6", "image_7", "image_8", "image_9",
               "image_10", "image_11", "image_12", "image_13", "image_14", "image_15", "image_16", "image_17",
               "image_18", "image_19", "image_20", "image_21", "image_22", "image_23", "image_24", "image_25",
               "image_26", "image_27", "image_28", "image_29", "image_30"]
write_headers = True
try:
    fileout_test = open('amazon_data.csv', 'r')
    write_headers = False
except:
    pass

fileout = open('amazon_data.csv', 'a', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=headers_csv)
if write_headers:
    writer.writeheader()

try:
    file_done = open('done_items.txt', 'r')
except:
    pass
file_done = open('done_items.txt', 'a')


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 500,
        'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 610},
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_APIKEY': '34f4cde68cf14c9f884dacf894fa670f',
        'AUTOTHROTTLE_ENABLED': False,
        # 'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'DOWNLOAD_TIMEOUT': 600,
        'DOWNLOAD_DELAY': 0.3,
        'RETRY_TIMES': 10,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 403, 404, 408],
        # 'HTTPCACHE_ENABLED': True,
        # 'HTTPCACHE_DIR': 'D:\cache'
    }
    headers = {'Host': 'www.amazon.co.uk', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1',
               'Sec-Fetch-Dest': 'document', 'Referer': 'https://www.amazon.co.uk/dp/1405291230',
               'Accept-Language': 'en-US,en;q=0.9',
               'Cookie': 'csm-sid=464-8242971-5379556; x-amz-captcha-1=1610294205830173; x-amz-captcha-2=ziRryopUzVoGVPb6hIGWRA=='}

    def start_requests(self):

        file_ = open('input.txt', 'r')
        links = file_.read().split('\n')
        links = [l for l in links if l.strip()]

        for link_id in links[:100]:
            link = 'https://www.amazon.co.uk/dp/{}'.format(link_id)
            yield scrapy.Request(url=link, meta={'link_id': link_id})

    def parse(self, response, **kwargs):
        if not response.css('#productTitle ::text').extract_first('').strip():
            yield scrapy.Request(response.url, headers=self.headers, dont_filter=True,
                                 meta={'link_id': response.meta['link_id']})
            return

        required = ["Manufacturer", "Brand", "Product Dimensions", "Pre-printed", "Sheet Size", "Paper Finish",
                    "Manufacturer Part Number", "Item Weight", "ASIN", "Customer Reviews", "Best Sellers Rank",
                    "Date First Available"]
        item = dict()
        file_done.write('{}\n'.format(response.meta['link_id']))
        file_done.flush()
        selected = response.text[response.text.find("'colorImages': ") + len("colorImages': "):]
        data = json.loads(selected[:selected.find("'colorToAsin': ")].strip()[:-1].replace("\'", "\""))

        item['link'] = response.url
        item['category'] = ' '.join(
            [v.strip() for v in response.css('ul.a-unordered-list.a-horizontal.a-size-small ::text').extract() if
             v.strip()])
        item['category'] = item['category'].replace('›', '>')
        item['title'] = response.css('#productTitle ::text').extract_first('').strip()
        try:
            item['price'] = response.css('#price_inside_buybox ::Text').extract_first().strip()
        except:
            try:
                item['price'] = response.css('#priceblock_ourprice::text').extract_first().strip()
            except:
                try:
                    item['price'] = response.css('#buyNew_noncbb span::text').extract_first().strip()
                except:
                    item['price'] = ''

        try:
            item['price'] = re.findall("\d+\.\d+", item['price'])
        except:
            pass

        if item['price']:
            item['price'] = item['price'][0]
        else:
            item['price'] = ''

        images = [v['hiRes'] for v in data['initial'] if v['hiRes']]
        for i, image in enumerate(images[:30]):
            item['image_{}'.format(i + 1)] = image.strip()

        for h, d in zip(response.css('#prodDetails th'), response.css('#prodDetails td')):
            if h.css('::text').extract_first('').strip() in required:
                item[h.css('::text').extract_first('').strip()] = re.sub('[^A-Za-z0-9]+', '', ' '.join(
                    d.css('::text').extract()).strip().encode().decode('utf-8'))
        item['ASIN'] = response.meta['link_id']
        print(item)
        writer.writerow(item)
        fileout.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(AmazonSpider)
process.start()
