import csv
import datetime
import json
import os

import requests
import scrapy
from scrapy.crawler import CrawlerProcess

ct = datetime.datetime.now()
ts = str(ct.timestamp()).replace('.', '')
cwd = os.getcwd()
cs = open('antonioli.csv', 'w', newline="", encoding='utf-8')
header_names = ['serial_no', 'ref', 'partner_id', 'product_type', 'group_sku', 'variation_type', 'product_sku', 'upc_ean', 'barcode', 'brand',
                'name_en', "original_price", 'strike_through_price', 'retail_price', 'whole_sale_price', 'description_en', 'gender',
                'main_category', 'category', 'sub_category', 'base_category', 'size', 'quantity', 'color', 'material', 'origin', 'size_slug',
                'description_plain_en', 'delivery_information', 'main_pic', 'pic_1', 'pic_2', 'pic_3', 'pic_4', 'pic_5', 'pic_6', 'pic_7', 'pic_8', 'pic_9', 'pic_10', 'pic_11', 'pic_12', 'pic_13', 'pic_14',
                'pic_15', 'pic_16', 'pic_17', 'pic_18', 'pic_19', 'pic_20', 'pic_21', 'pic_22', 'pic_23', 'pic_24', 'pic_25', 'pic_26', 'pic_27',
                'pic_28', 'pic_29', 'pic_30', 'pic_31', 'pic_32', 'pic_33', 'pic_34', 'pic_35', 'pic_36', "variant_1", "variant_1_stock", "variant_1_price",
                "variant_2", "variant_2_stock", "variant_2_price",
                "variant_3", "variant_3_stock", "variant_3_price",
                "variant_4", "variant_4_stock", "variant_4_price",
                "variant_5", "variant_5_stock", "variant_5_price",
                "variant_6", "variant_6_stock", "variant_6_price",
                "variant_7", "variant_7_stock", "variant_7_price",
                "variant_8", "variant_8_stock", "variant_8_price",
                "variant_9", "variant_9_stock", "variant_9_price",
                "variant_10", "variant_10_stock", "variant_10_price",
                "variant_11", "variant_11_stock", "variant_11_price",
                "variant_12", "variant_12_stock", "variant_12_price",
                "variant_13", "variant_13_stock", "variant_13_price",
                "variant_14", "variant_14_stock", "variant_14_price",
                "variant_15", "variant_15_stock", "variant_15_price",
                "variant_16", "variant_16_stock", "variant_16_price",
                "variant_17", "variant_17_stock", "variant_17_price",
                "variant_18", "variant_18_stock", "variant_18_price",
                "variant_19", "variant_19_stock", "variant_19_price",
                "variant_20", "variant_20_stock", "variant_20_price",
                "variant_21", "variant_21_stock", "variant_21_price",
                "variant_22", "variant_22_stock", "variant_22_price",
                "variant_23", "variant_23_stock", "variant_23_price",
                "variant_24", "variant_24_stock", "variant_24_price",
                "variant_25", "variant_25_stock", "variant_25_price",
                "variant_26", "variant_26_stock", "variant_26_price",
                "variant_27", "variant_27_stock", "variant_27_price",
                "variant_28", "variant_28_stock", "variant_28_price",
                "variant_29", "variant_29_stock", "variant_29_price",
                "variant_30", "variant_30_stock", "variant_30_price",
                "variant_31", "variant_31_stock", "variant_31_price",
                "variant_32", "variant_32_stock", "variant_32_price",
                "variant_33", "variant_33_stock", "variant_33_price",
                "variant_34", "variant_34_stock", "variant_34_price",
                "variant_35", "variant_35_stock", "variant_35_price",
                "variant_36", "variant_36_stock", "variant_36_price",
                "variant_37", "variant_37_stock", "variant_37_price",
                "variant_38", "variant_38_stock", "variant_38_price",
                "variant_39", "variant_39_stock", "variant_39_price",
                "variant_40", "variant_40_stock", "variant_40_price",
                "variant_41", "variant_41_stock", "variant_41_price",
                "variant_42", "variant_42_stock", "variant_42_price",
                "variant_43", "variant_43_stock", "variant_43_price",
                "variant_44", "variant_44_stock", "variant_44_price",
                "variant_45", "variant_45_stock", "variant_45_price",
                "variant_46", "variant_46_stock", "variant_46_price",
                "variant_47", "variant_47_stock", "variant_47_price",
                "variant_48", "variant_48_stock", "variant_48_price",
                "variant_49", "variant_49_stock", "variant_49_price",
                "variant_50", "variant_50_stock", "variant_50_price",
                "variant_51", "variant_51_stock", "variant_51_price",
                "variant_52", "variant_52_stock", "variant_52_price",
                "variant_53", "variant_53_stock", "variant_53_price",
                "variant_54", "variant_54_stock", "variant_54_price",
                "variant_55", "variant_55_stock", "variant_55_price",
                "variant_56", "variant_56_stock", "variant_56_price",
                "variant_57", "variant_57_stock", "variant_57_price",
                "variant_58", "variant_58_stock", "variant_58_price",
                "variant_59", "variant_59_stock", "variant_59_price",
                "variant_60", "variant_60_stock", "variant_60_price",
                "variant_61", "variant_61_stock", "variant_61_price",
                "variant_62", "variant_62_stock", "variant_62_price",
                "variant_63", "variant_63_stock", "variant_63_price",
                "variant_64", "variant_64_stock", "variant_64_price",
                "variant_65", "variant_65_stock", "variant_65_price",
                "variant_66", "variant_66_stock", "variant_66_price",
                "variant_67", "variant_67_stock", "variant_67_price",
                "variant_68", "variant_68_stock", "variant_68_price",
                "variant_69", "variant_69_stock", "variant_69_price",
                "variant_70", "variant_70_stock", "variant_70_price",
                "variant_71", "variant_71_stock", "variant_71_price",
                "variant_72", "variant_72_stock", "variant_72_price",
                "variant_73", "variant_73_stock", "variant_73_price",
                "variant_74", "variant_74_stock", "variant_74_price",
                "variant_75", "variant_75_stock", "variant_75_price",
                "variant_76", "variant_76_stock", "variant_76_price",
                "variant_77", "variant_77_stock", "variant_77_price",
                "variant_78", "variant_78_stock", "variant_78_price",
                "variant_79", "variant_79_stock", "variant_79_price",
                "variant_80", "variant_80_stock", "variant_80_price",
                "variant_81", "variant_81_stock", "variant_81_price",
                "variant_82", "variant_82_stock", "variant_82_price",
                "variant_83", "variant_83_stock", "variant_83_price",
                "variant_84", "variant_84_stock", "variant_84_price",
                "variant_85", "variant_85_stock", "variant_85_price",
                "variant_86", "variant_86_stock", "variant_86_price",
                "variant_87", "variant_87_stock", "variant_87_price",
                "variant_88", "variant_88_stock", "variant_88_price",
                "variant_89", "variant_89_stock", "variant_89_price",
                "variant_90", "variant_90_stock", "variant_90_price",
                "variant_91", "variant_91_stock", "variant_91_price",
                "variant_92", "variant_92_stock", "variant_92_price",
                "variant_93", "variant_93_stock", "variant_93_price",
                "variant_94", "variant_94_stock", "variant_94_price",
                "variant_95", "variant_95_stock", "variant_95_price",
                "variant_96", "variant_96_stock", "variant_96_price",
                "variant_97", "variant_97_stock", "variant_97_price",
                "variant_98", "variant_98_stock", "variant_98_price",
                "variant_99", "variant_99_stock", "variant_99_price",
                "variant_100", "variant_100_stock", "variant_100_price"
                ]
