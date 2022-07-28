import json
import csv
import scrapy
from scrapy.crawler import CrawlerProcess

headers = ['name', 'nid', 'productUrl', 'image', 'originalPrice', 'DiscountedPrice', 'discount', 'ratingScore', 'review', 'tItemType', 'location', 'brandId', 'brandName', 'sellerId', 'sellerName', 'itemId']
fileinput = open('lazadadotcom.csv','w',encoding='utf-8', newline='')
writer = csv.DictWriter(fileinput, fieldnames=headers)
writer.writeheader()

class lazadadotcom(scrapy.Spider):
    name = 'lazadadotcom'

    def start_requests(self):
        url = 'https://www.lazada.com.my/'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        for res in response.css('.lzd-site-menu-grand-item'):
            link = 'https:' + res.css('a::attr(href)').extract_first()
            yield scrapy.Request(url=link, callback=self.parsepagination, dont_filter=True)
        for res in response.css('.sub-item-remove-arrow'):
            link = 'https:' + res.css('a::attr(href)').extract_first()
            yield scrapy.Request(url=link, callback=self.parsepagination, dont_filter=True)

    def parsepagination(self, response):
        try:
            jsontext = [v for v in response.css('head script ::text').extract() if 'window.pageData =' in v][0].split('= ')[1].split('};')[0] + '}'
            jsonData = json.loads(jsontext)
            totalpages = (int(jsonData['mainInfo']['totalResults'])) / 40
            if not totalpages.is_integer():
                totalpages = int(totalpages) + 1
            else:
                totalpages = int(totalpages)
            i = 1
            while i <= totalpages:
                url = response.url + f'?page={i}'
                i += 1
                yield scrapy.Request(url=url, callback=self.parseitem, dont_filter=True)
        except:
            pass

    def parseitem(self, response):
        try:
            jsontext = [v for v in response.css('head script ::text').extract() if 'window.pageData =' in v][0].split('= ')[1].split('};')[0] + '}'
            jsonData = json.loads(jsontext)
            for data in jsonData['mods']['listItems']:
                try:
                    if '-7' in data['discount'] or '-8' in data['discount'] or '-9' in data['discount']:
                        if '-7%' not in data['discount'] or '-8%' not in data['discount'] or '-9%' not in data['discount']:
                            item = dict()
                            item['name'] = data['name']
                            item['nid'] = data['nid']
                            item['productUrl'] = 'https:'+data['productUrl']
                            item['image'] = data['image']
                            item['originalPrice'] = data['originalPrice']
                            item['DiscountedPrice'] = data['price']
                            item['discount'] = data['discount']
                            item['ratingScore'] = data['ratingScore']
                            item['review'] = data['review']
                            item['tItemType'] = data['tItemType']
                            item['location'] = data['location']
                            item['brandId'] = data['brandId']
                            item['brandName'] = data['brandName']
                            item['brandName'] = data['brandName']
                            item['sellerId'] = data['sellerId']
                            item['sellerName'] = data['sellerName']
                            item['itemId'] = data['itemId']
                            writer.writerow(item)
                            fileinput.flush()
                except:
                    pass
        except:
            pass


process = CrawlerProcess({
    'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"})

process.crawl(lazadadotcom)
process.start()
