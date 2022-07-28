import csv
import datetime
import json
import re
import requests
import scrapy
from colour import Color
from scrapy.crawler import CrawlerProcess

ct = datetime.datetime.now()
TS = str(ct.timestamp()).replace('.', '')
headers_csv = ['serial_no', 'ref', 'url_key', 'partner_id', 'product_type', 'group_sku', 'condition', 'ticker', 'style_id',
               'variation_type', 'product_sku', 'upc_ean', 'barcode', 'brand',
               'name_en', "original_price", 'strike_through_price', 'retail_price', 'whole_sale_price', 'description_en', 'gender',
               'main_category', 'category', 'sub_category', 'base_category', 'size', 'quantity', 'color', 'material',
               'origin', 'size_slug',
               'description_plain_en', 'delivery_information', 'main_pic',

               "pic_1", "pic_2", "pic_3", "pic_4", "pic_5", "pic_6", "pic_7", "pic_8", "pic_9", "pic_10", "pic_11",
               "pic_12", "pic_13", "pic_14",
               "pic_15", "pic_16", "pic_17", "pic_18", "pic_19", "pic_20", "pic_21", "pic_22", "pic_23", "pic_24",
               "pic_25", "pic_26", "pic_27",
               "pic_28", "pic_29", "pic_30", "pic_31", "pic_32", "pic_33", "pic_34", "pic_35", "pic_36",

               "variant_1", "variant_1_price", "variant_2", "variant_2_price",
               "variant_3", "variant_3_price", "variant_4", "variant_4_price", "variant_5", "variant_5_price",
               "variant_6", "variant_6_price", "variant_7", "variant_7_price", "variant_8", "variant_8_price",
               "variant_9", "variant_9_price", "variant_10", "variant_10_price", "variant_11", "variant_11_price",
               "variant_12", "variant_12_price", "variant_13", "variant_13_price", "variant_14", "variant_14_price",
               "variant_15", "variant_15_price", "variant_16", "variant_16_price", "variant_17", "variant_17_price",
               "variant_18", "variant_18_price", "variant_19", "variant_19_price", "variant_20", "variant_20_price",
               "variant_21", "variant_21_price", "variant_22", "variant_22_price", "variant_23", "variant_23_price",
               "variant_24", "variant_24_price", "variant_25", "variant_25_price", "variant_26", "variant_26_price",
               "variant_27", "variant_27_price", "variant_28", "variant_28_price", "variant_29", "variant_29_price",
               "variant_30", "variant_30_price", "variant_31", "variant_31_price", "variant_32", "variant_32_price",
               "variant_33", "variant_33_price", "variant_34", "variant_34_price", "variant_35", "variant_35_price",
               "variant_36", "variant_36_price", "variant_37", "variant_37_price", "variant_38", "variant_38_price",
               "variant_39", "variant_39_price", "variant_40", "variant_40_price", "variant_41", "variant_41_price",
               "variant_42", "variant_42_price", "variant_43", "variant_43_price", "variant_44", "variant_44_price",
               "variant_45", "variant_45_price", "variant_46", "variant_46_price", "variant_47", "variant_47_price",
               "variant_48", "variant_48_price", "variant_49", "variant_49_price", "variant_50", "variant_50_price",
               "variant_51", "variant_51_price", "variant_52", "variant_52_price", "variant_53", "variant_53_price",
               "variant_54", "variant_54_price", "variant_55", "variant_55_price", "variant_56", "variant_56_price",
               "variant_57", "variant_57_price", "variant_58", "variant_58_price", "variant_59", "variant_59_price",
               "variant_60", "variant_60_price", "variant_61", "variant_61_price", "variant_62", "variant_62_price",
               "variant_63", "variant_63_price", "variant_64", "variant_64_price", "variant_65", "variant_65_price",
               "variant_66", "variant_66_price", "variant_67", "variant_67_price", "variant_68", "variant_68_price",
               "variant_69", "variant_69_price", "variant_70", "variant_70_price", "variant_71", "variant_71_price",
               "variant_72", "variant_72_price", "variant_73", "variant_73_price", "variant_74", "variant_74_price",
               "variant_75", "variant_75_price", "variant_76", "variant_76_price", "variant_77", "variant_77_price",
               "variant_78", "variant_78_price", "variant_79", "variant_79_price", "variant_80", "variant_80_price",
               "variant_81", "variant_81_price", "variant_82", "variant_82_price", "variant_83", "variant_83_price",
               "variant_84", "variant_84_price", "variant_85", "variant_85_price", "variant_86", "variant_86_price",
               "variant_87", "variant_87_price", "variant_88", "variant_88_price", "variant_89", "variant_89_price",
               "variant_90", "variant_90_price", "variant_91", "variant_91_price", "variant_92", "variant_92_price",
               "variant_93", "variant_93_price", "variant_94", "variant_94_price", "variant_95", "variant_95_price",
               "variant_96", "variant_96_price", "variant_97", "variant_97_price", "variant_98", "variant_98_price",
               "variant_99", "variant_99_price", "variant_100", "variant_100_price"
               ]

