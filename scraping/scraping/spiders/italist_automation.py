import csv
import datetime
import json
import re

import csvdiff
import requests
import scrapy
from colour import Color
from scrapy.crawler import CrawlerProcess

ct = datetime.datetime.now()
TS = str(ct.timestamp()).replace('.', '')

'''file for magento'''
priceupdateheaders = ['sku', 'price', 'status', 'store_view_code']
pricemagentoHNfile = open('italist_pricelist_magento_temp.csv', 'w', newline='', encoding='utf-8')
pricemagentowriterHN = csv.DictWriter(pricemagentoHNfile, fieldnames=priceupdateheaders)
pricemagentowriterHN.writeheader()

'''file for pricelist'''
pricelistheaders = ['GROUP SKU', 'PRODUCT SKU', 'RETAIL PRICE', 'WEBSITES']
priceodooHNfile = open('italist_pricelist_odoo_temp.csv', 'w', newline='', encoding='utf-8')
priceodoowriterHN = csv.DictWriter(priceodooHNfile, fieldnames=pricelistheaders)
priceodoowriterHN.writeheader()


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
        # res = requests.get('https://www.italist.com/pk/women/shoes/108/')
        # resp = scrapy.Selector(text=res.content.decode('utf-8'))
        # totalpages = int(resp.css('.pagination-list .pagination-element')[-1].css('a::text').extract_first())
        # skip = 0
        # for ws in range(0, totalpages):
        #     yield scrapy.Request(f'https://www.italist.com/pk/women/shoes/108/?skip={skip}', meta={'main_category': 'women', 'category': 'shoes'})
        #     skip += 60
        #
        # '''mens_shoes'''
        # res = requests.get('https://www.italist.com/pk/men/shoes/202/')
        # resp = scrapy.Selector(text=res.content.decode('utf-8'))
        # totalpages = int(resp.css('.pagination-list .pagination-element')[-1].css('a::text').extract_first())
        # skip = 0
        # for ws in range(0, totalpages):
        #     yield scrapy.Request(f'https://www.italist.com/pk/men/shoes/202/?skip={skip}', meta={'main_category': 'men', 'category': 'shoes'})
        #     skip += 60
        #
        # '''womens_bags'''
        # res = requests.get('https://www.italist.com/pk/women/bags/76/')
        # resp = scrapy.Selector(text=res.content.decode('utf-8'))
        # totalpages = int(resp.css('.pagination-list .pagination-element')[-1].css('a::text').extract_first())
        # skip = 0
        # for ws in range(0, totalpages):
        #     yield scrapy.Request(f'https://www.italist.com/pk/women/bags/76/?skip={skip}', meta={'main_category': 'women', 'category': 'bags'})
        #     skip += 60
        #
        # '''mens_bags'''
        # res = requests.get('https://www.italist.com/pk/men/bags/173/')
        # resp = scrapy.Selector(text=res.content.decode('utf-8'))
        # totalpages = int(resp.css('.pagination-list .pagination-element')[-1].css('a::text').extract_first())
        # skip = 0
        # for ws in range(0, totalpages):
        #     yield scrapy.Request(f'https://www.italist.com/pk/men/bags/173/?skip={skip}', meta={'main_category': 'men', 'category': 'bags'})
        #     skip += 60
        #
        # '''womens_glasses'''
        # res = requests.get('https://www.italist.com/pk/women/accessories/eyewear/84/')
        # resp = scrapy.Selector(text=res.content.decode('utf-8'))
        # totalpages = int(resp.css('.pagination-list .pagination-element')[-1].css('a::text').extract_first())
        # skip = 0
        # for ws in range(0, totalpages):
        #     yield scrapy.Request(f'https://www.italist.com/pk/women/accessories/eyewear/84/?skip={skip}', meta={'main_category': 'women', 'category': 'sunglasses'})
        #     skip += 60
        #
        # '''mens_glasses'''
        # res = requests.get('https://www.italist.com/pk/men/accessories/eyewear/180/')
        # resp = scrapy.Selector(text=res.content.decode('utf-8'))
        # totalpages = int(resp.css('.pagination-list .pagination-element')[-1].css('a::text').extract_first())
        # skip = 0
        # for ws in range(0, totalpages):
        #     yield scrapy.Request(f'https://www.italist.com/pk/men/accessories/eyewear/180/?skip={skip}', meta={'main_category': 'men', 'category': 'sunglasses'})
        #     skip += 60
        yield scrapy.Request(url='https://www.italist.com/pk/women/bags/totes/tory-burch-mcgraw-leather-bag/11964681/12133246/tory-burch/', dont_filter=True, callback=self.parse_product)
    def parse(self, response, **kwargs):
        # for res in response.css('.product-list-container a'):
        #     url = 'https://www.italist.com/pk/' + '/'.join(res.css('::attr(href)').extract_first().split('/')[2:])
        #     yield scrapy.Request(url=url, callback=self.parse_product, meta={'main_category': response.meta['main_category'], 'category': response.meta['category']})
        yield scrapy.Request(url='https://www.italist.com/pk/women/shoes/high-heeled-shoes/corset-style-satin-slingback/11900912/12069477/dolce-gabbana/',dont_filter=True, callback=self.parse_product, meta={'main_category': response.meta['main_category'], 'category': response.meta['category']})
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
        if data['sku'].isalnum() or data['sku'] =='':
            item['group_sku'] = data['modelNumber'] + '-' + item['color']
        else:
            item['group_sku'] = data['sku'] + '-' + item['color']
        item['group_sku'] = re.sub('[^A-Za-z0-9-.\s+]+', '', item['group_sku'])
        if (item['group_sku']).strip()[0] == '-':
            item['group_sku'] = (item['group_sku']).strip()[1:]
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
            if 'One-Size' in sz['size']:
                item['variant_{}'.format(index + 1)] = 'OS'
            else:
                item['variant_{}'.format(index + 1)] = sz['size']
            item[f'variant_{index + 1}_price'] = item['original_price']

            for j in range(0, 3):
                PUitem = dict()
                PUitem['sku'] = item['group_sku'] + '-' + str(item[f'variant_{index + 1}'])
                PUitem['sku'] = re.sub('[^A-Za-z0-9-.\s+]+', '', PUitem['sku'])
                if j == 0:
                    PUitem['store_view_code'] = 'en'
                    PUitem['price'] = int((35 + 1.12 * item['variant_{}_price'.format(index + 1)]) * 5.4)
                    PUitem['status'] = 1
                    if item['variant_{}_price'.format(index + 1)] == 0:
                        PUitem['price'] = 0
                        PUitem['status'] = 2
                elif j == 1:
                    PUitem['store_view_code'] = 'sa_en'
                    PUitem['price'] = int(((((35 + 1.12 * item['variant_{}_price'.format(index + 1)]) * 5.4) * 10) / 100) + ((35 + 1.12 * item['variant_{}_price'.format(index + 1)]) * 5.4))
                    PUitem['status'] = 1
                    if item['variant_{}_price'.format(index + 1)] == 0:
                        PUitem['price'] = 0
                        PUitem['status'] = 2
                elif j == 2:
                    PUitem['store_view_code'] = 'us_en'
                    PUitem['price'] = int(item['variant_{}_price'.format(index + 1)])
                    PUitem['status'] = 1
                    if item['variant_{}_price'.format(index + 1)] == 0:
                        PUitem['price'] = 0
                        PUitem['status'] = 2

                pricemagentowriterHN.writerow(PUitem)
                pricemagentoHNfile.flush()

                """This is for oodo"""

                PLitem = dict()
                PLitem['GROUP SKU'] = item['group_sku']
                PLitem['PRODUCT SKU'] = item['group_sku'] + '-' + str(item[f'variant_{index + 1}'])
                PLitem['PRODUCT SKU'] = re.sub('[^A-Za-z0-9-.\s+]+', '', PLitem['PRODUCT SKU'])
                PLitem['RETAIL PRICE'] = int((35 + 1.12 * item['variant_{}_price'.format(index + 1)]) * 5.4)
                if item['variant_{}_price'.format(index + 1)] == 0:
                    PLitem['RETAIL PRICE'] = 0
                PLitem['WEBSITES'] = 'United Arab Emirates'
                priceodoowriterHN.writerow(PLitem)
                priceodooHNfile.flush()

            index += 1
        # writer.writerow(item)
        # fileout.flush()

    def close(self, reason):
        pricemagentoHNfile.close()
        priceodooHNfile.close()
        '''delta file for magento'''
        patch = csvdiff.diff_files('italist_pricelist_magento_original.csv',
                                   'italist_pricelist_magento_temp.csv',
                                   ['sku', 'store_view_code'])
        deltaupdateheaders = ['sku', 'price', 'status', 'store_view_code']
        deltapriceupdate = open('italist_pricelist_magento_delta.csv', 'w', newline='', encoding='utf-8')
        deltapricewriter = csv.DictWriter(deltapriceupdate, fieldnames=deltaupdateheaders)
        deltapricewriter.writeheader()

        originalpriceupdate = open('italist_pricelist_magento_original.csv', 'a+', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltaupdateheaders)

        removed = []
        for item in patch['removed']:
            try:
                item__ = dict()
                item__['sku'] = item['sku']
                item__['store_view_code'] = item['store_view_code']
                item__['status'] = '2'
                item__['price'] = 0
                deltapricewriter.writerow(item__)
                deltapriceupdate.flush()
                removed.append(item__)
            except:
                jj = 1

        for item in patch['added']:
            deltapricewriter.writerow(item)
            deltapriceupdate.flush()
            originalpriceupdatewriter.writerow(item)
            originalpriceupdate.flush()

        changed = []
        for item in patch['changed']:
            item_ = dict()
            item_['sku'] = item['key'][0]
            item_['store_view_code'] = item['key'][1]
            if item['fields']['price']['to'] != '0':
                item_['status'] = '1'
            else:
                item_['status'] = '2'
            item_['price'] = item['fields']['price']['to']
            deltapricewriter.writerow(item_)
            deltapriceupdate.flush()
            changed.append(item_)

        original_list = list(csv.DictReader(open('italist_pricelist_magento_original.csv')))
        originalpriceupdate = open('italist_pricelist_magento_original.csv', 'w', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltaupdateheaders)
        originalpriceupdatewriter.writeheader()
        finalChangeList = changed + removed
        for o_item in original_list:
            for c_item in finalChangeList:
                if o_item['sku'] == c_item['sku'] and o_item['store_view_code'] == c_item['store_view_code']:
                    o_item['price'] = c_item['price']
                    o_item['status'] = c_item['status']
            originalpriceupdatewriter.writerow(o_item)
            originalpriceupdate.flush()

        text_file = open('italist_skus.txt', 'r')
        skus_list_temp = []
        not_match_skus = []

        with open('italist_pricelist_magento_temp.csv', 'r', encoding='utf-8') as magento_temp:
            reader = csv.DictReader(magento_temp)
            for row in reader:
                try:
                    skus_list_temp.append(row['sku'])
                except:
                    a = 1

            magento_temp.close()

        for line in text_file.readlines():

            try:

                if line.strip() not in skus_list_temp:
                    not_match_skus.append(line.strip())
            except:
                a = 1

        text_file.close()

        original_list = list(csv.DictReader(open('italist_pricelist_magento_original.csv')))
        originalpriceupdate = open('italist_pricelist_magento_original.csv', 'w', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate,
                                                   fieldnames=['sku', 'price', 'status', 'store_view_code'])
        originalpriceupdatewriter.writeheader()

        for row in original_list:
            if row['sku'] in not_match_skus:
                row['price'] = 0
                row['status'] = 2
            originalpriceupdatewriter.writerow(row)
            originalpriceupdate.flush()
        """for oodoo"""
        patch_2 = csvdiff.diff_files('italist_pricelist_odoo_original.csv',
                                     'italist_pricelist_odoo_temp.csv',
                                     ['GROUP SKU', 'PRODUCT SKU', 'WEBSITES'])
        '''delta file for pricelist'''
        deltapricelistheaders = ['GROUP SKU', 'PRODUCT SKU', 'RETAIL PRICE', 'WEBSITES']
        deltapricelistfile = open('italist_pricelist_odoo_delta.csv', 'w', newline='', encoding='utf-8')
        deltapricelistwriter = csv.DictWriter(deltapricelistfile, fieldnames=deltapricelistheaders)
        deltapricelistwriter.writeheader()

        originalpricelist = open('italist_pricelist_odoo_original.csv', 'a+', newline='', encoding='utf-8')
        originalpricelistwriter = csv.DictWriter(originalpricelist, fieldnames=deltapricelistheaders)

        removed = []
        for item in patch_2['removed']:
            item__ = dict()
            item__['GROUP SKU'] = item['GROUP SKU']
            item__['PRODUCT SKU'] = item['PRODUCT SKU']
            item__['WEBSITES'] = item['WEBSITES']
            item__['RETAIL PRICE'] = 0
            deltapricelistwriter.writerow(item__)
            deltapricelistfile.flush()
            removed.append(item__)

        for item in patch_2['added']:
            deltapricelistwriter.writerow(item)
            deltapricelistfile.flush()
            originalpricelistwriter.writerow(item)
            originalpricelist.flush()

        changed = []
        for item in patch_2['changed']:
            item_ = dict()
            item_['GROUP SKU'] = item['key'][0]
            item_['PRODUCT SKU'] = item['key'][1]
            item_['WEBSITES'] = item['key'][2]
            item_['RETAIL PRICE'] = item['fields']['RETAIL PRICE']['to']
            deltapricelistwriter.writerow(item_)
            deltapricelistfile.flush()
            changed.append(item_)

        original_list = list(csv.DictReader(open('italist_pricelist_odoo_original.csv')))
        originalpriceupdate = open('italist_pricelist_odoo_original.csv', 'w', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltapricelistheaders)
        originalpriceupdatewriter.writeheader()
        finalChangeslist = changed + removed
        for o_item in original_list:
            for c_item in finalChangeslist:
                if o_item['PRODUCT SKU'] == c_item['PRODUCT SKU']:
                    o_item['RETAIL PRICE'] = c_item['RETAIL PRICE']
            originalpriceupdatewriter.writerow(o_item)
            originalpriceupdate.flush()

        text_file_sku_still_available2 = open('italist_skus.txt', 'r')
        skus_list_temp = []
        not_match_skus = []

        with open('italist_pricelist_odoo_temp.csv', 'r', encoding='utf-8') as magento_temp:
            reader = csv.DictReader(magento_temp)
            for row in reader:
                try:
                    skus_list_temp.append(row['PRODUCT SKU'])
                # skus_list_temp.append(row['PRODUCT SKU'])
                except:
                    j = 1

            magento_temp.close()

        for line in text_file_sku_still_available2.readlines():

            try:

                if line.strip() not in skus_list_temp:
                    not_match_skus.append(line.strip())
            except:
                a = 1

        text_file_sku_still_available2.close()

        original_list = list(csv.DictReader(open('italist_pricelist_odoo_original.csv')))
        originalpriceupdate = open('italist_pricelist_odoo_original.csv', 'w', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate,
                                                   fieldnames=['GROUP SKU', 'PRODUCT SKU', 'RETAIL PRICE', 'WEBSITES'])
        originalpriceupdatewriter.writeheader()

        for row in original_list:
            try:
                if row['PRODUCT SKU'] in not_match_skus:
                    row['RETAIL PRICE'] = 0
                originalpriceupdatewriter.writerow(row)
                originalpriceupdate.flush()
            except:
                k = 1

        text_file_sku_update = open('italist_skus.txt', 'a')
        for item in patch_2['added']:
            text_file_sku_update.write('\n' + item['PRODUCT SKU'])
            text_file_sku_update.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(italist)
process.start()
