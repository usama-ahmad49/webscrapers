import csv

import scrapy
from scrapy.crawler import CrawlerProcess

header = ['name', 'img', 'catagory', 'design_code', 'old_price', 'new_price', 'size', 'url']
file_out = open('threadandmotifs.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(file_out, fieldnames=header)
writer.writeheader()


class threadandmotifs(scrapy.Spider):
    name = 'threadandmotifs'

    start_urls = ['https://www.threadsandmotifs.com/']

    def parse(self, response):
        for cat in response.css('.site-nav.list--inline li')[1:]:
            catagory = 'https://www.threadsandmotifs.com' + cat.css('a::attr(href)').extract_first()
            yield scrapy.Request(url=catagory, callback=self.parse_catagory)

    def parse_catagory(self, response):
        pages = len(response.css('.list--inline.pagination')[:1].css('li')[1:-1])
        i = 1
        while i <= pages:
            url = response.url + f'?page={i}'
            i = i + 1
            yield scrapy.Request(url=url, callback=self.parse_products)

    def parse_products(self, response):
        for prod in response.css('.grid__item.grid__item--collection-temp2.col-xs-6.col-md-4'):
            product_link = 'https://www.threadsandmotifs.com' + prod.css('.grid-view-item a::attr(href)').extract_first()
            yield scrapy.Request(url=product_link, callback=self.parse_ind_product)

    def parse_ind_product(self, response):
        item = dict()
        item['name'] = response.css('.product-single__title.product-title::text').extract_first('')
        item['img'] = '  ||  '.join(response.css('.grid__item.product-single__photos.product-wrapper.col-md-7 img::attr(src)').extract())
        item['design_code'] = response.css('.variant-sku::text').extract_first('')
        item['old_price'] = response.css('#ComparePrice-product-template-custom span::text').extract_first('')
        item['new_price'] = response.css('#ProductPrice-product-template-custom span.money::text').extract_first('')
        item['size'] = '; '.join(response.css("#SingleOptionSelector-0 option::text").extract())
        item['catagory'] = response.url.split('/')[4]
        item['url'] = response.url

        writer.writerow(item)
        file_out.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(threadandmotifs)
process.start()