fileout = open('italist.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(fileout, fieldnames=headers_csv)
writer.writeheader()


def check_color(color):
    try:
        # Converting 'deep sky blue' to 'deepskyblue'
        color = color.replace(" ", "")
        Color(color)
        # if everything goes fine then return True
        return True
    except ValueError:  # The color code was not found
        return False


class italist(scrapy.Spider):
    name = 'italist'
    custom_settings = {
        'CONCURRENT_REQUESTS': 80
    }

    def start_requests(self):
        '''womens_shoes'''
        res = requests.get('https://www.italist.com/pk/women/shoes/108/')
        resp = scrapy.Selector(text=res.content.decode('utf-8'))
        totalpages = int(resp.css('.pagination-list .pagination-element')[-1].css('a::text').extract_first())
        skip = 0
        for ws in range(0, totalpages):
            yield scrapy.Request(f'https://www.italist.com/pk/women/shoes/108/?skip={skip}', meta={'main_category': 'women', 'category': 'shoes'})
            skip += 60

        '''mens_shoes'''
        res = requests.get('https://www.italist.com/pk/men/shoes/202/')
        resp = scrapy.Selector(text=res.content.decode('utf-8'))
        totalpages = int(resp.css('.pagination-list .pagination-element')[-1].css('a::text').extract_first())
        skip = 0
        for ws in range(0, totalpages):
            yield scrapy.Request(f'https://www.italist.com/pk/men/shoes/202/?skip={skip}', meta={'main_category': 'men', 'category': 'shoes'})
            skip += 60

        '''womens_bags'''
        res = requests.get('https://www.italist.com/pk/women/bags/76/')
        resp = scrapy.Selector(text=res.content.decode('utf-8'))
        totalpages = int(resp.css('.pagination-list .pagination-element')[-1].css('a::text').extract_first())
        skip = 0
        for ws in range(0, totalpages):
            yield scrapy.Request(f'https://www.italist.com/pk/women/bags/76/?skip={skip}', meta={'main_category': 'women', 'category': 'bags'})
            skip += 60

        '''mens_bags'''
        res = requests.get('https://www.italist.com/pk/men/bags/173/')
        resp = scrapy.Selector(text=res.content.decode('utf-8'))
        totalpages = int(resp.css('.pagination-list .pagination-element')[-1].css('a::text').extract_first())
        skip = 0
        for ws in range(0, totalpages):
            yield scrapy.Request(f'https://www.italist.com/pk/men/bags/173/?skip={skip}', meta={'main_category': 'men', 'category': 'bags'})
            skip += 60

        '''womens_glasses'''
        res = requests.get('https://www.italist.com/pk/women/accessories/eyewear/84/')
        resp = scrapy.Selector(text=res.content.decode('utf-8'))
        totalpages = int(resp.css('.pagination-list .pagination-element')[-1].css('a::text').extract_first())
        skip = 0
        for ws in range(0, totalpages):
            yield scrapy.Request(f'https://www.italist.com/pk/women/accessories/eyewear/84/?skip={skip}', meta={'main_category': 'women', 'category': 'sunglasses'})
            skip += 60

        '''mens_glasses'''
        res = requests.get('https://www.italist.com/pk/men/accessories/eyewear/180/')
        resp = scrapy.Selector(text=res.content.decode('utf-8'))
        totalpages = int(resp.css('.pagination-list .pagination-element')[-1].css('a::text').extract_first())
        skip = 0
        for ws in range(0, totalpages):
            yield scrapy.Request(f'https://www.italist.com/pk/men/accessories/eyewear/180/?skip={skip}', meta={'main_category': 'men', 'category': 'sunglasses'})
            skip += 60

    def parse(self, response, **kwargs):
        for res in response.css('.product-list-container a'):
            yield scrapy.Request('https://www.italist.com' + res.css('::attr(href)').extract_first(), callback=self.parse_product, meta={'main_category': response.meta['main_category'], 'category': response.meta['category']})

    def parse_product(self, response):
        jsonstrings = response.css('script[type="application/json"]::text').extract_first()
        data = json.loads(jsonstrings)['props']['pageProps']['productDetails']['product']
        item = dict()
        item['serial_no'] = data['productId']
        item['ref'] = TS
        item['product_type'] = data['model']
        for clr in data['storeColor'].split():
            if check_color(clr):
                item['color'] = clr.title()
        if 'color' not in item.keys():
            try:
                item['color'] = data['storeColor'].split()[0].title()
            except:
                for clr in data['model'].split():
                    if check_color(clr):
                        item['color'] = clr.title()
                if 'color' not in item.keys():
                    item['color'] = ''
        item['url_key'] = response.url
        item['group_sku'] = re.sub('[^A-Za-z0-9-.\s+]+', '', (data['sku'] + '-' + item['color']))
        item['style_id'] = data['modelNumber']
        item['brand'] = data['brand']['name']
        item['name_en'] = data['model']
        item['original_price'] = int(data['price']['reducedBeforeTax'] / 100)
        item['strike_through_price'] = data['price']['baseAfterTax'] / 100
        item['retail_price'] = int((35 + (1.12 * item['original_price'])) * 5.4)
        item['whole_sale_price'] = int((35 + (1.12 * item['original_price'])) * 5.4)
        item['description_en'] = data['description']
        item['gender'] = response.meta['main_category']
        item['main_category'] = response.meta['main_category']
        item['category'] = response.meta['category']
        item['sub_category'] = data['category']['name']
        item['base_category'] = item['main_category'] + '/' + item['category'] + '/' + item['sub_category']
        item['origin'] = 'website'
        item['size_slug'] = data['countryOfOrigin']
        item['description_plain_en'] = data['description']
        item['delivery_information'] = '15 to 20 days'
        item['main_pic'] = data['images'][0]['medium']
        for i, res in enumerate(data['images']):
            if i > 36:
                break
            item[f'pic_{i + 1}'] = res['medium']
        index = 0
        for sz in data['sizesList']:
            item['variant_{}'.format(index + 1)] = sz['size']
            item[f'variant_{index + 1}_price'] = item['original_price']
            #(1.13*Discount price)*5.4
            index += 1
        writer.writerow(item)
        fileout.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(italist)
process.start()
