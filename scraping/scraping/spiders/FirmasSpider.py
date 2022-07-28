import csv

import scrapy
from scrapy.crawler import CrawlerProcess

headers = ['name', 'phone']
fileout = open('FirmasSpider.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=headers)
writer.writeheader()


class FirmasSpider(scrapy.Spider):
    name = 'firmasspider'

    def start_requests(self):
        url = 'https://www.firmas.lv/profile/list/'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        for resp in response.css('.pagi-item'):
            url = 'https://www.firmas.lv' + resp.css('::attr(href)').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        for resp in response.css('.pagi')[1].css('.pagi-item')[1:-1]:
            url = 'https://www.firmas.lv' + resp.css('::attr(href)').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_page_ind, dont_filter=True)

    def parse_page_ind(self, response):
        for resp in response.css('.firms-item'):
            item = dict()
            item['name'] = resp.css('.firms-name a::text').extract_first('')
            item['phone'] = resp.css('.firms-phone::text').extract_first('')
            writer.writerow(item)
            fileout.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(FirmasSpider)
process.start()
