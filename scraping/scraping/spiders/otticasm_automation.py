import csv
import datetime
import re
import requests
import csvdiff
import scrapy
from scrapy.crawler import CrawlerProcess
ct = datetime.datetime.now()
ts = str(ct.timestamp()).replace('.', '')
'''file for magento'''
priceupdateheaders = ['sku', 'price', 'status', 'store_view_code']
priceupdate = open('otticasm_pricelist_magento_temp.csv', 'w', newline='', encoding='utf-8')
pricewriter = csv.DictWriter(priceupdate, fieldnames=priceupdateheaders)
pricewriter.writeheader()

'''file for pricelist'''
pricelistheaders = ['GROUP SKU', 'PRODUCT SKU', 'RETAIL PRICE', 'WEBSITES']
pricelistfile = open('otticasm_pricelist_odoo_temp.csv', 'w', newline='', encoding='utf-8')
pricelistwriter = csv.DictWriter(pricelistfile, fieldnames=pricelistheaders)
pricelistwriter.writeheader()

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'kk_leadtag=true; _gcl_au=1.1.690698482.1633068621; _ga=GA1.2.2015648700.1633068621; _stlouid=8d5eea8f-d19c-d932-82f9-4b45418eb6a1; _pin_unauth=dWlkPVpUbGhZMlJqTURVdFlUQmhNaTAwTnpBeUxXSXpNVFl0WmpFeFpUZzRPVFF5WkdGag; __zlcmid=16LkN6katDL1IgX; cookielaw=1; cookie-popup=nascondi; _derived_epik=dj0yJnU9TnA4WGpyN1dkcFpQNDFCWGlRZ0dja1NsYnNFb1dzbzkmbj1zQkJyOU5kOW5xbkFpNkZCWFRxOXhRJm09MSZ0PUFBQUFBR0YydnRRJnJtPTEmcnQ9QUFBQUFHRjJ2dFE; frontend=3411fc55589d5fa32ec303577cca8605; frontend_cid=uFSuDyouJBYDrjEc; __cf_bm=3ZKt1DmezZW90aJ.5wS07Ras1J4ccirwgMJcnB.AxOg-1635757261-0-AcQ4M1dcN71O76xULuplCjU3veBOEfmvwDH/J+goDeXOE/pvkm0OgPvZ+btF2TmuJ9Mlx8xgsqklErzTVI52F+lLca/J9D9dKcUTqit8teuDK9L6EA2f7AuMPC4Xlj+GzA==; _gid=GA1.2.1187998080.1635757262; external_no_cache=1; FPC_PRODUCT_VIEWED=57992%2C102457%2C; currency=EUR',
    'dnt': '1',
    'referer': "https://www.otticasm.com/occhiali-da-sole-havaianas-paraty-s-223840-qpn-z9.html",
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': "document",
    'sec-fetch-mode': "navigate",
    'sec-fetch-site': "same-origin",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
}


