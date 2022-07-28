import csv

import scrapy
from scrapy.crawler import CrawlerProcess

header = ['SKU', 'has_variants', 'name_ar', 'name_en', 'description_ar', 'description_en', 'quantity', 'categories', 'keywords', 'weight', 'published', 'option1_name_ar', 'option1_name_en', 'option1_value_ar', 'option1_value_en', 'option2_name_ar', 'option2_name_en', 'option2_value_ar', 'option2_value_en', 'option3_name_ar', 'option3_name_en', 'option3_value_ar', 'option3_value_en', 'price', 'sale_price', 'cost', 'images', ]
fileoutput = open('amazonarabic.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileoutput, fieldnames=header)
writer.writeheader()

fileinput = open('amazonarabic.txt', 'r')
urlinput = fileinput.read().split('\n')


class amazonarabic(scrapy.Spider):
    name = 'amazonarabic'
    custom_settings = {
        'CONCURRENT_REQUESTS' : 1,
        'DOWNLOAD_DELAY': 5,
        }
    def start_requests(self):
        for url in urlinput:
            yield scrapy.Request(url=url)

    def parse(self, response):
        item = dict()
        item['name_ar'] = response.css('#productTitle::text').extract_first().strip()
        try:
            item['sale_price'] = float(response.css('#price #priceblock_ourprice_row #priceblock_ourprice ::text').extract_first().split()[0].replace(',',''))
        except:
            item['sale_price'] = float(response.css('#olp_feature_div .a-size-base.a-color-price::text').extract_first().split()[0].replace(',',''))
        try:
            item['price'] = float(response.css('#price tr td.a-span12.a-color-secondary.a-size-base span::text').extract_first().split()[0].replace(',',''))
        except:
            item['price'] = ''
        cost=(item['sale_price']*25)/100
        if cost > 10.0:
            item['cost'] = item['sale_price']+cost
        else:
            item['cost'] = 10.0
        if response.css('#variation_style_name'):
            item['has_variants'] = True
        else:
            item['has_variants'] = False
        for des in response.css('.apm-sidemodule-textright ul li span'):
            if 'الوزن' in des.css('::text').extract_first():
                item['weight'] = des.css('::text').extract_first().split(':')[1]
                break
        item['images'] = response.css('#imgTagWrapperId img::attr(src)').extract_first()
        if response.css('#buybox-see-all-buying-choices-announce'):
            item['quantity'] = 'Out of Stock'
        else:
            item['quantity'] = 'In Stock'

        item['description_en'] = ''.join(response.css('#feature-bullets .a-unordered-list.a-vertical.a-spacing-mini li ::text').extract()[7:])
        catagory = ''
        if response.css('#prodDetails'):
            for cat in response.css('#productDetails_detailBullets_sections1 tr'):
                if 'تصنيف الأفضل مبيعاً' in cat.css('th::text').extract_first():
                    catagory = cat.css('td span span::text').extract_first()
                    catagory = (catagory.split('في')[1]).split('(')[0]
        elif response.css('#detailBulletsWrapper_feature_div'):
            for cat in response.css('#detailBulletsWrapper_feature_div .a-unordered-list.a-nostyle.a-vertical.a-spacing-none.detail-bullet-list'):
                if '' in cat.css('li span.a-list-item span.a-text-bold'):
                    catagory = cat.css('li span.a-list-item::text').extract_first()
                    catagory = (catagory.split('في')[1]).split('(')[0]
        item['categories'] = catagory
        writer.writerow(item)
        fileoutput.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(amazonarabic)
process.start()
