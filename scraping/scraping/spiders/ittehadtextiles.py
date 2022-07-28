import csv

import scrapy
from scrapy.crawler import CrawlerProcess

header = ["name", "vendor", "code", "old_price", "new_price", "size", "color", "stock", "image", "url"]
fileout = open('ittehadtextiles.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=header)
writer.writeheader()


class itthadtextiles(scrapy.Spider):
    name = 'itthadtextiles'

    start_urls = ['https://www.ittehadtextiles.com/']

    def parse(self, response):
        for links in response.css('.header-item.header-item--navigation li a::attr(href)').extract():
            if not 'https://' in links:
                links = 'https://www.ittehadtextiles.com' + links
            if '#' in links:
                continue
            yield scrapy.Request(url=links, callback=self.get_pages)

    def get_pages(self, response):
        totalpages = len(response.css('.pagination span')[1:-1])
        if totalpages != 0:
            i = 1
            while i <= totalpages:
                link = response.url + f'?page={i}'
                i = i + 1
                yield scrapy.Request(url=link, callback=self.get_prod_link)
        else:
            for prod in response.css('.grid-product__content'):
                prodlink = 'https://www.ittehadtextiles.com' + prod.css('a::attr(href)').extract_first()
                yield scrapy.Request(url=prodlink, callback=self.parse_product)

    def get_prod_link(self, response):
        for prod in response.css('.grid-product__content'):
            prodlink = 'https://www.ittehadtextiles.com' + prod.css('a::attr(href)').extract_first()
            yield scrapy.Request(url=prodlink, callback=self.parse_product)

    def parse_product(self, response):
        item = dict()
        item['name'] = response.css('.h2.product-single__title::text').extract_first().strip()
        item['code'] = response.css('.product-single__sku::text').extract_first().strip()
        item['old_price'] = response.css('.product__price.product__price--compare .money::text').extract_first().strip()
        item['new_price'] = response.css('.product__price.on-sale .money::text').extract_first().strip()
        if response.css('.product-single__form .variant-wrapper.variant-wrapper--dropdown.js')[0].css('.variant__label::text').extract_first().strip() == 'Size':
            item['size'] = ('||'.join(response.css('.product-single__form .variant-wrapper.variant-wrapper--dropdown.js')[0].css('.variant-input-wrap option::text').extract())).replace('\n', '').replace(' ', '')
            try:
                item['color'] = ('||'.join(response.css('.product-single__form .variant-wrapper.variant-wrapper--dropdown.js')[1].css('.variant-input-wrap option::text').extract())).replace('\n', '').replace(' ', '')
            except:
                item['color'] = ''
        elif response.css('.product-single__form .variant-wrapper.variant-wrapper--dropdown.js')[0].css('.variant__label::text').extract_first().strip() == 'Color':
            item['color'] = ('||'.join(response.css('.product-single__form .variant-wrapper.variant-wrapper--dropdown.js')[0].css('.variant-input-wrap option::text').extract())).replace('\n', '').replace(' ', '')
            item['size']=''
        else:
            item['size'] = ''
            item['color'] =''
        item['stock'] = response.css('.product__inventory::text').extract_first().strip()
        item['image'] = response.css('.grid__item.medium-up--two-fifths img::attr(data-photoswipe-src)').extract_first()
        item['vendor'] = response.css('.product-single__vendor::text').extract_first().strip()
        writer.writerow(item)
        fileout.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(itthadtextiles)
process.start()