class otticasm(scrapy.Spider):
    name = 'otticasm'
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': False,
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 70,
        # 'DOWNLOAD_TIMEOUT': 10,
        'RETRY_TIMES': 30,
        'RETRY_HTTP_CODES': [302, 503, 400, 403, 522],
    }

    def start_requests(self):
        url = 'https://www.otticasm.com'
        res = requests.get(url)
        response = scrapy.Selector(text=res.text)
        allbrands = response.css('body > div.wrapper > div > div.header-container.type4 > div.header-wrapper > div > div > div > div > ul > li:nth-child(1) > div > div > div > div > div > ul li.menu-item.menu-item-has-children.menu-parent-item div.nav-sublist.level1 li.menu-item')

        for brnd in allbrands:
            url = 'https:'+brnd.css('a::attr(href)').extract_first()
            yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        for res in response.css('.products-grid.columns3.hide-addtolinks.hide-addtocart li'):
            lnk = res.css('.product-image::attr(href)').extract_first()
            yield scrapy.Request(url=lnk, callback=self.parse_data, headers=headers)

        try:
            if 'prossimo' in response.css('.pages li')[-1].css('a::attr(title)').extract_first():
                nextpage = response.css('.pages li')[-1].css('a::attr(href)').extract_first()
                yield scrapy.Request(url=nextpage, callback=self.parse)
        except:
            pass

    def parse_data(self, response, **kwargs):
        item = dict()
        item['ref'] = ts
        item['material'] = ''
        for res in response.css('#product-attribute-specs-table tr'):
            if 'Cod. articolo' in res.css('.label::text').extract_first():
                item['group_sku'] = res.css('.data::text').extract_first()
            elif 'Marchio' in res.css('.label::text').extract_first():
                item['brand'] = res.css('.data::text').extract_first()
            elif 'Genere' in res.css('.label::text').extract_first():
                item['gender'] = res.css('.data::text').extract_first()
            elif 'Colore Lente' in res.css('.label::text').extract_first():
                item['color'] = res.css('.data::text').extract_first()
            elif 'Materiale' in res.css('.label::text').extract_first():
                if 'Materiale Lenti' in res.css('.label::text').extract_first():
                    item['material'] = item['material'] + res.css('.data::text').extract_first() + '-'
                if 'Materiale Aste' in res.css('.label::text').extract_first():
                    item['material'] = item['material'] + res.css('.data::text').extract_first() + '-'
                if 'Materiale Frontale' in res.css('.label::text').extract_first():
                    item['material'] = item['material'] + res.css('.data::text').extract_first()

        try:
            item['group_sku'] = item['group_sku'] + '-' + item['color']
        except:
            pass
        try:
            item['original_price'] = int(float(response.css('.product-info .price-box .special-price .price::text').extract_first().strip().replace(',', '.').split()[0]))
        except:
            pass
        item['retail_price'] = response.css('.product-info .price-box .special-price .price::text').extract_first().strip().replace(',', '.')
        item['whole_sale_price'] = response.css('.product-info .price-box .special-price .price::text').extract_first().strip().replace(',', '.')
        item['strike_through_price'] = response.css('.product-info .price-box .old-price .price::text').extract_first().strip().replace(',', '.')
        item['description_en'] = ' '.join(response.css('#tab_additional_tabbed_contents p::text').extract())
        item['description_plain_en'] = ' '.join(response.css('#tab_additional_tabbed_contents p::text').extract())

        item['name_en'] = response.css('h1 ::text').extract_first()
        item['main_category'] = item['gender']
        item['category'] = 'Glasses'
        item['sub_category'] = 'Sunglasses'
        item['base_category'] = item['main_category'] + '/' + item['category'] + '/' + item['sub_category']
        item['origin'] = 'Website'
        item['delivery_information'] = '10 to 15 Days'
        item['size'] = response.css('#product-options-wrapper .input-box option:nth-child(2)::text').extract_first()
        t = 1
        for img in response.css('.main-carousel .carousel-cell img::attr(src)').extract():
            if t < 37:
                item['pic_' + str(t)] = img
                t = t + 1
        try:
            item['main_pic'] = item['pic_1']
        except:
            pass

        index = 1
        try:
            for var in response.css('.products-grid.columns4')[0].css('li'):
                if index <= 100:
                    if '(' in item['name_en'] and ')' in item['name_en']:
                        item[f'variant_{index}'] = var.css('.list-sku ::text').extract_first().split()[-1]
                    else:
                        item[f'variant_{index}'] = var.css('.list-sku ::text').extract_first().split('-')[-1]
                    item[f'variant_{index}_price'] = int(float(var.css('.action-area .special-price .price::text').extract_first().strip().replace(',', '.').split()[0]))
                    if (response.css('.product-info .availability ::text').extract_first() == 'Disponibile'):
                        item[f'variant_{index}_stock'] = "In Stock"
                    else:
                        item[f'variant_{index}_stock'] = "Out Of Stock"

                    for i in range(0, 3):
                        PUitem = dict()
                        PUitem['sku'] = item['group_sku'] + '-' + item['variant_{}'.format(index)]
                        PUitem['sku'] = re.sub('[^A-Za-z0-9-]+', '', PUitem['sku'])
                        if i == 0:
                            PUitem['store_view_code'] = 'en'
                            PUitem['price'] = int((30 + (1.13 * item['variant_{}_price'.format(index)])) * 5.7)  # (50 + (item['variant_{}_price'.format(index)] * 1.13)) * 4.86
                            if item[f'variant_{index}_stock'] == "In Stock":
                                PUitem['status'] = 1
                            else:
                                PUitem['price'] = 0
                                PUitem['status'] = 2

                        elif i == 1:
                            PUitem['store_view_code'] = 'sa_en'
                            PUitem['price'] = int(((((30 + (1.13 * item['variant_{}_price'.format(index)])) * 5.7) * 10) / 100) + (30 + (1.13 * item['variant_{}_price'.format(index)])) * 5.7)
                            if item[f'variant_{index}_stock'] == "In Stock":
                                PUitem['status'] = 1
                            else:
                                PUitem['price'] = 0
                                PUitem['status'] = 2
                        elif i == 2:
                            PUitem['store_view_code'] = 'us_en'
                            PUitem['price'] = int(item['variant_{}_price'.format(index)])
                            if item[f'variant_{index}_stock'] == "In Stock":
                                PUitem['status'] = 1
                            else:
                                PUitem['price'] = 0
                                PUitem['status'] = 2
                        pricewriter.writerow(PUitem)
                        priceupdate.flush()

                    PLitem = dict()

                    PLitem['GROUP SKU'] = item['group_sku']
                    PLitem['PRODUCT SKU'] = item['group_sku'] + '-' + item['variant_{}'.format(index)]
                    PLitem['PRODUCT SKU'] = re.sub('[^A-Za-z0-9-]+', '', PLitem['PRODUCT SKU'])
                    PLitem['RETAIL PRICE'] = int((30 + (1.13 * item['variant_{}_price'.format(index)])) * 5.7)
                    if item[f'variant_{index}_stock'] == "Out Of Stock":
                        PLitem['RETAIL PRICE'] = 0
                    PLitem['WEBSITES'] = 'United Arab Emirates'
                    pricelistwriter.writerow(PLitem)
                    pricelistfile.flush()
                index += 1
        except:
            if 'variant_1' not in item.keys():
                item['variant_1'] = item['group_sku'] + '-OS'
                item['variant_1_price'] = item['original_price']
                item['variant_1_stock'] = 'In Stock'
                for i in range(0, 3):
                    PUitem = dict()
                    PUitem['sku'] = item['variant_1']
                    PUitem['sku'] = re.sub('[^A-Za-z0-9-]+', '', PUitem['sku'])
                    if i == 0:
                        PUitem['store_view_code'] = 'en'
                        PUitem['price'] = int((30 + (1.13 * item['variant_1_price'])) * 5.7)  # (50 + (item['variant_{}_price'.format(index)] * 1.13)) * 4.86
                        if item[f'variant_{index}_stock'] == "In Stock":
                            PUitem['status'] = 1
                        else:
                            PUitem['price'] = 0
                            PUitem['status'] = 2

                    elif i == 1:
                        PUitem['store_view_code'] = 'sa_en'
                        PUitem['price'] = int(((((30 + (1.13 * item['variant_1_price'])) * 5.7) * 10) / 100) + (30 + (1.13 * item['variant_1_price'])) * 5.7)
                        if item[f'variant_1_stock'] == "In Stock":
                            PUitem['status'] = 1
                        else:
                            PUitem['price'] = 0
                            PUitem['status'] = 2
                    elif i == 2:
                        PUitem['store_view_code'] = 'us_en'
                        PUitem['price'] = int(item['variant_1_price'])
                        if item[f'variant_1_stock'] == "In Stock":
                            PUitem['status'] = 1
                        else:
                            PUitem['price'] = 0
                            PUitem['status'] = 2
                    pricewriter.writerow(PUitem)
                    priceupdate.flush()

                PLitem = dict()

                PLitem['GROUP SKU'] = item['group_sku']
                PLitem['PRODUCT SKU'] = item['group_sku'] + '-OS'  # + item['variant_{}'.format(index)]
                PLitem['PRODUCT SKU'] = re.sub('[^A-Za-z0-9-]+', '', PLitem['PRODUCT SKU'])
                PLitem['RETAIL PRICE'] = int((30 + (1.13 * item['variant_1_price'])) * 5.7)
                if item[f'variant_1_stock'] == "Out Of Stock":
                    PLitem['RETAIL PRICE'] = 0
                PLitem['WEBSITES'] = 'United Arab Emirates'
                pricelistwriter.writerow(PLitem)
                pricelistfile.flush()
        item['size_slug'] = 'EU'
        # csv_writer.writerow(item)
        # cs.flush()

    def close(spider, reason):
        priceupdate.close()
        pricelistfile.close()
        diffmagento = csvdiff.diff_files("otticasm_pricelist_magento_original.csv", "otticasm_pricelist_magento_temp.csv", ['sku', 'store_view_code'])
        '''delta file for magento'''
        deltaupdateheaders = ['sku', 'price', 'status', 'store_view_code']
        deltapriceupdate = open('otticasm_pricelist_magento_delta.csv', 'w', newline='', encoding='utf-8')
        deltapricewriter = csv.DictWriter(deltapriceupdate, fieldnames=deltaupdateheaders)
        deltapricewriter.writeheader()

        originalpriceupdate = open('otticasm_pricelist_magento_original.csv', 'a+', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltaupdateheaders)

        removed = []
        for item in diffmagento['removed']:
            item__ = dict()
            item__['sku'] = item['sku']
            item__['store_view_code'] = item['store_view_code']
            item__['status'] = '2'
            item__['price'] = 0
            deltapricewriter.writerow(item__)
            deltapriceupdate.flush()
            removed.append(item__)

        for added in diffmagento['added']:
            deltapricewriter.writerow(added)
            originalpriceupdatewriter.writerow(added)
            originalpriceupdate.flush()
            deltapriceupdate.flush()
        change = []
        for changed in diffmagento['changed']:
            chang = dict()
            chang['sku'] = changed['key'][0]
            try:
                chang['price'] = int(float(changed['fields']['price']['to']))
                if changed['fields']['price']['to'] != '0':
                    chang['status'] = '1'
                else:
                    chang['status'] = '2'
            except:
                chang['status'] = changed['fields']['status']['to']
                if chang['status'] == '2':
                    chang['price'] = '0'
            chang['store_view_code'] = changed['key'][-1]
            deltapricewriter.writerow(chang)
            deltapriceupdate.flush()
            change.append(chang)
        original_list = list(csv.DictReader(open('otticasm_pricelist_magento_original.csv')))
        originalpriceupdate = open('otticasm_pricelist_magento_original.csv', 'w', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltaupdateheaders)
        originalpriceupdatewriter.writeheader()
        finalChangeslist = change + removed
        for o_item in original_list:
            for c_item in finalChangeslist:
                if o_item['sku'] == c_item['sku'] and o_item['store_view_code'] == c_item['store_view_code']:
                    o_item['price'] = int(c_item['price'])
                    o_item['status'] = c_item['status']

            originalpriceupdatewriter.writerow(o_item)
            originalpriceupdate.flush()

        '''delta file for pricelist'''
        diffpricelist = csvdiff.diff_files('otticasm_pricelist_odoo_original.csv', 'otticasm_pricelist_odoo_temp.csv', ['GROUP SKU', 'PRODUCT SKU', 'WEBSITES'])
        deltapricelistheaders = ['GROUP SKU', 'PRODUCT SKU', 'RETAIL PRICE', 'WEBSITES']
        deltapricelistfile = open('otticasm_pricelist_odoo_delta.csv', 'w', newline='', encoding='utf-8')
        deltapricelistwriter = csv.DictWriter(deltapricelistfile, fieldnames=deltapricelistheaders)
        deltapricelistwriter.writeheader()

        originalpricelist = open('otticasm_pricelist_odoo_original.csv', 'a+', newline='', encoding='utf-8')
        originalpricelistwriter = csv.DictWriter(originalpricelist, fieldnames=deltapricelistheaders)

        removed = []
        for item in diffpricelist['removed']:
            item__ = dict()
            item__['GROUP SKU'] = item['GROUP SKU']
            item__['PRODUCT SKU'] = item['PRODUCT SKU']
            item__['RETAIL PRICE'] = 0
            item__['WEBSITES'] = item['WEBSITES']
            deltapricelistwriter.writerow(item__)
            deltapricelistfile.flush()
            removed.append(item__)

        for added in diffpricelist['added']:
            deltapricelistwriter.writerow(added)
            originalpricelistwriter.writerow(added)
            originalpricelist.flush()
            deltapricelistfile.flush()
        change = []
        for changed in diffpricelist['changed']:
            chng = dict()
            chng['PRODUCT SKU'] = changed['key'][1]
            chng['GROUP SKU'] = changed['key'][0]
            chng['RETAIL PRICE'] = int(float(changed['fields']['RETAIL PRICE']['to']))
            chng['WEBSITES'] = changed['key'][2]

            deltapricelistwriter.writerow(chng)
            deltapricelistfile.flush()
            change.append(chng)

        original_list = list(csv.DictReader(open('otticasm_pricelist_odoo_original.csv')))
        originalpriceupdate = open('otticasm_pricelist_odoo_original.csv', 'w', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltapricelistheaders)
        originalpriceupdatewriter.writeheader()

        finalChangeslist = change + removed
        for o_item in original_list:
            for c_item in finalChangeslist:
                if o_item['PRODUCT SKU'] == c_item['PRODUCT SKU']:
                    o_item['RETAIL PRICE'] = int(float(c_item['RETAIL PRICE']))
            originalpriceupdatewriter.writerow(o_item)
            originalpriceupdate.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(otticasm)
process.start()
