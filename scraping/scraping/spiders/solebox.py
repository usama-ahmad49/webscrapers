import json

import scrapy
from currency_converter import CurrencyConverter
from scrapy.crawler import CrawlerProcess

import odooApi

c = CurrencyConverter()

processed = []
odooClient = odooApi.odooClient()
vendor = 'solebox'


class solebox(scrapy.Spider):
    name = 'solebox'
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': False,
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_TIMEOUT': 1000,
        'RETRY_TIMES': 5,
        # 'RETRY_HTTP_CODES': [302, 503],

        'ROTATING_PROXY_LIST_PATH': 'E:\Project\pricescraperlk\scraping\scraping\spiders\proxy.txt',
        'DOWNLOADER_MIDDLEWARES': {
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620
        }
        # 'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 610},
        # 'CRAWLERA_ENABLED': True,
        # 'CRAWLERA_APIKEY': 'c29fb925abf7499ea97801bc05ce2863',
    }

    def start_requests(self):
        url = 'https://www.solebox.com/de_DE/c/footwear?prefn1=soleboxExclusive&prefv1=true&srule=standard&openCategory=false&sz=all'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        for res in response.css('.b-product-grid-tile.js-tile-container'):
            for link in res.css('a::attr(href)').extract():
                url = 'https://www.solebox.com' + link
                yield scrapy.Request(url=url, callback=self.parse_data)

    def parse_data(self, response):
        for var in response.css('.b-pdp-color-carousel-item'):
            jsondatastring = var.css('a::attr(data-sizes)').extract_first()
            dt = json.loads(jsondatastring)
            for size in dt:
                j = 0
                while j < 2:
                    jdstring = var.css('a::attr(data-gtm)').extract_first()
                    data = json.loads(jdstring)
                    if data['category'] == 'Schuhpflege':
                        continue
                    item = dict()
                    item['brand'] = data['brand']
                    item['group_sku'] = response.css('tr[data-attr="manufacturerSKU"] td.js-fact-value::text').extract_first()
                    item['product_sku'] = response.css('tr[data-attr="manufacturerSKU"] td.js-fact-value::text').extract_first() + '-' + size
                    item['category'] = data['category']
                    item['name_en'] = data['name']

                    OnSale = data['dimension20']
                    # item['Stock'] = data['dimension33']
                    if j == 0:
                        item['serial_no'] = data['id'] + 'AED'
                        if OnSale == 'yes':
                            UsdPrice = c.convert(data['price'], 'EUR', 'USD')
                            item['retail_price'] = (50 + ((UsdPrice) * 1.13)) * 4.86
                            item['whole_sale_price'] = (50 + ((UsdPrice) * 1.13)) * 4.86
                            item['original_price'] = data['price']
                        else:
                            UsdPrice = c.convert(data['metric1'], 'EUR', 'USD')
                            item['retail_price'] = ((((50 + ((UsdPrice) * 1.13)) * 4.86) * 10) / 100) + (50 + ((UsdPrice) * 1.13)) * 4.86
                            item['whole_sale_price'] = ((((50 + ((UsdPrice) * 1.13)) * 4.86) * 10) / 100) + (50 + ((UsdPrice) * 1.13)) * 4.86
                            item['original_price'] = data['metric1']
                    if j == 1:
                        item['serial_no'] = data['id'] + 'KSA'
                        if OnSale == 'yes':
                            UsdPrice = c.convert(data['price'], 'EUR', 'USD')
                            item['retail_price'] = (50 + ((UsdPrice) * 1.13)) * 4.86
                            item['whole_sale_price'] = (50 + ((UsdPrice) * 1.13)) * 4.86
                            item['original_price'] = data['price']
                        else:
                            UsdPrice = c.convert(data['metric1'], 'EUR', 'USD')
                            item['retail_price'] = ((((50 + ((UsdPrice) * 1.13)) * 4.86) * 10) / 100) + (50 + ((UsdPrice) * 1.13)) * 4.86
                            item['whole_sale_price'] = ((((50 + ((UsdPrice) * 1.13)) * 4.86) * 10) / 100) + (50 + ((UsdPrice) * 1.13)) * 4.86
                            item['original_price'] = data['metric1']
                    item['color'] = data['dimension25']
                    item['material'] = data['dimension24']
                    item['description_en'] = ''.join(response.css('div.b-details-content')[0].css('::text').extract()).strip()
                    item['description_plain_en'] = ''.join(response.css('div.b-details-content')[0].css('::text').extract()).strip().replace('\n', ' ')
                    item['size'] = size
                    item['gender'] = 'UniSex'

                    if response.css('.b-free-shipping'):
                        item['delivery_information'] = 'Free Shipping'
                    else:
                        item['delivery_information'] = 'Shipping Charges Applied'
                    item['main_category'] = 'Shoes'
                    try:
                        item['sub_category'] = response.css('.b-breadcrumb.js-breadcrumbs ')[0].css('.b-breadcrumb-item')[2:][1].css('a::text').extract_first().strip()
                    except:
                        item['sub_category'] = 'not available'
                    try:
                        item['base_category'] = ''.join(response.css('.b-breadcrumb.js-breadcrumbs ')[0].css('.b-breadcrumb-item')[2:].css('a::text').extract()).strip().replace('\n', '/').replace(' ', '')
                    except:
                        pass
                    item['variation_type'] = data['name'] + '-' + size + '-' + data['dimension25']
                    item['main_pic'] = response.css('.b-pdp-carousel-item img')[0].css('::attr(data-src)').extract_first()
                    item['origin'] = response.url
                    item['size_slug'] = 'dontknow'
                    for i, img in enumerate(response.css('.b-pdp-carousel-item img')[1:]):
                        if i > 4:
                            break
                        item['pic{}'.format(i + 1)] = img.css('::attr(data-src)').extract_first()
                    processed.append(item)
                    j += 1
                if len(processed) > 200:
                    odooClient.insert_records(processed, vendor)
                    processed.clear()

    def close(spider, reason):
        if len(processed) > 1:
            odooClient.insert_records(processed, vendor)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(solebox)
process.start()
