import scrapy
import json
import csv
from scrapy.crawler import CrawlerProcess

header = ["name","main_img","extra_img","stock","design_code","price","size","description","color","category","volume","collection","fabric","url"]
fileout = open('junaidjamshed.csv','w',newline='',encoding='utf-8')
writer=csv.DictWriter(fileout,fieldnames=header)
writer.writeheader()

class junaidjamshed(scrapy.Spider):
    name = 'junaidjamshed'
    start_urls = ['https://www.junaidjamshed.com/']

    def parse(self, response):
        for catagory_link in response.css('.navigation li a::attr(href)').extract():
            yield scrapy.Request(url=catagory_link,callback=self.parse_products_pagination)

    def parse_products_pagination(self,response):
        totalpages=len(response.css('.items.pages-items li'))
        if totalpages !=0:
            i=1
            while i<=totalpages:
                url=response.url+f'?p={i}'
                i=i+1
                yield scrapy.Request(url=url,callback=self.parse_products)

    def parse_products(self,response):
        for product_link in response.css('.product_image .product.photo.product-item-photo::attr(href)').extract():
            yield scrapy.Request(url=product_link,callback=self.parse_ind_product)

    def parse_ind_product(self, response):
        item=dict()
        item['url'] = response.url
        item['name'] = response.css('.page-title span::text').extract_first()
        item['main_img'] = response.css('#mtImageContainer img::attr(src)').extract_first()
        item['extra_img'] ='"'+('" || "'.join(response.css('.MagicToolboxSelectorsContainer div a::attr(href)').extract()))+'"'
        item['stock'] = response.css('.stock.available span::text').extract_first()
        item['design_code'] = ''.join(response.css('.product.attribute.sku ::text').extract()).strip().replace('\n','#')
        item['price'] = response.css('.product-info-price .price-container.price-final_price.tax.weee span::text').extract_first()
        if response.css('.product-add-form .product-options-wrapper .swatch-option.text::text').extract_first():
            json_text=(((response.text).split('"jsonSwatchConfig": ')[1]).split("mediaCallback")[0]).split('}}')[0]+'}}'
            json_data=json.loads(json_text)
            sizes = [v1 for v1 in [v for v in json_data.values()][0].values()]
            sizes = [v['value'] for v in sizes[:-1]]

            item['size'] = ' || '.join(sizes)
        else:
            for info in response.css('#product-attribute-specs-table tr'):
                if info.css('th::text').extract_first() == 'Size':
                    item['size'] = info.css('td::text').extract_first()
                    break

        try:
            item['description'] = ', '.join(response.css('.product.attribute.overview .value p::text').extract())
        except:
            item['description'] =''
        for info in response.css('#product-attribute-specs-table tr'):
            if info.css('th::text').extract_first() == 'Color':
                item['color'] = info.css('td::text').extract_first()
            elif info.css('th::text').extract_first() == 'Product Category':
                item['category']=info.css('td::text').extract_first()
            elif info.css('th::text').extract_first() == 'Volume':
                item['volume']=info.css('td::text').extract_first()
            elif info.css('th::text').extract_first() == 'Collection':
                item['collection']=info.css('td::text').extract_first()
            elif info.css('th::text').extract_first() == 'Fabric':
                item['fabric']=info.css('td::text').extract_first()
        writer.writerow(item)
        fileout.flush()









process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(junaidjamshed)
process.start()
