import csv
import datetime
import re
import csvdiff
import scrapy
from colour import Color
from scrapy.crawler import CrawlerProcess


def check_color(color):
    try:
        # Converting 'deep sky blue' to 'deepskyblue'
        color = color.replace(" ", "")
        Color(color)
        # if everything goes fine then return True
        return True
    except ValueError:  # The color code was not found
        return False


ct = datetime.datetime.now()
ts = str(ct.timestamp()).replace('.', '')

'''file for magento'''
priceupdateheaders = ['sku', 'price', 'status', 'store_view_code']
pricemagentoHNfile = open('vitkac_pricelist_magento_temp.csv', 'w', newline='', encoding='utf-8')
pricemagentowriterHN = csv.DictWriter(pricemagentoHNfile, fieldnames=priceupdateheaders)
pricemagentowriterHN.writeheader()

'''file for pricelist'''
pricelistheaders = ['GROUP SKU', 'PRODUCT SKU', 'RETAIL PRICE', 'WEBSITES']
priceodooHNfile = open('vitkac_pricelist_odoo_temp.csv', 'w', newline='', encoding='utf-8')
priceodoowriterHN = csv.DictWriter(priceodooHNfile, fieldnames=pricelistheaders)
priceodoowriterHN.writeheader()

class vikac(scrapy.Spider):
    name = 'vitkac'
    start_urls = ['https://www.vitkac.com/jp/shop/men/shoes?targets=topFilter%2CproductList%2Coffsets_bottom&main_category=&page=1',
                  'https://www.vitkac.com/jp/shop/men/bags-1?targets=topFilter%2CproductList%2Coffsets_bottom&main_category=&page=1',
                  'https://www.vitkac.com/jp/shop/men/glasses-1?targets=topFilter%2CproductList%2Coffsets_bottom&main_category=&page=1',
                  'https://www.vitkac.com/jp/shop/women/shoes-1?targets=topFilter%2CproductList%2Coffsets_bottom&main_category=&page=1',
                  'https://www.vitkac.com/jp/shop/women/bags-2?targets=topFilter%2CproductList%2Coffsets_bottom&main_category=&page=1',
                  'https://www.vitkac.com/jp/shop/women/glasses-2?targets=topFilter%2CproductList%2Coffsets_bottom&main_category=&page=1'

                  ]

    # count = 2

    def parse(self, response):
        for i in response.css('div.product-media-query a::attr(href)').getall():
            url = i.split('.com/')[0]+'.com/ae/'+'/'.join(i.split('.com/')[-1].split('/')[1:])
            yield scrapy.Request(url=url, callback=self.next)

        max_count = int(response.css('span#offsets_top p.max span::text').get())

        for j in range(2, max_count + 1):
            url = response.url.split('page=')[0] + f'page={j}'
            yield scrapy.Request(url=url, callback=self.parse)

    def next(self, response):
        if 'Sold out' in response.css('.add-to-cart-btn::attr(data-info)').extract_first():
            return
        item = dict()
        item['ref'] = ts
        item['brand'] = response.css('div.prod-header-module.col-xs-12.p-0 h1 a::text').get()
        item['original_price'] = int(float(response.css('p.price span::text').get().strip()[1:].replace(',', '')))
        item['retail_price'] = int((30 + (0.85 * item['original_price'])) * 4.49)
        item['whole_sale_price'] = int((30 + (0.85 * item['original_price'])) * 4.49)
        if response.css('p.price-old::text').get() is not None:
            item['strike_through_price'] = response.css('p.price-old::text').get().strip()[1:]
        item['description_en'] = response.css('p.productDescription::text').get().strip()
        item['description_plain_en'] = item['description_en']

        for color in item['description_en'].split(" "):
            color.replace(",", "")
            color.strip()
            if '-' in color:
                for clr in color.split('-'):
                    flag = check_color(clr)
                    break

            else:
                flag = check_color(color)
            if flag == True:
                item['color'] = color
                break

        if 'color' not in item.keys():
            item['color'] = item['description_en'].split(" ")[0]
        item['color'] = re.sub('[^A-Za-z0-9]+', '', item['color'])
        item['group_sku'] = re.sub('[^A-Za-z0-9-]+', ' ', response.css('span#productSymbol::text').get()+'#')
        item['name_en'] = response.css('div.prod-header-module.col-xs-12.p-0 h1 span::text').get()
        item['group_sku'] =  item['group_sku']+ '-' + item['color']
        # item['product_type'] = response.css('span#productSymbol::text').get()+'-'+item['color'].replace(' ', '-')
        item['url_key'] = response.url
        item['gender'] = response.css('ol.breadcrumb.col-xs-12 li')[1].css('a span::text').get()
        item['main_category'] = item['gender']
        item['category'] = response.css('ol.breadcrumb.col-xs-12 li')[2].css('a span::text').get()
        item['sub_category'] = response.css('ol.breadcrumb.col-xs-12 li')[3].css('a span::text').get()
        item['base_category'] = item['main_category'] + '/' + item['category'] + '/' + item['sub_category']
        item['origin'] = 'Website'
        item['delivery_information'] = '10 to 15 Days'

        t = 1
        for img in response.css('div.miniSlider span img::attr(src)').getall():
            if t < 37:
                item['pic_' + str(t)] = img.replace('/sm/','/up/')
                t = t + 1
        if len(response.css('div.miniSlider span img::attr(src)').getall()) > 0:
            item['main_pic'] = item['pic_1']


        if response.css('form.row.m-0 div.col-xs-12.p-0 p::text').get() is not None:
            item['variant_1'] = response.css('form.row.m-0 div.col-xs-12.p-0 p::text').get().replace('+', '.5')
            item['variant_1_price'] = item['original_price']
            item['variant_1_stock'] = "In Stock"
            if item['variant_1'] =='UNI':
                item['variant_1'] = 'OS'
            for j in range(0, 3):
                PUitem = dict()
                PUitem['sku'] = item['group_sku'] + '-' + str(item['variant_1'])
                PUitem['sku'] = re.sub('[^A-Za-z0-9-]+', '', PUitem['sku'])
                if j == 0:
                    PUitem['store_view_code'] = 'en'
                    # PUitem['price'] = int((45 + 1.1 * item['variant_{}_price'.format(i+1)]) * 5.2)   #remeber change formula
                    PUitem['price'] = int((30 + 0.83 * item['variant_1_price']) * 4.57)  # remeber change formula
                    PUitem['status'] = 1
                    if item['variant_1_stock'] == 'Out Of Stock':
                        PUitem['price'] = 0
                        PUitem['status'] = 2
                elif j == 1:
                    PUitem['store_view_code'] = 'sa_en'
                    PUitem['price'] = int(
                        ((((30 + 0.83 * item['variant_1_price']) * 4.57) * 10) / 100) + ((30 + 0.83 *item['variant_1_price']) * 4.57))  # remeber change formula
                    PUitem['status'] = 1
                    if item['variant_1_stock'] == 'Out Of Stock':
                        PUitem['price'] = 0
                        PUitem['status'] = 2
                elif j == 2:
                    PUitem['store_view_code'] = 'us_en'
                    PUitem['price'] = int(item['variant_1_price'])
                    PUitem['status'] = 1
                    if item['variant_1_stock'] == 'Out Of Stock':
                        PUitem['price'] = 0
                        PUitem['status'] = 2

                pricemagentowriterHN.writerow(PUitem)
                pricemagentoHNfile.flush()

                """This is for oodo"""

                PLitem = dict()
                PLitem['GROUP SKU'] = item['group_sku']
                PLitem['PRODUCT SKU'] = item['group_sku'] + '-' + str(item['variant_1'])
                PLitem['PRODUCT SKU'] = re.sub('[^A-Za-z0-9-]+', '', PLitem['PRODUCT SKU'])
                PLitem['RETAIL PRICE'] = int((30 + 0.83 * item['variant_1_price']) * 4.57)
                if item['variant_1_stock'] == 'Out Of Stock':
                    PLitem['RETAIL PRICE'] = 0
                PLitem['WEBSITES'] = 'United Arab Emirates'
                priceodoowriterHN.writerow(PLitem)
                priceodooHNfile.flush()
        index = 0
        for var in response.css('div#product_sizes ul li'):
            if index <= 100:
                item[f'variant_{index+1}'] = var.css('a::text').get().strip().replace(',', '.')
                item[f'variant_{index+1}_price'] = item['original_price'] #(30+0.83*Discount Price )*4.57
                if item[f'variant_{index+1}'] == 'UNI':
                    item[f'variant_{index+1}'] = 'OS'
                if (var.css('a span::text').get().strip() == 'last item') or (var.css('a span::text').get().strip() == 'Available'):
                    item[f'variant_{index+1}_stock'] = "In Stock"
                else:
                    item[f'variant_{index+1}_stock'] = "Out Of Stock"
                for j in range(0, 3):
                    PUitem = dict()
                    PUitem['sku'] = item['group_sku'] + '-' + str(item[f'variant_{index + 1}'])
                    PUitem['sku'] = re.sub('[^A-Za-z0-9-]+', '', PUitem['sku'])
                    if j == 0:
                        PUitem['store_view_code'] = 'en'
                        # PUitem['price'] = int((45 + 1.1 * item['variant_{}_price'.format(i+1)]) * 5.2)   #remeber change formula
                        PUitem['price'] = int((30 + 0.83 * item['variant_{}_price'.format(index + 1)]) * 4.57)  # remeber change formula
                        PUitem['status'] = 1
                        if item['variant_{}_stock'.format(index + 1)] == 'Out Of Stock':
                            PUitem['price'] = 0
                            PUitem['status'] = 2
                    elif j == 1:
                        PUitem['store_view_code'] = 'sa_en'
                        PUitem['price'] = int(
                            ((((30 + 0.83 * item['variant_{}_price'.format(index + 1)]) * 4.57) * 10) / 100) + ((30 + 0.83 *item['variant_{}_price'.format(index + 1)]) * 4.57))  # remeber change formula
                        PUitem['status'] = 1
                        if item['variant_{}_stock'.format(index + 1)] == 'Out Of Stock':
                            PUitem['price'] = 0
                            PUitem['status'] = 2
                    elif j == 2:
                        PUitem['store_view_code'] = 'us_en'
                        PUitem['price'] = int(item['variant_{}_price'.format(index + 1)])
                        PUitem['status'] = 1
                        if item['variant_{}_stock'.format(index + 1)] == 'Out Of Stock':
                            PUitem['price'] = 0
                            PUitem['status'] = 2

                    pricemagentowriterHN.writerow(PUitem)
                    pricemagentoHNfile.flush()

                    """This is for oodo"""

                    PLitem = dict()
                    PLitem['GROUP SKU'] = item['group_sku']
                    PLitem['PRODUCT SKU'] = item['group_sku'] + '-' + str(item[f'variant_{index + 1}'])
                    PLitem['PRODUCT SKU'] = re.sub('[^A-Za-z0-9-]+', '', PLitem['PRODUCT SKU'])
                    PLitem['RETAIL PRICE'] = int((30 + 0.83 * item['variant_{}_price'.format(index + 1)]) * 4.57)
                    if item['variant_{}_stock'.format(index + 1)] == 'Out Of Stock':
                        PLitem['RETAIL PRICE'] = 0
                    PLitem['WEBSITES'] = 'United Arab Emirates'
                    priceodoowriterHN.writerow(PLitem)
                    priceodooHNfile.flush()


                index += 1
        try:
            if 'variant_1' not in item.keys():
                item['variant_1'] = response.css('form.row.m-0 small::text').extract_first().strip()
                item['variant_1_price'] = item['original_price']
                item['variant_1_stock'] = 'In Stock'
                if item['variant_1'] == 'UNI':
                    item['variant_1'] = 'OS'
                for j in range(0, 3):
                    PUitem = dict()
                    PUitem['sku'] = item['group_sku'] + '-' + str(item['variant_1'])
                    PUitem['sku'] = re.sub('[^A-Za-z0-9-]+', '', PUitem['sku'])
                    if j == 0:
                        PUitem['store_view_code'] = 'en'
                        # PUitem['price'] = int((45 + 1.1 * item['variant_{}_price'.format(i+1)]) * 5.2)   #remeber change formula
                        PUitem['price'] = int((30 + 0.83 * item['variant_1_price']) * 4.57)  # remeber change formula
                        PUitem['status'] = 1
                        if item['variant_1_stock'] == 'Out Of Stock':
                            PUitem['price'] = 0
                            PUitem['status'] = 2
                    elif j == 1:
                        PUitem['store_view_code'] = 'sa_en'
                        PUitem['price'] = int(((((30 + 0.83 * item['variant_1_price']) * 4.57) * 10) / 100) + ((30 + 0.83 * item['variant_1_price']) * 4.57))  # remeber change formula
                        PUitem['status'] = 1
                        if item['variant_1_stock'] == 'Out Of Stock':
                            PUitem['price'] = 0
                            PUitem['status'] = 2
                    elif j == 2:
                        PUitem['store_view_code'] = 'us_en'
                        PUitem['price'] = int(item['variant_1_price'])
                        PUitem['status'] = 1
                        if item['variant_1_stock'] == 'Out Of Stock':
                            PUitem['price'] = 0
                            PUitem['status'] = 2

                    pricemagentowriterHN.writerow(PUitem)
                    pricemagentoHNfile.flush()

                    """This is for oodo"""

                    PLitem = dict()
                    PLitem['GROUP SKU'] = item['group_sku']
                    PLitem['PRODUCT SKU'] = item['group_sku'] + '-' + str(item['variant_1'])
                    PLitem['PRODUCT SKU'] = re.sub('[^A-Za-z0-9-]+', '', PLitem['PRODUCT SKU'])
                    PLitem['RETAIL PRICE'] = int((30 + 0.83 * item['variant_1_price']) * 4.57)
                    if item['variant_1_stock'] == 'Out Of Stock':
                        PLitem['RETAIL PRICE'] = 0
                    PLitem['WEBSITES'] = 'United Arab Emirates'
                    priceodoowriterHN.writerow(PLitem)
                    priceodooHNfile.flush()


        except:
            pass
        try:
            if 'UNI' in item['variant_1']:
                item['size_slug'] = 'EU'
            elif float(item['variant_1']) > 35:
                item['size_slug'] = 'EU'
            elif float(item['variant_1']) < 14:
                item['size_slug'] = 'UK'
        except:
            item['size_slug'] = 'EU'
        # csv_writer.writerow(item)
        # cs.flush()
    def close(self, reason):
        pricemagentoHNfile.close()
        priceodooHNfile.close()
        '''delta file for magento'''
        patch = csvdiff.diff_files('vitkac_pricelist_magento_original.csv',
                                   'vitkac_pricelist_magento_temp.csv',
                                   ['sku', 'store_view_code'])
        deltaupdateheaders = ['sku', 'price', 'status', 'store_view_code']
        deltapriceupdate = open('vitkac_pricelist_magento_delta.csv', 'w', newline='', encoding='utf-8')
        deltapricewriter = csv.DictWriter(deltapriceupdate, fieldnames=deltaupdateheaders)
        deltapricewriter.writeheader()

        originalpriceupdate = open('vitkac_pricelist_magento_original.csv', 'a+', newline='', encoding='utf-8')
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
                jj=1


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

        original_list = list(csv.DictReader(open('vitkac_pricelist_magento_original.csv')))
        originalpriceupdate = open('vitkac_pricelist_magento_original.csv', 'w', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltaupdateheaders)
        originalpriceupdatewriter.writeheader()
        finalChangeList=changed+removed
        for o_item in original_list:
            for c_item in finalChangeList:
                if o_item['sku'] == c_item['sku'] and o_item['store_view_code'] == c_item['store_view_code']:
                    o_item['price'] = c_item['price']
                    o_item['status'] = c_item['status']
            originalpriceupdatewriter.writerow(o_item)
            originalpriceupdate.flush()

        text_file = open('vitkac_skus.txt', 'r')
        skus_list_temp = []
        not_match_skus = []

        with open('vitkac_pricelist_magento_temp.csv', 'r', encoding='utf-8') as magento_temp:
            reader = csv.DictReader(magento_temp)
            for row in reader:
                try:
                    skus_list_temp.append(row['sku'])
                except:
                    a=1


            magento_temp.close()

        for line in text_file.readlines():

            try:

                if line.strip() not in skus_list_temp:
                    not_match_skus.append(line.strip())
            except:
                a = 1

        text_file.close()

        original_list = list(csv.DictReader(open('vitkac_pricelist_magento_original.csv')))
        originalpriceupdate = open('vitkac_pricelist_magento_original.csv', 'w', newline='', encoding='utf-8')
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
        patch_2 = csvdiff.diff_files('vitkac_pricelist_odoo_original.csv',
                                     'vitkac_pricelist_odoo_temp.csv',
                                     ['GROUP SKU', 'PRODUCT SKU', 'WEBSITES'])
        '''delta file for pricelist'''
        deltapricelistheaders = ['GROUP SKU', 'PRODUCT SKU', 'RETAIL PRICE', 'WEBSITES']
        deltapricelistfile = open('vitkac_pricelist_odoo_delta.csv', 'w', newline='', encoding='utf-8')
        deltapricelistwriter = csv.DictWriter(deltapricelistfile, fieldnames=deltapricelistheaders)
        deltapricelistwriter.writeheader()

        originalpricelist = open('vitkac_pricelist_odoo_original.csv', 'a+', newline='', encoding='utf-8')
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

        original_list = list(csv.DictReader(open('vitkac_pricelist_odoo_original.csv')))
        originalpriceupdate = open('vitkac_pricelist_odoo_original.csv', 'w', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltapricelistheaders)
        originalpriceupdatewriter.writeheader()
        finalChangeslist = changed + removed
        for o_item in original_list:
            for c_item in finalChangeslist:
                if o_item['PRODUCT SKU'] == c_item['PRODUCT SKU']:
                    o_item['RETAIL PRICE'] = c_item['RETAIL PRICE']
            originalpriceupdatewriter.writerow(o_item)
            originalpriceupdate.flush()

        text_file_sku_still_available2 = open('vitkac_skus.txt', 'r')
        skus_list_temp = []
        not_match_skus = []

        with open('vitkac_pricelist_odoo_temp.csv', 'r', encoding='utf-8') as magento_temp:
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

        original_list = list(csv.DictReader(open('vitkac_pricelist_odoo_original.csv')))
        originalpriceupdate = open('vitkac_pricelist_odoo_original.csv', 'w', newline='', encoding='utf-8')
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

        text_file_sku_update = open('vitkac_skus.txt', 'a')
        for item in patch_2['added']:
            text_file_sku_update.write('\n' + item['PRODUCT SKU'])
            text_file_sku_update.flush()


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(vikac)
    process.start()
