import csv
import datetime

import csvdiff
import scrapy
from scrapy.crawler import CrawlerProcess

ct = datetime.datetime.now()
ts = str(ct.timestamp()).replace('.', '')

'''file for magento'''
priceupdateheaders = ['sku', 'price', 'status', 'store_view_code']
pricemagentoHNfile = open('linoricci_pricelist_magento_temp.csv', 'w', newline='', encoding='utf-8')
pricemagentowriterHN = csv.DictWriter(pricemagentoHNfile, fieldnames=priceupdateheaders)
pricemagentowriterHN.writeheader()

'''file for pricelist'''
pricelistheaders = ['GROUP SKU', 'PRODUCT SKU', 'RETAIL PRICE', 'WEBSITES']
priceodooHNfile = open('linoricci_pricelist_odoo_temp.csv', 'w', newline='', encoding='utf-8')
priceodoowriterHN = csv.DictWriter(priceodooHNfile, fieldnames=pricelistheaders)
priceodoowriterHN.writeheader()



class linoricci(scrapy.Spider):
    name = 'linoricci'

    def start_requests(self):
        '''women bags'''
        url = 'https://www.linoricci.com/en/16-bags-and-luggages'
        yield scrapy.Request(url=url, meta={'main_category': 'women', 'category': 'bags'})
        '''women shoes'''
        url = 'https://www.linoricci.com/en/17-shoes'
        yield scrapy.Request(url=url, meta={'main_category': 'women', 'category': 'shoes'})
        '''women sunglasses'''
        url = 'https://www.linoricci.com/en/58-sunglasses'
        yield scrapy.Request(url=url, meta={'main_category': 'women', 'category': 'sunclasses'})
        '''men bags'''
        url = 'https://www.linoricci.com/en/135-bags-and-luggages'
        yield scrapy.Request(url=url, meta={'main_category': 'men', 'category': 'bags'})

        '''men shoes'''
        url = 'https://www.linoricci.com/en/81-shoes'
        yield scrapy.Request(url=url, meta={'main_category': 'men', 'category': 'shoes'})

    def parse(self, response):
        # yield scrapy.Request(url='https://www.linoricci.com/en/69414207-66761-givenchy-trompe-l-oeil-shopping-tote-bag.html?SubmitCurrency=1&id_currency=1', callback=self.final_page, meta={'main_category': response.meta['main_category'], 'category': response.meta['category']})
        for i in response.css('section#products article div.product-image a::attr(href)').getall():
            url = i.split('.html')[0]+'.html?SubmitCurrency=1&id_currency=1'
            yield scrapy.Request(url=url, callback=self.final_page, meta={'main_category': response.meta['main_category'], 'category': response.meta['category']})

        if response.css('nav.pagination a[rel=next]::attr(href)').get():
            yield scrapy.Request(url=response.css('nav.pagination a[rel=next]::attr(href)').get(), callback=self.parse, meta={'main_category': response.meta['main_category'], 'category': response.meta['category']})

    def final_page(self, response):
        item = dict()
        item['name_en'] = response.css('h1.product-detail-name::text').get()
        if response.css('div.product-prices div.product-discount span::text').get() is not None:
            item['strike_through_price'] = float(response.css('div.product-prices div.product-discount span::text').get()[1:].replace(',', ''))

        item['ref'] = ts
        item['original_price'] = int(float(response.css('div.product-prices div.current-price span[itemprop=price]::text').get()[1:].replace(',', '')))
        item['retail_price'] = float(response.css('div.product-prices div.current-price span[itemprop=price]::text').get()[1:].replace(',', ''))
        item['whole_sale_price'] = float(response.css('div.product-prices div.current-price span[itemprop=price]::text').get()[1:].replace(',', ''))
        brand = response.css('div.product-attributes-label div.product-manufacturer span a::text').get()
        if brand == None:
            item['brand'] = item['name_en'].split()[0] + ' ' + item['name_en'].split()[1]
        else:
            item['brand'] = brand

        item['description_en'] = ''.join(response.css('div.description-short p::text').getall())
        item['description_plain_en'] = item['description_en']
        item['color'] = response.css('div.product-variants span.color span::text').get()
        sku = response.css('div.product-reference span::text').get().split('/')[1]
        if item['color'] is not None:
            item['group_sku'] = sku + '-' + (item['color']).title()
        else:
            item['group_sku'] = sku
        item['gender'] = response.meta['main_category']
        item['main_category'] = response.meta['main_category']
        item['category'] = response.meta['category']
        item['sub_category'] = response.css('div.box-breadcrumb a span::text').getall()[-2]
        item['base_category'] = item['main_category'] + '/' + item['category'] + '/' + item['sub_category']
        item['origin'] = 'Website'
        item['delivery_information'] = '10 to 15 days'

        index = 1
        for var in response.css('div.product-variants select option::text').getall():
            if index <= 100:
                if var[-1] == '+':
                    item[f'variant_{index}'] = var.replace('+', '.5')
                else:
                    item[f'variant_{index}'] = var
                item[f'variant_{index}_price'] = item['original_price']
                if 'PZ' in item[f'variant_{index}']:
                    item[f'variant_{index}'] = 'OS'

            """This is for magento"""
            for i in range(0, 3):
                PUitem = dict()
                PUitem['sku'] = item['group_sku'] + '-' + str(item[f'variant_{index}'])
                if i == 0:
                    PUitem['store_view_code'] = 'en'
                    PUitem['price'] = int((45 + 1.1 * item['variant_{}_price'.format(index)]) * 5.2)
                    PUitem['status'] = 1
                    if item['variant_{}_price'.format(index)] == 0:
                        PUitem['price'] = 0
                        PUitem['status'] = 2
                elif i == 1:
                    PUitem['store_view_code'] = 'sa_en'
                    PUitem['price'] = int(((((45 + 1.1 * item['variant_{}_price'.format(index)]) * 5.2) * 10) / 100) + ((45 + 1.1 * item['variant_{}_price'.format(index)]) * 5.2))
                    PUitem['status'] = 1
                    if item['variant_{}_price'.format(index)] == 0:
                        PUitem['price'] = 0
                        PUitem['status'] = 2
                elif i == 2:
                    PUitem['store_view_code'] = 'us_en'
                    PUitem['price'] = int(item['variant_{}_price'.format(index)])
                    PUitem['status'] = 1
                    if item['variant_{}_price'.format(index)] == 0:
                        PUitem['price'] = 0
                        PUitem['status'] = 2

                pricemagentowriterHN.writerow(PUitem)
                pricemagentoHNfile.flush()

            """This is for oodo"""

            PLitem = dict()
            PLitem['GROUP SKU'] = item['group_sku']
            PLitem['PRODUCT SKU'] = item['group_sku'] + '-' + str(item[f'variant_{index}'])
            PLitem['RETAIL PRICE'] = int((45 + (1.1 * item['variant_{}_price'.format(index)])) * 5.2)
            if item['variant_{}_price'.format(index)] == 0:
                PLitem['RETAIL PRICE'] = 0
            PLitem['WEBSITES'] = 'United Arab Emirates'
            priceodoowriterHN.writerow(PLitem)
            priceodooHNfile.flush()

        try:
            if float(item['variant_1']) > 35:
                item['size_slug'] = 'EU'
            elif float(item['variant_1']) < 16:
                item['size_slug'] = 'UK'
        except:
            item['size_slug'] = 'EU'

        t = 1
        for j in response.css('div#thumb-gallery img::attr(src)').getall():
            if t < 37:
                item['pic_' + str(t)] = j
                t = t + 1
            else:
                break

        item['main_pic'] = item['pic_1']
        index += 1

    def close(self, reason):
        priceodooHNfile.close()
        pricemagentoHNfile.close()

        '''delta file for magento'''
        patch = csvdiff.diff_files('linoricci_pricelist_magento_original.csv',
                                   'linoricci_pricelist_magento_temp.csv',
                                   ['sku', 'store_view_code'])
        deltaupdateheaders = ['sku', 'price', 'status', 'store_view_code']
        deltapriceupdate = open('linoricci_pricelist_magento_delta.csv', 'w', newline='', encoding='utf-8')
        deltapricewriter = csv.DictWriter(deltapriceupdate, fieldnames=deltaupdateheaders)
        deltapricewriter.writeheader()

        originalpriceupdate = open('linoricci_pricelist_magento_original.csv', 'a+', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltaupdateheaders)
        removed = []
        for item in patch['removed']:
            item__ = dict()
            item__['sku'] = item['sku']
            item__['store_view_code'] = item['store_view_code']
            item__['status'] = '2'
            item__['price'] = 0
            deltapricewriter.writerow(item__)
            deltapriceupdate.flush()
            removed.append(item__)
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

        original_list = list(csv.DictReader(open('linoricci_pricelist_magento_original.csv')))
        originalpriceupdate = open('linoricci_pricelist_magento_original.csv', 'w', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltaupdateheaders)
        originalpriceupdatewriter.writeheader()
        finalChangeslist = changed + removed
        for o_item in original_list:
            for c_item in finalChangeslist:
                if o_item['sku'] == c_item['sku'] and o_item['store_view_code'] == c_item['store_view_code']:
                    o_item['price'] = c_item['price']
                    o_item['status'] = c_item['status']
            originalpriceupdatewriter.writerow(o_item)
            originalpriceupdate.flush()

        text_file = open('linoricci_skus.txt', 'r')
        skus_list_temp = []
        not_match_skus = []

        with open('linoricci_pricelist_magento_temp.csv', 'r', encoding='utf-8') as magento_temp:
            reader = csv.DictReader(magento_temp)
            for row in reader:
                skus_list_temp.append(row['sku'])

            magento_temp.close()

        for line in text_file.readlines():
            try:
                if line not in skus_list_temp:
                    not_match_skus.append(line)
                    # not_match_skus.append(text_sku_size)
            except:
                a = 1

        text_file.close()

        original_list = list(csv.DictReader(open('linoricci_pricelist_magento_original.csv')))
        originalpriceupdate = open('linoricci_pricelist_magento_original.csv', 'w', newline='', encoding='utf-8')
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
        patch_2 = csvdiff.diff_files('linoricci_pricelist_odoo_original.csv', 'linoricci_pricelist_odoo_temp.csv', ['GROUP SKU', 'PRODUCT SKU', 'WEBSITES'])
        '''delta file for pricelist'''
        deltapricelistheaders = ['GROUP SKU', 'PRODUCT SKU', 'RETAIL PRICE', 'WEBSITES']
        deltapricelistfile = open('linoricci_pricelist_odoo_delta.csv', 'w', newline='', encoding='utf-8')
        deltapricelistwriter = csv.DictWriter(deltapricelistfile, fieldnames=deltapricelistheaders)
        deltapricelistwriter.writeheader()

        originalpricelist = open('linoricci_pricelist_odoo_original.csv', 'a+', newline='', encoding='utf-8')
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

        original_list = list(csv.DictReader(open('linoricci_pricelist_odoo_original.csv')))
        originalpriceupdate = open('linoricci_pricelist_odoo_original.csv', 'w', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltapricelistheaders)
        originalpriceupdatewriter.writeheader()
        finalChangeslist = changed + removed
        for o_item in original_list:
            for c_item in finalChangeslist:
                if o_item['PRODUCT SKU'] == c_item['PRODUCT SKU']:
                    o_item['RETAIL PRICE'] = c_item['RETAIL PRICE']
            originalpriceupdatewriter.writerow(o_item)
            originalpriceupdate.flush()

        text_file_sku_still_available2 = open('linoricci_skus.txt', 'r')
        skus_list_temp = []
        not_match_skus = []

        with open('linoricci_pricelist_odoo_temp.csv', 'r', encoding='utf-8') as magento_temp:
            reader = csv.DictReader(magento_temp)
            for row in reader:
                try:
                    skus_list_temp.append(row['PRODUCT SKU'])
                except:
                    j = 1
            magento_temp.close()

        for line in text_file_sku_still_available2.readlines():
            try:
                if line not in skus_list_temp:
                    not_match_skus.append(line)
            except:
                a = 1

        text_file_sku_still_available2.close()

        original_list = list(csv.DictReader(open('linoricci_pricelist_odoo_original.csv')))
        originalpriceupdate = open('linoricci_pricelist_odoo_original.csv', 'w', newline='', encoding='utf-8')
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

        text_file_sku_update = open('linoricci_skus.txt', 'a')
        for item in patch_2['added']:
            text_file_sku_update.write('\n' + item['PRODUCT SKU'])
            text_file_sku_update.flush()


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(linoricci)
    process.start()