csv_writer = csv.DictWriter(cs, fieldnames=header_names)
csv_writer.writeheader()


class antonioli(scrapy.Spider):
    name = 'antonioli'
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': False,
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_TIMEOUT': 10,
        'RETRY_TIMES': 30,
        'RETRY_HTTP_CODES': [302, 503, 400, 403],
        # 'Handle_httpstatus_list': [400, 403],
        'ROTATING_PROXY_LIST_PATH': f'{cwd}/proxy.txt',
        'DOWNLOADER_MIDDLEWARES': {
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620
        },
    }
    # start_urls=['https://www.coltortiboutique.com/en/men/men-bags.html']

    def start_requests(self):
        '''for man and  women'''
        response = requests.get('https://www.antonioli.eu/en/PK')  # url change
        res = scrapy.Selector(text=response.content.decode('utf-8'))
        for gender in res.css('div.navigation div.navLink--desktop a'):
            main_category = gender.css('a span::text').extract_first().strip()
            for level1 in gender.css('.level0.submenu .level1.parent'):
                if level1.css('a span::text').extract_first().strip() not in ['Shoes', 'Bags']:
                    continue
                else:
                    category = level1.css('a span::text').extract_first().strip()
                for subcat in level1.css('.subcategories .content a'):
                    subcatagory = subcat.css('span::text').extract_first().strip()
                    url = subcat.css('a::attr(href)').extract_first()
                    yield scrapy.Request(url=url, meta={'main_category': main_category, 'category': category,
                                                        'sub_category': subcatagory})

    def parse(self, response):
        for i in response.css('div#amasty-shopby-product-list div.product-item-info a.product.photo.product-item-photo::attr(href)').getall():
            yield scrapy.Request(url=i, callback=self.final_page, meta={'main_category': response.meta['main_category'], 'category': response.meta['category'], 'sub_category': response.meta['sub_category']})
            # yield scrapy.Request(url='https://www.coltortiboutique.com/en/backpacks-vetements-202396aza000001-black.html',callback=self.final_page)

        if response.css('div.pages li.item.pages-item-next a::attr(href)').get():
            yield scrapy.Request(url=response.css('div.pages li.item.pages-item-next a::attr(href)').get(), callback=self.parse, meta={'main_category': response.meta['main_category'], 'category': response.meta['category'], 'sub_category': response.meta['sub_category']})

    def final_page(self, response):
        item = dict()
        item['ref'] = ts
        item['brand'] = response.css('div.product-info-main div.product.attribute.manufacturer h2::text').get().strip()
        item['name_en'] = response.css('div.product-info-main div.product-info-price h1 div::text').get()
        item['original_price'] = response.css('span.normal-price span.price::text').get()[1:]
        item['retail_price'] = item['original_price']
        item['whole_sale_price'] = item['original_price']

        if response.css('div.old-price span.price::text').get() is not None:
            item['strike_through_price'] = response.css('div.old-price span.price::text').get()

        item['color'] = response.css('div.product.attribute.colore div.value div::text').get()
        if item['color'] is not None:
            item['group_sku'] = str(response.css('div.product-info-main div.product.attribute.sku div.value::text').get()) + '-' + item['color']
        else:
            item['group_sku'] = response.css('div.product-info-main div.product.attribute.sku div.value::text').get()
        item['description_en'] = response.css('div.product.attribute.description div.value::text').get()
        item['description_plain_en'] = item['description_en']
        item['main_category'] = response.meta['main_category']
        item['gender'] = item['main_category']
        item['category'] = response.meta['category']
        item['sub_category'] = response.meta['sub_category']
        item['base_category'] = item['main_category'] + '/' + item['category'] + '/' + item['sub_category']
        item['origin'] = 'Website'
        item['size_slug'] = 'EU'
        item['delivery_information'] = '10 to 15 days'

        t = 1
        for img in response.css('div.imgs-container a img::attr(src)').getall():
            if t < 37:
                if img != None:
                    item['pic_' + str(t)] = img
                    t = t + 1

        item['main_pic'] = item['pic_1']

        json_size = response.css('script[type="text/x-magento-init"]::text').getall()[9]
        size_dict = json.loads(json_size)['#product_addtocart_form']['configurable']['spConfig']['stockInfo']

        index = 1
        for var in json.loads(json_size)['#product_addtocart_form']['configurable']['spConfig']['stockInfo']:
            if index <= 100:
                item[f'variant_{index}'] = size_dict[var]['label_option'].replace(',', '.')
                item[f'variant_{index}_price'] = item['original_price']
                if size_dict[var]['is_in_stock'] == True:
                    item[f'variant_{index}_stock'] = "In Stock"
                else:
                    item[f'variant_{index}_stock'] = "Out Of Stock"
                index += 1

        csv_writer.writerow(item)
        cs.flush()


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(antonioli)
    process.start()
